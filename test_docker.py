#!/usr/bin/env python3
"""
Simplified test for Docker (no numpy dependency)
"""

import sys
import os
sys.path.insert(0, '/app')

try:
    import myalgo
    print("✅ Module imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_basic():
    """Basic test without numpy"""
    print("\n=== Basic Conversion Test ===")
    
    # Simple 2x2 image
    rgb_image = [
        [[255.0, 0.0, 0.0],    # Red
         [0.0, 255.0, 0.0]],   # Green
        [[0.0, 0.0, 255.0],    # Blue
         [255.0, 255.0, 255.0]]  # White
    ]
    
    gray = myalgo.GrayScale.convert_to_gray(rgb_image)
    
    # Expected values
    expected_red = 0.299 * 255
    expected_green = 0.587 * 255
    expected_blue = 0.114 * 255
    expected_white = 255.0
    
    print(f"Red pixel: {gray[0][0]:.2f} (expected: {expected_red:.2f})")
    print(f"Green pixel: {gray[0][1]:.2f} (expected: {expected_green:.2f})")
    print(f"Blue pixel: {gray[1][0]:.2f} (expected: {expected_blue:.2f})")
    print(f"White pixel: {gray[1][1]:.2f} (expected: {expected_white:.2f})")
    
    # Check
    errors = []
    if abs(gray[0][0] - expected_red) > 1e-10:
        errors.append("Red pixel mismatch")
    if abs(gray[0][1] - expected_green) > 1e-10:
        errors.append("Green pixel mismatch")
    if abs(gray[1][0] - expected_blue) > 1e-10:
        errors.append("Blue pixel mismatch")
    if abs(gray[1][1] - expected_white) > 1e-10:
        errors.append("White pixel mismatch")
    
    if errors:
        print(f"❌ Errors: {errors}")
        return False
    else:
        print("✅ All basic tests passed")
        return True

def test_error_handling():
    """Test error handling"""
    print("\n=== Error Handling Test ===")
    
    tests = [
        ("Empty image", [], True),
        ("Wrong dimensions", [[[1,2,3]], [[4,5,6], [7,8,9]]], True),
        ("Wrong channels", [[[1,2], [3,4]]], True),
    ]
    
    passed = 0
    for name, image, should_fail in tests:
        try:
            myalgo.GrayScale.convert_to_gray(image)
            if should_fail:
                print(f"❌ {name}: Should have failed but didn't")
            else:
                print(f"✅ {name}: Passed")
                passed += 1
        except Exception as e:
            if should_fail:
                print(f"✅ {name}: Correctly failed ({type(e).__name__})")
                passed += 1
            else:
                print(f"❌ {name}: Unexpected error: {e}")
    
    if passed == len(tests):
        print("✅ All error tests passed")
        return True
    else:
        print(f"❌ Error tests: {passed}/{len(tests)} passed")
        return False

def main():
    print("=" * 60)
    print("Testing myalgo in Docker")
    print("=" * 60)
    
    test1 = test_basic()
    test2 = test_error_handling()
    
    print("\n" + "=" * 60)
    print(f"Results: Test 1: {'✅' if test1 else '❌'}, Test 2: {'✅' if test2 else '❌'}")
    
    if test1 and test2:
        print("🎉 All Docker tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
