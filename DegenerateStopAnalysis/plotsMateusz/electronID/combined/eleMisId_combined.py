#eleMisId_combined.py

import ROOT
import os, sys

#import Workspace.RA4Analysis.cmgTuples_Spring15_25ns_fromArtur
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *

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


def makeLine():
   line = "\n************************************************************************************************************************************************************************\n"
   return line

def makeDoubleLine():
   line = "\n************************************************************************************************************************************************************************\n\
*********************************************************************************************************************************************************************\n"
   return line

def newLine():
   print ""
   return 

def makehist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname + " / GeV")
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.SetFillColor(ROOT.kAzure+2)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist 

def drawhist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000):
   #hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   sample.Draw(varname, sel) #+ ">>hist"
   #hist.SetTitle(varname + " Plot")
   #hist.GetXaxis().SetTitle(varname + " / GeV")
   #hist.GetYaxis().SetTitle("Counts")
   #hist.GetXaxis().CenterTitle()
   #hist.GetYaxis().CenterTitle()
   #hist.Draw()
   #hist.SetFillColor(ROOT.kAzure+2)
   #hist.SetLineColor(ROOT.kBlack)
   #hist.SetLineWidth(3)
   #ROOT.gPad.Update()

#Selection function
def select(varname, cut, option): #option = {>, =, <}
  if option == ">" or options == "=" or option == "<": 
      sel = "abs(" + varname + option + str(cut) + ")"
  return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.775,0.45,0.875,0.65)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TPaveText(0.775,0.40,0.875,0.65, "NDC") #NB & ARC
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

def alignStats(hist):
   st = hist.FindObject("stats")
   st.SetX1NDC(0.775)
   st.SetX2NDC(0.875)
   st.SetY1NDC(0.7)
   st.SetY2NDC(0.85)

##Fit Function
#fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
#fitFunc.SetParNames("Normalisation", "Edge", "Resolution", "Y-Offset")
##fitFunc.SetParameter(0, 0.5)
##fitFunc.SetParameter(1, 150)
##fitFunc.SetParameter(2, 50)  
##fitFunc.SetParLimits(0, 0.4, 0.65) 
#fitFunc.SetParLimits(1, 0, 200) #init: [0,200]
#fitFunc.SetParLimits(2, 0, 60) #init: [0,60]
#fitFunc.SetParLimits(3, 0.45, 0.8) #init: [0.45,0.8]
 
#CMG Tuples
#data_path = "/data/nrad/cmgTuples/RunII/RunIISpring15MiniAODv2/"
#signal_path = "/data/nrad/cmgTuples/RunII/7412/T2DegStop_300_270/"

print makeLine()
print "Signal Samples:"
newLine()
for s in allSignals: print s['name']
print makeLine()
print "Background Samples:"
newLine()
for s in samples: print s['name']
#print makeLine()

sample = "WJets" #"signal" #"WJets"
print makeLine()
print "Using", sample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

for f in getChunks(WJetsToLNu)[0]: Events.Add(f['file']) # allSignals[0] WJetsToLNu TTJets_LO

deltaR = "sqrt((genLep_eta - LepGood_eta)^2 + (genLep_phi - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt - LepGood_pt)/genLep_pt)" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

#Bin size 
nbins = 100 #80
min = 0 #GeV
max = 500 # 20 #GeV 

#Zoom
zoom = False
z = ""
if zoom == True:
   nbins = 100
   max = 50
   z = "_lowPt"

#Selection criteria
#genSel = "ngenLep == 1 && abs(genLep_pdgId) == 11 && abs(genLep_eta) < 2.5" #nLepGood == 1 biases your efficiency
#matchSel = "abs(LepGood_pdgId) == 11 && LepGood_mcMatchId != 0 &&" + "Min$(" + deltaR +") &&" + deltaR + "<" + str(deltaRcut)
recoSel = "abs(LepGood_pdgId == 11)"
misMatchSel = "LepGood_mcMatchId == 0"
cutSel = "LepGood_SPRING15_25ns_v1 >="

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Reconstructed selection
h1 = makehist(Events, "LepGood_pt", recoSel, nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h1.SetName("genEle")
h1.SetTitle("Fake Electron p_{T} for Various IDs")
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
l1.AddEntry("genEle", "Electron p_{T} (no ID)", "F")

alignStats(h1)

h8= makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "1", nbins, min, max)
h2 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "1", nbins, min, max)
h2.SetName("electrons_veto")
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kGreen+3)
h2.SetLineWidth(3)
l1.AddEntry("electrons_veto", "Veto ID", "F")

h9= makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "2", nbins, min, max)
h3 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "2", nbins, min, max)
h3.SetName("electrons_loose")
h3.Draw("same")
h3.SetFillColor(0)
h3.SetLineColor(ROOT.kBlue+1)
h3.SetLineWidth(3)
l1.AddEntry("electrons_loose", "Loose ID", "F")

h10 = makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "3", nbins, min, max)
h4 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "3", nbins, min, max)
h4.SetName("electrons_medium")
h4.Draw("same")
h4.SetFillColor(0)
h4.SetLineColor(ROOT.kOrange-2)
h4.SetLineWidth(3)
l1.AddEntry("electrons_medium", "Medium ID", "F")

h11 = makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "4", nbins, min, max)
h5 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "4", nbins, min, max)
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

h12 = makehist(Events, "LepGood_pt", recoSel + "&&" + mvaSel1, nbins, min, max)
h6 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel1, nbins, min, max)
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

h13 = makehist(Events, "LepGood_pt", recoSel + "&&" + mvaSel2, nbins, min, max)
h7 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel2, nbins, min, max)
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
efficiency1.SetLineColor(ROOT.kBlack)
efficiency1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency1.GetPaintedGraph().GetXaxis().SetLimits(min,max)
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
efficiency2.SetLineColor(ROOT.kBlack)
efficiency2.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency2.GetPaintedGraph().GetXaxis().SetLimits(min,max)
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
efficiency3.SetLineColor(ROOT.kBlack)
efficiency3.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency3.GetPaintedGraph().GetXaxis().SetLimits(min,max)
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
efficiency4.SetLineColor(ROOT.kBlack)
efficiency4.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency4.GetPaintedGraph().GetXaxis().SetLimits(min,max)
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
efficiency5.SetLineColor(ROOT.kBlack)
efficiency5.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency5.GetPaintedGraph().GetXaxis().SetLimits(min, max)
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
efficiency6.SetLineColor(ROOT.kBlack)
efficiency6.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency6.GetPaintedGraph().GetXaxis().SetLimits(min,max)
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
c1.SaveAs(savedir + "electronMisId_" + sample + z + ".root")
c1.SaveAs(savedir + "electronMisId_" + sample + z + ".png")
c1.SaveAs(savedir + "electronMisId_" + sample + z + ".pdf")
