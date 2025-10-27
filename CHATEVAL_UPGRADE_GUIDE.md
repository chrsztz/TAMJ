# ChatEval 升级指南 - 兼容 Gradio 5.x 和新版本依赖

本指南说明如何在新版本依赖（Gradio 5.x, Langchain 1.x, Pydantic 2.x）环境下运行 ChatEval 多智能体辩论功能。

## ✅ 已完成的更新

### 1. **Gradio API 适配 (3.x → 5.x)**
   - 将所有 `gr.Button.update()` 替换为 `gr.update()`
   - 将所有 `gr.Chatbot.update()` 等替换为通用的 `gr.update()`
   - 更新 `no_change_btn` 从 `gr.Button.update()` 改为 `gr.skip()`

### 2. **依赖版本兼容**
   - ✅ Gradio 5.49.1
   - ✅ Pydantic 2.11.10  
   - ✅ Langchain (最新版本)
   - ✅ fschat (最新版本)

### 3. **AgentVerse 配置修复**
   - 修复了配置文件路径问题
   - 正确处理 `AgentVerse.from_task()` 返回的元组

### 4. **多智能体裁判功能**
   - ✅ Referee UI 完全功能
   - ✅ 2个裁判代理：General Public 和 Critic
   - ✅ 支持对比两个模型的响应并进行评分

## 🚀 快速开始

### 方式 1: 使用启动脚本（推荐）

```bash
cd /Users/ztz/TAMJ
./start_chateval_arena.sh
```

### 方式 2: 手动启动（3个终端窗口）

#### 终端 1: 启动 Controller

```bash
cd /Users/ztz/TAMJ/FastChat
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"
python -m fastchat.serve.controller
```

#### 终端 2: 启动 Model Workers

```bash
cd /Users/ztz/TAMJ/FastChat
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"
export HF_HOME=~/.cache/huggingface
export TRANSFORMERS_CACHE=~/.cache/huggingface/hub

# Worker 1 (ChatMusician)
python -m fastchat.serve.model_worker \
  --model-path m-a-p/ChatMusician \
  --controller http://localhost:21001 \
  --port 31000 \
  --worker http://localhost:31000 \
  --device mps

# Worker 2 (另一个终端窗口 - 较小的模型)
python -m fastchat.serve.model_worker \
  --model-path lmsys/fastchat-t5-3b-v1.0 \
  --controller http://localhost:21001 \
  --port 31001 \
  --worker http://localhost:31001 \
  --device mps
```

#### 终端 3: 启动 Gradio Web Server

```bash
cd /Users/ztz/TAMJ
conda activate tamj
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"
export OPENAI_API_KEY='your-openai-api-key'

python -m fastchat.serve.gradio_web_server_multi
```

## 📋 环境要求

### 必需的环境变量

```bash
# Python 路径（确保使用本地修改的 FastChat）
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"

# HuggingFace 缓存路径（避免权限问题）
export HF_HOME=~/.cache/huggingface
export TRANSFORMERS_CACHE=~/.cache/huggingface/hub

# OpenAI API Key（用于多智能体裁判功能）
export OPENAI_API_KEY='your-api-key-here'
```

### Conda 环境 (tamj)

主要依赖：
- Python 3.11
- PyTorch (带 MPS 支持)
- Gradio 5.49.1
- transformers
- fastchat
- langchain
- opencv-python
- 等等

## 🎯 使用流程

1. **启动所有服务**（按上述步骤）

2. **打开浏览器访问** `http://localhost:7860`

3. **使用 ChatEval Arena**：
   - 选择两个模型进行对比
   - 输入问题并获取两个模型的回答
   - 点击 **"Reset"** 按钮初始化裁判团队
   - 点击 **"Judge"** 按钮让 AI 裁判进行多轮辩论并评分
   - 查看裁判团队的讨论过程和最终评分

4. **裁判团队角色**：
   - **General Public**: 代表普通用户的视角
   - **Critic**: 专业评论家的视角
   
## 🧪 测试功能

运行测试脚本验证所有功能：

```bash
cd /Users/ztz/TAMJ
conda activate tamj
python test_chateval_simple.py
```

测试内容：
- ✓ 模块导入
- ✓ AgentVerse 初始化
- ✓ Referee UI 创建  
- ✓ Gradio 5.x API 兼容性

