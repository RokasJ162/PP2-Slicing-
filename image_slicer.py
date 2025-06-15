import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import logging
import json
import time

logging.basicConfig(
    filename='image.slicer_logger.log',
    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

with open('config.json') as f:
    config = json.load(f)

print("Begining to slice")
users_image = input("Input exact name of the image that is in your python projects' folder (eg. 'image.jpg'): ")

try:
    image = Image.open(users_image).convert('RGB')
except Exception as e:
    print(f"Error opening image: {e}")
    exit()

#stopwatch begin
start_time = time.perf_counter()

# Load and prepare image
image = Image.open(users_image).convert('RGB')
img_array = np.array(image)

strip_width = config["strip_width"]  # vertical slice width
strip_height = config["strip_height"] # horizontal slice height

# Slicing verticaly
vertical_strips = [img_array[:, i:i+strip_width, :] for i in range(0, img_array.shape[1], strip_width)]

# Enumerating into odds and evens
imgA_strips = []
for idx, strip in enumerate(vertical_strips):
    if idx % 2 == 0:
        imgA_strips.append(strip)

imgB_strips = []
for idx, strip in enumerate(vertical_strips):
    if idx % 2 == 1:
        imgB_strips.append(strip)

# Merging strips
imgA = np.hstack(imgA_strips)
imgB = np.hstack(imgB_strips)

# Slicing and merging horizontaly
def horizontal_split(img):
    strips = []
    for i in range(0, img.shape[0], strip_height):
        strips.append(img[i:i+strip_height, :, :])

    even_strips = []
    odd_strips = []

    for idx, strip in enumerate(strips):
        if idx % 2 == 0:
            even_strips.append(strip)
        else:
            odd_strips.append(strip)

    img1 = np.vstack(even_strips)
    img2 = np.vstack(odd_strips)

    return img1, img2

imgA1, imgA2 = horizontal_split(imgA)
imgB1, imgB2 = horizontal_split(imgB)

# Showing results
fig, axs = plt.subplots(2, 4, figsize=(16, 10))

axs[0, 0].imshow(img_array)
axs[0, 0].set_title('Original')
axs[0, 0].axis('off')

axs[0, 1].imshow(imgA)
axs[0, 1].set_title('imgA (even vertical strips)')
axs[0, 1].axis('off')

axs[0, 2].imshow(imgB)
axs[0, 2].set_title('imgB (odd vertical strips)')
axs[0, 2].axis('off')

axs[1, 0].imshow(imgA1)
axs[1, 0].set_title('imgA1 (even horizontal from A)')
axs[1, 0].axis('off')

axs[1, 1].imshow(imgA2)
axs[1, 1].set_title('imgA2 (odd horizontal from A)')
axs[1, 1].axis('off')

axs[1, 2].imshow(imgB1)
axs[1, 2].set_title('imgB1 (even horizontal from B)')
axs[1, 2].axis('off')

axs[1, 3].imshow(imgB2)
axs[1, 3].set_title('imgB2 (odd horizontal from B)')
axs[1, 3].axis('off')

axs[0, 3].axis('off')

plt.tight_layout()
output_filename = "Sliced image.jpg"
plt.savefig(output_filename, dpi=300)
plt.show()

end_time = time.perf_counter()
time_elapsed = end_time - start_time
logging.info(f'{time_elapsed} seconds elapsed.')

logging.shutdown()