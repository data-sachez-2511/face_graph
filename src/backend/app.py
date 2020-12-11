import json

from flask import Flask, request
from flask_cors import CORS, cross_origin
import base64
import cv2
import numpy as np
from random import randint

from manage import Manage

K = 15
app = Flask('edges')
CORS(app)
manage_ = Manage()


def cv_engine(img, operation, id):
    if operation == 'detect':
        faces = [encode_image(_).decode("utf-8") for _ in manage_.detect(img)]
        message = 'Find {} faces.'.format(len(faces))
        return {'result': faces, 'message': message}
    elif operation == 'add_face':
        message = manage_.add(img, label=id, meta=str({'id': id}), with_detect=False)
        return {'result': None, 'message': message}
    elif operation == 'add_link':
        message = manage_.add(img, label=None, meta='', with_detect=True)
        return {'result': None, 'message': message}
    elif operation == 'query':
        result = manage_.query(img, k=K)
        if len(result) == 0:
            return {'result': [], 'message': 'Database is empty.'}
        else:
            for i in range(len(result)):
                nparr = np.fromstring(result[i]['image'], np.uint8)
                result[i]['image'] = encode_image(cv2.imdecode(nparr, cv2.IMREAD_COLOR)).decode("utf-8")
            return {'result': result, 'message': 'Received {} persons from database.'.format(len(result))}

    elif operation == 'neighbors':
        result = manage_.neighbors(id)
        if len(result) == 0:
            return {'result': [], 'message': 'Not found links for user with id: {}.'.format(id)}
        else:
            for i in range(len(result)):
                nparr = np.fromstring(result[i]['image'], np.uint8)
                result[i]['image'] = encode_image(cv2.imdecode(nparr, cv2.IMREAD_COLOR)).decode("utf-8")
            return {'result': result, 'message': 'Founded {} links from database.'.format(len(result))}
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
    try:
        if not request.json or 'msg' not in request.json:
            return 'Server Error!', 500
        operation = request.json['operation']
        print('Operation: {}'.format(operation))
        id = request.json['image_data']['id']
        image_data = None
        if operation != 'neighbors':
            image_data = request.json['image_data']['data'][23:].encode()
        img = read_image(image_data)
        result = cv_engine(img, operation, id)
        return json.dumps(result), 200
    except Exception as e:
        print(e)
        manage_.hnsw.save()
        print('Database was saved.')
        return "", 500


@app.route('/')
def index():
    return 'Python is AWESOME!'


if __name__ == '__main__':
    app.run(debug=True)
