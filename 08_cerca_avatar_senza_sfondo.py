"""
Cerca avatar senza sfondo fisso (transparent, circle, o normal)
"""

import requests
from config import BASE_URL, get_headers

def find_avatars_no_background():
    """Trova avatar che permettono sfondo personalizzato"""

    r = requests.get(f"{BASE_URL}/v2/avatars", headers=get_headers())

    if r.status_code != 200:
        print(f"Errore: {r.status_code}")
        return

    data = r.json()
    avatars = data.get('data', {}).get('avatars', [])

    print(f"Totale avatar: {len(avatars)}\n")

    # Filtra avatar senza sfondo fisso
    no_bg_avatars = []

    for av in avatars:
        avatar_id = av.get('avatar_id', '')
        name = av.get('avatar_name', '')

        # Cerca avatar che NON hanno "office", "studio", "room" nel nome
        # e che hanno "transparent", "circle", "normal" o nessun suffisso di ambiente
        lower_id = avatar_id.lower()

        has_fixed_bg = any(word in lower_id for word in [
            '_office', '_studio', '_room', '_kitchen', '_library',
            '_cafe', '_lobby', '_outdoor', '_street', '_park'
        ])

        if not has_fixed_bg:
            no_bg_avatars.append(av)

    print("="*70)
    print("AVATAR SENZA SFONDO FISSO (probabili)")
    print("="*70)

    for av in no_bg_avatars[:30]:  # Mostra primi 30
        avatar_id = av.get('avatar_id', '')
        name = av.get('avatar_name', '')
        preview = av.get('preview_image_url', '')[:50] if av.get('preview_image_url') else 'N/A'

        print(f"\nID: {avatar_id}")
        print(f"Nome: {name}")

    print(f"\n\nTotale trovati: {len(no_bg_avatars)}")

    # Cerca specificamente "transparent" o "circle"
    print("\n" + "="*70)
    print("AVATAR CON 'transparent' o 'circle' nel nome")
    print("="*70)

    for av in avatars:
        avatar_id = av.get('avatar_id', '')
        lower_id = avatar_id.lower()

        if 'transparent' in lower_id or 'circle' in lower_id:
            print(f"\nID: {avatar_id}")
            print(f"Nome: {av.get('avatar_name', '')}")

if __name__ == "__main__":
    find_avatars_no_background()
