---
name: runninghub
description: "Generate images, videos, audio, and 3D models via RunningHub API (170+ endpoints). Covers text-to-image, image-to-video, text-to-speech, music generation, 3D modeling, image upscaling, and more. Run python3 /root/.openclaw/workspace/scripts/runninghub.py for all operations."
homepage: https://www.runninghub.cn
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3", "curl"] },
        "primaryEnv": "RUNNINGHUB_API_KEY",
      },
  }
---

# RunningHub Skill — Universal Media Generation

170+ API endpoints for image, video, audio, 3D, and text understanding.

Script path: `python3 /root/.openclaw/workspace/scripts/runninghub.py`
Data path: `/root/.openclaw/workspace/data/capabilities.json`

## Setup & account check

Before first use, run:

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py --check
```

React based on the `status` field in the JSON output:

- `"ready"` — All good. Proceed with generation. Shows wallet balance.
- `"no_key"` — Guide the user:
  1. Register at https://www.runninghub.cn
  2. Create API Key: https://www.runninghub.cn/enterprise-api/sharedApi (click "新建")
  3. Recharge wallet: https://www.runninghub.cn/vip-rights/4
  4. Configure: `openclaw skills config runninghub RUNNINGHUB_API_KEY <key>`
- `"no_balance"` — Wallet is empty, guide to recharge: https://www.runninghub.cn/vip-rights/4
- `"invalid_key"` — Key is invalid, guide to manage keys: https://www.runninghub.cn/enterprise-api/sharedApi

Do NOT attempt generation until status is `"ready"`.

## One-time install

```bash
mkdir -p /root/.openclaw/workspace/scripts /root/.openclaw/workspace/data
cp /data/RHClaw/runninghub/scripts/runninghub.py /root/.openclaw/workspace/scripts/runninghub.py
cp /data/RHClaw/runninghub/data/capabilities.json /root/.openclaw/workspace/data/capabilities.json
chmod +x /root/.openclaw/workspace/scripts/runninghub.py

mkdir -p /root/.openclaw/workspace/skills/runninghub
cp /data/RHClaw/runninghub/SKILL.md /root/.openclaw/workspace/skills/runninghub/SKILL.md
```

## Execution policy

- When user asks to generate/edit media, run immediately.
- Do not ask user to set/export API key first — the script resolves it from config.
- Do not pass placeholder values like `your_api_key_here`.
- If the script returns an error JSON, react based on the `error` field (see Error Handling below).

## Quick Routing Table

Use this table to pick the best endpoint for the user's intent. Rank 1 = most popular.

### Image Generation

| Intent | Best Endpoint | Alt | Notes |
|--------|--------------|-----|-------|
| Text to image | `rhart-image-n-pro/text-to-image` | `rhart-image-g-1.5/text-to-image` | General purpose, highest usage |
| Image to image (edit) | `rhart-image-n-pro/edit` | `rhart-image-g-1.5/edit` | Modify existing image with prompt |
| Ultra quality image | `rhart-image-n-pro-official/text-to-image-ultra` | `rhart-image-n-pro-official/edit-ultra` | Higher quality, slower |
| Midjourney style | `youchuan/text-to-image-v7` | `youchuan/text-to-image-niji7` | niji = anime style |
| Image upscale | `topazlabs/image-upscale-standard-v2` | `topazlabs/image-upscale-high-fidelity-v2` | Enhance resolution |
| AI image editing | `alibaba/qwen-image-2.0-pro/image-edit` | `alibaba/qwen-image-2.0/image-edit` | Qwen-based editing |

### Video Generation

| Intent | Best Endpoint | Alt | Notes |
|--------|--------------|-----|-------|
| Text to video | `rhart-video-s/text-to-video` | `rhart-video-s/text-to-video-pro` | Sora-based, most popular |
| Image to video | `rhart-video-s/image-to-video` | `rhart-video-s/image-to-video-pro` | Animate a still image |
| Realistic person i2v | `rhart-video-s-official/image-to-video-realistic` | | Optimized for real people |
| Start+end frame video | `rhart-video-v3.1-pro/start-end-to-video` | `vidu/start-end-to-video-q3-pro` | Two keyframes → video |
| Video extend | `rhart-video-v3.1-pro-official/video-extend` | `rhart-video-v3.1-fast-official/video-extend` | Extend existing video |
| Video editing | `rhart-video-g-official/edit-video` | `kling-video-o3-pro/video-edit` | Edit video with prompt |
| Reference to video | `rhart-video-v3.1-pro-official/reference-to-video` | `kling-video-o3-pro/reference-to-video` | Use reference video for style |
| Motion control | `kling-v3.0-pro/motion-control` | `kling-v2.6-pro/motion-control` | Control motion trajectory |
| Kling text to video | `kling-v3.0-pro/text-to-video` | `kling-video-o3-pro/text-to-video` | Kling model family |
| Kling image to video | `kling-v3.0-pro/image-to-video` | `kling-video-o3-pro/image-to-video` | Kling model family |
| Vidu text to video | `vidu/text-to-video-q3-pro` | `vidu/text-to-video-q3-turbo` | Vidu model (turbo = faster) |
| MiniMax video | `minimax/hailuo-02/t2v-pro` | `minimax/hailuo-2.3/t2v-pro` | Hailuo video models |
| Video upscale | `topazlabs/video-upscale` | | Enhance video resolution |

### Audio

| Intent | Best Endpoint | Notes |
|--------|--------------|-------|
| Text to speech (best) | `rhart-audio/text-to-audio/speech-2.8-hd` | HD quality, supports interjections |
| Text to speech (fast) | `rhart-audio/text-to-audio/speech-2.8-turbo` | Faster, lower cost |
| Music generation | `rhart-audio/text-to-audio/music-2.5` | Prompt + lyrics |
| Voice clone | `rhart-audio/text-to-audio/voice-clone` | Clone voice from audio sample |

### 3D Model Generation

| Intent | Best Endpoint | Notes |
|--------|--------------|-------|
| Text to 3D | `hunyuan3d-v3.1/text-to-3d` | Hunyuan 3D v3.1 |
| Image to 3D | `hunyuan3d-v3.1/image-to-3d` | Photo → 3D model |
| Multi-image to 3D | `hitem3d-v2/multi-image-to-3d` | Multiple views → 3D |

### Text Understanding (Multimodal)

| Intent | Best Endpoint | Notes |
|--------|--------------|-------|
| Describe image | `rhart-text-g-25-pro/image-to-text` | Image understanding |
| Describe video | `rhart-text-g-25-pro/video-to-text` | Video understanding |
| Text processing | `rhart-text-g-25-pro/text-to-text` | Text-to-text tasks |

## Command Reference

### Text to image

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-image-n-pro/text-to-image \
  --prompt "a cute puppy playing on green grass, 4K cinematic lighting" \
  --param resolution=2k --param aspectRatio=16:9 \
  --output /tmp/runninghub-output/puppy.png
```

