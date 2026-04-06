# Visual Redesign — 三套主题系统

## 概要

将现有的浅色/暗色双模式重构为三套完整主题，用户可在设置中切换。所有 emoji 图标替换为统一的 1.8px 线性 SVG icon。底栏改为浮岛式设计。

## 三套主题

### 1. 暮色 Dusk（冷色）
- **背景**：多色渐变 `linear-gradient(170deg, #2a1f3d 0%, #1a2235 30%, #1c2a30 60%, #1e2520 100%)`
- **环境光**：顶部紫色光晕 `radial-gradient(ellipse, rgba(160,120,200,0.15), transparent)`，右侧琥珀光晕
- **卡片**：`rgba(255,255,255,0.05)` + `backdrop-filter:blur(16px)` + `1px solid rgba(255,255,255,0.07)`
- **主色/强调**：紫色系 `#c8a8e8` 用于 active tab、控制 pill、图表柱
- **辅助色**：青绿 `rgba(120,180,160)` 用于跟读相关
- **文字**：标题 `#f0ebe5`，正文 `#ece6de`，次要 `rgba(255,255,255,0.35)`，翻译 `rgba(255,255,255,0.3)`
- **Tab**：pill 样式，选中 `rgba(255,255,255,0.1)` + blur + border
- **JLPT 标签**：描边式 `1px solid rgba(255,255,255,0.1)` + `rgba(255,255,255,0.3)` 文字

### 2. 暖云 Warm Cloud（暖色 / 浅色）
- **背景**：暖灰棕渐变 `linear-gradient(175deg, #e8ddd0 0%, #ddd2c4 40%, #d8ccbc 100%)`
- **环境光**：顶部暖光 `radial-gradient(circle, rgba(255,240,220,0.35), transparent)`
- **卡片**：`rgba(255,255,255,0.5)` + `backdrop-filter:blur(20px)` + `1px solid rgba(255,255,255,0.4)` + `box-shadow:0 4px 20px rgba(0,0,0,0.04)`
- **主色/强调**：暖棕 `#5a4a38`（深），`#a08868`（中），`#b0a090`（浅）
- **文字**：标题 `#2a2420`，正文 `#2a2420`，次要 `#8a7a68`，翻译 `#8a7a68`
- **Tab**：segmented control，选中白色毛玻璃 + shadow
- **JLPT 标签**：`rgba(0,0,0,0.05)` 背景 + `#a09080` 文字
- **按钮**：实心暗棕 `rgba(90,74,56,0.85)` + 白色文字

### 3. 墨金 Ink & Amber（暗色）
- **背景**：冷灰黑渐变 `linear-gradient(180deg, #141518 0%, #18191e 50%, #141518 100%)`
- **环境光**：顶部微金 `radial-gradient(ellipse, rgba(220,180,120,0.06), transparent)`
- **卡片**：`rgba(255,255,255,0.03)` + `1px solid rgba(255,255,255,0.05)`（不用 blur）
- **主色/强调**：琥珀金 `#dcb478`，低透明度背景 `rgba(220,180,120,0.08~0.1)`
- **辅助色**：青绿 `rgba(120,180,160)` 用于跟读，紫 `rgba(160,140,200)` 用于练习
- **文字**：标题 `#f0ebe5`，正文 `#ece6de`，次要 `rgba(255,255,255,0.3)`
- **Tab**：segmented control，选中 `rgba(220,180,120,0.1)` + amber border
- **JLPT 标签**：`rgba(220,180,120,0.08)` 背景 + `#dcb478` 文字

## 通用组件设计

### 底栏导航（浮岛式，三套通用）
- 浮动在底部，不贴边：`left:22px; right:22px; bottom:20px`
- 暗色主题：`background:rgba(0,0,0,0.4); backdrop-filter:blur(24px); border-radius:20px; border:1px solid rgba(255,255,255,0.06)`
- 暖云主题：`background:rgba(255,255,255,0.45); backdrop-filter:blur(24px); border-radius:18px; border:1px solid rgba(255,255,255,0.3)`
- 选中项：icon + 文字横排 + 柔和背景色块
- 未选中项：icon + 文字纵排，低透明度

### 图标系统
- 统一使用 SVG inline icon，stroke-width: 1.8px，stroke-linecap: round
- 底栏图标：听（音符）/ 练（钢笔）/ 统计（柱状图），尺寸 17-20px
- 功能图标：搜索、设置（滑块）、返回、播放、音量、关闭、展开、循环、麦克风、星标
- 不再使用任何 emoji

### 文章详情页
- 返回按钮 + 标题 + JLPT 标签一行
- 控制 pill 按钮行：译文（active 用主色背景）、假名、性别、全部播放（右对齐，主色强调）
- 句子卡片列表：当前播放句左侧 3px 色条 + 主色背景区分
- Ruby/furigana 用主色低透明度显示

### 播放器（LoopBar 展开态）
- 顶部：索引 + 操作按钮（展开/关闭）
- 居中大字：42px 加粗单词
- 下方：读音（主色低透明度）+ 释义（次要文字色）
- 星标按钮
- 渐变进度条（主色系）
- 播放控件：上一首 / 播放（60px 圆形，主色渐变背景）/ 下一首
- 循环按钮

### 统计页
- 标题「今日の学習」
- 2x2 统计卡片网格：每张用对应功能色（听力/跟读/练习/掌握）低透明度背景 + 对应 icon
- 数字大字 24px + 单位小字 + 标签
- 周学习柱状图：双色堆叠柱（听力色 + 跟读色）
- 设置区（合并卡片）：主题切换（三色圆点选择器）、学习语言、界面语言

### 主题切换器
- 三个 20px 圆点，各显示对应主题的渐变色
- 当前主题圆点加 2px 主色描边 + 外阴影
- 放在统计页设置区内

## 技术实现方式

- 继续使用 CSS 自定义属性（CSS Variables）驱动主题
- 现有 `:root` 和 `:root.theme-dark` 改为 `:root.theme-dusk`、`:root.theme-warm`、`:root.theme-ink`
- `useTheme` composable 扩展为支持三套主题切换
- localStorage key 保持 `app_theme_mode_v1`，值从 `light/dark` 改为 `dusk/warm/ink`
- 背景渐变和环境光晕通过 `body` 和 `body::before` 伪元素实现
- SVG icon 抽取为 Vue 组件或统一的 icon map
- 底栏浮岛：修改 AppNav.vue 的 position 和样式

## 不变的部分

- 整体布局结构（header + sidebar/bottom-nav + content）
- 功能逻辑和交互行为
- 字体栈（系统字体 + 日文字体）
- 响应式断点和安全区适配
- 组件文件结构
