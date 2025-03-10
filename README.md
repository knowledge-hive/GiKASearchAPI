# GiKASearchAPI

GiKASearchAPI is a search API designed to help you find fashion products based on user queries. It leverages advanced machine learning models to provide accurate and relevant search results.

## Installing Environment

To set up the environment for GiKASearchAPI, follow these steps:

1. **Create a Conda Environment**: This ensures that all dependencies are isolated and do not interfere with other projects.
    ```bash
    conda create -n gikasearchapi python=3.10.16 cudatoolkit=11.8.0
    ```
    This command creates a new Conda environment named `gikasearchapi` with Python version 3.10.16 and CUDA toolkit 11.8.0.

2. **Activate the Conda Environment**: Switch to the newly created environment.
    ```bash
    conda activate gikasearchapi
    ```
    Download and add the GPG Key:

        ```bash
        wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo tee /usr/share/keyrings/elasticsearch-keyring.asc
        ```
    Add it to repo:
        ```bash
        echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.asc] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
        ```
    Update the package:
        ```bash
        sudo apt update
        ```
    Install Elasticsearch:
        ```bash
        sudo apt install elasticsearch -y
        ```
    Enable and start Elasticsearch:
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl enable elasticsearch
        sudo systemctl start elasticsearch
        ```
    Check status:
        ```bash
        sudo systemctl status elasticsearch
        ```

3. **Install Required Dependencies**: Use the `requirements.txt` file to install all necessary Python packages.
    ```bash
    pip install -r requirements.txt
    ```

## Storage Directory

The storage directory contains essential data files required for the API to function correctly. Follow these steps to set it up:

1. **Download the Storage Directory**: Obtain the storage directory from the provided link. (storage.tar.gz)[https://drive.google.com/file/d/1FIl7Qf_XCaXYnEJqDusBeHiY-ElZEdPK/view?usp=sharing]

    You can download the storage directory from the provided link and save it in a directory named `storage`.

2. **Place the Storage Directory**: Ensure the storage directory is placed in the current directory where the GiKASearchAPI project resides.

3. **Verify the Directory Structure**: The storage directory should have the following structure:
    ```
    storage
    ├── Final_data.json
    ├── Knowledge
    │   ├── ...
    │   ├── Policy.txt
    │   └── Terms.txt
    ├── fashion_image_index.faiss
    ├── fashion_index_cosine.faiss
    ├── filtered_output.csv
    └── resources
        ├── attribute_mapping.json
        ├── embeddings.json
        ├── value_groups.json
        └── value_mapping.json
    ```

## .env Modification

The `.env` file contains environment variables that configure the API. Edit this file according to your needs:

1. **FLASK Configuration**:
    ```
    FLASK_APP="http://localhost:7000"
    FLASK_HOST="localhost"
    FLASK_PORT="7000"
    ```
    These variables set up the Flask application to run on `localhost` at port `7000`.

2. **Elasticsearch Configuration**:
    ```
    ELASTICSEARCH_HOST="https://localhost:9200"
    ELASTICSEARCH_INDEX_NAME="fashion_products"
    ELASTICSEARCH_USERNAME=""
    ELASTICSEARCH_PASSWORD=""
    ELASTICSEARCH_DATA_PATH="storage/Final_data.json"
    ```
    These variables configure the connection to the Elasticsearch instance. Ensure Elasticsearch is running and accessible at the specified host and port.

3. **Image Search Configuration**:
    ```
    IMAGE_SEARCH_DF="storage/filtered_output.csv"
    IMAGE_SEARCH_INDEX='storage/fashion_image_index.faiss'
    IMAGE_SEARCH_COIN='storage/fashion_index_cosine.faiss'
    ```
    These variables specify the paths to the image search data files.

4. **Domain Knowledge Path**:
    ```
    DOMAIN_KNOWLEDGE_PATH="storage/Knowledge"
    ```
    This variable sets the path to the directory containing domain knowledge files.

5. **Session History and Default Config Paths**:
    ```
    SESSION_HISTORY_PATH="./working_dirs/session_history.json"
    DEFAULT_CONFIG_PATH="./working_dirs/default/config.json"
    ```
    These variables specify the paths for session history and default configuration files.

## Edit Config

Edit the configuration file located at `working_dirs/default/config.json` to match your specific requirements. This file contains various settings that control the behavior of the API.

## Starting the Server in nohup

To start the server and keep it running in the background, use the `nohup` command:

```bash
nohup python -m GiKASearchAPI.flask_app &
```

- `nohup` allows the server to continue running even after you log out.
- The `&` at the end of the command runs the server in the background.

## Endpoint Examples

Here are some examples of how to use the API endpoints:

### Get Response

To get a response based on a user query, use the following code:

```python
import requests

payload = {
    "session_id": "Test",
    "user_query": "Show me some kaftan dresses"
}
response = requests.post("http://localhost:7000/get_response", json=payload)
print(response.json())
```

### Full Search

To perform a full search based on a user query, use the following code:

```python
import requests

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
print(response.json())
```

### Search Products via Image

To search for products using an image, use the following code:

```python
import requests
import base64

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
print(response.json())
```

## Additional Information

- **Ensure Elasticsearch is Running**: Make sure Elasticsearch is running and accessible at the specified host and port.
- **Verify Storage Directory**: Ensure the storage directory is correctly placed and all paths in the `.env` file are accurate.
- **Monitor Server Logs**: You can monitor the server logs using the `nohup.out` file generated by the `nohup` command.

By following these detailed instructions, you should be able to set up and run the GiKASearchAPI successfully.
