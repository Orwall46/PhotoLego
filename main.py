import glob
from PIL import Image
from scipy import spatial
import numpy as np


# Sources and settings
if __name__ == "__main__":
    main_photo_path = "elephant.jpg"
    tile_photos_path = "tiles\\*"
    tile_size = (7, 7)
    output_path = "output_full.jpg"


# Get all tiles
tile_paths = []
for file in glob.glob(tile_photos_path):
    tile_paths.append(file)


# Open and resize all tiles
tiles = []
for path in tile_paths:
    tile = Image.open(path)
    tile = tile.resize(tile_size)
    tiles.append(tile)


# Calculate dominant color
colors = []
for tile in tiles:
    mean_color = np.array(tile).mean(axis=0).mean(axis=0)
    colors.append(mean_color)


# Pixelate (resize) main photo
main_photo = Image.open(main_photo_path)
width, height = main_photo.size

if width <= height:
    cr_height = int(width*3/4)
    cr = int((height-cr_height)/2)
    main_photo = main_photo.crop((0, cr, width, height-cr))
    print(main_photo.size)
elif width > height and width/height > 4/3:
    cr_width = int(height*4/3)
    cr = int((width-cr_width)/2)
    main_photo = main_photo.crop((cr, 0, width-cr, height))
elif width > height:
    cr_height = int(width*3/4)
    cr = int((height-cr_height)/2)
    main_photo = main_photo.crop((0, cr, width, height-cr))

main_photo.thumbnail((510, 510), Image.Resampling.LANCZOS)

width = int(np.round(main_photo.size[0] / tile_size[0]))
height = int(np.round(main_photo.size[1] / tile_size[1]))

resized_photo = main_photo.resize((width, height), Image.Resampling.NEAREST)

# Find closest tile photo for every pixel
tree = spatial.KDTree(colors)
closest_tiles = np.zeros((width, height), dtype=np.uint32)


for i in range(width):
    for j in range(height):
        closest = tree.query(resized_photo.getpixel((i, j)))
        closest_tiles[i, j] = closest[1]


# Create an output image
output = Image.new('L', main_photo.size)
print(output.size)
total = len(range(width)) * len(range(height))
print(f"Total Lego Brings - {total}")

# Draw tiles
for i in range(width):
    for j in range(height):
        # Offset of tile
        x, y = i*tile_size[0], j*tile_size[1]
        # Index of tile
        index = closest_tiles[i, j]
        # Draw tile
        output.paste(tiles[index], (x, y))


# Save output
output.save(output_path)
