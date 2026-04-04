# R2 音频上传指南

## 概述

音频文件存储在 Cloudflare R2，通过公开 CDN 访问。

- **Bucket**: `hylingo-audio`
- **公开地址**: `https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/`
- **目录结构**:
  - `jp/` — 日语音频
  - `en/` — 英语音频

## 前置条件

已安装 rclone 并配置好 R2（配置文件在 `~/.config/rclone/rclone.conf`）。

如需重新配置：

```bash
brew install rclone

cat > ~/.config/rclone/rclone.conf << 'EOF'
[r2]
type = s3
provider = Cloudflare
access_key_id = 639329d4a0beaa429bc216a6bc4001bd
secret_access_key = d807392f1297d33054732dd118f8de17324c60f2f23e1b85bcc80b5f2da73528
endpoint = https://ef8d128d9bdcf1b79a431669a6cf627f.r2.cloudflarestorage.com
acl = private
EOF
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
