# Real-Time Hand Tracking System with Virtual Boundary Detection

**Arvyax Internship Assignment**

A computer vision system that tracks hand position in real-time and detects proximity to a virtual boundary using classical CV techniques (no MediaPipe or OpenPose).

## Demo

The system provides real-time visual feedback with three states:
- 🟢 **SAFE** - Hand is far from the virtual boundary
- 🟡 **WARNING** - Hand is approaching the boundary
- 🔴 **DANGER** - Hand is extremely close/touching the boundary

When in DANGER state, a flashing **"!!! DANGER DANGER !!!"** warning appears on screen.

## Features

✅ **Hand Detection without pose APIs**
- Skin color segmentation using HSV color space
- Gaussian blur for noise reduction
- Morphological operations (opening, closing, dilation)
- Contour detection and analysis
- Convex hull for hand region identification

✅ **Virtual Boundary**
- Circular boundary drawn at screen center
- Two zones: Warning zone (yellow) and Danger zone (red)
- Real-time distance calculation

✅ **Dynamic State Logic**
- **SAFE**: Distance > 120 pixels
- **WARNING**: Distance 50-120 pixels  
- **DANGER**: Distance < 50 pixels

✅ **Visual Feedback Overlay**
- Current state display with color coding
- Hand position marker (green dot)
- Distance line and measurement
- Flashing DANGER warning
- Real-time FPS counter
- Debug mask window

✅ **Real-Time Performance**
- Target: ≥8 FPS on CPU
- Optimized with efficient image processing
- FPS averaging over 30 frames
- Works on standard laptop webcam

## Technical Approach

### Hand Detection Pipeline:

1. **Color Space Conversion**: BGR → HSV
2. **Noise Reduction**: Gaussian blur (5x5 kernel)
3. **Skin Detection**: HSV range filtering
   - Lower bound: [0, 20, 70]
   - Upper bound: [20, 255, 255]
4. **Morphological Cleanup**:
   - Closing: Fill small holes
   - Opening: Remove noise
   - Dilation: Enhance hand region
5. **Contour Analysis**:
   - Find largest contour (assumed to be hand)
   - Filter by minimum area (3000 pixels)
   - Calculate centroid using moments

### Distance Calculation:
- Euclidean distance from hand centroid to boundary center
- Real-time state updates based on thresholds

## Requirements

- Python 3.7+
- OpenCV 4.8+
- NumPy 1.24+
- Webcam

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
```

## Usage

### Run the System

```bash
python hand_tracker.py
```

### Controls

- **Show your hand** to the camera (palm facing camera works best)
- **Move your hand** towards the center circle
- **Observe state changes**: SAFE → WARNING → DANGER
- Press **'q'** to quit
- Press **'c'** to toggle calibration mode (for different lighting)

### Tips for Best Results

1. **Lighting**: Use good, even lighting
2. **Background**: Plain background works better
3. **Hand Position**: Palm facing camera with fingers spread
4. **Distance**: Start ~2 feet from camera
5. **Skin Tone**: Works with various skin tones; adjust HSV range if needed

## System Output

### Main Window: "Hand Tracking System"
- Live camera feed with overlays
- Virtual boundary (yellow and red circles)
- Hand position marker (green dot)
- Distance line and measurement
- State display (top left)
- FPS counter (top right)
- DANGER warning (bottom, when triggered)

### Debug Window: "Hand Detection Mask"
- Binary mask showing detected hand region
- Useful for troubleshooting detection issues

## Performance

Tested on:
- **Hardware**: Intel Core i5 (CPU only)
- **Camera**: 640x480 @ 30fps
- **Achieved FPS**: 15-25 FPS (exceeds 8 FPS requirement)

Performance optimizations:
- Reduced frame resolution (640x480)
- Efficient morphological operations
- Single largest contour processing
- Minimal computational overhead

## Troubleshooting

### Hand Not Detected
- Check lighting conditions
- Ensure hand is clearly visible
- Try calibration mode ('c' key)
- Adjust HSV range in code if needed

### Low FPS
- Close other applications
- Reduce camera resolution
- Check CPU usage
- Ensure camera drivers are updated

### False Detections
- Use plain background
- Remove objects with similar skin color
- Adjust minimum contour area threshold

## Code Structure

```python
class HandTracker:
    def __init__()              # Initialize camera and parameters
    def detect_hand()           # Skin detection + contour analysis
    def calculate_distance()    # Euclidean distance calculation
    def update_state()          # SAFE/WARNING/DANGER logic
    def draw_virtual_boundary() # Draw circular boundary
    def draw_tracking_info()    # Hand marker and distance line
    def draw_state_overlay()    # State display and DANGER warning
    def update_fps()            # FPS calculation
    def run()                   # Main processing loop
```

## Technical Details

### Classical CV Techniques Used:
1. **Color Segmentation**: HSV-based skin detection
2. **Gaussian Blur**: Noise reduction
3. **Morphological Operations**: Mask cleanup
4. **Contour Detection**: Hand region identification
5. **Moments Calculation**: Centroid computation
6. **Convex Hull**: Hand shape analysis (implicit in contour)

### NOT Used (Per Requirements):
- ❌ MediaPipe
- ❌ OpenPose
- ❌ Cloud AI APIs
- ❌ Pre-trained pose detection models

## Assignment Requirements ✓

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Real-time hand tracking | ✅ | Color segmentation + contours |
| No MediaPipe/OpenPose | ✅ | Classical CV only |
| Virtual boundary | ✅ | Circular boundary at center |
| Distance-based states | ✅ | SAFE/WARNING/DANGER |
| Visual feedback | ✅ | Overlays + DANGER warning |
| ≥8 FPS on CPU | ✅ | Achieves 15-25 FPS |
| OpenCV/NumPy allowed | ✅ | Used for implementation |

## Future Enhancements

- Multi-hand tracking
- Gesture recognition
- Adjustable boundary shapes
- Configuration file for parameters
- Recording/playback functionality
- Multiple virtual objects

## Author

Created for Arvyax Internship Application

## License

This project is created for assignment submission purposes.
