#!/usr/bin/env bash
# 用环境变量在本机创建 rclone remote（不写进 Git）。
#
# 在 Cloudflare 控制台：R2 → 管理 R2 API 令牌 → 创建 API 令牌，
# 得到 Access Key ID、Secret、以及 S3 API 的 Endpoint（形如 https://<账户子域>.r2.cloudflarestorage.com）。
#
# 用法（一次性，在仓库根目录或任意目录执行均可）:
#   export R2_ACCESS_KEY_ID='你的 Key ID'
#   export R2_SECRET_ACCESS_KEY='你的 Secret'
#   export R2_ENDPOINT='https://xxxx.r2.cloudflarestorage.com'
#   bash scripts/setup_rclone_r2.sh
#
# 若 remote 名不想叫 r2:
#   export RCLONE_REMOTE_NAME=myr2
#
set -euo pipefail

REMOTE="${RCLONE_REMOTE_NAME:-r2}"

if [[ -z "${R2_ACCESS_KEY_ID:-}" || -z "${R2_SECRET_ACCESS_KEY:-}" || -z "${R2_ENDPOINT:-}" ]]; then
  echo "请先 export 以下变量后再运行:" >&2
  echo "  R2_ACCESS_KEY_ID" >&2
  echo "  R2_SECRET_ACCESS_KEY" >&2
  echo "  R2_ENDPOINT（完整 URL，含 https://）" >&2
  exit 1
fi

if rclone config show "${REMOTE}" &>/dev/null; then
  echo "已存在名为「${REMOTE}」的 remote。若需重建：" >&2
  echo "  rclone config delete ${REMOTE}" >&2
  exit 1
fi

mkdir -p "${HOME}/.config/rclone"

rclone config create "${REMOTE}" s3 \
  provider Cloudflare \
  access_key_id "${R2_ACCESS_KEY_ID}" \
  secret_access_key "${R2_SECRET_ACCESS_KEY}" \
  endpoint "${R2_ENDPOINT}" \
  acl private \
  --non-interactive

echo ""
echo "已创建 remote: ${REMOTE}"
echo "配置文件: ${HOME}/.config/rclone/rclone.conf"
echo ""
echo "测试列出桶内日语音频（前几行）:"
rclone ls "${REMOTE}:hylingo-audio/jp/" 2>/dev/null | head -5 || {
  echo "（若报错 403/404，请检查令牌权限是否包含该桶的读写、Endpoint 是否正确）" >&2
  exit 1
}
echo ""
echo "上传本次生成的 MP3:"
echo "  rclone copy audio/jp/ ${REMOTE}:hylingo-audio/jp/ --transfers 32 --progress"
