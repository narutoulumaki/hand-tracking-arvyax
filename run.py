"""
Run hand tracker with error handling
"""

import sys
import traceback

try:
    from hand_tracker import HandTracker
    
    print("\n" + "=" * 60)
    print("Starting Hand Tracking System...")
    print("=" * 60 + "\n")
    
    tracker = HandTracker(camera_index=0)
    tracker.run()
    
except KeyboardInterrupt:
    print("\n\nProgram interrupted by user")
except Exception as e:
    print("\n" + "=" * 60)
    print("ERROR occurred:")
    print("=" * 60)
    print(f"\n{type(e).__name__}: {e}\n")
    traceback.print_exc()
    print("\n" + "=" * 60)
    input("\nPress Enter to exit...")
finally:
    print("\nCleaning up...")
    import cv2
    cv2.destroyAllWindows()
