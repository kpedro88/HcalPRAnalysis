import requests
import json

def getPRinfo(PRnum,PRprimary,PRdict):
    PR = str(PRnum)
    prim = str(PRprimary)
    

# list of PRs
PRs = [12883, 12905, 12916, 12974, 13004, 13139, 13205, 13232, 13255, 13290, 13252, 13331, 13307, 13334, 13389, 13491, 13557, 13567, 13683, 13704, 13832, 13822, 13861, 13868, 13915, 13997, 14101, 14139, 14313, 14314, 14363, 14383, 14456, 14418, 14461, 14482, 14526, 14594, 14572, 14691, 14749, 14838, 14920, 14599, 14856, 15061, 15092, 15180, 15214, 15241, 15254, 15261, 15320, [15321,15520], 15322, [15324,15419], 15357, 15363, 15364, 15374, 15380, 15382, 15403, 15406, 15474, 15499, 15521, 15467, 15606, 15626, 15646, 15627, 15679, 15663, 15686, 15695, 15690, 15688, 15569, 15712, 15714, 15715, 15735, 15779, 15834, 15839, 15735, 15856, 15884, 15925, 15924, 15915, 15889, 15916, 15945, 15959, 15993, 16002, 16009, 16005, 16048, 16006, 16072, 16080, 16082, 16011, 16057, 16059, [16070, 16315], 16067, 16083, 16101, 16089, 16102, 16097, 16180, 16183, 16156, 16197, 16211, 16230, 16208, 16266, 16259, 16302, 16326, 16314, 16328, 16286, 16301, 16343]

# open cached database of PR properties
with open("PRdict.json",'r') as PRfile:
    PRdictCached = json.load(PRfile)

PRdict = {}
    
num_merged = 0
    
for PRitem in PRs:
    # handle PRs with multiple numbers
    if isinstance(PRitem,list):
        PRlist = PRitem
        primary = PRlist[0]
    else:
        PRlist = [PRitem]
        primary = PRitem
    
    skip = False
        
    for PRnum in PRlist:
        if skip: break
        PR = str(PRnum)
        pri = str(primary)

        if PRnum==primary:
            # skip finished PRs
            if pri in PRdictCached.keys() and (PRdictCached[pri]["merged"] or PRdictCached[pri]["closed"]):
                PRdict[pri] = PRdictCached[pri]
                if PRdict[pri]["merged"]: num_merged += 1
                skip = True
                continue
        # call API (https://developer.github.com/v3/pulls/)
        r = requests.get('https://api.github.com/repos/cms-sw/cmssw/pulls/'+str(PR))
        if(r.ok):
            PRitem = json.loads(r.text or r.content)
            # create or reset dict entry
            if PRnum==primary:
                PRdict[PR] = {}
            # get properties            
            if PRnum==primary:
                # some properties are taken from primary only
                PRdict[pri]["created_at"] = PRitem["created_at"]
                PRdict[pri]["comments"] = PRitem["comments"]
                
                # some are taken from primary to start
                PRdict[pri]["merged"] = PRitem["merged"]
                PRdict[pri]["closed"] = PRitem["state"] != "open"
                PRdict[pri]["merged_at"] = PRitem["merged_at"]
                PRdict[pri]["closed_at"] = PRitem["closed_at"]
                PRdict[pri]["commits"] = PRitem["commits"]
                PRdict[pri]["additions"] = PRitem["additions"]
                PRdict[pri]["deletions"] = PRitem["deletions"]
                PRdict[pri]["changed_files"] = PRitem["changed_files"]
            else:    
                # some are overwritten from secondary
                PRdict[pri]["merged"] = PRitem["merged"]
                PRdict[pri]["closed"] = PRitem["state"] != "open"
                PRdict[pri]["merged_at"] = PRitem["merged_at"]
                PRdict[pri]["closed_at"] = PRitem["closed_at"]
                PRdict[pri]["commits"] = PRitem["commits"]
                PRdict[pri]["additions"] = PRitem["additions"]
                PRdict[pri]["deletions"] = PRitem["deletions"]
                PRdict[pri]["changed_files"] = PRitem["changed_files"]
            
                # some are combined
                PRdict[pri]["comments"] += PRitem["comments"]

            if PRdict[pri]["closed"] and not PRdict[pri]["merged"]: print "PR "+PR+" was closed without being merged"
            if PRdict[pri]["merged"]: num_merged += 1
        
# save cached database
with open("PRdict.json",'w') as PRfile:
    json.dump(PRdict,PRfile, indent=2)

# print summary
print str(len(PRs))+" PRs, "+str(num_merged)+" merged"   
