#!/usr/local/bin/python3
import sys
# from radon.complexity import cc_rank, cc_visit
from radon.complexity import cc_rank, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester
import json
import requests

from flask import Flask, jsonify, request, make_response, abort, url_for
# from flask_kerberos import requires_authentication
from flask_restful import Api, Resource
from flask_restful import reqparse
from flask_restful import fields, marshal
# app = Flask(__name__)
# api = Api(app)

# print ("r:", r)


## --------------------------------------


class worker ():
    def __init__(self):
        self.config = Config(
            exclude="",
            ignore="",
            order=SCORE,
            no_assert=True,
            show_complexity=True,
            average=True,
            total_average=True,
            show_closures=True,
            min='A',
            max='F'
            )
    def run (self):
        print ("running")
        self.done = False
        while self.done == False:
            r = requests.get('http://127.0.0.1:8080/jobs').json()
            print ("r:", r)
            if "job" in r:
                print ("gonna compute: ", r["job"])
                paths="./testing_dir/" + str(r["job"])
                avg = self.compute(paths)
                if avg != None:
                    r = requests.post('http://127.0.0.1:8080/jobs', json = { 'job' : r["job"], 'avg' : avg } ).json()
                    print (r)
                else:
                    pass
                    # print ("no avg!?")
            else:
                print ("no compute")
                self.done = True
        print ("Done!")
    def compute(self, paths):
        print ("PATH:", paths)
        h = CCHarvester([paths], self.config)
        results = h.to_terminal()
        for result in results:
            line, args, kwargs = result[0], result[1], result[2]
            if type(line) == str:
                if "Average complexity:" in line:
                    print ("FOUND THE AVG!")
                    avg = args[2]
                    print ("AVG", avg)
                    return avg
                # print(line.format(*args, **kwargs))
            else:
                for l in line:
                    pass
                    # print ("{}".format(l))
        return None

if __name__ == '__main__':
    w = worker()
    w.run()
## --------------------------------------
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






