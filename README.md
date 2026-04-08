# Japanese Learning (日本語学習)

一个基于 Vue 3 的日语学习 Web 应用，支持单词学习、文章阅读、测验练习、跟读训练、语音循环播放等功能，并支持手机端锁屏后台播放。

🌐 在线访问：<https://hylingo.github.io/>

> 💡 建议使用 **Chrome** 打开，并通过浏览器菜单"添加到主屏幕"安装到桌面，体验接近原生 App。

## 技术栈

- **前端框架**: Vue 3 (Composition API + `<script setup>`)
- **状态管理**: Pinia
- **样式**: Tailwind CSS
- **构建工具**: Vite
- **后端/认证**: Firebase
- **语言**: TypeScript
- **部署**: GitHub Pages (`gh-pages`)

## 项目结构

```
src/
├── App.vue                    # 主入口，Tab 切换各面板
├── stores/app.ts              # 全局状态管理
├── composables/               # 组合式函数
│   ├── useAudio.ts            # 音频播放
│   ├── useFirebase.ts         # Firebase 认证与数据
│   ├── useLoopPlayer.ts       # 循环播放器
│   ├── useQuiz.ts             # 测验逻辑
│   ├── useSpacedRepetition.ts # 间隔重复算法
│   ├── useStats.ts            # 学习统计
│   ├── useSwipe.ts            # 滑动手势
│   ├── useTheme.ts            # 主题切换
│   └── ...
├── components/
│   ├── articles/              # 文章阅读模块
│   ├── list/                  # 单词列表
│   ├── quiz/                  # 测验卡片
│   ├── practice/              # 练习面板
│   ├── stats/                 # 学习统计
│   ├── kana/                  # 假名表
│   ├── loop/                  # 循环播放条
│   ├── layout/                # 布局（Header、Nav）
│   ├── auth/                  # 登录
│   └── common/                # 通用组件（分页、骨架屏等）
├── utils/                     # 工具函数
public/
├── data/
│   ├── ja_articles.json       # 文章数据
│   └── audio_map.json         # 音频映射
```

## 文章内容统计

共 **162 篇**文章，分布如下：

| 级别 | 数量 |
|------|------|
| N5 | 5 |
| N5–N4 | 1 |
| N5–N3 | 6 |
| N4–N3 | 56 |
| N3 | 46 |
| N3–N2 | 12 |
| N2 | 32 |
| N1 | 4 |

格式：散文 84 篇，对话 78 篇。

## 开发

```bash
npm install
npm run dev
```

## 构建与部署

```bash
npm run build
npm run deploy   # 部署到 GitHub Pages
```
