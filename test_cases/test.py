
import requests
import base64
import json

payload = {
    "session_id": "Test",
    # "user_query": "reset",
    "user_query": "classy knee-length cocktail dress",
    # "search_filters": {
    #     "Season": "Summer",
    # },
    "return_attrs": {
        "Category",
        "Item_url",
        "Display_image"
    }
}
response = requests.post("http://localhost:7000/full_search", json=payload)
print(json.dumps(response.json(), indent=2))

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

with open("image.png", "rb") as f:
    image_bytes = f.read()

payload = {
    "session_id": "Test",
    "image_bytes": encode_image_to_base64(image_bytes),
    "return_attrs": {
        "Category",
        "Brand"
    }
}
response = requests.post("http://localhost:7000/get_products_img", json=payload)
print(json.dumps(response.json(), indent=2))