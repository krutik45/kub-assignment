from flask import Flask, request, jsonify
import requests,os

app = Flask(__name__)

#testing first trigger ----->
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        dataBody = request.get_json()
        nameToFind = dataBody.get('file')
        productName = dataBody.get('product')
        if nameToFind is None:
            return jsonify({"file": None, "error": "Invalid JSON input."})
        container2Response = callContainer2(nameToFind, productName)
        return jsonify(container2Response) 

    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        json_data = request.json
        print(json_data)

        if json_data['file'] is None:
            return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

        file_name = json_data['file']
        data = json_data['data']

        directory = '/file_Dir/'

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)

        with open(file_path, 'w') as file:
            file.write(data)

        if os.path.isfile(file_path):
            return jsonify({'file': file_name, 'message': 'Success.'}), 200
        else:
            return jsonify({'file': file_name, 'error': 'Error while storing the file to the storage.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def callContainer2(nameToFind, productName):
    container2Url = "http://container2-pod:7000/giveTotal"
    payloadToSend = {"file": nameToFind, "product": productName}
    response = requests.post(container2Url, json=payloadToSend)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)