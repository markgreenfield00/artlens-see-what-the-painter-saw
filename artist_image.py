import os
from io import BytesIO
from datetime import datetime
from PIL import Image
from google import genai

# --- Setup ---
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
os.makedirs("outputs", exist_ok=True)

# --- Photoreal prompts per painting ---
PROMPTS = {
    "01_starry_night.jpg": (
        "Photorealistic travel photo (2025) of the real location Van Gogh might have seen "
        "before The Starry Night in Saint-Rémy-de-Provence. Shot on a modern DSLR, natural night lighting, "
        "realistic lens characteristics. No painterly textures."
    ),
    "02_water_lilies.jpg": (
        "Photorealistic daytime travel photo (2025) of Monet’s Giverny water garden: reflective pond with water lilies, "
        "arched Japanese-style footbridge, soft diffuse light, natural greenery. Modern DSLR look, real textures, "
        "no painterly effects."
    ),
    "03_persistence_memory.jpg": (
        "Photorealistic coastal Catalonia landscape (2025), as a plausible real scene inspiring Dalí’s The Persistence of Memory: "
        "rocky shoreline near Port Lligat/Cadaqués, quiet cove, sunlit rocks, sparse coastal vegetation. "
        "Modern DSLR look, real materials, no painterly textures."
    ),
}

def save_first_inline_image(response, base_name):
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            img = Image.open(BytesIO(part.inline_data.data))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = f"outputs/{base_name}_{ts}.png"
            img.save(out_path)
            print(f"✅ Saved: {out_path}")
            return True
    print("⚠️ No image returned—try re-running or tweak the prompt.")
    return False

def process_one(filename, prompt):
    path = os.path.join("inputs", filename)
    if not os.path.exists(path):
        print(f"❌ Missing: {path}")
        return
    img = Image.open(path)
    # Order: prompt first, then image (matches Studio behavior closely)
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt, img],
    )
    base_name = os.path.splitext(os.path.basename(filename))[0]
    save_first_inline_image(response, base_name)

def main():
    for fname, prompt in PROMPTS.items():
        print(f"\n--- Generating for {fname} ---")
        process_one(fname, prompt)

if __name__ == "__main__":
    main()
