#!/usr/bin/env python3
"""
Full coverage icon processor for Simple Editor
Creates icons that fill the entire bubble space by cropping and scaling appropriately
"""

import os
import subprocess
import shutil
from PIL import Image

def crop_to_content(image, padding=0):
    """
    Crop image to remove any transparent or white padding around the content
    
    Args:
        image: PIL Image object
        padding: Additional padding to keep around content (in pixels)
    
    Returns:
        Cropped PIL Image
    """
    # Convert to RGBA if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get the bounding box of non-transparent content
    bbox = image.getbbox()
    
    if bbox is None:
        # No content found, return original
        return image
    
    # Add padding around the content
    x1, y1, x2, y2 = bbox
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(image.width, x2 + padding)
    y2 = min(image.height, y2 + padding)
    
    # Crop the image
    cropped = image.crop((x1, y1, x2, y2))
    
    return cropped

def create_full_coverage_icon(source_png: str = "simpleeditor.png", output_dir: str = "Simple Editor.iconset"):
    """
    Create icons that fill the entire bubble space
    
    Args:
        source_png: Path to the source PNG file
        output_dir: Directory to create the iconset in
    """
    # Check if source file exists
    if not os.path.exists(source_png):
        print(f"Error: Source PNG file not found: {source_png}")
        return False
    
    # Create iconset directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Standard macOS icon sizes
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    
    # Load the source image
    try:
        source_img = Image.open(source_png)
        print(f"✓ Loaded source image: {source_png} ({source_img.size[0]}x{source_img.size[1]})")
        
        # Convert to RGBA if not already
        if source_img.mode != 'RGBA':
            source_img = source_img.convert('RGBA')
            
        # Crop to remove any existing padding
        cropped_img = crop_to_content(source_img, padding=20)  # Keep a small padding
        print(f"✓ Cropped image to: {cropped_img.size[0]}x{cropped_img.size[1]}")
            
    except Exception as e:
        print(f"Error loading source image: {e}")
        return False
    
    # Generate icons for each size
    for size, filename in sizes:
        try:
            # Create a new image with the target size and transparent background
            icon_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            
            # Calculate scaling to fill the entire icon space
            # We want the icon to fill the whole bubble, so we'll scale it to fill the entire size
            scale_factor = min(size / cropped_img.width, size / cropped_img.height)
            
            # Calculate the new size after scaling
            new_width = int(cropped_img.width * scale_factor)
            new_height = int(cropped_img.height * scale_factor)
            
            # Resize the cropped image
            resized_img = cropped_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Calculate position to center the resized image
            x_offset = (size - new_width) // 2
            y_offset = (size - new_height) // 2
            
            # Paste the resized image onto the transparent background
            icon_img.paste(resized_img, (x_offset, y_offset), resized_img)
            
            # Save the icon
            output_path = os.path.join(output_dir, filename)
            icon_img.save(output_path, "PNG")
            print(f"✓ Created {filename} ({size}x{size}) - Full coverage")
            
        except Exception as e:
            print(f"Error creating {filename}: {e}")
            return False
    
    print(f"✓ Created iconset in {output_dir}")
    return True

def create_icns(iconset_dir: str = "Simple Editor.iconset", output_file: str = "icon.icns"):
    """
    Create ICNS file for macOS
    
    Args:
        iconset_dir: Directory containing the iconset
        output_file: Output ICNS filename
    """
    try:
        # Convert to ICNS using iconutil
        subprocess.run([
            "iconutil", "-c", "icns", iconset_dir, "-o", output_file
        ], check=True)
        print(f"✓ Created {output_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"⚠ Could not create ICNS file (iconutil not found)")
        print("  Creating simple ICNS from largest PNG...")
        
        # Fallback: Create a simple ICNS by copying the largest PNG
        try:
            png_files = [f for f in os.listdir(iconset_dir) if f.endswith('.png')]
            if png_files:
                # Use the 512x512 version if available, otherwise the largest
                largest_png = None
                for png_file in png_files:
                    if '512x512' in png_file:
                        largest_png = png_file
                        break
                
                if not largest_png:
                    # Find the largest file by size
                    largest_size = 0
                    for png_file in png_files:
                        file_path = os.path.join(iconset_dir, png_file)
                        if os.path.getsize(file_path) > largest_size:
                            largest_size = os.path.getsize(file_path)
                            largest_png = png_file
                
                if largest_png:
                    # Copy the largest PNG as a simple ICNS
                    shutil.copy2(os.path.join(iconset_dir, largest_png), output_file)
                    print(f"✓ Created simple {output_file} from {largest_png}")
                    return True
                else:
                    print("  No PNG files found in iconset")
                    return False
            else:
                print("  No PNG files found in iconset")
                return False
        except Exception as e:
            print(f"  Error creating simple ICNS: {e}")
            return False

def main():
    """Main function to generate the app icon"""
    print("Creating full coverage app icon for Simple Editor...")
    
    # Create iconset
    if create_full_coverage_icon():
        # Create ICNS
        create_icns()
        print("✓ Full coverage icon generation complete!")
    else:
        print("✗ Icon generation failed!")

if __name__ == "__main__":
    main()
