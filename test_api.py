import requests

def test_ocr():
    url = "http://localhost:8000/ocr/"
    
    # 测试 EasyOCR
    data = {
        "image_path": "test.png",
        "type": "easyocr"
    }
    response = requests.post(url, json=data)
    print("EasyOCR 结果:", response.json())
    
    # 测试 Tesseract
    data["type"] = "tesseract"
    response = requests.post(url, json=data)
    print("Tesseract 结果:", response.json())

if __name__ == "__main__":
    test_ocr() 