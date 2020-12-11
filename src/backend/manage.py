import cv2

from db_utils.hnsw import HNSW
from db_utils.sqlite import ResultStorage, Face
from face_utils.facepipe import FacePipe


def normalize_prob(prob, threshold=(0.4, 0.6)):
    prob = 1 - prob
    if prob < threshold[0]:
        return 0
    elif prob > threshold[1]:
        return 100
    else:
        return (prob - threshold[0]) / (threshold[1] - threshold[0]) * 100


class Manage:
    def __init__(self):
        self.pipe = FacePipe()
        self.hnsw = HNSW()
        self.db = ResultStorage()
        self.fields = [Face.id, Face.face_blob, Face.meta, Face.neighbors]

    def add(self, image, label=None, meta="{}", with_detect=False):
        if with_detect:
            faces, embeds = self.pipe(image, with_detect=with_detect)
        else:
            faces = [image]
            embeds = self.pipe(image, with_detect=with_detect)
        if len(faces) == 0:
            return "Don\'t find faces in image."
        if len(faces) == 1:
            if label == None:
                return "You must add user_id"
            _, message = self.hnsw.add(vecs=embeds[0], label=label)
            if message == 'Success':
                insert_data = [(label, cv2.imencode('.jpg', faces[0])[1].tostring(), meta, '')]
                with self.db.db.atomic():
                    Face.insert_many(insert_data, self.fields).execute()
            return message
        if label != None:
            return "Finded > 1 faces. You should delete user_id for this image. A link between persons will be added."
        links, message = self.hnsw.add(vecs=embeds)
        for user in links:
            face_ = Face.select().where(Face.id == user).get()
            new = set(map(str, links[user]))
            old = set(face_.neighbors.split(','))
            new = set.union(new, old)
            face_.neighbors = ','.join(new)
            face_.save()

        return message + '| Find {} links.'.format(len(links) ** 2 - len(links))

    def query(self, image, k=10):
        embeds = self.pipe(image, with_detect=False)
        k = min(k, self.hnsw.index.get_current_count())
        labels, distances = self.hnsw.query(vecs=embeds, k=k)
        result = []
        for i in range(len(labels[0])):
            for face in Face.select().where(Face.id == labels[0][i]):
                result.append({'image': face.face_blob, 'id': face.id, 'meta': face.meta,
                               'prob': normalize_prob(distances[0][i])})
        result = sorted(result, key=lambda x: x['prob'], reverse=True)
        print(len(result))
        return result

    def neighbors(self, face_id):
        result = []
        for face_ in Face.select().where(Face.id == face_id):
            neighbors = list(map(int, face_.neighbors.split(',')))
            for idx in neighbors:
                for neighbor_face in Face.select().where(Face.id == idx):
                    result.append(
                        {'image': neighbor_face.face_blob, 'id': neighbor_face.id, 'meta': neighbor_face.meta})
                    break
            break
        return result

    def detect(self, image):
        return self.pipe(image, with_detect=True)[0]
