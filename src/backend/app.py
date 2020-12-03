import json

from flask import Flask, request
from flask_cors import CORS, cross_origin
import base64
import cv2
import numpy as np
from random import randint

from manage import Manage

app = Flask('edges')
CORS(app)
manage_ = Manage()


def cv_engine(img, operation):
    if operation == 'detect':
        faces = manage_.detect([img])
        if len(faces) > 0:
            return faces
        else:
            return None
    elif operation == 'add':
        message = manage_.add(img, label=randint(0, 100000), meta='it is test')
        return message
    elif operation == 'query':
        result = manage_.query(img, k=20)
        if len(result) == 0:
            return None
        else:
            result = result[0]
            for i in range(len(result)):
                nparr = np.fromstring(result[i]['image'], np.uint8)
                result[i]['image'] = encode_image(cv2.imdecode(nparr, cv2.IMREAD_COLOR)).decode("utf-8")

            return result
    else:
        return None


def read_image(image_data):
    image_data = base64.decodebytes(image_data)
    nparr = np.fromstring(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def encode_image(img):
    ret, data = cv2.imencode('.jpg', img)
    return base64.b64encode(data)


# This is the server to handle requests and get images from client
@app.route('/process_image', methods=['POST'])
def process_image():
    if not request.json or 'msg' not in request.json:
        return 'Server Error!', 500

    image_data = request.json['image_data'][23:].encode()
    operation = request.json['operation']
    print(operation)
    img = read_image(image_data)
    result = cv_engine(img, operation)
    if operation == 'detect':
        return encode_image(result[0]).decode("utf-8"), 200
    else:
        print(result)
        return json.dumps(result), 200


@app.route('/')
def index():
    return 'Python is AWESOME!'


if __name__ == '__main__':
    app.run(debug=True)
