# HeyGen Video Generator

Python toolkit for creating AI avatar videos using the [HeyGen API](https://docs.heygen.com/).

## Features

- **List Resources** - Browse available avatars and voices
- **Single Scene Videos** - Quick video generation with one avatar
- **Multi-Scene Videos** - Create videos with multiple scenes and backgrounds
- **Image Backgrounds** - Upload custom images as video backgrounds
- **Asset Management** - Upload, list, and delete media assets
- **Credit Tracking** - Monitor API credit usage

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API key

Get your API key from [HeyGen App Settings](https://app.heygen.com/settings) > API tab.

Create a `.env` file:

```env
HEYGEN_API_KEY=your_api_key_here
```

### 3. Explore available resources (free)

```bash
python 01_list_avatars_voices.py
```

### 4. Create your first video

```bash
python 02_create_simple_video.py
```

## Scripts

| Script | Description | Credits |
|--------|-------------|---------|
| `01_list_avatars_voices.py` | List available avatars, voices, and check quota | Free |
| `02_create_simple_video.py` | Create a simple single-scene video | ~0.5-1 |
| `03_multi_scene_video.py` | Create video with multiple scenes | ~1-2 |
| `04_video_casa_vacanze.py` | Full workflow: upload images + multi-scene video | ~2-3 |

## Utilities

| File | Purpose |
|------|---------|
| `config.py` | API configuration and headers |
| `utils_crediti.py` | Check remaining API credits |
| `utils_assets.py` | Upload, list, and delete assets |

## API Usage Pattern

```python
from config import BASE_URL, get_headers
import requests

# 1. Create video
payload = {
    "video_inputs": [{
        "character": {"type": "avatar", "avatar_id": "...", "avatar_style": "normal"},
        "voice": {"type": "text", "input_text": "Hello!", "voice_id": "..."},
        "background": {"type": "color", "value": "#FAFAFA"}
    }],
    "dimension": {"width": 1280, "height": 720}
}

response = requests.post(f"{BASE_URL}/v2/video/generate", headers=get_headers(), json=payload)
video_id = response.json()["data"]["video_id"]

# 2. Poll for completion
while True:
    status = requests.get(f"{BASE_URL}/v1/video_status.get", headers=get_headers(), params={"video_id": video_id})
    if status.json()["data"]["status"] == "completed":
        print(status.json()["data"]["video_url"])
        break
```

## Background Types

```python
# Solid color
{"type": "color", "value": "#1a1a2e"}

# Image (upload first via utils_assets.py)
{"type": "image", "image_asset_id": "asset_id_here"}

# Video background
{"type": "video", "video_asset_id": "...", "play_style": "loop"}
```

## Credit Costs

| Avatar Type | Cost |
|-------------|------|
| Photo Avatar | 1 credit/min |
| Video Avatar | 2 credits/min |
| Avatar IV | 6 credits/min |

## Limits

- Max 5000 characters per text input
- Max 50 scenes per video
- Video URLs expire after 7 days
- Dimensions: 128-4096 px

## Resources

- [HeyGen API Docs](https://docs.heygen.com/)
- [API Reference](https://docs.heygen.com/reference)

## License

MIT
