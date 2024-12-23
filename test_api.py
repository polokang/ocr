import requests
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ocr_api():
    try:
        # API 地址
        url = "http://localhost:8000/ocr/"
        
        # 使用当前目录下的测试图片
        image_path = os.path.abspath("test.jpg")  # 确保test.jpg存在
        
        logger.debug(f"准备发送请求到 {url}")
        logger.debug(f"图片路径: {image_path}")
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            logger.error(f"测试图片不存在: {image_path}")
            return
        
        # 发送请求
        response = requests.post(
            url,
            json={"image_path": image_path}
        )
        
        # 检查响应状态码
        response.raise_for_status()
        
        # 打印详细信息
        logger.debug(f"响应状态码: {response.status_code}")
        logger.debug(f"响应头: {response.headers}")
        logger.debug(f"响应内容: {response.json()}")
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        logger.error("连接错误：请确保服务器已启动")
    except requests.exceptions.RequestException as e:
        logger.error(f"请求错误: {str(e)}")
    except Exception as e:
        logger.error(f"发生未知错误: {str(e)}", exc_info=True)

if __name__ == "__main__":
    result = test_ocr_api() 