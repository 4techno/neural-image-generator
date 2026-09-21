import argparse
import os
import sys
import json
import time
from pathlib import Path

def expand_prompt(raw: str) -> str:
    """Enrich a bare prompt with compositional detail."""
    style_suffix = ", cinematic lighting, 8K ultra-detailed, professional photography, trending on ArtStation"
    return raw.strip().rstrip(".") + style_suffix

def generate_dalle(prompt: str, size: str, output_dir: Path) -> str:
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        url = response.data[0].url
        import urllib.request
        slug = str(int(time.time()))
        img_path = output_dir / f"{slug}.png"
        meta_path = output_dir / f"{slug}.json"
        urllib.request.urlretrieve(url, img_path)
        meta = {"prompt": prompt, "model": "dall-e-3", "size": size, "url": url}
        meta_path.write_text(json.dumps(meta, indent=2))
        return str(img_path)
    except ImportError:
        print("[!] openai package not installed. Run: pip install openai")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Neural Image Generator")
    parser.add_argument("--prompt", type=str, help="Single prompt string")
    parser.add_argument("--batch", type=str, help="Path to .txt file with one prompt per line")
    parser.add_argument("--backend", default="dalle", choices=["dalle","sd","replicate"], help="Generation backend")
    parser.add_argument("--size", default="1024x1024", help="Image size (DALL-E: 1024x1024, 1792x1024, 1024x1792)")
    parser.add_argument("--output", default="./output", help="Output directory path")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompts = []
    if args.prompt:
        prompts = [args.prompt]
    elif args.batch:
        prompts = [l.strip() for l in Path(args.batch).read_text().splitlines() if l.strip()]
    else:
        print("Error: provide --prompt or --batch")
        sys.exit(1)

    for raw in prompts:
        enriched = expand_prompt(raw)
        print(f"[*] Generating: {raw[:60]}...")
        if args.backend == "dalle":
            result = generate_dalle(enriched, args.size, output_dir)
            print(f"[✓] Saved: {result}")
        else:
            print(f"[!] Backend '{args.backend}' requires local setup. See README for instructions.")

if __name__ == "__main__":
    main()
