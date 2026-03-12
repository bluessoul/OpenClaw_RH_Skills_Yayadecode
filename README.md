# RHClaw — RunningHub Skill for OpenClaw

[English](./README_en.md)

为 [OpenClaw](https://github.com/openclaw/openclaw) 打造的通用多媒体生成技能，由 [RunningHub](https://www.runninghub.cn) API 驱动。

**170+ 个 API 端点**，覆盖图片、视频、音频、3D 模型生成和多模态文本理解。

## 能力一览

| 类别 | 端点数 | 支持任务 |
|------|--------|----------|
| **图片** | 42 | 文生图、图生图、图片放大、Midjourney 风格 |
| **视频** | 94 | 文生视频、图生视频、首尾帧生成、视频续写/编辑、运动控制 |
| **音频** | 8 | 文字转语音、音乐生成、声音克隆 |
| **3D** | 12 | 文字转 3D、图片转 3D、多图转 3D |
| **文本** | 14 | 图片理解、视频理解、文本处理 |

## 快速开始

### 安装

在 OpenClaw 对话中发送：

> 从 https://github.com/HM-RunningHub/OpenClaw_RH_Skills 安装 RunningHub 技能

助手会自动克隆仓库、复制文件到工作区，并引导你完成 API Key 配置。

### 更新

当技能有新版本时，在 OpenClaw 对话中发送：

> 从 https://github.com/HM-RunningHub/OpenClaw_RH_Skills 更新 并重新读取@runninghub/SKILL.md

助手会拉取最新代码并重新加载技能配置，无需重新输入 API Key。

### 前置条件

- **API Key** — 在 [RunningHub API 管理页面](https://www.runninghub.cn/enterprise-api/sharedApi) 创建（点击"新建"）
- **账户余额** — [前往充值](https://www.runninghub.cn/vip-rights/4)，API 调用需要余额

## 使用方式

安装完成后，直接用自然语言跟助手对话即可：

- *"帮我画一只在公园里玩耍的小狗"*
- *"把这张照片做成视频"*
- *"给我的视频配个背景音乐"*
- *"把这张图放大到 4K"*
- *"把这张图转成 3D 模型"*

助手会自动选择最合适的 RunningHub 端点来完成你的请求。

### 视频生成交互

生成视频时，助手会展示 8 个精选模型让你选择：

> 1. 🚀 **全能视频V3.1 Fast** — 又快效果又好，性价比之王
> 2. 🔥 **全能视频G** — Grok 驱动，画面想象力超强
> 3. 🎯 **可灵 v3.0 Pro** — 运动自然，拍人物首选
> 4. 🎬 **全能视频V3.1 Pro** — 电影感拉满
> 5. ✨ **Vidu Q3 Pro** — 风格化独特
> 6. ⭐ **全能视频S** — Sora 同款引擎
> 7. 🌊 **海螺 Hailuo** — 速度快画面细腻
> 8. 🌱 **Seedance v1.5 Pro** — 动作流畅细腻

选个数字就能开始生成，不选默认用全能视频V3.1 Fast。

## 项目结构

```
runninghub/
├── SKILL.md                        # OpenClaw 技能定义（路由表 + 示例 + 交互规则）
├── scripts/
│   ├── runninghub.py               # 通用 API 客户端（170+ 端点）
│   └── build_capabilities.py       # 从 models_registry.json 生成 capabilities.json
└── data/
    └── capabilities.json           # 完整端点目录（自动生成）
```

## 脚本模式

| 模式 | 命令 | 用途 |
|------|------|------|
| **检查** | `--check` | 验证 API Key + 查询余额 |
| **列表** | `--list [--type T] [--task T]` | 浏览可用端点 |
| **详情** | `--info ENDPOINT` | 查看端点参数 |
| **执行** | `--endpoint EP --prompt "..." -o /tmp/out` | 使用指定端点执行 |
| **自动** | `--task TASK --prompt "..." -o /tmp/out` | 自动选择最佳端点 |

## 更新能力目录

当 RunningHub 上线新的 API 端点时，重新生成目录：

```bash
python3 scripts/build_capabilities.py \
  --registry /path/to/ComfyUI_RH_OpenAPI/models_registry.json \
  --output data/capabilities.json
```

## 许可证

[Apache-2.0](./LICENSE)
