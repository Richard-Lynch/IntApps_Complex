#!/usr/local/bin/python3
import sys
import os
import requests
import json
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
        commit = 0
        if this_job > 1:
            commit = 1
        if commit not in done_jobs and commit not in total:
            done_jobs[commit] = {}
            total[commit] = 0
        return {'job' : files[this_job], 'commit' : commit}
    def post(self):
        global done_jobs
        global total
        r = request.json
        if "job" in r and "avg" in r:
            print ("job:", r["job"])
            print ("avg:", r["avg"])
            done_jobs[r["commit"]][r["job"]] = r["avg"]
            total[r["commit"]] += r["avg"]
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
        return {"done_jobs" : self.average()}
    def delete(self):
        global done_jobs
        global job
        global total
        done_jobs = {}
        job = -1
        total = {}
        return {"done_jobs" : []}
    def average(self):
        global total
        global done_jobs
        done = []
        for commit in done_jobs:
            done.append({\
                    "commit" : commit, \
                    "num_done": len(done_jobs[commit]), \
                    "average": total[commit]/len(done_jobs[commit]) \
                    })
        return done
api.add_resource(results, '/done', endpoint = 'done')

def make_address(owner, repo):
    return "https://api.github.com/repos/" + str(owner) + "/" + str(repo)

def get_commits(address):
    global token
    payload = {"access_token" : token}
    address += "/commits"
    commits = requests.get(address, params=payload).json()
    return commits

def get_trees(owner, repo):
    global token
    print("t:", token)
    payload = {"access_token" : token, "recursive" : 1}
    address = make_address(owner, repo)
    print ("addres", address)
    commits = get_commits(address)
    print ("commits")
    trees = {}
    # each tree contains all of the files in a commit, with the commits sha as a key
    print ("commits:", commits)
    for commit in commits:
        print ("getting commits")
        if "sha" in commit:
            sha = commit["sha"]
            address += "/git/trees/" + sha
            # each tree has a list of files or dirs
            tree = get_dirs(requests.get(address, params=payload).json()['trees'])
            trees[sha] = tree
        else:
            print ("issue with commit:", commit)
    return trees

def get_dirs(tree):
    new_tree = []
    print ("in get dirs")
    # for each file in the dir
    for file_dir in tree:
        print ("getting file_dir", file_dir)
        # if item is a dir
        if "type" in file_dir and file_dir["type"] == "tree":
            # call recursivly and create flat structure
            print ("calling rec")
            new_tree.extend(get_dirs(file_dir))
        # if item is a file
        else:
            # append to list
            print ("adding to file")
            new_tree.append(file_dir)
    return new_tree

if __name__ == '__main__':
    path="./testing_dir/"
    files = os.listdir(path)
    job = -1
    max_job = len(files)
#----------------
    token = ""
    with open ("token", "r") as f:
        token = f.read()
        print("t:", token)
    print("t:", token)
    owner="Richard-Lynch"
    repo="IntApps_Complex"
    trees = get_trees(owner, repo)
    for sha in trees:
        print ("sha", sha)

    sys.exit
#----------------    
    done_jobs = {}
    total = {}
    app.run(host='0.0.0.0', debug=True, port=8080)
