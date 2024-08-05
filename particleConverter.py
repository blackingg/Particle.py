from PIL import Image, ImageDraw, ImageFont
import numpy as np

def generate_particles(new_text, image_width, image_height, font_path='arial.ttf'):
    if not new_text:
        return []

    # Create a blank image with black background
    image = Image.new('RGB', (image_width, image_height), 'black')
    draw = ImageDraw.Draw(image)

    # Dynamically adjust font size
    font_size = min(image_width // len(new_text), 200)
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text position using font.getbbox
    text_bbox = draw.textbbox((0, 0), new_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2

    # Draw the text onto the image
    draw.text((text_x, text_y), new_text, font=font, fill='white')

    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    image_data = np.array(grayscale_image)

    # Generate particles
    particles = []
    for y in range(0, image_data.shape[0], 2):
        for x in range(0, image_data.shape[1], 2):
            if image_data[y, x] > 128:  # Checking for "white" pixels
                particles.append({
                    'x': x,
                    'y': y,
                    'originX': x,
                    'originY': y,
                    'radius': 1,
                    'color': 'white',
                    'vx': 0,
                    'vy': 0,
                    'mass': 1,
                })

    return particles

def save_particles_to_file(particles, filename):
    with open(filename, 'w') as file:
        for particle in particles:
            file.write(f"{particle}\n")

# Main script
new_text = input("Enter the text: ")
image_width = 800
image_height = 600
font_path = 'arial.ttf'  # Change this to the path of your .ttf file

particles = generate_particles(new_text, image_width, image_height, font_path)
save_particles_to_file(particles, 'particles.txt')

print(f"Generated {len(particles)} particles. Details saved to particles.txt.")
