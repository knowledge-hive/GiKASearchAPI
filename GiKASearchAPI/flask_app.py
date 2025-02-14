from dotenv import load_dotenv
import os
import logging
from flask import Flask, request, jsonify
from .modules.integrator import load_endpoints
from werkzeug.exceptions import HTTPException

module_name = os.path.splitext(os.path.basename(__file__))[0]

# Configure logger for this module
logger = logging.getLogger(module_name)
logger.setLevel(logging.DEBUG)

# Create a file handler per module
os.makedirs("logs", exist_ok=True)
log_file = f"logs/{module_name}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create and set formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    
logger.info(f"Logger initialized for {module_name}")

# Load environment variables from a .env file
load_dotenv()

# Get host and port from environment variables or use default values
HOST = os.environ.get('FLASK_HOST', 'localhost')
PORT = os.environ.get('FLASK_PORT', 7000)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "gika-graph"
app.config["SESSION_TYPE"] = "filesystem"

# Log request information before handling the request
@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url} - Args: {request.args} - JSON: {request.get_json()}")

# Log response information after handling the request
@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status} - Data: {response.get_data(as_text=True)} - Headers: {response.headers}")
    return response

# Error handler for HTTP exceptions
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    logger.error(f"HTTP exception: {e.description}")
    response = e.get_response()
    response.data = jsonify({"error": e.description})
    response.content_type = "application/json"
    return response

# Error handler for general exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({"error": "Internal Server Error"}), 500

# Dynamically create routes for each function in integrator.py

load_endpoints(app)
# for name, func in inspect.getmembers(integrator, inspect.isfunction):
#     def create_endpoint(func):
#         def endpoint():
#             try:
#                 # Extract arguments from request.json
#                 args = request.json or {}
#                 # Convert arguments to the correct types based on function signature
#                 sig = inspect.signature(func)
#                 typed_args = {
#                     k: (v if p.annotation == inspect._empty else p.annotation(v))
#                     for k, v in args.items()
#                     if k in sig.parameters
#                     and (p := sig.parameters[k])
#                 }
#                 # Call the function and return the result
#                 result = func(**typed_args)
#                 return jsonify({"result": result})
#             except TypeError as e:
#                 logger.error(f"Type error in endpoint {func.__name__}: {e}")
#                 return jsonify({"error": "Invalid arguments"}), 400
#             except Exception as e:
#                 logger.error(f"Error in endpoint {func.__name__}: {e}", exc_info=True)
#                 return jsonify({"error": "Internal Server Error"}), 500
#         endpoint.__name__ = func.__name__
#         return endpoint
    
#     # Register the route
#     logger.info(f"Registered endpoint: {name}")
#     app.add_url_rule(f"/{name}", view_func=create_endpoint(func), methods=["POST"])

# Run the Flask app
if __name__ == "__main__":
    app.run(host=HOST, port=PORT)