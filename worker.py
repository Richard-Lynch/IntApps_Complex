#!/usr/local/bin/python3

# from flask import Flask, jsonify, request, make_response, abort, url_for
# # from flask_kerberos import requires_authentication
# from flask_restful import Api, Resource
# from flask_restful import reqparse
# from radon.complexity import cc_rank, cc_visit
from radon.complexity import cc_rank, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester
paths = "/Users/richie/programs/IntApps_Complex/"
config = Config(
    exclude=None,
    ignore=None,
    order=SCORE,
    no_assert=True,
    show_closures=False,
    min='A',
    max='F',
)
print ("config", config)
h = CCHarvester(paths, config)
print ("harvester made")
results = h._to_dicts()
print ("results", results)

# app = Flask(__name__)
# api = Api(app)

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)
# @app.errorhandler(403)
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)




# class PalListApi(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('name', type = str, location = 'json')
#         # self.reqparse.add_argument('description', type = str, default = "", location = 'json')
#         super(PalListApi, self).__init__()
#     def get(self):
#         return jsonify({'pals' : [make_public_pal(p) for p in pals]})
#     def put(self, p_id):
#         pass
#     def delete(self, p_id):
#         pass
# api.add_resource(PalListApi, '/pals', endpoint = 'pals')


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

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8080)

