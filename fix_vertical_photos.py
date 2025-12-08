"""
Converte foto verticali in orizzontali aggiungendo sfocatura ai lati
Crea copie nella cartella foto_casa_vacanze_fixed
"""

from PIL import Image, ImageFilter
import os

INPUT_FOLDER = "foto_casa_vacanze"
OUTPUT_FOLDER = "foto_casa_vacanze_fixed"
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

def fix_photo(input_path, output_path):
    """Converte foto verticale in orizzontale con sfondo sfocato"""

    img = Image.open(input_path)
    orig_width, orig_height = img.size

    # Calcola aspect ratio
    orig_ratio = orig_width / orig_height
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT

    if orig_ratio >= target_ratio:
        # Foto già orizzontale o quadrata - ridimensiona e basta
        img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        img_resized.save(output_path, quality=95)
        return "orizzontale (ridimensionata)"
    else:
        # Foto verticale - aggiungi sfondo sfocato ai lati
        # 1. Crea sfondo sfocato dalla stessa immagine
        background = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        background = background.filter(ImageFilter.GaussianBlur(radius=30))

        # 2. Ridimensiona foto mantenendo proporzioni
        scale = TARGET_HEIGHT / orig_height
        new_width = int(orig_width * scale)
        img_scaled = img.resize((new_width, TARGET_HEIGHT), Image.LANCZOS)

        # 3. Centra la foto sullo sfondo sfocato
        x_offset = (TARGET_WIDTH - new_width) // 2
        background.paste(img_scaled, (x_offset, 0))

        background.save(output_path, quality=95)
        return "verticale (con sfondo sfocato)"

def main():
    # Crea cartella output
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print(f"Processo foto da '{INPUT_FOLDER}' -> '{OUTPUT_FOLDER}'")
    print(f"Dimensione target: {TARGET_WIDTH}x{TARGET_HEIGHT}")
    print("="*60)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            result = fix_photo(input_path, output_path)
            print(f"{filename}: {result}")

    print("="*60)
    print(f"Fatto! Foto salvate in '{OUTPUT_FOLDER}'")
    print("\nOra modifica FOTO_FOLDER nello script per usare la nuova cartella")

if __name__ == "__main__":
    main()
