from flask import Flask, request, jsonify
from urllib.parse import unquote
from base64 import b64decode

app = Flask(__name__)

def dynamicLV(url):
    print(f"Input URL: {url}") # Debug print
    try:
        parts = url.split('r=')
        print(f"Parts after split: {parts}") # Debug print
        if len(parts) > 1:
            base64_string = parts[-1]
            print(f"Base64 string before unquote: {base64_string}") # Debug print
            decoded_base64 = unquote(base64_string)
            print(f"Base64 string after unquote: {decoded_base64}") # Debug print
            try:
                result = b64decode(decoded_base64).decode('utf-8')
                print(f"Decode successfull with {result}") # Debug print
                return result
            except Exception as b64_err:
                 print(f"b64decode Error: {b64_err}") # Debug print
                 return None
        else:
            print("URL does not contain 'r='")  # Debug print
            return None
    except Exception as e:
        print(f"Overall Exception Error: {e}") # Debug print
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
