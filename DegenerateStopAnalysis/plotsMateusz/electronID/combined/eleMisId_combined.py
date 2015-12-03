#eleMisId_combined.py

import ROOT
import os, sys
from array import *
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *

#Input options
inputSample = "WJets" # "signal" "WJets" "TTJets"
zoom = True
save = True

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetOptTitle(0) #suppresses title box
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)

 
#CMG Tuples
#data_path = "/data/nrad/cmgTuples/RunII/RunIISpring15MiniAODv2/"

print makeLine()
print "Signal Samples:"
newLine()
for s in allSignals: print s['name']
print makeLine()
print "Background Samples:"
newLine()
for s in samples: print s['name']
#print makeLine()

print makeLine()
print "Using", inputSample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])
#Bin size 
#nbins = 100
xmin = 0
xmax = 1000
sampleName = allSignals[0]

if inputSample == "signal":
   sampleName = allSignals[0]
   xmax = 150
elif inputSample == "WJets":
   sampleName = WJetsToLNu
   xmax = 500
elif inputSample == "TTJets":
   sampleName = TTJets_LO
   xmax = 500
else:
   print "Sample unavailable (check name)."
   sys.exit(0)

for f in getChunks(sampleName)[0]: Events.Add(f['file'])

bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size

#Zoom
z = ""
if zoom == True:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax+2,2))
   z = "_lowPt"

#Selection criteria
#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
recoSel = "abs(LepGood_pdgId) == 11"
misMatchSel = "LepGood_mcMatchId == 0"
cutSel = "LepGood_SPRING15_25ns_v1 >="


##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Reconstructed selection
h1 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + cutSel + "1", bins) #match gen cuts to LepGood cuts (eta, pt) 
h1.SetName("recoEle")
h1.SetTitle("Fake (Non-Prompt) Electron p_{T} for Various IDs (Veto, Loose, Medium, Tight, MVA)")
h1.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h1.GetXaxis().SetTitleOffset(1.2)
h1.GetYaxis().SetTitleOffset(1.2)
h1.Draw()
h1.SetFillColor(ROOT.kBlue-9)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(3)

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

l1 = makeLegend()
l1.AddEntry("recoEle", "Reconstructed Electron p_{T}", "F")

alignStats(h1)

h8= makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + cutSel + "1", bins)
h2 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "1", bins)
h2.SetName("electrons_veto")
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kGreen+3)
h2.SetLineWidth(3)
l1.AddEntry("electrons_veto", "Veto ID", "F")

h9= makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + cutSel + "2", bins)
h3 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "2", bins)
h3.SetName("electrons_loose")
h3.Draw("same")
h3.SetFillColor(0)
h3.SetLineColor(ROOT.kBlue+1)
h3.SetLineWidth(3)
l1.AddEntry("electrons_loose", "Loose ID", "F")

h10 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + cutSel + "3", bins)
h4 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "3", bins)
h4.SetName("electrons_medium")
h4.Draw("same")
h4.SetFillColor(0)
h4.SetLineColor(ROOT.kOrange-2)
h4.SetLineWidth(3)
l1.AddEntry("electrons_medium", "Medium ID", "F")

h11 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + cutSel + "4", bins)
h5 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "4", bins)
h5.SetName("electrons_tight")
h5.Draw("same")
h5.SetFillColor(0)
h5.SetLineColor(ROOT.kRed+1)
h5.SetLineWidth(3)
l1.AddEntry("electrons_tight", "Tight ID", "F")

#MVA IDs

WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

WP = "WP90"

mvaSel1 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" # < 2.5 (applied already in LepGood)

h12 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + mvaSel1, bins)
h6 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel1, bins)
h6.SetName("electrons_mva_wp90")
h6.Draw("same")
h6.SetFillColor(0)
h6.SetLineColor(ROOT.kMagenta+2)
h6.SetLineWidth(3)

l1.AddEntry("electrons_mva_wp90", "MVA ID (" + WP + ")", "F")

WP = "WP80"

mvaSel2 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" # < 2.5 (applied already in LepGood)

h13 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + mvaSel2, bins)
h7 = makeHistVarBins(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel2, bins)
h7.SetName("electrons_mva_wp80")
h7.Draw("same")
h7.SetFillColor(0)
h7.SetLineColor(ROOT.kAzure+5)
h7.SetLineWidth(3)

l1.AddEntry("electrons_mva_wp80", "MVA ID (" + WP + ")", "F")
l1.Draw()

#Efficiency curves
c1.cd(2)
l2 = makeLegend()

