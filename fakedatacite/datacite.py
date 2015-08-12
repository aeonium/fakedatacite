
from flask import Flask, request, make_response
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

@api.representation('text/plain')
def text(data, code, headers=None):
    if not data:
        data = ''
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp

dois = { }

class DoiList(Resource):
    def get(self):
        return dois.keys()

    def post(self):
        data = request.get_data()
        doi = {}
        for l in data.splitlines():
            sl = l.strip()
            if not sl:
                continue
            k, v = l.split('=', 2)
            doi[k] = v
        dois[doi['doi']] = doi
        return 'CREATED', 201

class Doi(Resource):
    def get(self, doi_id):
        try:
            return dois[doi_id]['url']
        except KeyError:
            abort(404)

api.add_resource(DoiList, '/doi')
api.add_resource(Doi, '/doi/<string:doi_id>')

if __name__ == '__main__':
    app.run(debug=True)