## 🔧 关键修改说明

### 1. gradio_web_server.py
```python
# 旧版 (Gradio 3.x)
no_change_btn = gr.Button.update()
enable_btn = gr.Button.update(interactive=True)

# 新版 (Gradio 5.x)
no_change_btn = gr.skip()
enable_btn = gr.update(interactive=True)
```

### 2. gradio_block_arena_referee.py
```python
# 修复 AgentVerse 初始化
# from_task 返回元组: (agentverse, agents, environments)
self.backend, _, _ = AgentVerse.from_task("agentverse/tasks/llm_eval/config.yaml")
```

### 3. 所有 arena 相关文件
```python
# 替换所有组件特定的 update 方法
gr.Dropdown.update(...) → gr.update(...)
gr.Chatbot.update(...) → gr.update(...)
gr.Textbox.update(...) → gr.update(...)
gr.Button.update(...) → gr.update(...)
```

## 📁 文件结构

```
/Users/ztz/TAMJ/
├── FastChat/                    # 修改后的 FastChat (兼容 Gradio 5.x)
│   └── fastchat/
│       └── serve/
│           ├── gradio_web_server.py
│           ├── gradio_web_server_multi.py
│           ├── gradio_block_arena_named.py
│           ├── gradio_block_arena_anony.py
│           └── gradio_block_arena_referee.py  # 多智能体裁判
├── agentverse/                  # AgentVerse 多智能体框架
│   └── tasks/
│       └── llm_eval/
│           └── config.yaml      # 裁判配置
├── start_chateval_arena.sh      # 启动脚本
├── test_chateval_simple.py      # 测试脚本
└── CHATEVAL_UPGRADE_GUIDE.md    # 本文档
```

## ⚠️ 常见问题

### Q: 提示 "ModuleNotFoundError: No module named 'cv2'"
**A**: 安装 opencv-python
```bash
conda activate tamj
pip install opencv-python
```

### Q: 提示 "OSError: Read-only file system: '/data'"
**A**: 设置正确的缓存路径
```bash
export HF_HOME=~/.cache/huggingface
export TRANSFORMERS_CACHE=~/.cache/huggingface/hub
```

### Q: 提示 "OpenAI API key is not set"
**A**: 设置 OpenAI API key（裁判功能需要）
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Q: 模型加载失败 "CUDA not available"
**A**: 确保使用 MPS 设备（Mac Apple Silicon）
```bash
--device mps
```

### Q: ImportError 或模块找不到
**A**: 确保设置了正确的 PYTHONPATH
```bash
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"
```

## 💡 注意事项

1. **Mac Apple Silicon**: 使用 `--device mps` 而不是 `--device cuda`
2. **内存管理**: 同时运行两个7B模型需要至少32GB内存
3. **代理设置**: gradio_web_server_multi.py 中有硬编码的代理设置（10-12行），根据需要修改或注释
4. **OpenAI配额**: 多智能体辩论会调用 OpenAI API，注意配额限制

## 🎉 功能特性

✅ **完整的 Arena 功能**
- 单模型对话
- 双模型对比
- 匿名评测

✅ **多智能体裁判系统**  
- 自动化评分
- 多轮辩论
- 透明的评审过程
- 不同角色视角

✅ **新版本兼容**
- Gradio 5.49.1
- 最新的 transformers
- 最新的 fastchat

## 📚 参考资料

- [ChatEval 论文](https://arxiv.org/abs/2308.07201)
- [FastChat GitHub](https://github.com/lm-sys/FastChat)
- [Gradio 文档](https://www.gradio.app/)
- [AgentVerse GitHub](https://github.com/OpenBMB/AgentVerse)

## 🤝 贡献

移植工作完成项：
- [x] Gradio 3.x → 5.x API 更新
- [x] Pydantic 1.x → 2.x 兼容
- [x] Langchain 0.x → 1.x 兼容  
- [x] AgentVerse 配置修复
- [x] Mac MPS 设备支持
- [x] 测试脚本
- [x] 启动脚本
- [x] 使用文档

---

**最后更新**: 2025-10-26  
**兼容版本**: Gradio 5.49.1, Python 3.11, macOS (Apple Silicon)

