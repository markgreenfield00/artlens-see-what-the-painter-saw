# ArtLens — See What the Painter Saw

Transform famous paintings into contemporary, photorealistic travel photos of the real scenes their artists likely saw.

## Demo
- **AI Studio App (public):** https://ai.studio/apps/drive/1mEFf_dscV3mFMIDleVbC-OJQBK3Jve-e
- **Video demo (≤2 min):** <ADD_YOUTUBE_LINK_HERE>

## How it works
We use **Gemini 2.5 Flash Image Preview** via the `google-genai` SDK.  
We send a short, photography-first prompt and the input painting to `generate_content`, then save the returned `inline_data` image.

## Quickstart (local)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY="YOUR_KEY"   # do not commit your key
mkdir -p inputs outputs            # place a painting in inputs/
python artist_image.py