### Image to image (edit)

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-image-n-pro/edit \
  --prompt "change the background to a cyberpunk city at night" \
  --image /tmp/runninghub-output/puppy.png \
  --param resolution=2k \
  --output /tmp/runninghub-output/puppy-edited.png
```

### Text to video

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-video-s/text-to-video \
  --prompt "a puppy running through a meadow, cinematic slow motion" \
  --param duration=10 --param aspectRatio=16:9 \
  --output /tmp/runninghub-output/puppy-video.mp4
```

### Image to video

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-video-s/image-to-video \
  --prompt "the puppy starts running and wagging its tail" \
  --image /tmp/runninghub-output/puppy.png \
  --param duration=10 \
  --output /tmp/runninghub-output/puppy-animated.mp4
```

### Text to speech

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-audio/text-to-audio/speech-2.8-hd \
  --prompt "Hello! Welcome to RunningHub, your AI creation platform." \
  --param voiceId=male-qn-qingse \
  --output /tmp/runninghub-output/speech.mp3
```

### Music generation

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint rhart-audio/text-to-audio/music-2.5 \
  --prompt "upbeat electronic dance music, 128 BPM, energetic" \
  --param lyrics="[Verse 1] Feel the beat..." \
  --output /tmp/runninghub-output/music.mp3
```

### Image to 3D

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint hunyuan3d-v3.1/image-to-3d \
  --image /tmp/runninghub-output/object.png \
  --param enablePbr=true \
  --output /tmp/runninghub-output/model.glb
```

### Image upscale

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --endpoint topazlabs/image-upscale-standard-v2 \
  --image /tmp/runninghub-output/photo.png \
  --param scale=4x \
  --output /tmp/runninghub-output/photo-upscaled.png
```

### Auto-select best endpoint (shortcut)

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py \
  --task text-to-image \
  --prompt "a beautiful sunset over the ocean" \
  --output /tmp/runninghub-output/sunset.png
```

## Discover more endpoints

List all endpoints:

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py --list
```

Filter by type or task:

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py --list --type video
python3 /root/.openclaw/workspace/scripts/runninghub.py --list --task text-to-image
```

Show endpoint details (parameters, options, defaults):

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py --info rhart-video-s/image-to-video
```

## Parameter passing

Common parameters use dedicated flags:
- `--prompt "text"` — maps to the `prompt` or `text` field
- `--image /path` — maps to the first IMAGE parameter (repeatable with `-i`)
- `--video /path` — maps to the first VIDEO parameter
- `--audio /path` — maps to the first AUDIO parameter
- `--output /path` — where to save the result

All other parameters use `--param key=value`:
- `--param resolution=2k`
- `--param aspectRatio=16:9`
- `--param duration=10`
- `--param voiceId=male-qn-qingse`

## Error handling

The script outputs structured JSON errors. React based on the `error` field:

| Error | Meaning | Action |
|-------|---------|--------|
| `NO_API_KEY` | No key configured | Guide user: register → create key → recharge → configure |
| `AUTH_FAILED` | Key invalid/expired | Guide to key management: https://www.runninghub.cn/enterprise-api/sharedApi |
| `INSUFFICIENT_BALANCE` | Wallet empty | Guide to recharge: https://www.runninghub.cn/vip-rights/4 |
| `TASK_FAILED` | Generation failed | Show the error message to user |
| `API_ERROR` | Other API error | Show the error message to user |

## Output format

- Image/video/audio/3D: prints `MEDIA:/absolute/path` for OpenClaw attachment rendering.
- Text results (understanding endpoints): prints `TEXT_RESULT:content`.

## Notes

- Video generation is slower (1-5 min); the script polls automatically up to 15 min.
- Key resolution: `--api-key` flag → `RUNNINGHUB_API_KEY` env → `~/.openclaw/openclaw.json` config.
- Images < 5MB are sent as base64 data URIs; larger files are uploaded first.
- The `--task` flag auto-selects the most popular endpoint for that task type.
