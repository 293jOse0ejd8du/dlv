from flask import Flask, request, jsonify
import re
from urllib.parse import unquote
from base64 import b64decode

# Initialize the Flask application
app = Flask(__name__)

# Function to decode Linkvertise URLs
def dynamicLV(url):
    # Regular expression to find the Base64-encoded part of the Linkvertise URL
    url_pattern = r'https:\/\/linkvertise\.com\/.*r=([^&]*)'
    match = re.search(url_pattern, url) # Search for the url_pattern in the given url

    if match:
        base64_string = match.group(1) # Extract the Base64 encoded string from regex match
        decoded_base64 = unquote(base64_string) # URL decode the extracted Base64 string
        try:
            # Attempt to Base64 decode and then UTF-8 decode the string
            return b64decode(decoded_base64).decode('utf-8')
        except Exception:
            # Return None if there is an exception during decoding
            return None
    else:
        # Return None if the url doesn't match the url_pattern
        return None

# Define the API endpoint for decoding Linkvertise URLs
@app.route('/api/dlv', methods=['GET'])
def decode_url():
    try:
        # Get the 'url' parameter from the URL query string
        linkvertise_url = request.args.get('url')

        # Check if the 'url' parameter is missing
        if not linkvertise_url:
            # Return an error response with a 400 status code if missing.
            return jsonify({'error': 'Missing "url" parameter'}), 400

        # Call the dynamicLV function to decode the URL
        decoded_url = dynamicLV(linkvertise_url)

        # Check if decoding is successful
        if decoded_url:
            # Return the decoded URL in the 'result' key with a 200 status code
            return jsonify({'result': decoded_url}), 200
        else:
            # Return an error response if decoding fails with a 400 status code
            return jsonify({'error': 'Invalid or un-decodable Linkvertise URL'}), 400

    except Exception as e:
        # Handle any exceptions that may occur during the process
        return jsonify({'error': 'Error processing request', 'details':str(e)}), 500

# Run the Flask app in debug mode when the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
