"""
Real-Time Hand Tracking System with Virtual Boundary Detection
Arvyax Internship Assignment

This system tracks hand position using classical computer vision techniques
(color segmentation, contours, convex hull) without using MediaPipe or OpenPose.
"""

import cv2
import numpy as np
import time
from typing import Tuple, Optional, List


class HandTracker:
    """
    Hand tracking system using skin color detection and contour analysis.
    """
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize the hand tracker.
        
        Args:
            camera_index: Camera device index (default: 0)
        """
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Virtual boundary (center circle)
        self.boundary_center = (320, 240)  # Center of 640x480 frame
        self.boundary_radius = 100
        
        # Distance thresholds for states
        self.danger_threshold = 50   # pixels
        self.warning_threshold = 120  # pixels
        
        # State tracking
        self.current_state = "SAFE"
        self.hand_position = None
        
        # Performance tracking
        self.fps = 0
        self.frame_times = []
        
        # HSV range for skin detection (works for various skin tones)
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
    def detect_hand(self, frame: np.ndarray) -> Tuple[Optional[Tuple[int, int]], np.ndarray]:
        """
        Detect hand using skin color segmentation and contour analysis.
        
        Args:
            frame: Input BGR frame
            
        Returns:
            Tuple of (hand_center_position, mask)
        """
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Apply Gaussian blur to reduce noise
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Dilate to make hand region more prominent
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, mask
        
        # Find the largest contour (assumed to be the hand)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Filter out small contours (noise)
        if cv2.contourArea(largest_contour) < 3000:
            return None, mask
        
        # Calculate centroid of the hand
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy), mask
        
        return None, mask
    
    def calculate_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            point1: First point (x, y)
            point2: Second point (x, y)
            
        Returns:
            Distance in pixels
        """
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def update_state(self, distance: float) -> str:
        """
        Update system state based on distance to boundary.
        
        Args:
            distance: Distance from hand to boundary center
            
        Returns:
            Current state string
        """
        if distance <= self.danger_threshold:
            return "DANGER"
        elif distance <= self.warning_threshold:
            return "WARNING"
        else:
            return "SAFE"
    
    def draw_virtual_boundary(self, frame: np.ndarray):
        """
        Draw the virtual boundary object on the frame.
        
        Args:
            frame: Frame to draw on
        """
        # Draw outer circle (warning zone)
        cv2.circle(frame, self.boundary_center, self.warning_threshold, 
                  (0, 255, 255), 2)  # Yellow
        
        # Draw danger zone circle
        cv2.circle(frame, self.boundary_center, self.danger_threshold, 
                  (0, 0, 255), 2)  # Red
        
        # Draw center point
        cv2.circle(frame, self.boundary_center, 5, (255, 0, 255), -1)
        
        # Add labels
        cv2.putText(frame, "DANGER ZONE", 
                   (self.boundary_center[0] - 70, self.boundary_center[1]),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    def draw_tracking_info(self, frame: np.ndarray):
        """
        Draw hand tracking visualization and state information.
        
        Args:
            frame: Frame to draw on
        """
        if self.hand_position:
            x, y = self.hand_position
            
            # Draw hand position marker
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
            
            # Draw line from hand to boundary center
            cv2.line(frame, (x, y), self.boundary_center, (255, 0, 0), 2)
            
            # Calculate distance
            distance = self.calculate_distance((x, y), self.boundary_center)
            
            # Draw distance text
            mid_x = (x + self.boundary_center[0]) // 2
            mid_y = (y + self.boundary_center[1]) // 2
            cv2.putText(frame, f"{int(distance)}px", 
                       (mid_x, mid_y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def draw_state_overlay(self, frame: np.ndarray):
        """
        Draw state information overlay on the frame.
        
        Args:
            frame: Frame to draw on
        """
        height, width = frame.shape[:2]
        
        # State colors
        state_colors = {
            "SAFE": (0, 255, 0),      # Green
            "WARNING": (0, 255, 255),  # Yellow
            "DANGER": (0, 0, 255)      # Red
        }
        
        color = state_colors[self.current_state]
        
        # Draw state background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 60), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw state text
        cv2.putText(frame, f"STATE: {self.current_state}", 
                   (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        
        # DANGER DANGER warning
        if self.current_state == "DANGER":
            # Flashing effect
            if int(time.time() * 4) % 2 == 0:
                # Draw large warning text
                text = "!!! DANGER DANGER !!!"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_BOLD, 1.5, 4)[0]
                text_x = (width - text_size[0]) // 2
                text_y = height - 30
                
                # Background
                cv2.rectangle(frame, (text_x - 10, text_y - text_size[1] - 10),
                            (text_x + text_size[0] + 10, text_y + 10),
                            (0, 0, 255), -1)
                
                # Text
                cv2.putText(frame, text, (text_x, text_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
        
        # Draw FPS counter
        cv2.putText(frame, f"FPS: {self.fps:.1f}", 
                   (width - 120, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def update_fps(self, frame_time: float):
        """
        Update FPS calculation.
        
        Args:
            frame_time: Time taken for current frame
        """
        self.frame_times.append(frame_time)
        
        # Keep only last 30 frames for averaging
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)
        
        # Calculate average FPS
        if self.frame_times:
            avg_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_time if avg_time > 0 else 0
    
    def run(self):
        """
        Main loop for hand tracking system.
        """
        print("=" * 60)
        print("Hand Tracking System - Arvyax Assignment")
        print("=" * 60)
        print("\nInstructions:")
        print("- Show your hand to the camera")
        print("- Move your hand towards the center circle")
        print("- Observe state changes: SAFE -> WARNING -> DANGER")
        print("- Press 'q' to quit")
        print("- Press 'c' to calibrate skin color (optional)")
        print("\nStarting camera...")
        
        if not self.cap.isOpened():
            print("ERROR: Could not open camera!")
            return
        
        print("Camera opened successfully!\n")
        
        calibration_mode = False
        
        while True:
            start_time = time.time()
            
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hand
            hand_pos, mask = self.detect_hand(frame)
            self.hand_position = hand_pos
            
            # Update state if hand is detected
            if hand_pos:
                distance = self.calculate_distance(hand_pos, self.boundary_center)
                self.current_state = self.update_state(distance)
            else:
                self.current_state = "SAFE"
            
            # Draw visualizations
            self.draw_virtual_boundary(frame)
            self.draw_tracking_info(frame)
            self.draw_state_overlay(frame)
            
            # Show calibration mode info
            if calibration_mode:
                cv2.putText(frame, "CALIBRATION MODE - Adjust lighting", 
                           (10, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Display frames
            cv2.imshow('Hand Tracking System', frame)
            cv2.imshow('Hand Detection Mask', mask)
            
            # Update FPS
            frame_time = time.time() - start_time
            self.update_fps(frame_time)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                calibration_mode = not calibration_mode
                print(f"Calibration mode: {'ON' if calibration_mode else 'OFF'}")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("Session Summary:")
        print(f"Average FPS: {self.fps:.1f}")
        print("=" * 60)


def main():
    """Main entry point."""
    tracker = HandTracker(camera_index=0)
    tracker.run()


if __name__ == "__main__":
    main()
