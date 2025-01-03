# 多引擎 OCR 服务

这是一个基于 FastAPI 的 OCR 服务，集成了多个 OCR 引擎，包括 EasyOCR、Tesseract 和 Azure Computer Vision。

## 功能特点

- 支持多种 OCR 引擎：
  - EasyOCR（默认）
  - Tesseract OCR
  - Azure Computer Vision
- 支持多种语言识别
- RESTful API 接口
- 详细的日志记录
- 健康检查接口
- MongoDB 数据存储
- 文件上传功能

## 安装要求

- Python 3.7+
- 依赖包：
  ```bash
  pip install -r requirements.txt
  ```

- Tesseract OCR 引擎（如需使用 Tesseract）：
  - Windows: 从 [这里](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`
  - macOS: `brew install tesseract tesseract-lang`

- MongoDB 数据库

## 配置

1. Azure OCR 配置（如需使用）：
   - 在 `.env` 文件中设置您的 Azure key 和 endpoint

2. Tesseract 配置（如需使用）：
   - Windows: 确保 Tesseract 安装路径正确（默认：`C:\Program Files\Tesseract-OCR\tesseract.exe`）
   - Linux/macOS: 确保 Tesseract 已正确安装

3. MongoDB 配置：
   - 在 `.env` 文件中设置 MongoDB 连接信息

## 运行服务

```bash
# 方式1：直接运行
python -m app.main

# 方式2：使用 uvicorn
uvicorn app.main:app --reload
```

服务将在 http://localhost:8003 启动

## API 文档

### 1. 图片上传并OCR

**接口**：`POST /api/v1/upload-and-ocr/`

**参数**：
- `file`: 图片文件（multipart/form-data）
- `engine`: OCR引擎类型（可选，默认"easyocr"）
  - `easyocr`: EasyOCR引擎
  - `tesseract`: Tesseract引擎
  - `azure`: Azure计算机视觉
- `language`: 识别语言（可选，默认"en"）
  - `en`: 英文
  - `zh-Hans`: 中文简体

**响应**：
```json
{
    "status": "success",
    "filename": "20240101_120000_image.jpg",
    "text": ["识别的文本内容"]
}
```

### 2. 健康检查

**接口**：`GET /health`

**响应**：
```json
{
    "status": "healthy"
}
```

## 文件上传说明

1. 支持的图片格式：
   - JPG/JPEG
   - PNG
   - BMP

2. 文件大小限制：10MB

3. 上传的文件将保存在 `static/uploads` 目录

4. 文件命名规则：`{时间戳}_{原始文件名}`

5. 文件信息和OCR结果将保存在MongoDB中

## 示例代码

### Python 请求示例

```python
import requests

# 上传图片并OCR
def ocr_image(image_path, engine="easyocr", language="en"):
    url = "http://localhost:8000/api/v1/upload-and-ocr/"
    
    # 准备文件和参数
    files = {
        "file": open(image_path, "rb")
    }
    params = {
        "engine": engine,
        "language": language
    }
    
    # 发送请求
    response = requests.post(url, files=files, params=params)
    return response.json()

# 使用示例
result = ocr_image(
    image_path="test.png",
    engine="azure",
    language="en"
)
print(result)
```

### cURL 请求示例

```bash
# 使用EasyOCR引擎
curl -X POST "http://localhost:8000/api/v1/upload-and-ocr/" \
     -H "accept: application/json" \
     -F "file=@test.png" \
     -F "engine=easyocr"

# 使用Azure引擎（英文识别）
curl -X POST "http://localhost:8000/api/v1/upload-and-ocr/" \
     -H "accept: application/json" \
     -F "file=@test.png" \
     -F "engine=azure" \
     -F "language=en"
```

### JavaScript 请求示例

```javascript
// 使用 Fetch API
async function ocrImage(file, engine = 'easyocr', language = 'en') {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(
        `http://localhost:8000/api/v1/upload-and-ocr/?engine=${engine}&language=${language}`,
        {
            method: 'POST',
            body: formData
        }
    );
    
    return await response.json();
}

// 使用示例
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const result = await ocrImage(file, 'azure', 'en');
    console.log(result);
});
```

## 错误处理

服务会返回适当的 HTTP 状态码和错误信息：
- 400: 不支持的文件类型
- 404: 文件不存在
- 413: 文件太大
- 500: 服务器内部错误

每个错误响应都包含详细的错误信息：
```json
{
    "detail": "错误描述"
}