import json

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, fields, marshal
import base64
import cv2
import numpy as np
from random import randint

from manage import Manage

K = 15
app = Flask('edges')
api = Api(app, version='1.0', title='FaceGraph API',
          description='API для работы с библиотекой распознования лиц - FaceGraph',
          )
CORS(app)
namespace = api.namespace('api', description='Список всех возможных API-запросов')
manage_ = Manage()


def cv_engine(img, operation, id):
    if operation == 'detect':
        faces = [encode_image(_).decode("utf-8") for _ in manage_.detect(img)]
        message = 'Find {} faces.'.format(len(faces))
        return {'result': faces, 'message': message}
    elif operation == 'add':
        message = manage_.add(img, label=id, meta=str({'id': id}), with_detect=False)
        return {'result': None, 'message': message}
    elif operation == 'links':
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
        # print('Request: {}'.format(request.json))
        id = request.json['image_data']['id']
        img = None
        if operation != 'neighbors':
            if request.json['image_data']['data'] == None:
                return "", 500
            image_data = request.json['image_data']['data'][23:].encode()
            img = read_image(image_data)
        if id:
            id = int(id)
            print('ID: {}, {}'.format(type(id), id))
        result = cv_engine(img, operation, id)
        # print('Response: {}'.format(result))
        return json.dumps(result), 200
    except Exception as e:
        print(e)
        manage_.hnsw.save()
        print('Database was saved.')
        return "", 500


faces = api.model('Faces', {
    'result': fields.List(fields.String)
})

image = api.model('Image', {
    'image': fields.String
})

face_k = api.model('Face_k', {
    'face': fields.String,
    'k': fields.Integer
})

similar_person = api.model('Similar person', {
    'face': fields.String,
    'id': fields.String,
    'meta': fields.String,
    'score': fields.Float
})

similar = api.model('Similar', {
    'result': fields.List(
        fields.Nested(similar_person)
    )
})

person = api.model('Link', {
    'face': fields.String,
    'id': fields.String,
    'meta': fields.String,
})

links = api.model('Links', {
    'result': fields.List(
        fields.Nested(person)
    )
})

id_ = api.model('Id', {
    'id': fields.String
})

message = api.model('Message', {
    'message': fields.String
})




class Faces(object):
    def __init__(self, result):
        self.result = result


class Similar(object):
    def __init__(self, result):
        self.result = result


class Link(object):
    def __init__(self, result):
        self.result = result

class Message(object):
    def __init__(self, message):
        self.message = message


@namespace.route('/detect')
class DetectApi(Resource):
    @namespace.doc('Возвращает список лиц в формате base64')
    @namespace.expect(image)
    @namespace.marshal_with(faces, code=200)
    def post(self):
        data = api.payload
        image = read_image(data['image'].encode())
        print(image.shape)
        faces = [encode_image(_).decode("utf-8") for _ in manage_.detect(image)]
        print(len(faces))
        return Faces(result=faces), 200


@namespace.route('/search')
class SearchApi(Resource):
    @namespace.doc('Возвращает список похожих лиц с заданным числом ближайших соседей')
    @namespace.expect(face_k)
    @namespace.marshal_with(similar, code=200)
    def post(self):
        data = api.payload
        face = read_image(data['face'].encode())
        k = data['k']
        result = manage_.query(face, k=k)
        if len(result) == 0:
            return Similar(result=[]), 200
        else:
            for i in range(len(result)):
                nparr = np.fromstring(result[i]['image'], np.uint8)
                result[i]['face'] = encode_image(cv2.imdecode(nparr, cv2.IMREAD_COLOR)).decode("utf-8")
                del result[i]['image']
                del result[i]['prob']
            return Similar(result=result), 200


@namespace.route('/link')
class SearchApi(Resource):
    @namespace.doc('Возвращает список лиц, с которыми заданный человек встречался на одной фотографии')
    @namespace.expect(id_)
    @namespace.marshal_with(links, code=200)
    def post(self):
        data = api.payload
        id = data['id']
        result = manage_.neighbors(id)
        if len(result) == 0:
            return Link(result=[]), 200
        else:
            for i in range(len(result)):
                nparr = np.fromstring(result[i]['image'], np.uint8)
                result[i]['face'] = encode_image(cv2.imdecode(nparr, cv2.IMREAD_COLOR)).decode("utf-8")
                del result[i]['image']
            return Link(result=result), 200


@namespace.route('/add_face')
class AddFaceApi(Resource):
    @namespace.doc('Добавляет лицо в базу данных')
    @namespace.expect(person)
    @namespace.marshal_with(message, code=200)
    def post(self):
        data = api.payload
        message = manage_.add(image=read_image(data['face'].encode()), label=data['id'], meta=data['meta'], with_detect=False)
        return Message(message=message)


@namespace.route('/add_links')
class AddFaceApi(Resource):
    @namespace.doc('Добавляет связи')
    @namespace.expect(image)
    @namespace.marshal_with(message, code=200)
    def post(self):
        data = api.payload
        message = manage_.add(image=read_image(data['image'].encode()), label=None, meta=None, with_detect=True)
        return Message(message=message)


@app.route('/')
def index():
    return 'Python is AWESOME!'


if __name__ == '__main__':
    app.run(debug=True)
