# 待办

## R2 / CDN：清理句子库移除后的孤儿音频

语料已去掉 `sentences.json` / `en_sentences.json`，仓库内已跑过 `prune_orphan_audio.py` 并更新 `audio_map.json`；**Cloudflare R2 桶里对应 MP3 仍需在本机删除**（线上 CDN 不会自动同步删除）。

- [ ] 确认本机已安装并配置 `rclone`（密钥仅在本机，见 `docs/r2-audio-upload.md`）
- [ ] 若有未合并的语料/音频改动，先合并后再执行下一步，避免误删
- [ ] 预览：`python scripts/prune_orphan_audio.py --dry-run`
- [ ] 更新 map 与清单：`python scripts/prune_orphan_audio.py`
- [ ] 核对 `docs/orphan-audio-r2-delete.txt` 行数与抽样路径
- [ ] 按文档执行 `rclone deletefile` 循环（或等价批量删除），真正清空 R2 上孤儿文件
- [ ] 抽样 `curl -I` 公开 URL，确认仍在用的音频可访问
- [ ] （若曾把 R2 密钥提交进公开仓库）在 Cloudflare 轮换 API 令牌

详细命令与说明：`docs/r2-audio-upload.md` → 章节「删除孤儿音频」。
