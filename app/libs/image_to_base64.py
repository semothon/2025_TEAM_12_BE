import base64
import os

def image_to_base64(image_path: str) -> str:
    """이미지 파일 경로를 base64 문자열로 변환"""
    if not os.path.exists(image_path):
        return None
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
