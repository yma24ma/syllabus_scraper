from PIL import Image, ImageEnhance, ImageOps
import numpy as np

def process_logo(input_path, output_path):
    print(f"Processing {input_path}...")
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Fuzz Removal: Check distance from white
        # If a pixel is very light (e.g., > 200 in all channels), it's likely background or fringe
        # Being more aggressive: if R,G,B are all high, make it transparent
        threshold = 220 
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            # Color Adjustment: Make the blues brighter/neon
            if item[2] > item[0] and item[2] > item[1]: # Blue dominant
                # Boost brightness/saturation
                # Create a neon cyan: High Green, High Blue, Low Red
                r = 0
                g = 255 
                b = 255
                # We blend the original intensity to keep anti-aliasing shape
                intensity = item[2] / 255.0
                
                # Dynamic alpha based on intensity to smooth edges? 
                # For now, let's just hard set the neon color but keep original alpha (255)
                # actually, to preserve the 'shape', we should respect the original darkness
                # Darker blue pixels in original -> Darker neon pixels? 
                # Or just flat neon. Let's try to keep some shading.
                
                factor = 1.2
                r_new = min(int(item[0] * factor), 50) # Keep red low
                g_new = min(int(item[1] * 2.5), 255)   # Boost green significantly
                b_new = min(int(item[2] * 2.0), 255)   # Boost blue
                
                new_data.append((r_new, g_new, b_new, 255))
            else:
                 # If it's a dark line (black/grey), keep it but maybe darken it to remove grey fuzz
                 if item[0] < 50 and item[1] < 50 and item[2] < 50:
                     new_data.append((0, 0, 0, 255)) # Pure black
                 else:
                     # Any other intermediate greys -> transparent to kill fuzz
                     new_data.append((255, 255, 255, 0))

    img.putdata(new_data)
    
    # Save as high-quality PNG
    img.save(output_path, "PNG", quality=100)
    print(f"Saved processed logo to {output_path}")

if __name__ == "__main__":
    # Original 'Option 1' logo path
    input_logo = "/Users/yukima24ma/.gemini/antigravity/brain/04d1c6c2-87b6-4c66-978f-1bb1febe1d66/logo_v1_doc_cal_1767425548441.png"
    output_logo = "assets/logo.png"
    process_logo(input_logo, output_logo)