#Mismatch Efficiency Veto
efficiency1 = ROOT.TEfficiency(h2, h8) #(passed, total)
efficiency1.SetName("eff1")
efficiency1.SetTitle("Electron Mismatch Efficiency for Various IDs ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency1.SetMarkerColor(ROOT.kGreen+3)
efficiency1.SetMarkerStyle(33)
efficiency1.SetMarkerSize(1.5)
efficiency1.Draw() 
efficiency1.SetLineColor(ROOT.kGreen+3)
efficiency1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency1.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency1.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency1.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff1", "Veto ID", "P")

#Mismatch Efficiency Loose
efficiency2 = ROOT.TEfficiency(h3, h9) #(passed, total)
efficiency2.SetName("eff2")
#efficiency2.SetTitle("Electron Mismatch Efficiency for Loose ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency2.SetMarkerColor(ROOT.kBlue+1)
efficiency2.SetMarkerStyle(33)
efficiency2.SetMarkerSize(1.5)
efficiency2.Draw("sameP") 
efficiency2.SetLineColor(ROOT.kBlue+1)
efficiency2.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency2.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#efficiency2.GetPaintedGraph().GetXaxis().CenterTitle()
#efficiency2.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff2", "Loose ID", "P")

#Mismatch Efficiency Medium
efficiency3 = ROOT.TEfficiency(h4, h10) #(passed, total)
efficiency3.SetName("eff3")
#efficiency3.SetTitle("Electron Mismatch Efficiency for Medium ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency3.SetMarkerColor(ROOT.kOrange-2)
efficiency3.SetMarkerStyle(33)
efficiency3.SetMarkerSize(1.5)
efficiency3.Draw("sameP") 
efficiency3.SetLineColor(ROOT.kOrange-2)
efficiency3.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency3.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency3.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#efficiency3.GetPaintedGraph().GetXaxis().CenterTitle()
#efficiency3.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff3", "Medium ID", "P")

#Mismatch Effciency Tight
efficiency4 = ROOT.TEfficiency(h5, h11) #(passed, total)
efficiency4.SetName("eff4")
#efficiency4.SetTitle("Electron Mismatch Efficiency for Tight ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency4.SetMarkerColor(ROOT.kRed+1)
efficiency4.SetMarkerStyle(33)
efficiency4.SetMarkerSize(1.5)
efficiency4.Draw("sameP") 
efficiency4.SetLineColor(ROOT.kRed+1)
efficiency4.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency4.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency4.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#efficiency4.GetPaintedGraph().GetXaxis().CenterTitle()
#efficiency4.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff4", "Tight ID", "P")

#MVA
#Efficiency WP90
efficiency5 = ROOT.TEfficiency(h6, h12) #(passed, total)
efficiency5.SetName("eff5")
#efficiency5.SetTitle("Electron Mismatch Efficiency Plot for MVA ID (" + WP + "); Reconstructed Electron p_{T} / GeV ; Counts")
efficiency5.SetMarkerColor(ROOT.kMagenta+2)
efficiency5.SetMarkerStyle(33)
efficiency5.SetMarkerSize(1)
efficiency5.Draw("sameP")
efficiency5.SetLineColor(ROOT.kMagenta+2)
efficiency5.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency5.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency5.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#efficiency5.GetPaintedGraph().GetXaxis().CenterTitle()
#efficiency5.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff5", "MVA ID (WP90)", "P")

#Efficiency WP80
efficiency6 = ROOT.TEfficiency(h7, h13) #(passed, total)
efficiency6.SetName("eff6")
#efficiency6.SetTitle("Electron Mismatch Efficiency Plot for MVA ID (" + WP + "); Reconstructed Electron p_{T} / GeV ; Counts")
efficiency6.SetMarkerColor(ROOT.kAzure+5)
efficiency6.SetMarkerStyle(33)
efficiency6.SetMarkerSize(1)
efficiency6.Draw("sameP")
efficiency6.SetLineColor(ROOT.kAzure+5)
efficiency6.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency6.GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#efficiency6.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#efficiency6.GetPaintedGraph().GetXaxis().CenterTitle()
#efficiency6.GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff6", "MVA ID (WP80)", "P")

l2.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/combined/misId/" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "electronMisId_" + inputSample + z + ".root")
c1.SaveAs(savedir + "electronMisId_" + inputSample + z + ".png")
c1.SaveAs(savedir + "electronMisId_" + inputSample + z + ".pdf")
