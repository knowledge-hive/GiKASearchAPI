
import requests
import base64

payload = {
    "session_id": "Test",
    "user_query": "Show me some kaftan dresses"
}
response = requests.post("http://localhost:7000/full_search", json=payload)
print(response.json())

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

with open("image.png", "rb") as f:
    image_bytes = f.read()

payload = {
    "session_id": "Test",
    "image_bytes": encode_image_to_base64(image_bytes),
    "min_similarity": 0.9
}
response = requests.post("http://localhost:7000/get_products_img", json=payload)
print(response.json())