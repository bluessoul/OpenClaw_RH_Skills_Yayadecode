# RHClaw — RunningHub Skill for OpenClaw

Universal media generation skill for [OpenClaw](https://github.com/openclaw/openclaw), powered by [RunningHub](https://www.runninghub.cn) API.

**170+ endpoints** covering image, video, audio, 3D model generation, and multimodal text understanding.

## Capabilities

| Category | Endpoints | Tasks |
|----------|-----------|-------|
| **Image** | 42 | text-to-image, image-to-image, image upscale, Midjourney-style |
| **Video** | 94 | text-to-video, image-to-video, start-end frames, video extend/edit, motion control |
| **Audio** | 8 | text-to-speech, music generation, voice clone |
| **3D** | 12 | text-to-3D, image-to-3D, multi-image-to-3D |
| **Text** | 14 | image-to-text, video-to-text, text-to-text |

## Quick start

### 1. Install the skill

```bash
# Copy script + data
mkdir -p /root/.openclaw/workspace/scripts /root/.openclaw/workspace/data
cp /data/RHClaw/runninghub/scripts/runninghub.py /root/.openclaw/workspace/scripts/runninghub.py
cp /data/RHClaw/runninghub/data/capabilities.json /root/.openclaw/workspace/data/capabilities.json
chmod +x /root/.openclaw/workspace/scripts/runninghub.py

# Copy skill definition
mkdir -p /root/.openclaw/workspace/skills/runninghub
cp /data/RHClaw/runninghub/SKILL.md /root/.openclaw/workspace/skills/runninghub/SKILL.md
```

### 2. Configure API key

Get your API key from [RunningHub API Management](https://www.runninghub.cn/enterprise-api/sharedApi), then:

```bash
openclaw skills config runninghub RUNNINGHUB_API_KEY <your-key>
```

Make sure your [wallet has balance](https://www.runninghub.cn/vip-rights/4) — API calls require funds.

### 3. Verify setup

```bash
python3 /root/.openclaw/workspace/scripts/runninghub.py --check
```

Should return `{"status": "ready", ...}` with your balance.

## Usage

Once installed, just talk to your OpenClaw assistant:

- *"Generate a picture of a dog playing in the park"*
- *"Turn this photo into a video"*
- *"Create background music for my video"*
- *"Upscale this image to 4K"*
- *"Convert this image to a 3D model"*

The assistant automatically selects the best RunningHub endpoint based on your request.

## Architecture

```
runninghub/
├── SKILL.md                        # OpenClaw skill definition (routing table + examples)
├── scripts/
│   ├── runninghub.py               # Universal API client (170+ endpoints)
│   └── build_capabilities.py       # Generates capabilities.json from models_registry.json
└── data/
    └── capabilities.json           # Full endpoint catalog (auto-generated)
```

## Script modes

| Mode | Command | Purpose |
|------|---------|---------|
| **Check** | `--check` | Verify API key + check wallet balance |
| **List** | `--list [--type T] [--task T]` | Browse available endpoints |
| **Info** | `--info ENDPOINT` | View endpoint parameters |
| **Execute** | `--endpoint EP --prompt "..." -o /tmp/out` | Run with specific endpoint |
| **Auto** | `--task TASK --prompt "..." -o /tmp/out` | Auto-select best endpoint |

## Updating capabilities

When RunningHub adds new API endpoints, regenerate the catalog:

```bash
python3 scripts/build_capabilities.py \
  --registry /path/to/ComfyUI_RH_OpenAPI/models_registry.json \
  --output data/capabilities.json
```

Then copy the updated `capabilities.json` to the OpenClaw workspace.
