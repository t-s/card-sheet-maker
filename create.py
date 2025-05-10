import os
import argparse
from PIL import Image
import math

def create_print_sheet(image_path, output_dir, copies=9, page_size=(8.5, 11), dpi=300):
    """
    Create a print sheet with multiple copies of an image arranged in a grid.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the output image
        copies: Number of copies to place on sheet (default: 9)
        page_size: Tuple of page width and height in inches (default: 8.5x11)
        dpi: Dots per inch for the output image (default: 300)
    """
    # Convert page size from inches to pixels
    page_width_px = int(page_size[0] * dpi)
    page_height_px = int(page_size[1] * dpi)
    
    # Calculate grid dimensions (square grid)
    grid_size = int(math.sqrt(copies))
    
    # Load the original image
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening {image_path}: {e}")
        return False
    
    # Calculate dimensions for each card on the sheet
    # Allow for 0.25 inch margins on all sides
    margin_px = int(0.25 * dpi)
    available_width = page_width_px - (2 * margin_px)
    available_height = page_height_px - (2 * margin_px)
    
    card_width = available_width // grid_size
    card_height = available_height // grid_size
    
    # Resize the original image to fit the card dimensions
    # Preserve aspect ratio
    img_aspect = img.width / img.height
    card_aspect = card_width / card_height
    
    if img_aspect > card_aspect:
        # Image is wider than card
        new_width = card_width
        new_height = int(card_width / img_aspect)
    else:
        # Image is taller than card
        new_height = card_height
        new_width = int(card_height * img_aspect)
    
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Create a new blank page with white background
    new_page = Image.new('RGB', (page_width_px, page_height_px), (255, 255, 255))
    
    # Place copies of the image in a grid
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate position for this card
            x = margin_px + (col * card_width) + ((card_width - new_width) // 2)
            y = margin_px + (row * card_height) + ((card_height - new_height) // 2)
            
            # Paste the resized image onto the page
            new_page.paste(resized_img, (x, y))
    
    # Create output filename
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_sheet.png")
    
    # Save the new page
    new_page.save(output_path, dpi=(dpi, dpi))
    print(f"Created sheet: {output_path}")
    return True

def process_directory(input_dir, output_dir, copies=9):
    """Process all images in a directory and create print sheets."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    processed = 0
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in image_extensions):
            if create_print_sheet(file_path, output_dir, copies):
                processed += 1
    
    print(f"Processed {processed} images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create print sheets with multiple copies of credit card sized images")
    parser.add_argument("input_dir", help="Directory containing input images")
    parser.add_argument("--output_dir", help="Directory for output sheets", default="output")
    parser.add_argument("--copies", type=int, default=9, help="Number of copies per sheet (default: 9)")
    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output_dir, args.copies)
