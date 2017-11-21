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
from threading import Lock
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

class start(Resource):
    def __init__(self):
        super(start, self).__init__()
    def get(self):
        global mast
        return {"start" : mast.start}
    def post(self):
        global mast
        r = request.json
        if "user" in r and "repo" in r and mast.start == False:
            mast.user = r["user"]
            mast.repo = r["repo"]
            mast.run()
            return { "success" : True }
        else:
            return { "success" : False }
api.add_resource(start, '/start', endpoint = 'start')

class jobs(Resource):
    def __init__(self):
        super(jobs, self).__init__()
    def get(self):
        global mast
        # get the next valid job
        this_job, this_file, this_commit = mast.get_job()
        # if this job is none, we're done
        if this_job == None:
            return {'done' : True}
        # otherwise, respond with job
        else:
            return {'url' : this_job, 'commit' : this_commit, "path" : this_file}
    def post(self):
        r = request.json
        if "url" in r and "avg" in r and "path" in r:
            print ("avg:", r["avg"])
            global mast
            mast.add_to_total(r)
        else:
            print ("post", r)
        return {"thanks" : "pal"}
api.add_resource(jobs, '/jobs', endpoint = 'jobs')

class results(Resource):
    def __init__(self):
        super(results, self).__init__()
    def get(self):
        global mast
        return {"done_jobs" : mast.average()}
    def delete(self):
        global mast
        if mast.delete_results() == True:
            return {"done_jobs" : []}
        else:
            return {"error" : ["still active"]}
api.add_resource(results, '/done', endpoint = 'done')

class master():
    def __init__(self, token):
        self.token = token
        self.start = False
        self.owner="Richard-Lynch"
        self.repo="flask_test"
        self.job_lock = Lock()
        self.results_lock = Lock()
        # self.done_files = {} # dict of done file, sha of commit as key, list of done files as values
        # self.current_commit = 0
        # self.current_file = 0
        # self.done_commits = 0
        # self.done_files = {} # dict of done file, sha of commit as key, list of done files as values

    def run(self):
        self.job_lock.acquire()
        self.results_lock.acquire()
        self.trees, self.commits = self.get_trees(self.owner, self.repo)
        self.trees = self.remove_trees(self.trees)
        # print
        for sha in self.trees:
            print ("sha:", sha)
            for file_details in self.trees[sha]:
                print ("\tfile: {} ({})".format(file_details["path"], file_details["url"]))
        self.current_commit = 0
        self.current_file = 0
        self.done_commits = 0
        self.done_files = {} # dict of done file, sha of commit as key, list of done files as values
        self.job_lock.release()
        self.results_lock.release()
        self.start = True

    def delete_results(self):
        if self.start == False:
            self.results_lock.acquire()
            self.done_files, self.current_file, self.current_commit, self.done_commits = {}, 0, 0, 0
            self.results_lock.release()
            return True
            return {"done_jobs" : []}
        else:
            return False
            return {"error" : ["still active"]}

    def average(self):
        self.results_lock.acquire()
        done = []
        for commit in self.done_files:
            count = self.done_files[commit]["count"]
            total = self.done_files[commit]["total"]
            expected = self.done_files[commit]["expected"]
            broken = self.done_files[commit]["broken"]
            if count > 0:
                avg = total/count
            else:
                avg = 0
            finished = count + broken == expected
            done.append({\
                    "commit" : commit, \
                    "count": count, \
                    "broken" : broken, \
                    "expected": expected, \
                    "total" : total, \
                    "average":  avg, \
                    "finished": finished \
                    })
        self.results_lock.release()
        return done

    def add_to_total(self, result):
# if "url" in r and "avg" in r and "path" in r:
        self.results_lock.acquire()
        commit = result["commit"]
        if commit not in self.done_files:
            print ("adding commit", commit)
            self.done_files[result["commit"]] = { \
                    "total" : 0, \
                    "count" : 0, \
                    "broken" : 0, \
                    "expected" : len(self.trees[commit]), \
                    "files" : {} \
                    }
        self.done_files[commit]["files"][result["url"]] = result
        if result["avg"] != None:
            self.done_files[commit]["total"] += result["avg"]
            self.done_files[commit]["count"] += 1
        else:
            self.done_files[commit]["broken"] += 1
        if self.done_files[commit]["count"]+self.done_files[commit]["broken"] == self.done_files[commit]["expected"]:
            print ("DONE!:", commit)
            self.done_commits += 1
            if self.done_commits >= len(self.trees):
                print ("TOTALY DONE")
                self.start = False
        self.results_lock.release()

    def get_trees(self, owner, repo):
        payload = {"access_token" : str(self.token), "recursive" : 1}
        address = self.make_address(owner, repo)
        commits = self.get_commits(address)
        trees = {}
        commit_list = []
        # each tree contains all of the files in a commit, with the commits sha as a key
        for commit in commits:
            if "sha" in commit:
                sha = commit["sha"]
                commit_list.append(sha)
                temp_address = address + "/git/trees/" + sha
                # each tree has a list of files or dirs
                tree = requests.get(temp_address, params=payload).json()
                if 'tree' in tree:
                    new_tree = []
                    for file_details in tree['tree']:
                        new_tree.append(file_details)
                    trees[sha] = new_tree
                else:
                    print ("issue with tree:", sha)
            else:
                print ("issue with commit:", commit)
        return trees, commit_list

    def get_job(self):
        self.job_lock.acquire()
        if self.current_commit < len(self.trees): # finished all commits
            commit = self.commits[self.current_commit] # sha of commit
            tree = self.trees[commit] # list of files for this commit
            if len(tree) > self.current_file:
                file_details = tree[self.current_file] # file_details of job
                print ("path:", file_details["path"])
                self.current_file += 1
                self.job_lock.release()
                return file_details["url"], file_details["path"], commit
            else:
                self.current_commit += 1
                self.current_file = 0 # restart file counter on new commit
                self.job_lock.release()
                return self.get_job() # call rec
        else:
            self.job_lock.release()
            return None, None, None

    def remove_trees(self, trees):
        new_trees = {}
        for sha in trees:
            new_sha = []
            for file_details in trees[sha]:
                if file_details["type"] != "tree":
                   new_sha.append(file_details) 
            new_trees[sha] = new_sha
        return new_trees

    def make_address(self, owner, repo):
        return "https://api.github.com/repos/" + str(owner) + "/" + str(repo)

    def get_commits(self, address):
        payload = {"access_token" : self.token}
        address += "/commits"
        commits = requests.get(address, params=payload).json()
        return commits

if __name__ == '__main__':
#----------------
    token = ""
    with open ("token", "r") as f:
        token = f.read().split()[0]
    mast = master(token)
#----------------    
    app.run(host='0.0.0.0', debug=True, port=8080)
