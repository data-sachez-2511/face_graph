import cv2

from db_utils.hnsw import HNSW
from db_utils.sqlite import ResultStorage, Face
from face_utils.facepipe import FacePipe


class Manage:
    def __init__(self):
        self.pipe = FacePipe()
        self.hnsw = HNSW()
        self.db = ResultStorage()
        self.fields = [Face.id, Face.face_blob, Face.meta, Face.neighbors]

    def add(self, image, label=None, meta="{}"):
        dets = list(self.pipe([image]))
        if len(dets) == 0:
            return "Don\'t find faces in image."
        if len(dets) == 1:
            if label == None:
                return "You must add user_id"
            _, message = self.hnsw.add(vecs=[dets[0][2]], label=label)
            if message == 'Success':
                insert_data = [(label, cv2.imencode('.jpg', dets[0][1])[1].tostring(), meta, '')]
                with self.db.db.atomic():
                    Face.insert_many(insert_data, self.fields).execute()
            return message
        if label != None:
            return "Finded > 1 faces. You should delete user_id for this image. A link between persons will be added."
        links, message = self.hnsw.add(vecs=[_[2] for _ in dets])
        for user in links:
            face_ = Face.select().where(Face.id == user).get()
            new = set(map(str, links[user]))
            old = set(face_.neighbors.split(','))
            new = set.union(new, old)
            face_.neighbors = ','.join(new)

        return message + '| Fin {} links.'.format(len(links) ** 2 - len(links))

    def query(self, image, k=10):
        dets = [(image, face, embed) for _, face, embed in self.pipe([image])]
        k = min(k, self.hnsw.index.get_current_count())
        labels, distances = self.hnsw.query(vecs=[_[2] for _ in dets], k=k)
        result = []
        for i in range(len(labels[0])):
            r = []
            for face in Face.select().where(Face.id == labels[0][i]):
                r.append({'image': face.face_blob, 'id': face.id, 'meta': face.meta})
            result.append(r)
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

    def detect(self, images):
        return [face for _, face, embed in self.pipe(images)]
