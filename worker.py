#!/usr/local/bin/python3
import sys
# from radon.complexity import cc_rank, cc_visit
from radon.complexity import cc_rank, SCORE, cc_visit
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
        self.get_job_address='http://127.0.0.1:8080/jobs'
        self.send_avg_address='http://127.0.0.1:8080/jobs'

    def get_job(self):
        return requests.get(self.get_job_address).json()

    def send_avg(self, avg, job):
        response = requests.post(self.send_avg_address, json = { \
                'url' : job["url"], \
                'avg' : avg, \
                'commit' : job["commit"], \
                'path' : job["path"] \
                }).json()
        return response

    def run (self):
        print ("running")
        self.done = False
        while self.done == False:
            # get a job from master
            job = self.get_job()
            # if its a valid job (not exhuastive)
            if "url" in job:
                # compute avg
                avg = self.compute(job)
                # post the avg back to master
                post_response = self.send_avg(avg, job)
                # if received a valid response
                if post_response != None:
                    print ("post response:", post_response)
            # if done, stop asking for jobs
            elif "done" in job:
                print ("master is done")
                self.done = True
                break
            # if unknown message, stop asking for jobs
            else:
                print ("unknown message:")
                print (job)
                self.done = True
                break
        print ("Done!")

    def compute(self, paths):
        # print data from master
        for key in paths:
            print ("{}: {}".format(key, paths[key]))
        # get auth token for github access
        token = ""
        with open ("token", "r") as f:
            token = f.read().split()[0]
            if token == "":
                return None
        # download file
        files = './temp/{}.py'.format(paths["commit"])
        with open(files, 'w') as f:
            f.write( requests.get(\
                    paths['url'], \
                    params={"access_token" : str(token)}, \
                    headers={'Accept' : 'application/vnd.github.v3.raw'}\
                    ).text)
        #compute complexity
        results = CCHarvester([files], self.config).to_terminal()
        # extract avg from results
        for result in results:
            line, args, kwargs = result[0], result[1], result[2]
            if type(line) == str:
                if "Average complexity:" in line:
                    avg = args[2]
                    print ("AVG", avg)
                    return avg
        print ("cant find avg")
        return None

if __name__ == '__main__':
    w = worker()
    w.run()
## --------------------------------------
