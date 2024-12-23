# 项目描述
    新建一个 python 项目，我本机目前的python 版本是3.10.6 。 我想实现一个后台接口，用户输入图片路径后，返回图片中的文字
# 步骤
    1. 安装python3.10.6
    2. 安装fastapi
    3. 安装EasyOCR
    4. 在项目目录下创建虚拟环境
        `python -m venv venv`
    5. 创建 requirements.txt 文件：
    6. 首先安装依赖：
        # 激活虚拟环境
            source venv/bin/activate  # Linux/Mac
        # 或
            .\venv\Scripts\activate  # Windows
        # 安装依赖
            pip install -r requirements.txt
    7. 运行服务：
        # Linux/Mac
            chmod +x start.sh
            ./start.sh
        # Windows
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    8. 创建一个 Windows 批处理文件： start.bat
    9. 测试 API：http://localhost:8000/ocr/  
        {
            "image_path": "d:\\Learning\\ocr\\test.png"
        }