#!/usr/local/bin/python3
from flask import Flask, jsonify, request, make_response, abort, url_for
# from flask_kerberos import requires_authentication
from flask_restful import Api, Resource
from flask_restful import reqparse
from flask_restful import fields, marshal
app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
@app.errorhandler(403)
def unauthed():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

class jobs(Resource):
    def __init__(self):
        # self.reqparse = reqparse.RequestParser()
        # self.reqparse.add_argument('filename', type = str, location = 'json', required = True)
        # self.reqparse.add_argument('commitID', type = str, location = 'json', required = True)
        super(jobs, self).__init__()
    def get(self):
        global job
        global max_job
        global files
        job += 1
        if job >= max_job:
            return {'done' : True}
        this_job = job
        return {'job' : files[this_job]}
    def post(self):
        global done_jobs
        r = request.json
        if "job" in r and "avg" in r:
            print ("job:", r["job"])
            print ("avg:", r["avg"])
            done_jobs[r["job"]] = r["avg"]
        else:
            print ("post", r)
        return {"thanks" : "pal"}
    def delete(self, p_id):
        pass
api.add_resource(jobs, '/jobs', endpoint = 'jobs')

class results(Resource):
    def __init__(self):
        super(results, self).__init__()
    def get(self):
        global done_jobs
        return {"done_jobs" : done_jobs}
api.add_resource(results, '/done', endpoint = 'done')

if __name__ == '__main__':
    files = ['test1.py', 'test2.py']
    job = -1
    max_job = 2
    done_jobs = {}
    app.run(host='0.0.0.0', debug=True, port=8080)



# class PalApi(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('name', type = str, location = 'json')
#         super(PalApi, self).__init__()
#     def get(self, p_id):
#         p = list(filter(lambda P: P['id'] == p_id, pals))
#         if len(p) == 0:
#             abort(404)
#         return {'pal' : make_public_pal(p[0])}
#     def put(self, p_id):
#         p = list(filter(lambda P: P['id'] == p_id, pals))
#         if len(p) == 0:
#             abort(404)
#         p = p[0]
#         args = self.reqparse.parse_args()
#         print ("args:", args)
#         print ("name:", args['name'])
#         p['name'] = args['name']
#         # for k, v in args.iteritems():
#             # if v != None:
#                 # p[k] = v
#         return { 'pal': make_public_pal(p) }
#     def delete(self, p_id):
#         p = list(filter(lambda P: P['id'] == p_id, pals))
#         if len(p) == 0:
#             abort(404)
#         p = p[0]
#         pals.remove(p)
#         return { 'success' : True }
# api.add_resource(PalApi, '/pals/<int:p_id>', endpoint = 'pal')
