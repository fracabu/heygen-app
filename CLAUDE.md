# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HeyGen API integration project for generating AI avatar videos. Reference documentation from docs.heygen.com is stored in the project root.

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run any script
python <script_name>.py
```

## Project Structure

- `config.py` - API configuration with `HEYGEN_API_KEY`, `BASE_URL`, and `get_headers()` helper
- `utils_crediti.py` - Check remaining API credits via `check_credits()`
- `utils_assets.py` - Asset management: `list_assets()`, `upload_image()`, `delete_asset()`
- Numbered scripts (`01_*.py`, `02_*.py`, etc.) - Example workflows in progressive complexity

## Script Workflow

Scripts are numbered to indicate learning progression:
1. `01_list_avatars_voices.py` - List available avatars/voices (no credits used)
2. `02_create_simple_video.py` - Create single-scene video
3. `03_multi_scene_video.py` - Create multi-scene video with different backgrounds
4. `04_video_casa_vacanze.py` - Complete workflow: upload images → create multi-scene video

## Architecture Pattern

All scripts follow this pattern:
1. Import `BASE_URL` and `get_headers()` from `config.py`
2. Build payload with `video_inputs` array (one per scene)
3. POST to `/v2/video/generate` → get `video_id`
4. Poll `/v1/video_status.get` until `completed` or `failed`

For image backgrounds: upload to `https://upload.heygen.com/v1/asset` first, then use returned `image_asset_id` in background config.

## Authentication

All requests require `X-Api-Key` header with API token from HeyGen App Settings > API tab.

```
headers = {
    "X-Api-Key": "<your-api-key>",
    "Content-Type": "application/json"
}
```

## Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v2/video/generate` | POST | Create avatar video (1-50 scenes) |
| `/v1/video_status.get?video_id={id}` | GET | Check video status |
| `/v2/avatars` | GET | List available avatars |
| `/v2/voices` | GET | List available voices |
| `/v2/template/{id}/generate` | POST | Generate video from template |
| `/v1/asset` | POST | Upload asset (image/audio/video) |

## Video Generation - Request Structure

```json
{
  "video_inputs": [
    {
      "character": {
        "type": "avatar",
        "avatar_id": "<avatar_id>",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "Text to speak",
        "voice_id": "<voice_id>"
      },
      "background": {
        "type": "color",
        "value": "#FAFAFA"
      }
    }
  ],
  "dimension": {
    "width": 1280,
    "height": 720
  }
}
```

## Voice Input Options

**Text-to-speech:**
```json
"voice": {
  "type": "text",
  "input_text": "Your script here",
  "voice_id": "<voice_id>"
}
```

**Audio file:**
```json
"voice": {
  "type": "audio",
  "audio_url": "https://..."
}
```
Or use `audio_asset_id` instead of `audio_url`.

## Background Options

| Type | Configuration |
|------|---------------|
| Color | `{"type": "color", "value": "#HEXCODE"}` |
| Image | `{"type": "image", "url": "..."}` or `{"type": "image", "image_asset_id": "..."}` |
| Video | `{"type": "video", "video_asset_id": "...", "play_style": "loop"}` |

**Video play_style values:** `fit_to_scene`, `freeze`, `loop`, `full_video`

**Green screen:** Use `"value": "#008000"` with color type.

## Video Status Polling

```python
import time
import requests

while True:
    response = requests.get(
        f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
        headers=headers
    )
    status = response.json()["data"]["status"]

    if status == "completed":
        video_url = response.json()["data"]["video_url"]
        break
    elif status == "failed":
        break
    time.sleep(5)
```

## Template Variables

```python
payload = {
    "title": "Video Title",
    "variables": {
        "variable_name": {
            "name": "variable_name",
            "type": "text",
            "properties": {"content": "Value"}
        }
    }
}
```

## API Limits by Plan

| Plan | Credits/mo | Concurrent | Max Duration | Resolution |
|------|------------|------------|--------------|------------|
| Free | 10 | 1 | 3 min | 720p |
| Pro | 100 | 3 | 5 min | 1080p |
| Scale | 660 | 6 | 30 min | 4K |

## Credit Costs

- Photo Avatar: 1 credit/min (30 sec increments)
- Video Avatar: 2 credits/min (30 sec increments)
- Avatar IV (from photo): 6 credits/min
- Streaming: 0.2 credits/min

## Resource Limits

- Text input: max 5000 characters
- Audio input: max 10 minutes
- Max 50 scenes per video
- Video URLs expire after 7 days
- Supported formats: MP4 (<100MB), JPG/PNG (<50MB), WAV/MP3 (<50MB)
- Dimension limits: 128 < width/height < 4096

## Video Status Values

- `pending`: Queued for rendering
- `waiting`: In waiting state
- `processing`: Currently rendering
- `completed`: Ready for download
- `failed`: Error occurred

## Special Features

- **WebM transparent videos**: Only HeyGen studio avatars, paid plans only
- **Avatar IV**: Create video from single photo with custom motion prompts
- **Templates**: Reusable video designs with variable placeholders
