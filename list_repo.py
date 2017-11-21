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


owner="Richard-Lynch"
repo="IntApps_Complex"
address="https://api.github.com/repos/" + owner + "/" + repo + "/commits"
# print ("address:", address)
r = requests.get(address).json()
for key in r:
    print ("K:", key)
    if "sha" in key:
        print ("sha:", key["sha"])
    else:
        print ("no sha")
    continue
    # sha = key["sha"]
    address="https://api.github.com/repos/" + owner + "/" + repo + "/git/trees/" + sha
# r = requests.get(r["url"]).json()
    r = requests.get(address).json()
# print ("response:", r)

    for file_dir in r['tree']:
        print (file_dir["path"])
        if file_dir["type"] == "blob":
            print ("\tthis is a file")
        elif file_dir["type"] == "tree":
            print ("\tthis is a dir")
        else:
            print ("dunno what that is")
