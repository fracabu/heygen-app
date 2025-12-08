"""
Dettaglio completo di un video specifico
"""

import requests
import json
from config import BASE_URL, get_headers

VIDEO_ID = "d4b5443a03984b13a97f237a5b51003e"

r = requests.get(
    f"{BASE_URL}/v1/video_status.get",
    headers=get_headers(),
    params={"video_id": VIDEO_ID}
)

print(f"Status: {r.status_code}\n")
print("Risposta completa:")
print(json.dumps(r.json(), indent=2))
