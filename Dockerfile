# Album Live Art — Spotify now-playing vinyl display.
#
# Build:  docker build -t album-live-art .
# Run:    docker run -p 8080:8080 --env-file .env album-live-art
#
# The first run needs an interactive Spotify OAuth callback, so generate the
# token cache once on the host (run app.py) and mount it in:
#   docker run -p 8080:8080 --env-file .env \
#     -v "$PWD/.cache-barath:/app/.cache-barath" album-live-art
#
# For a dedicated display (e.g. a Raspberry Pi wired to a monitor), point a
# fullscreen/kiosk browser at http://<host>:8080.
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python", "app.py"]
