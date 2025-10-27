#!/bin/bash
# ChatEval Arena 启动脚本
# 适配 Gradio 5.x + 新版本依赖

set -e

echo "======================================"
echo "ChatEval Arena 启动脚本"
echo "======================================"

# 激活 conda 环境
echo "正在激活 conda tamj 环境..."
eval "$(conda shell.bash hook)"
conda activate tamj

# 设置 Python 路径，确保使用本地修改的 FastChat
export PYTHONPATH="/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:$PYTHONPATH"

# 设置 HuggingFace 缓存路径
export HF_HOME=~/.cache/huggingface
export TRANSFORMERS_CACHE=~/.cache/huggingface/hub

# 检查 OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  警告: OPENAI_API_KEY 未设置"
    echo "ChatEval 的裁判功能需要 OpenAI API"
    echo "请运行: export OPENAI_API_KEY='your-api-key'"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "请选择要启动的服务:"
echo "1) 完整 Arena (需要启动 controller + workers + web server)"
echo "2) 仅启动 Controller"
echo "3) 仅启动 Model Worker"  
echo "4) 仅启动 Gradio Web Server"
echo ""
read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "启动完整 Arena 需要 3 个终端窗口:"
        echo "1. Controller (端口 21001)"
        echo "2. Model Workers (端口 31000, 31001)"
        echo "3. Gradio Web Server (端口 7860)"
        echo ""
        echo "请按照以下步骤操作:"
        echo ""
        echo "=== 终端 1: Controller ==="
        echo "cd /Users/ztz/TAMJ/FastChat"
        echo "export PYTHONPATH=\"/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH\""
        echo "conda activate tamj"
        echo "python -m fastchat.serve.controller"
        echo ""
        echo "=== 终端 2: Model Workers ==="
        echo "# Worker 1:"
        echo "cd /Users/ztz/TAMJ/FastChat"
        echo "export PYTHONPATH=\"/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH\""
        echo "export HF_HOME=~/.cache/huggingface"
        echo "conda activate tamj"
        echo "python -m fastchat.serve.model_worker --model-path m-a-p/ChatMusician --controller http://localhost:21001 --port 31000 --worker http://localhost:31000 --device mps"
        echo ""
        echo "# Worker 2 (新终端):"
        echo "python -m fastchat.serve.model_worker --model-path lmsys/fastchat-t5-3b-v1.0 --controller http://localhost:21001 --port 31001 --worker http://localhost:31001 --device mps"
        echo ""
        echo "=== 终端 3: Gradio Web Server ==="
        echo "cd /Users/ztz/TAMJ"
        echo "export PYTHONPATH=\"/Users/ztz/TAMJ:/Users/ztz/TAMJ/FastChat:\$PYTHONPATH\""
        echo "export OPENAI_API_KEY='your-api-key'"
        echo "conda activate tamj"
        echo "python -m fastchat.serve.gradio_web_server_multi"
        ;;
    2)
        echo "启动 Controller..."
        cd /Users/ztz/TAMJ/FastChat
        python -m fastchat.serve.controller
        ;;
    3)
        echo ""
        read -p "输入模型路径 (默认: m-a-p/ChatMusician): " model_path
        model_path=${model_path:-m-a-p/ChatMusician}
        
        read -p "输入端口号 (默认: 31000): " port
        port=${port:-31000}
        
        echo "启动 Model Worker..."
        cd /Users/ztz/TAMJ/FastChat
        python -m fastchat.serve.model_worker \
            --model-path "$model_path" \
            --controller http://localhost:21001 \
            --port "$port" \
            --worker "http://localhost:$port" \
            --device mps
        ;;
    4)
        echo "启动 Gradio Web Server..."
        cd /Users/ztz/TAMJ
        python -m fastchat.serve.gradio_web_server_multi
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

