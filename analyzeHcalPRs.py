from ROOT import *
import json
from array import array

# open cached database of PR properties
with open("PRdict.json",'r') as PRfile:
    PRdict = json.load(PRfile)

gROOT.ProcessLine(
"struct pull_t { \
    Int_t number;\
    Bool_t merged;\
    Bool_t closed;\
    Int_t comments;\
    Int_t commits;\
    Int_t additions;\
    Int_t deletions;\
    Int_t changed_files;\
};"
)
    
file = TFile.Open("PRtree.root","RECREATE")
tree = TTree("tree","HCAL PRs from GitHub")

pull = pull_t()
created_at = TDatime()
merged_at = TDatime()
closed_at = TDatime()

tree.Branch('number', AddressOf(pull,'number'), 'number/I')
tree.Branch('merged', AddressOf(pull,'merged'), 'merged/O')
tree.Branch('closed', AddressOf(pull,'closed'), 'closed/O')
tree.Branch('created_at', "TDatime", created_at)
tree.Branch('merged_at', "TDatime", merged_at)
tree.Branch('closed_at', "TDatime", closed_at)
tree.Branch('comments', AddressOf(pull,'comments'), 'comments/I')
tree.Branch('commits', AddressOf(pull,'commits'), 'commits/I')
tree.Branch('additions', AddressOf(pull,'additions'), 'additions/I')
tree.Branch('deletions', AddressOf(pull,'deletions'), 'deletions/I')
tree.Branch('changed_files', AddressOf(pull,'changed_files'), 'changed_files/I')

for PR,prop in PRdict.iteritems():
    #print " INPUT created_at: "+str(prop["created_at"])+" merged_at: "+str(prop["merged_at"])+" closed_at: "+str(prop["closed_at"])
    pull.number = int(PR)
    pull.merged = int(prop["merged"])
    pull.closed = int(prop["closed"])
    if prop["created_at"] != None: created_at.Set(prop["created_at"].replace("T"," ").replace("Z",""))
    else: created_at.Set(TDatime().AsSQLString())
    if prop["merged_at"] != None: merged_at.Set(prop["merged_at"].replace("T"," ").replace("Z",""))
    else: merged_at.Set(TDatime().AsSQLString())
    if prop["closed_at"] != None: closed_at.Set(prop["closed_at"].replace("T"," ").replace("Z",""))
    else: closed_at.Set(TDatime().AsSQLString())
    #print "OUTPUT created_at: "+created_at.AsSQLString()+"  merged_at: "+merged_at.AsSQLString()+"  closed_at: "+closed_at.AsSQLString()
    pull.comments = int(prop["comments"])
    pull.commits = int(prop["commits"])
    pull.additions = int(prop["additions"])
    pull.deletions = int(prop["deletions"])
    pull.changed_files = int(prop["changed_files"])
    
    tree.Fill()
    
file.Write()
file.Close()