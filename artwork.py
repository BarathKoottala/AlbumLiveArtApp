import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image, ImageDraw
import requests
from auth import get_auth_token

def get_artwork(album_id):
    """
    Function to get album artwork of currenlty playing song
    """
    token = get_auth_token()
    parameters = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + token,
        "Host": "api.spotify.com",
    }
    print("album_id is: " + album_id)
    album_url = "https://api.spotify.com/v1/albums/" + album_id
    response = requests.get(album_url, params=parameters)
    print(response.json)
    return response

def delete_picture(image_path):
    """
    Function to clear pictures
    """
    os.remove(image_path)

def make_record_picture_circular(record_path, output_path):
    record = Image.open(record_path).convert("RGBA")
    record_diameter, record_height = record.size
    record_resized = record.resize((record_diameter, record_diameter), Image.Resampling.LANCZOS)
    record.save(output_path, format="PNG")
    print(f"Saved the resulting image to {output_path}")

def draw_record_overlay(record_path, album_path, output_path):
    # Step 1: Open the images

    record = Image.open(record_path).convert("RGBA")
    album = Image.open(album_path).convert("RGBA")
    
    # Step 2: Make the record circular
    record_width, record_height = record.size
    album_diameter = record_width // 2
    album_resized = album.resize((album_diameter, album_diameter), Image.Resampling.LANCZOS)

     # Step 3: Make the album circular
    mask = Image.new("L", (album_diameter, album_diameter), 0)  # Create a blank grayscale mask
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, album_diameter, album_diameter), fill=255)  # Draw a filled circle
    album_circular = Image.new("RGBA", (album_diameter, album_diameter))  # Create a circular album canvas
    album_circular.paste(album_resized, (0, 0), mask)  # Apply the mask to make the album circular

    # Step 4: Center the circular album on the record
    center_x = (record_width - album_diameter) // 2
    center_y = (record_height - album_diameter) // 2
    record.paste(album_circular, (center_x, center_y), album_circular)  # Use the album_circular as a mask
    
    # Step 5: Save the result
    record.save(output_path, format="PNG")
    print(f"Saved the resulting image to {output_path}")


# draw_record_overlay("./static/record.png", "./static/album_art.jpg", "./static/vinyl.png")
# make_record_picture_circular("./static/record.png", "./static/record.png")