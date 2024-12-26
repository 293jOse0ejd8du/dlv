from flask import Flask, request, jsonify
import re
from urllib.parse import unquote
from base64 import b64decode

app = Flask(__name__)

def dynamicLV(url):
    url_pattern = r'https:\/\/linkvertise\.com\/.*r=([^&]*)'
    match = re.search(url_pattern, url)
    if match:
        base64_string = match.group(1)
        decoded_base64 = unquote(base64_string)
        try:
            return b64decode(decoded_base64).decode('utf-8')
        except Exception:
            return None
    else:
        return None

@app.route('/api/loot', methods=['GET'])
def decode_url():
    try:
        linkvertise_url = request.args.get('url')
        if not linkvertise_url:
            return jsonify({'error': 'Missing "url" parameter'}), 400

        decoded_url = dynamicLV(linkvertise_url)

        if decoded_url:
            return jsonify({'decoded_url': decoded_url}), 200
        else:
            return jsonify({'error': 'Invalid or un-decodable Linkvertise URL'}), 400

    except Exception as e:
        return jsonify({'error': 'Error processing request', 'details':str(e)}), 500
if __name__ == '__main__':
  app.run(debug=True)
