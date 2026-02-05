# AI Excuse Generator — Mini Spec

## 目标
帮助用户在任何需要借口的场景下，一键生成自然、可信、个性化的完美借口。不想上班？不想聚会？AI帮你找个完美的借口！

## 核心功能
- **场景选择**：提供常见场景（不想上班、躲避聚会、迟到、忘记任务等）
- **借口生成**：AI 基于场景、紧急程度、对象关系生成自然借口
- **风格调节**：从"真诚感人"到"荒诞搞笑"多种风格可选
- **复制分享**：一键复制借口，方便发送

## 技术方案
- 前端：React + Vite (TypeScript) + TailwindCSS
- 后端：Python FastAPI
- AI 调用：通过 llm-proxy.densematrix.ai
- 部署：Docker → langsheng

## 完成标准
- [x] 核心功能可用
- [x] 部署到 excuse.demo.densematrix.ai
- [x] Health check 通过
- [x] 基本 UI 可用
- [x] 7 语言 i18n 支持
- [x] Creem 支付集成
