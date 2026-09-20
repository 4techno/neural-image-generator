# Neural Image Generator

An AI image synthesis and prompt orchestration tool that generates high-quality artwork using Stable Diffusion and the DALL-E API. Supports batch prompt execution, style transfer pipelines, and local model inference via `diffusers`.

## Features

- **Multi-Backend Support**: Routes generation jobs to DALL-E 3, Stable Diffusion (local via `diffusers`), or Replicate hosted models.
- **Prompt Engineer**: Chain-of-thought prompt expander that enriches bare keywords into detailed compositional prompts.
- **Batch Mode**: Accepts a `.txt` list of prompts and generates all images concurrently, saving to organized output directories.
- **Style Transfer**: Apply reference style images to target content using IP-Adapter or ControlNet conditioning.
- **Metadata Logging**: Every generated image is saved with a `.json` sidecar containing the prompt, seed, model, and parameters.

## Quick Start

```bash
git clone https://github.com/4techno/neural-image-generator.git
cd neural-image-generator
pip install -r requirements.txt
```

### Generate a Single Image (DALL-E)

```bash
python generate.py --prompt "a cyberpunk robot engineer in a neon-lit lab" --backend dalle --size 1024x1024
```

### Batch Generation from Prompt File

```bash
python generate.py --batch prompts.txt --backend dalle --output ./output
```

## Architecture

```
generate.py
     │
     ├── --backend dalle      → OpenAI DALL-E 3 API
     ├── --backend sd         → Local Stable Diffusion (diffusers)
     └── --backend replicate  → Replicate hosted inference
```

## Requirements

```
openai>=1.30.0
diffusers>=0.27.0
transformers>=4.40.0
accelerate>=0.29.0
Pillow>=10.3.0
```

## License

MIT License.
