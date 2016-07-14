from ROOT import *
import json
import array
import numpy
import math
import itertools

def get_stats(vals):
    test = numpy.array(vals)
    mean = numpy.mean(test)
    std = numpy.std(test)
    return [mean, std]

file = TFile.Open("PRtree.root")
tree = file.Get("tree")
tree.SetAlias("days","((merged_at.Convert()-created_at.Convert())/60/60/24)")

#drawing strings
draw="number:days:additions+deletions:changed_files:comments"
cut="merged"

#get tree entries
nentries = tree.GetEntries()
tree.SetEstimate(nentries)
tree.Draw(draw,cut,"para goff")

draw_split = draw.split(':')
row_dict = {}
for i,d in enumerate(draw_split):
    v = tree.GetVal(i)
    v.SetSize(tree.GetSelectedRows())
    row_dict[d] = v
    
#find outliers
outliers = {}
outlier_numbers = []
for qty,vals in row_dict.iteritems():
    if qty=="number": continue
    mean, std = get_stats(vals)
    outliers[qty] = []
    for i,val in enumerate(vals):
        pull = (val-mean)/std
        if abs(pull)>3:
            out_number = row_dict["number"][i]
            print "Outlier: "+str(out_number)+", "+qty+" = "+"{:.1f}".format(val)+" ("+"{:.1f}".format(pull)+" sigma)"
            outliers[qty].append(val)
            outlier_numbers.append(out_number)

#find ranges, excluding outliers
ranges = {}
for qty,vals in row_dict.iteritems():
    if qty=="number": continue
    ranges[qty] = [0, max([val for i,val in enumerate(vals) if val not in outliers[qty]])]
    print qty+": 0, "+"{:.1f}".format(ranges[qty][1])

#1D plots
nbins = int(ranges["days"][1])
for qty,vals in row_dict.iteritems():
    if qty=="number": continue
    
    can = TCanvas(qty,qty)
    can.Draw()
    
    maxbin = math.ceil(ranges[qty][1])
    hist = TH1F(qty,"",nbins,ranges[qty][0],maxbin)
    hist.SetStats(False)
    hist.GetXaxis().SetTitle(qty)
    for val in vals:
        # last bin contains overflow
        if val <= maxbin: hist.Fill(val)
        else: hist.Fill(hist.GetBinCenter(nbins))
    hist.Draw("hist")
    
    mean, std = get_stats(vals)
    pave = TPaveText(0.65,0.7,0.85,0.8,"NDC")
    pave.AddText("Mean = {:.1f}".format(mean))
    pave.AddText("RMS = {:.1f}".format(std))
    pave.SetFillColor(0)
    pave.SetBorderSize(0)
    pave.SetTextFont(42)
    pave.SetTextSize(0.05)
    pave.Draw("same")
    
    can.Print(qty+".png","png")

#2D plots
for qty in draw_split[2:]:
    xvals = [float(x) for x in row_dict["days"]]
    yvals = [float(y) for y in row_dict[qty]]
    mask = [1]*len(xvals)
    for i,x in enumerate(xvals):
        if row_dict["number"][i] in outlier_numbers: mask[i] = 0
    xvals_clean = list(itertools.compress(xvals,mask))
    yvals_clean = list(itertools.compress(yvals,mask))
    
    name = "days_vs_"+qty
    can = TCanvas(name,name)
    can.Draw()
    
    graph = TGraph(len(xvals_clean),numpy.array(xvals_clean),numpy.array(yvals_clean))
    graph.SetTitle("")
    graph.GetXaxis().SetTitle("days")
    graph.GetYaxis().SetTitle(qty)
    graph.SetMarkerStyle(20)
    graph.Draw("ap")
    
    pave = TPaveText(0.55,0.75,0.85,0.8,"NDC")
    pave.AddText("Correlation = {:.2f}".format(graph.GetCorrelationFactor()))
    pave.SetFillColor(0)
    pave.SetBorderSize(0)
    pave.SetTextFont(42)
    pave.SetTextSize(0.05)
    pave.Draw("same")
    
    can.Print(name+".png","png")
