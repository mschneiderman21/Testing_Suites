from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ai_sensor', methods=['GET', 'POST'])

def webhook():
    if request.method == 'POST':
        data = request.json
        # Process the data here
        return jsonify({"message": "POST request received", "data": data}), 200
    else:
        return jsonify({"message": "GET request received"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
