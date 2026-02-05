# AI Excuse Generator — Mini Spec

## 目标
为需要临时借口的人提供 AI 生成的创意借口——无论是迟到、忘记任务、还是需要委婉拒绝。

## 核心功能
- **情境选择**: 选择借口场景（迟到、请假、拒绝邀请、忘事、等等）
- **紧急程度**: 选择借口的可信度等级（常规、紧急、极端）
- **AI 生成**: 通过 LLM 生成 3 个创意借口供选择
- **一键复制**: 点击即可复制借口到剪贴板
- **历史记录**: 本地存储使用过的借口（可选功能）

## 技术方案
- 前端：React + Vite (TypeScript) + Tailwind CSS
- 后端：Python FastAPI
- AI 调用：通过 llm-proxy.densematrix.ai（gemini-3-flash-preview）
- 部署：Docker → langsheng

## 美学方向
**Retro Typewriter / 老式打字机风格**
- 字体：Courier Prime（打字机）+ Space Mono（UI）
- 配色：米黄纸张背景 + 深墨色文字 + 红色强调（打字机色带）
- 元素：打字机按键效果、纸张纹理、打字机声音动画
- 整体感觉：像在用老式打字机撰写正式的借口信

## 支付模型
- 免费试用：每设备 1 次
- 付费包：
  - 10 次借口生成 - $4.99
  - 30 次借口生成 - $9.99
  - 无限次（月订阅）- $14.99/月

## i18n
支持 7 种语言：en, zh, ja, de, fr, ko, es

## 完成标准
- [x] 核心功能可用（选择情境 → 生成借口 → 复制）
- [ ] 部署到 excuse.demo.densematrix.ai
- [ ] Health check 通过
- [ ] 前端设计符合美学方向（Retro Typewriter）
- [ ] Creem 支付集成
- [ ] 7 种语言 i18n
- [ ] 测试覆盖率 >= 95%
