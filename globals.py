global_palette = None  # palette variable to serve html page (kept for /getPalette)

# Shared "now playing" state, updated by the music thread and read by /nowPlaying.
# art_version increments whenever new artwork is drawn so the frontend knows to
# crossfade to it; tempo (BPM) drives the vinyl rotation speed.
now_playing = {
    "track": None,
    "artist": None,
    "album": None,
    "art_version": 0,
    "palette": [[255, 255, 255]],
    "tempo": None,        # BPM, or None if unavailable
    "progress_ms": 0,
    "duration_ms": 0,
    "is_playing": False,
    "sampled_at": 0.0,    # server time.time() when progress was sampled
}
