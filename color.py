from PIL import Image
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
import time
import globals


def compute_palette(image_path, num_colors=5):
    """Single-shot dominant-colour extraction, most-dominant colour first.

    Returns a list of [r, g, b] lists. Cheap enough to run once whenever new
    artwork arrives, instead of looping forever on a timer.
    """
    image = Image.open(image_path).convert("RGB").resize((256, 256))
    pixels = np.array(image).reshape((-1, 3))

    # random_state/n_init make the result stable so the same artwork yields the
    # same palette every time instead of drifting.
    kmeans = MiniBatchKMeans(n_clusters=num_colors, batch_size=2048, random_state=42, n_init=3)
    labels = kmeans.fit_predict(pixels)
    # cluster_centers_ come back in arbitrary order, so order clusters by pixel
    # count (most-dominant first) — palette[0] is then the colour that actually
    # covers the most of the artwork.
    counts = np.bincount(labels, minlength=num_colors)
    order = np.argsort(counts)[::-1]
    centers = kmeans.cluster_centers_[order]
    return [[max(0, min(255, int(c))) for c in color] for color in centers]


def get_color_palette_min_batch(image_path, num_colors=5):
    """Legacy polling loop, kept for backwards compatibility. The app now calls
    compute_palette() event-driven from the music thread instead."""
    while True:
        globals.global_palette = compute_palette(image_path, num_colors)
        print(f"Finished calculating palette {globals.global_palette}")
        time.sleep(5)


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
