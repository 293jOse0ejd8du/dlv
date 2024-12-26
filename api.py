from flask import Flask, request, jsonify
from urllib.parse import unquote
from base64 import b64decode

app = Flask(__name__)

def dynamicLV(url):
    try:
        # Split the URL by 'r=' and get the last part
        parts = url.split('r=')
        if len(parts) > 1:
            base64_string = parts[-1]
            decoded_base64 = unquote(base64_string)
            return b64decode(decoded_base64).decode('utf-8')
        else:
          return None
    except Exception:
        return None

@app.route('/api/dlv', methods=['GET'])
def decode_url():
    try:
        linkvertise_url = request.args.get('url')
        if not linkvertise_url:
            return jsonify({'error': 'Missing "url" parameter'}), 400

        decoded_url = dynamicLV(linkvertise_url)

        if decoded_url:
            return jsonify({'result': decoded_url}), 200
        else:
            return jsonify({'error': 'Invalid or un-decodable Linkvertise URL'}), 400

    except Exception as e:
        return jsonify({'error': 'Error processing request', 'details':str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
