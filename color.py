from PIL import Image
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
import time
import globals


def get_color_palette_min_batch(image_path, num_colors=5):
    while True:
        # Open image
        image = Image.open(image_path)
        # Convert to RGB
        image = image.convert("RGB")
        # Resize for fsater processing
        image = image.resize((256, 256))
        # Convert to numpy array
        image_array = np.array(image)
        # Reshape to 2D array
        pixels = image_array.reshape((-1, 3))

        # Apply K-Means clustering
        # kmeans = KMeans(n_clusters=num_colors)
        kmeans = MiniBatchKMeans(n_clusters=num_colors, batch_size=2048)
        kmeans.fit(pixels)
        # Get cluster centers (most dominant color)
        # Ensure values are within valid RGB range (0-255)
        globals.global_palette = [tuple(map(lambda x: max(0, min(255, int(x))), color)) for color in kmeans.cluster_centers_]
        print(f"Finished calculating palette {globals.global_palette}")
        time.sleep(5)
    # return globals.global_palette


def get_color_palette(image_path, num_colors=5):
    # Open image
    image = Image.open(image_path)
    # Convert to RGB
    image = image.convert("RGB")
    # Resize for fsater processing
    image = image.resize((256, 256))
    # Convert to numpy array
    image_array = np.array(image)
    # Reshape to 2D array
    pixels = image_array.reshape((-1, 3))

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    # Get cluster centers (most dominant color)
    palette = kmeans.cluster_centers_

    # Convert to RGB tuples
    palette = [tuple(map(int, color)) for color in palette]
    return palette


# Benchmarking / demo code below ran on import — it called the infinite
# get_color_palette_min_batch() loop and hung any importer. Guarded so the
# module can be imported by app.py.
if __name__ == "__main__":
    image_path = "./static/album_art.jpg"
    start_time = time.time()
    palette = get_color_palette(image_path)
    end_time = time.time()
    print(palette)
    print(f"Time took to process regular was {end_time-start_time} seconds")

    image_path = "./static/album_art.jpg"
    start_time = time.time()
    palette = get_color_palette_min_batch(image_path)
    end_time = time.time()
    print(palette)
    print(f"Time took to process using mini batch was {end_time-start_time} seconds")
