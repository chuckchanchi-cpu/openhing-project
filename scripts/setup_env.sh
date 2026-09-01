#!/bin/bash
# Openhing 開發環境設置腳本
# 使用: bash setup_env.sh

echo "🚀 Openhing 環境設置 .."

# 1. 建立 Python 虛擬環境
echo "📦 建立 Python 虛擬環境..."
python3 -m venv venv
source venv/bin/activate

# 2. 安裝依賴
echo "📥 安裝依賴..."
pip install --upgrade pip
pip install crewai
pip install langchain-community  # 可選，用於工具整合

# 3. 設定環境變數
echo "🔑 請設定你的 LLM API 金鑰..."
echo "export OPENAI_API_KEY='your-key-here'" > .env
echo "請編輯 .env 檔案，填入你的 API 金鑰"

# 4. 建立 .gitignore
echo "📝 建立 .gitignore..."
cat > .gitignore << 'EOF'
venv/
.env
__pycache__/
*.pyc
.DS_Store
EOF

echo ""
echo "✅ 環境設置完成！"
echo ""
echo "下一步："
echo "  1. 編輯 .env 檔案填入 API 金鑰"
echo "  2. source venv/bin/activate"
echo "  3. python scripts/research_assistant.py --topic '你的主題'"