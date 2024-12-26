import os
from flask import Flask, request, jsonify
import re
from urllib.parse import unquote, urlparse
from base64 import b64decode
from typing import Optional
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_ENDPOINT = os.getenv("API_ENDPOINT", "/api/dlv")
# API_KEY = os.getenv("API_KEY", "your-secret-api-key") #Removed API Key

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

cache = {}

def dynamicLV(url: str) -> Optional[str]:
    if not isinstance(url, str) or not url.strip():
        logging.warning(f"Invalid input: URL must be a non-empty string")
        return None
    url_pattern = r'https:\/\/linkvertise\.com\/.*r=([^&]*)'
    match = re.search(url_pattern, url)
    if match:
        base64_string = match.group(1)
        decoded_base64 = unquote(base64_string)
        try:
            decoded_url = b64decode(decoded_base64).decode('utf-8')
            cache[url] = decoded_url
            return decoded_url
        except Exception as e:
            logging.error(f"Error decoding URL: {url}, Error: {e}")
            return None
    else:
        logging.info(f"Invalid Linkvertise URL format: {url}")
        return None

# @app.before_request #Removed API Key check
# def before_request():
#     if request.endpoint != "root" and request.headers.get("X-API-Key") != API_KEY:
#         return jsonify({"error":"Missing or Invalid API Key"}), 401

@app.route("/", methods=['GET'])
def root():
    return jsonify({
        "message": "Welcome to the Dynamic Linkvertise (DLV) API",
        "documentation": {
            "endpoint": API_ENDPOINT,
            "method": "GET",
            "query_parameters": {
                "url": "The Linkvertise URL to decode."
            },
           #  "headers": {  Removed the api key
           #      "X-API-Key": "API key for the service",
           #  },
            "response": {
                "success": "Returns the decoded url in the \"result\" key.",
                "error": "Returns an error message if the URL cannot be decoded or some other error happens."
            }
         }
    }), 200

@app.route(API_ENDPOINT, methods=['GET'])
@limiter.limit("100 per minute")
def decode_url():
    try:
        linkvertise_url = request.args.get('url')

        if not linkvertise_url:
            return jsonify({'error': 'Missing "url" parameter'}), 400
        
        if not urlparse(linkvertise_url).scheme:
            return jsonify({'error': 'Invalid URL format, please include "https://" or "http://"'}), 400
            
        decoded_url = dynamicLV(linkvertise_url)

        if decoded_url:
            return jsonify({'result': decoded_url}), 200
        else:
            return jsonify({'error': 'Invalid or un-decodable Linkvertise URL'}), 400

    except Exception as e:
        return jsonify({'error': 'Error processing request', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
