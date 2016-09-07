from ROOT import *

file = TFile.Open("PRtree.root")
tree = file.Get("tree")

cleanup = [15363,15320,15061,14856,15374]

cleanup_cut = "||".join(["number=="+str(cu) for cu in cleanup])

drawname = "1>>htemp(1,0.5,1.5)"
gname = "hist goff"
quantities = ["merged","additions","deletions","changed_files"]

print "Feature PRs:"
for q in quantities:
    tree.Draw(drawname,q+"*(merged&&!("+cleanup_cut+"))",gname)
    htemp = gDirectory.Get("htemp")
    print "  "+q+" = "+str(htemp.GetBinContent(1))
    
print "Cleanup PRs:"
for q in quantities:
    tree.Draw(drawname,q+"*(merged&&("+cleanup_cut+"))",gname)
    htemp = gDirectory.Get("htemp")
    print "  "+q+" = "+str(htemp.GetBinContent(1))
