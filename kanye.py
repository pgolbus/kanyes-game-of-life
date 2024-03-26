import numpy as np
import imageio
from PIL import Image

def initialize_board(size=(25, 25), density=0.1):
    """Create a random game board with a specified density of 'on' cells."""
    return np.random.choice([False, True], size=size, p=[1-density, density])

def apply_rules(board):
    """Apply the Game of Life rules."""
    neighbors = sum(np.roll(np.roll(board, i, 0), j, 1)
                    for i in (-1, 0, 1) for j in (-1, 0, 1)
                    if (i != 0 or j != 0))
    return (neighbors == 3) | (board & (neighbors == 2))

def create_frame(board, cell_image, overlay_image, cell_size):
    """Create a frame with custom PNGs for 'on' cells and an additional PNG overlay."""
    (height, width) = board.shape
    frame = Image.new('RGBA', (width * cell_size, height * cell_size), (255, 255, 255, 255))
    for row in range(height):
        for col in range(width):
            if board[row, col]:
                frame.paste(cell_image, (col * cell_size, row * cell_size), cell_image)
    # Paste the overlay image in the top left corner
    frame.paste(overlay_image, (0, 0), overlay_image)
    return frame

def game_of_life_to_gif_with_custom_png(output_filename, cell_image_path, overlay_image_path, frames=50, size=(15, 15), cell_size=50, interval=100, density=0.1):
    """Generate an animated GIF of the Game of Life with custom PNGs for 'on' cells and an additional PNG overlay."""
    cell_image = Image.open(cell_image_path).resize((cell_size, cell_size))
    overlay_image = Image.open(overlay_image_path)  # Load the overlay image without resizing, or resize as needed
    overlay_width, overlay_height = overlay_image.size
    scaled_width = int(overlay_width * 1.25)
    scaled_height = int(overlay_height * 1.25)
    overlay_image = overlay_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
    board = initialize_board(size, density)
    with imageio.get_writer(output_filename, mode='I', duration=interval / 1000.0, loop=0) as writer:
        for _ in range(frames):
            frame = create_frame(board, cell_image, overlay_image, cell_size)
            writer.append_data(np.array(frame))
            board = apply_rules(board)

# Adjust the path to your custom PNG, board size, cell size, and density as needed
game_of_life_to_gif_with_custom_png('game_of_life_custom.gif', 'bling.png', 'kanye.png', frames=30, size=(15, 15), cell_size=100, interval=100, density=0.1)
