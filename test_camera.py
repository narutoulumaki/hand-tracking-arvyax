"""
Test script to diagnose camera and OpenCV issues
"""

import cv2
import numpy as np
import sys

print("=" * 60)
print("Hand Tracker Diagnostic Test")
print("=" * 60)

# Test 1: OpenCV version
print("\n[Test 1] Checking OpenCV...")
try:
    print(f"  ✓ OpenCV version: {cv2.__version__}")
except Exception as e:
    print(f"  ✗ OpenCV error: {e}")
    sys.exit(1)

# Test 2: NumPy version
print("\n[Test 2] Checking NumPy...")
try:
    print(f"  ✓ NumPy version: {np.__version__}")
except Exception as e:
    print(f"  ✗ NumPy error: {e}")
    sys.exit(1)

# Test 3: Camera access
print("\n[Test 3] Testing camera access...")
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("  ✗ Cannot open camera (index 0)")
        print("  Trying alternate cameras...")
        for i in range(1, 3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"  ✓ Found camera at index {i}")
                break
        else:
            print("  ✗ No cameras found")
            sys.exit(1)
    else:
        print("  ✓ Camera 0 opened successfully")
    
    # Test frame capture
    print("\n[Test 4] Testing frame capture...")
    ret, frame = cap.read()
    if ret:
        print(f"  ✓ Frame captured successfully")
        print(f"  Frame shape: {frame.shape}")
    else:
        print("  ✗ Failed to capture frame")
        cap.release()
        sys.exit(1)
    
    cap.release()
    
except Exception as e:
    print(f"  ✗ Camera test error: {e}")
    sys.exit(1)

# Test 5: Create a test window
print("\n[Test 5] Testing window creation...")
try:
    test_img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(test_img, "Test Window - Press 'q' to close", 
                (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow("Test Window", test_img)
    print("  ✓ Window created successfully")
    print("  A test window should appear. Press 'q' to close it.")
    
    # Wait for 'q' key
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
    print("  ✓ Window closed successfully")
    
except Exception as e:
    print(f"  ✗ Window test error: {e}")
    cv2.destroyAllWindows()
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("You can now run: python hand_tracker.py")
print("=" * 60)
