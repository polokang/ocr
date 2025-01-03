import requests

def test_upload():
    # 测试不同引擎
    image_path = "woolworths.jpg"
    
    # 测试 EasyOCR
    print("测试 EasyOCR:")
    result = upload_and_ocr(image_path, "easyocr", "en")
    print(result)
    
    # 测试 Azure
    print("\n测试 Azure:")
    result = upload_and_ocr(image_path, "azure", "en")
    print(result)
    
    # 测试 Tesseract
    print("\n测试 Tesseract:")
    result = upload_and_ocr(image_path, "tesseract", "en")
    print(result)

def upload_and_ocr(image_path, engine="easyocr", language="en"):
    url = "http://localhost:8000/api/v1/upload-and-ocr/"
    files = {"file": open(image_path, "rb")}
    params = {"engine": engine, "language": language}
    response = requests.post(url, files=files, params=params)
    return response.json()

if __name__ == "__main__":
    test_upload() 