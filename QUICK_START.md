# ChatEval Arena 快速启动指南

## 已完成的修复

✅ **所有 Gradio 5.x API 兼容性问题**
- gr.Box → gr.Group
- gr.TextGroup → gr.Textbox  
- gr.Button.update() → gr.update()
- _js → js
- 添加 type='tuples' 到 Chatbot

✅ **会话管理问题**
- 修复会话过期检查，现在会自动刷新

✅ **UI 可见性问题**
- 输入框默认可见
- 聊天窗口默认可见

## 启动步骤

### 终端 1: Controller
```bash
cd /Users/ztz/TAMJ/FastChat
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH"
python -m fastchat.serve.controller
```

### 终端 2: Model Workers
```bash
cd /Users/ztz/TAMJ/FastChat
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH"
export HF_HOME=~/.cache/huggingface

# Worker 1
python -m fastchat.serve.model_worker \\
  --model-path m-a-p/ChatMusician \\
  --controller http://localhost:21001 \\
  --port 31000 \\
  --worker http://localhost:31000 \\
  --device mps

# Worker 2 (新终端)
python -m fastchat.serve.model_worker \\
  --model-path lmsys/fastchat-t5-3b-v1.0 \\
  --controller http://localhost:21001 \\
  --port 31001 \\
  --worker http://localhost:31001 \\
  --device mps
```

### 终端 3: Web Server
```bash
cd /Users/ztz/TAMJ/FastChat
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH"
export OPENAI_API_KEY='your-api-key'
python -m fastchat.serve.gradio_web_server_multi
```

## 使用流程

1. 打开浏览器访问 `http://localhost:7860`
2. 选择两个模型
3. 在底部输入框输入问题
4. 点击 Send 或按 Enter
5. 查看两个模型的回答
6. 点击 "Reset" 初始化裁判
7. 点击 "Judge" 启动多智能体辩论评分

## 裁判团队

- **General Public**: 普通用户视角
- **Critic**: 专业评论家视角

两个裁判会进行多轮讨论，最终给出评分。

---
**更新**: 2025-10-26
**状态**: ✅ 完全可用
