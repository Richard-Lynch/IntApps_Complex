#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, abort, url_for
# from flask_kerberos import requires_authentication
from flask_restful import Api, Resource
from flask_restful import reqparse
from flask_restful import fields, marshal
# from radon.complexity import cc_rank, cc_visit
from radon.complexity import cc_rank, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester
import json

#--------------------------------------
# paths="./testing_dir"
# ex = "./.git/*"
# config = Config(
#     exclude=ex,
#     ignore="worker.py",
#     order=SCORE,
#     no_assert=True,
#     show_complexity=True,
#     average=False,
#     total_average=True,
#     show_closures=True,
#     min='A',
#     max='F'
# )

# h = CCHarvester([paths], config)
# results = h.to_terminal()
# for result in results:
#     line, args, kwargs = result[0], result[1], result[2]
#     if type(line) == str:
#         if "Average complexity:" in line:
#             print ("FOUND THE AVG!")
#             avg = args[2]
#             print ("AVG", avg)
#         # print(line.format(*args, **kwargs))
#     else:
#         for l in line:
#             pass
#             # print ("{}".format(l))
#--------------------------------------
# results = h.results
# fileName = results[0][0]
# funcs = results[0][1]
# for func in funcs:
#     print ("f:\n", func)
# print ("")
# jresults = h.as_json()
# # print ("results\n",jresults)
# results = json.loads(jresults)
# # print ("results\n",results)
# # print ("type:", type(results))
# for key in results:
#     print ("k:", key)
#     # print (results[key])
#     print ("-------------")
#     for t in results[key]:
#         # print ("t:\n", t)
#         for value in t:
#             print ("{}: {}".format(value, t[value]))

#         print ("-------------")

#     # print (line.format(*args, **kwargs))
#     # for value in result[1]:
#         # print ("v:", value)
# # h.to_terminal()
# # print ("results", results)
# # results = h.results()
# # jresults = h.as_json()

# # print ("results", results)

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
@app.errorhandler(403)
def unauthorized():
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
    def put(self, p_id):
        pass
    def delete(self, p_id):
        pass
api.add_resource(jobs, '/jobs', endpoint = 'jobs')


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

if __name__ == '__main__':
    files = ['test1.py', 'test2.py']
    job = -1
    max_job = 2
    app.run(host='0.0.0.0', debug=True, port=8080)
