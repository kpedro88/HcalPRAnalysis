import requests
import json

# list of PRs
PRs = [12883, 12905, 12916, 12974, 13004, 13139, 13205, 13232, 13255, 13290, 13252, 13331, 13307, 13334, 13389, 13491, 13557, 13567, 13683, 13704, 13832, 13822, 13861, 13868, 13915, 13997, 14101, 14139, 14313, 14314, 14363, 14383, 14456, 14418, 14461, 14482, 14526, 14594, 14572, 14691, 14749, 14838, 14920, 14599, 14856, 15061, 15092, 15180, 15214]

# open cached database of PR properties
with open("PRdict.json",'r') as PRfile:
    PRdict = json.load(PRfile)

for PRnum in PRs:
    # skip finished PRs
    PR = str(PRnum)
    if PR in PRdict.keys() and (PRdict[PR]["merged"] or PRdict[PR]["closed"]): continue
    # call API (https://developer.github.com/v3/pulls/)
    r = requests.get('https://api.github.com/repos/cms-sw/cmssw/pulls/'+str(PR))
    if(r.ok):
        PRitem = json.loads(r.text or r.content)
        # create or reset dict entry
        PRdict[PR] = {}
        # get properties
        PRdict[PR]["merged"] = PRitem["merged"]
        PRdict[PR]["closed"] = PRitem["state"] != "open"
        PRdict[PR]["created_at"] = PRitem["created_at"]
        PRdict[PR]["merged_at"] = PRitem["merged_at"]
        PRdict[PR]["closed_at"] = PRitem["closed_at"]
        PRdict[PR]["comments"] = PRitem["comments"]
        PRdict[PR]["commits"] = PRitem["commits"]
        PRdict[PR]["additions"] = PRitem["additions"]
        PRdict[PR]["deletions"] = PRitem["deletions"]
        PRdict[PR]["changed_files"] = PRitem["changed_files"]

        if PRdict[PR]["closed"] and not PRdict[PR]["merged"]: print "PR "+str(PR)+" was closed without being merged"
        
# save cached database
with open("PRdict.json",'w') as PRfile:
    json.dump(PRdict,PRfile, indent=2)
