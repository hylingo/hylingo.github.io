# R2 音频上传指南

## 概述

音频文件存储在 Cloudflare R2，通过公开 CDN 访问。

- **Bucket**: `hylingo-audio`
- **公开地址**: `https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/`
- **目录结构**:
  - `jp/` — 日语音频
  - `en/` — 英语音频

## 前置条件

已安装 rclone，并在本机配置好 R2（**密钥不要写进 Git 仓库**）。配置文件一般在 `~/.config/rclone/rclone.conf`。

**说明：读这个 Markdown 不会自动获得任何权限。** 能对 R2 **上传/删除**的，只有：在你自己电脑上配置了 Access Key 的工具（如 rclone）、或 Cloudflare 控制台。网页端（GitHub Pages）和 Cursor 里的 AI **都不会**因为「看过这篇文档」就去连你的 R2。

在 Cloudflare 控制台创建 R2 的 **S3 API 令牌** 后，推荐用交互式配置（密钥只留在本机）：

```bash
brew install rclone
rclone config
# 新建 remote，选 S3 → Provider: Cloudflare → 填入 endpoint、access_key_id、secret_access_key
```

若你曾把真实密钥提交进仓库，请到 Cloudflare **轮换/作废旧密钥** 并换新，避免泄露。

`rclone.conf` 示例（请把占位符换成你自己的值，且勿提交到 git）：

```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = <你的_R2_Access_Key_ID>
secret_access_key = <你的_R2_Secret_Access_Key>
endpoint = https://<你的账户子域>.r2.cloudflarestorage.com
acl = private
```

## 上传命令

### 上传整个 audio 目录

```bash
rclone copy audio/ r2:hylingo-audio/ --transfers 64 --no-check-dest --progress
```

### 仅上传日语音频

```bash
rclone copy audio/jp/ r2:hylingo-audio/jp/ --transfers 64 --no-check-dest --progress
```

### 仅上传英语音频

```bash
rclone copy audio/en/ r2:hylingo-audio/en/ --transfers 64 --no-check-dest --progress
```

### 上传单个文件

```bash
rclone copyto audio/jp/xxxx.mp3 r2:hylingo-audio/jp/xxxx.mp3
```

## 验证

```bash
# 检查文件数量
rclone ls r2:hylingo-audio/jp/ | wc -l
rclone ls r2:hylingo-audio/en/ | wc -l

# 测试公开访问
curl -I "https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/jp/0001d9995503.mp3"
```

## 代码中的引用

音频路径在以下文件中配置：

- `src/composables/useAudio.ts` — `audioPath()` 函数
- `src/composables/useLoopPlayer.ts` — 循环播放路径

格式：`https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/{fn}`

其中 `fn` 为 `jp/xxxx.mp3` 或 `en/xxxx.mp3`。

## 删除孤儿音频（与语料同步）

移除 `sentences.json` 等语料后，R2 上可能仍留有**已不再被任何 JSON 引用**的 MP3。仓库内会维护：

1. **`scripts/prune_orphan_audio.py`**  
   - 扫描 `public/data` 下 `nouns.json`、`verbs.json`、`ja_articles.json`、`en_articles.json`、`en_nouns.json`、`article_audio_map_male.json` 中所有 `audio` / `audioExample` / `audioMale` 路径；  
   - **重写** `public/data/audio_map.json`，去掉指向「当前语料未引用文件」的条目；  
   - 生成 **`docs/orphan-audio-r2-delete.txt`**：每行一个路径（相对 bucket 根，如 `jp/xxx.mp3`），供在 R2 上删除。

```bash
# 预览统计（不改文件）
python scripts/prune_orphan_audio.py --dry-run

# 更新 audio_map + 重写删除清单
python scripts/prune_orphan_audio.py
```

2. **在 R2 上真正删除**（配置好与本指南一致的 `rclone` remote 名，例如 `r2`）：

```bash
# 先检查清单行数
grep -vE '^#|^$' docs/orphan-audio-r2-delete.txt | wc -l

# 逐条删除（路径相对于 hylingo-audio 根）
grep -vE '^#|^$' docs/orphan-audio-r2-delete.txt | while read -r p; do
  rclone deletefile "r2:hylingo-audio/$p"
done
```

**注意**：删除操作不可恢复；若本地还有未提交的语料改动，请先跑一遍 `prune_orphan_audio.py` 再删 CDN，避免误删仍需要的文件。
