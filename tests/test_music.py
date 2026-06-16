from music import Track


def test_track_parses_spotify_payload():
    item = {
        "name": "Song Title",
        "duration_ms": 200000,
        "id": "abc123",
        "album": {
            "name": "The Album",
            "artists": [{"name": "The Artist"}],
            "images": [{"url": "http://img/cover.jpg"}],
        },
    }
    t = Track(album=item["album"], item=item)
    assert t.track_name == "Song Title"
    assert t.artists == "The Artist"
    assert t.album_name == "The Album"
    assert t.album_art_url == "http://img/cover.jpg"
    assert t.duration == 200000
    assert t.track_id == "abc123"
