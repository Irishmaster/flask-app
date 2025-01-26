from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from pyzbar.pyzbar import decode
import cv2
import numpy as np

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for WebView compatibility
CORS(app)

# Route to serve the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle QR code scanning
@app.route("/scan", methods=["POST"])
def scan():
    # Extract frame data from request
    image = request.files.get('frame')  # Image file sent by the client
    current_location = request.form.get('location')  # Fetch location from client
    if image:
        # Convert image to numpy array
        np_image = np.frombuffer(image.read(), np.uint8)
        frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Decode QR code
        for barcode in decode(frame):
            qr_data = barcode.data.decode("utf-8")
            data = parse_qr_data(qr_data)
            data['current_location'] = current_location  # Add current location to data
            return render_template("results.html", data=data)
    
    return jsonify({"success": False, "message": "QR Code not found!"})

# Function to parse QR code data
def parse_qr_data(qr_data):
    # Example parsing logic; adjust based on QR code data format
    lines = qr_data.split('\n')
    data = {
        'object_name': lines[0] if len(lines) > 0 else 'Unknown',
        'waste_type': lines[1] if len(lines) > 1 else 'Unknown',
        'location': lines[2] if len(lines) > 2 else 'Unknown'
    }
    return data

# Run the application
if __name__ == "__main__":
    # Use host='0.0.0.0' to make the app publicly accessible when hosted
    app.run(debug=True, host="0.0.0.0", port=5000)






