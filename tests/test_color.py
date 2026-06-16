from PIL import Image

from color import compute_palette


def test_palette_returns_dominant_color_first(tmp_path):
    # 90% red, 10% blue -> the dominant (palette[0]) color must be the red region.
    img = Image.new("RGB", (100, 100), (200, 30, 30))
    for x in range(100):
        for y in range(90, 100):
            img.putpixel((x, y), (30, 30, 200))
    path = tmp_path / "art.png"
    img.save(path)

    palette = compute_palette(str(path), num_colors=3)

    assert len(palette) == 3
    r, g, b = palette[0]
    assert r > b  # dominant cluster is reddish, not the small blue strip


def test_palette_is_deterministic(tmp_path):
    img = Image.new("RGB", (64, 64), (120, 80, 40))
    img.putpixel((0, 0), (10, 200, 10))
    path = tmp_path / "art.png"
    img.save(path)

    assert compute_palette(str(path), 4) == compute_palette(str(path), 4)
