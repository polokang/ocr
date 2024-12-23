import os
import sys
import requests

def check_environment():
    print("=== 环境检查 ===")
    print(f"Python 版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    try:
        import easyocr
        print("EasyOCR 已安装")
    except ImportError:
        print("错误：EasyOCR 未安装")
    
    try:
        import fastapi
        print("FastAPI 已安装")
    except ImportError:
        print("错误：FastAPI 未安装")

def check_server():
    print("\n=== 服务器检查 ===")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("服务器运行正常")
        else:
            print(f"服务器返回异常状态码: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务器已启动")

def check_image_path(image_path):
    print("\n=== 图片路径检查 ===")
    if os.path.exists(image_path):
        print(f"图片文件存在: {image_path}")
        print(f"文件大小: {os.path.getsize(image_path)} 字节")
    else:
        print(f"错误：图片文件不存在: {image_path}")

if __name__ == "__main__":
    check_environment()
    check_server()
    # 替换为您的实际图片路径
    check_image_path(r"C:\Users\YourName\Pictures\test.jpg") 