
import sys
import os

# Add the directory to path
sys.path.append('/home/al-mubtakir/bayan_python_ide22/tezniti_3d')

print("1. Testing Imports...")
try:
    import ai_bridge
    print("   ✅ ai_bridge imported successfully.")
except ImportError as e:
    print(f"   ❌ Failed to import ai_bridge: {e}")
    sys.exit(1)

try:
    # We expect this to print some warnings about Kivy if in headless, but import should work
    import tezniti_3d
    print("   ✅ tezniti_3d imported successfully (dependency checks passed).")
except ImportError as e:
    print(f"   ❌ Failed to import tezniti_3d: {e}")
except SystemExit:
    print("   ⚠️ tezniti_3d called sys.exit() (likely due to missing Kivy, which is expected/handled).")


print("\n2. Testing Intelligence Bridge Logic...")
try:
    bridge = ai_bridge.TeznitiIntelligenceBridge()
    print("   ✅ Bridge initialized.")
    
    # Test 1: English Text Understanding (Smart Parsing)
    text = "I need a helical gear with module 2.5 and 32 teeth"
    print(f"   Input Text: '{text}'")
    result = bridge.understand_request(text)
    if result:
        print(f"   ✅ Text Result: Type={result.equation_type}, Params={result.parameters}")
        print(f"   Reasoning: {result.reasoning}")
        if "Bayan Logic" in result.reasoning:
             print("   🌟 SUCCESS: Real Bayan Engine was used!")
        else:
             print("   ⚠️ WARNING: Still using Mock Logic.")
    else:
        print("   ❌ Text Understanding failed.")

    # Test 1.5: Arabic Text Understanding (Advanced)
    text_ar = "أريد تصميم مسمار قطره 12 وطوله 60"
    print(f"\n   Input Arabic: '{text_ar}'")
    result_ar = bridge.understand_request(text_ar)
    if result_ar:
        print(f"   ✅ Arabic Result: Type={result_ar.equation_type}, Params={result_ar.parameters}")
        print(f"   Reasoning: {result_ar.reasoning}")
    else:
        print("   ❌ Arabic Understanding failed.")

    # Test 2: Visual Inference (Fake Square)
    # Square: (0,0) -> (100,0) -> (100,100) -> (0,100) -> (0,0)
    fake_stroke = [(0,0), (100,0), (100,100), (0,100), (0,0)]
    print(f"\n   Input Sketch: Square-like shape")
    viz_result = bridge.vision_inference([fake_stroke])
    if viz_result:
        print(f"   ✅ Vision Result: Type={viz_result.equation_type}, Params={viz_result.parameters}")
        print(f"   Reasoning: {viz_result.reasoning}")
    else:
        print("   ❌ Vision Inference failed.")

    # Test 1.6: Boite Rectangulaire (Priority Check)
    # User had issue where this became a box.
    # Note: 'Rectangulaire' contains 'aire' which matches nothing bad, but let's see.
    # Without 'bracket' keyword, it SHOULD be a box.
    text_box = "Boite Rectangulaire"
    print(f"\n   Input Priority Test 1: '{text_box}'")
    result_box = bridge.understand_request(text_box)
    print(f"   Result: Type={result_box.equation_type}")
    
    # Test 1.7: Support Rectangulaire (Should be Bracket)
    text_bracket = "Support Rectangulaire"
    print(f"\n   Input Priority Test 2: '{text_bracket}'")
    result_bracket = bridge.understand_request(text_bracket)
    print(f"   Result: Type={result_bracket.equation_type}")
    
    if result_bracket.equation_type in ['bracket', 'mounting_bracket']:
         print("   ✅ Priority Success: Support identified as Bracket.")
    else:
         print(f"   ❌ Priority Failure: Support identified as {result_bracket.equation_type}.")

    # Test 1.8: Bracket for Bolt (Should be Bracket, not Bolt)
    text_conflict = "Bracket for mounting a bolt"
    print(f"\n   Input Priority Test 3: '{text_conflict}'")
    result_conflict = bridge.understand_request(text_conflict)
    print(f"   Result: Type={result_conflict.equation_type}")
    
    if result_conflict.equation_type in ['bracket', 'mounting_bracket']:
         print("   ✅ Priority Success: Bracket > Bolt.")
    else:
         print(f"   ❌ Priority Failure: Became {result_conflict.equation_type} (Bolt priority too high?)")

    
    # Test 1.9: User's Complex Prompt (Reproducing the reported issue)
    text_complex = "Design a mechanical mounting bracket with a rectangular base of 120 mm length, 80 mm width, and 10 mm thickness. Add four bolt holes of 10 mm diameter, positioned 15 mm from each corner. Include a vertical support arm 80 mm high, 60 mm wide, and 10 mm thick."
    print(f"\n   Input User Case: '{text_complex}'")
    result_complex = bridge.understand_request(text_complex)
    print(f"   Result: Type={result_complex.equation_type}")
    
    if result_complex.equation_type == 'mounting_bracket':
         print("   ✅ User Case Success: Identified as mounting_bracket.")
    else:
         print(f"   ❌ User Case Failure: Identified as {result_complex.equation_type}.")

except Exception as e:
    print(f"   ❌ Bridge Logic Error: {e}")
