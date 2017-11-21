#!/usr/local/bin/python3

import requests
import json
# sha="a5ec11596e5569a195413a6eff28c83a7da153cf"
# sha="master"
# address="https://api.github.com/repos/" + owner + "/" + repo + "/commits/" + sha
# # print ("address:", address)
# r = requests.get(address).json()
# for key in r:
#     print ("K:", key)
# # print ("response:", r)
# # print ("commit:", r["commit"])
# # print ("url:", r["url"])
# sha="0b7338d6fae99183d2a8220a8ea73010427f8c6b"
# sha = r["sha"]
# address="https://api.github.com/repos/" + owner + "/" + repo + "/git/trees/" + sha
# # r = requests.get(r["url"]).json()
# r = requests.get(address).json()
# # print ("response:", r)

# for file_dir in r['tree']:
#     print (file_dir["path"])
#     if file_dir["type"] == "blob":
#         print ("\tthis is a file")
#     elif file_dir["type"] == "tree":
#         print ("\tthis is a dir")
#     else:
#         print ("dunno what that is")


if __name__ == '__main__':
    owner="Richard-Lynch"
    repo="IntApps_Complex"
    address="https://api.github.com/repos/" + owner + "/" + repo + "/commits"
    print ("address:", address)
    r = requests.get(address).json()
    print ("got r")
    for commit in r:
        # print ("K:", commit)
        if "sha" in commit:
            sha = commit["sha"]
            print ("sha:", sha)
            if "url" in commit:
                print ("url:", commit["url"])
        else:
            print ("no sha")
        # continue
        return
        address="https://api.github.com/repos/" + owner + "/" + repo + "/git/trees/" + sha
# r = requests.get(r["url"]).json()
        r = requests.get(address).json()
# print ("response:", r)

        for file_dir in r['tree']:
            print (file_dir["path"])
            if "url" in file_dir:
                print ("\turl:", file_dir["url"])
            if "sha" in file_dir:
                print ("\tsha:", file_dir["sha"])
            if file_dir["type"] == "blob":
                print ("\tthis is a file")
            elif file_dir["type"] == "tree":
                print ("\tthis is a dir")
            else:
                print ("dunno what that is")
# headers = {'Accept' : 
    r = requests.get("https://api.github.com/repos/Richard-Lynch/IntApps_Complex/git/blobs/efa5d9d2de7c715fad7cee7458828d1fe3f22a88", headers={'Accept' : 'application/vnd.github.v3.raw'})
    print ("R:",  r.text)

# with open ('test_out.txt', 'w') as f:
#     f.write(r.text)
#     print ("data written")

# r = requests.get(https://api.github.com/repos/Richard-Lynch/IntApps_Complex/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391)
