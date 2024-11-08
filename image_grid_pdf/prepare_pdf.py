import os
import sys
from pathlib import Path

from PIL import Image
from natsort import natsorted
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


try:
    target_dir = sys.argv[1]
except IndexError:
    print("Usage: python prepare_pdf.py <target_dir> <output_pdf>")
    sys.exit(1)
target_dir = os.path.abspath(target_dir)
print(f"Creating PDF from PNG images in directory: {target_dir}")

output_pdf = sys.argv[2]

print(f"Output PDF file: {output_pdf}")


def create_pdf_with_dotted_grid(target_dir='.', output_pdf="output.pdf", print_titles=True, images_per_row=4, images_per_column=5, image_padding=10):
    # Define A4 page dimensions
    page_width, page_height = A4
    margin = 20  # Margin around the edges of the page

    # Calculate grid cell dimensions
    cell_width = (page_width - 2 * margin) / images_per_row
    cell_height = (page_height - 2 * margin) / images_per_column

    # Get all PNG files in the current directory, sorted in natural order
    listing = os.listdir(target_dir)
    image_files = [
        os.path.join(target_dir, filename) 
        for filename in listing 
        if filename.endswith('.png')
    ]
    image_files = natsorted(image_files)  # Natural sort the image files

    if not image_files:
        print("No PNG images found in the current directory.")
        return
    print(f"Found {len(image_files)} PNG images.")

    # Create a canvas for PDF output
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=A4)

    # Loop through images and add them to the PDF
    x_start, y_start = margin, page_height - margin - cell_height
    x, y = x_start, y_start

    for index, image_file in enumerate(image_files):
        # Open the image and resize it to fit within the grid cell
        img = Image.open(image_file)

        width = cell_width - image_padding
        # if width > 90:
        #     width = 90

        height = cell_height - image_padding
        # if height > 90:
        #     height = 90

        img.thumbnail((width, height))

        # Subscription
        file_name = Path(image_file).stem

        # Calculate position to center the image within the grid cell
        x_offset = (cell_width - img.width) / 2
        y_offset = (cell_height - img.height) / 2

        # Draw image on the canvas
        pdf_canvas.drawImage(image_file, x + x_offset, y + y_offset, width=img.width, height=img.height)

        if print_titles:
            # Draw the file name text above the image
            text_x = x + cell_width / 2  # Center the text horizontally
            text_y = y + y_offset - 15  # Position below the image with a small offset
            pdf_canvas.setFont("Helvetica", 8)  # Set font and size for text
            pdf_canvas.drawCentredString(text_x, text_y, file_name)  # Centered text above the image

        # Move to the next cell
        x += cell_width

        # If we've reached the end of a row, reset x and move down a row
        if (index + 1) % images_per_row == 0:
            x = x_start
            y -= cell_height

        # If we've filled the page, add dotted grid lines and start a new page
        if (index + 1) % (images_per_row * images_per_column) == 0:
            draw_dotted_grid(pdf_canvas, x_start, y_start, cell_width, cell_height, images_per_row, images_per_column, page_width, page_height, margin)
            pdf_canvas.showPage()
            x, y = x_start, y_start

    # Draw grid lines on the final page if it's partially filled
    if (index + 1) % (images_per_row * images_per_column) != 0:
        draw_dotted_grid(pdf_canvas, x_start, y_start, cell_width, cell_height, images_per_row, images_per_column, page_width, page_height, margin)

    # Save the PDF file
    pdf_canvas.save()
    print(f"PDF saved as '{output_pdf}'.")


def draw_dotted_grid(pdf_canvas, x_start, y_start, cell_width, cell_height, images_per_row, images_per_column, page_width, page_height, margin):
    # Set the dash style for dotted lines
    pdf_canvas.setDash(1, 3)  # 1pt dash, 3pt gap

    # Vertical grid lines
    for col in range(1, images_per_row):
        x = x_start + col * cell_width
        pdf_canvas.line(x, page_height - margin, x, margin)

    # Horizontal grid lines
    for row in range(images_per_column + 1):  # Adjusted range to include the first line at the top
        y = page_height - margin - row * cell_height
        pdf_canvas.line(margin, y, page_width - margin, y)

    # Reset dash style to solid for further drawing if needed
    pdf_canvas.setDash()


# Usage
create_pdf_with_dotted_grid(target_dir=target_dir, output_pdf=output_pdf)
