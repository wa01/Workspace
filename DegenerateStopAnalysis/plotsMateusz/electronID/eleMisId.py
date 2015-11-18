#eleMisId.py

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
   hist.SetLineWidth(4)
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
   #hist.SetLineWidth(4)
   #ROOT.gPad.Update()

#Selection function
def select(varname, cut, option): #option = {>, =, <}
  if option == ">" or options == "=" or option == "<": 
      sel = "abs(" + varname + option + str(cut) + ")"
  return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.70,0.75,0.85)
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

sample = "signal" #"TTJets" #"signal" #"WJets"
print makeLine()
print "Using", sample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

for f in getChunks(allSignals[0])[0]: Events.Add(f['file']) #allSignals[0] WJetsToLNu TTJets_LO

deltaR = "sqrt((genLep_eta - LepGood_eta)^2 + (genLep_phi - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt - LepGood_pt)/genLep_pt)" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

#Bin size 
nbins = 100 #80
min = 0 #GeV
max = 150 # 20 #GeV 

#Zoom
zoom = False
z = ""
if zoom == True:
   nbins = 80
   max = 20
   z = "lowPt/"

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
h1.SetTitle("Fake Electron p_{T} for Veto ID")
h1.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h1.GetXaxis().SetTitleOffset(1.2)
h1.GetYaxis().SetTitleOffset(1.2)
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)

l1 = makeLegend()
l1.AddEntry("genEle", "Electron p_{T} (Veto ID)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

h2 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "1", nbins, min, max)
h2.SetName("electrons_veto")
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)

l1.AddEntry("electrons_veto", "Fake Electron p_{T} (Veto ID)", "F")
l1.Draw()

#Mismatch Efficiency Veto
c1.cd(2)
efficiency1 = ROOT.TEfficiency(h2, h1) #(passed, total)
efficiency1.SetTitle("Electron Mismatch Efficiency for Veto ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency1.SetMarkerColor(ROOT.kBlue)
efficiency1.SetMarkerStyle(33)
efficiency1.SetMarkerSize(3)
efficiency1.Draw("AP") 
efficiency1.SetLineColor(ROOT.kBlack)
efficiency1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency1.GetPaintedGraph().GetXaxis().SetLimits(min,max)
#efficiency1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency1.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency1.GetPaintedGraph().GetYaxis().CenterTitle()

c1.Modified()
c1.Update()

#################################################################################Canvas 2#############################################################################################
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

c2.cd(1)
h8 = makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "2", nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h8.SetName("genEle")
h8.SetTitle("Fake Electron p_{T} for Loose ID")
h8.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h8.GetXaxis().SetTitleOffset(1.2)
h8.GetYaxis().SetTitleOffset(1.2)
h8.Draw()
h8.SetFillColor(ROOT.kRed+1)
h8.SetLineColor(ROOT.kBlack)
h8.SetLineWidth(4)

l2 = makeLegend()
l2.AddEntry("genEle", "Electron p_{T} (Loose ID)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

h3 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "2", nbins, min, max)
h3.SetName("electrons_loose")
h3.Draw("same")
h3.SetFillColor(0)
h3.SetLineColor(ROOT.kAzure+7)
h3.SetLineWidth(4)

l2.AddEntry("electrons_loose", "Fake Electron p_{T} (Loose ID)", "F")
l2.Draw()

#Mismatch Efficiency Loose
c2.cd(2)
efficiency2 = ROOT.TEfficiency(h3, h8) #(passed, total)
efficiency2.SetTitle("Electron Mismatch Efficiency for Loose ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency2.SetMarkerColor(ROOT.kBlue)
efficiency2.SetMarkerStyle(33)
efficiency2.SetMarkerSize(3)
efficiency2.Draw("AP") 
efficiency2.SetLineColor(ROOT.kBlack)
efficiency2.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency2.GetPaintedGraph().GetXaxis().SetLimits(min,max)
#efficiency2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency2.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency2.GetPaintedGraph().GetYaxis().CenterTitle()

c2.Modified()
c2.Update()

#################################################################################Canvas 3#############################################################################################

c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
c3.Divide(1,2)

c3.cd(1)
h9 = makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "3", nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h9.SetName("genEle")
h9.SetTitle("Fake Electron p_{T} for Medium ID")
h9.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h9.GetXaxis().SetTitleOffset(1.2)
h9.GetYaxis().SetTitleOffset(1.2)
h9.Draw()
h9.SetFillColor(ROOT.kRed+1)
h9.SetLineColor(ROOT.kBlack)
h9.SetLineWidth(4)

l3 = makeLegend()
l3.AddEntry("genEle", "Electron p_{T} (Medium ID)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

h4 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "3", nbins, min, max)
h4.SetName("electrons_medium")
h4.Draw("same")
h4.SetFillColor(0)
h4.SetLineColor(ROOT.kAzure+7)
h4.SetLineWidth(4)

l3.AddEntry("electrons_medium", "Fake Electron p_{T} (Medium ID)", "F")
l3.Draw()

#Mismatch Efficiency Medium
c3.cd(2)
efficiency3 = ROOT.TEfficiency(h4, h9) #(passed, total)
efficiency3.SetTitle("Electron Mismatch Efficiency for Medium ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency3.SetMarkerColor(ROOT.kBlue)
efficiency3.SetMarkerStyle(33)
efficiency3.SetMarkerSize(3)
efficiency3.Draw("AP") 
efficiency3.SetLineColor(ROOT.kBlack)
efficiency3.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency3.GetPaintedGraph().GetXaxis().SetLimits(min,max)
#efficiency3.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency3.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency3.GetPaintedGraph().GetYaxis().CenterTitle()

c3.Modified()
c3.Update()

#################################################################################Canvas 4#############################################################################################

c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
c4.Divide(1,2)

c4.cd(1)
h10 = makehist(Events, "LepGood_pt", recoSel + "&&" + cutSel + "4", nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h10.SetName("genEle")
h10.SetTitle("Fake Electron p_{T} for Tight ID")
h10.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h10.GetXaxis().SetTitleOffset(1.2)
h10.GetYaxis().SetTitleOffset(1.2)
h10.Draw()
h10.SetFillColor(ROOT.kRed+1)
h10.SetLineColor(ROOT.kBlack)
h10.SetLineWidth(4)

l4 = makeLegend()
l4.AddEntry("genEle", "Electron p_{T} (Tight ID)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

h5 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + cutSel + "4", nbins, min, max)
h5.SetName("electrons_tight")
h5.Draw("same")
h5.SetFillColor(0)
h5.SetLineColor(ROOT.kAzure+7)
h5.SetLineWidth(4)

l4.AddEntry("electrons_tight", "Fake Electron p_{T} (Tight ID)", "F")
l4.Draw()

#Mismatch Effciency Tight
c4.cd(2)
efficiency4 = ROOT.TEfficiency(h5, h10) #(passed, total)
efficiency4.SetTitle("Electron Mismatch Efficiency for Tight ID ; Reconstructed Electron p_{T} / GeV ; Counts")
efficiency4.SetMarkerColor(ROOT.kBlue)
efficiency4.SetMarkerStyle(33)
efficiency4.SetMarkerSize(3)
efficiency4.Draw("AP") 
efficiency4.SetLineColor(ROOT.kBlack)
efficiency4.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency4.GetPaintedGraph().GetXaxis().SetLimits(min,max)
#efficiency4.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency4.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency4.GetPaintedGraph().GetYaxis().CenterTitle()

c4.Modified()
c4.Update()

##################################################################################Canvas 5#############################################################################################
WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

c5 = ROOT.TCanvas("c5", "Canvas 5", 1800, 1500)
c5.Divide(1,2)
c5.cd(1)

WP = "WP90"

mvaSel1 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" # < 2.5 (applied already in LepGood)

h10 = makehist(Events, "LepGood_pt", recoSel + "&&" + mvaSel1, nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h10.SetName("genEle")
h10.SetTitle("Fake Electron p_{T} for Tight ID")
h10.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h10.GetXaxis().SetTitleOffset(1.2)
h10.GetYaxis().SetTitleOffset(1.2)
h10.Draw()
h10.SetFillColor(ROOT.kRed+1)
h10.SetLineColor(ROOT.kBlack)
h10.SetLineWidth(4)

l5 = makeLegend()
l5.AddEntry("genEle", "Electron p_{T} (MVA ID WP90)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()


h6 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel1, nbins, min, max)
h6.SetName("electrons_mva_wp90")
h6.Draw("same")
h6.SetFillColor(0)
h6.SetLineColor(ROOT.kAzure+7)
h6.SetLineWidth(4)

l5.AddEntry("electrons_mva_wp90", "Fake Electron p_{T} (MVA ID " + WP + ")", "F")
l5.Draw()

c5.cd(2)
efficiency5 = ROOT.TEfficiency(h6, h10) #(passed, total)
efficiency5.SetTitle("Electron Mismatch Efficiency Plot for MVA ID (" + WP + "); Reconstructed Electron p_{T} / GeV ; Counts")
efficiency5.SetMarkerColor(ROOT.kBlue)
efficiency5.SetMarkerStyle(33)
efficiency5.SetMarkerSize(3)
efficiency5.Draw("AP")
efficiency5.SetLineColor(ROOT.kBlack)
efficiency5.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency5.GetPaintedGraph().GetXaxis().SetLimits(min, max)
#efficiency5.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency5.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency5.GetPaintedGraph().GetYaxis().CenterTitle()

c5.Modified()
c5.Update()

#################################################################################Canvas 6#############################################################################################
c6 = ROOT.TCanvas("c6", "Canvas 6", 1800, 1500)
c6.Divide(1,2)
c6.cd(1)

WP = "WP80"

mvaSel2 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" # < 2.5 (applied already in LepGood)

h11 = makehist(Events, "LepGood_pt", recoSel + "&&" + mvaSel2, nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h11.SetName("genEle")
h11.SetTitle("Fake Electron p_{T} for MVA ID (WP80)")
h11.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
h11.GetXaxis().SetTitleOffset(1.2)
h11.GetYaxis().SetTitleOffset(1.2)
h11.Draw()
h11.SetFillColor(ROOT.kRed+1)
h11.SetLineColor(ROOT.kBlack)
h11.SetLineWidth(4)

l6 = makeLegend()
l6.AddEntry("genEle", "Electron p_{T} (MVA ID WP80)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

h7 = makehist(Events, "LepGood_pt", recoSel + "&&" + misMatchSel + "&&" + mvaSel2, nbins, min, max)
h7.SetName("electrons_mva_wp80")
h7.Draw("same")
h7.SetFillColor(0)
h7.SetLineColor(ROOT.kAzure+7)
h7.SetLineWidth(4)

l6.AddEntry("electrons_mva_wp80", "Fake Electron p_{T} (MVA ID " + WP + ")", "F")
l6.Draw()

c6.cd(2)
efficiency6 = ROOT.TEfficiency(h7, h11) #(passed, total)
efficiency6.SetTitle("Electron Mismatch Efficiency Plot for MVA ID (" + WP + "); Reconstructed Electron p_{T} / GeV ; Counts")
efficiency6.SetMarkerColor(ROOT.kBlue)
efficiency6.SetMarkerStyle(33)
efficiency6.SetMarkerSize(3)
efficiency6.Draw("AP")
efficiency6.SetLineColor(ROOT.kBlack)
efficiency6.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency6.GetPaintedGraph().GetXaxis().SetLimits(min,max)
#efficiency6.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency6.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency6.GetPaintedGraph().GetYaxis().CenterTitle()

c6.Modified()
c6.Update()

#Write to file
savedir1 = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/misId/cut/" + sample + "/" + z #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
savedir2 = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/misId/mva/" + sample + "/" + z #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir1):
   os.makedirs(savedir1)

if not os.path.exists(savedir2):
   os.makedirs(savedir2)

#Save to Web
c1.SaveAs(savedir1 + "electronMisId_veto.root")
c1.SaveAs(savedir1 + "electronMisId_veto.png")
c1.SaveAs(savedir1 + "electronMisId_veto.pdf")

c2.SaveAs(savedir1 + "electronMisId_loose.root")
c2.SaveAs(savedir1 + "electronMisId_loose.png")
c2.SaveAs(savedir1 + "electronMisId_loose.pdf")

c3.SaveAs(savedir1 + "electronMisId_medium.png")
c3.SaveAs(savedir1 + "electronMisId_medium.root")
c3.SaveAs(savedir1 + "electronMisId_medium.pdf")

c4.SaveAs(savedir1 + "electronMisId_tight.root")
c4.SaveAs(savedir1 + "electronMisId_tight.png")
c4.SaveAs(savedir1 + "electronMisId_tight.pdf")

c5.SaveAs(savedir2 + "electronMisId_MVA_WP90.root")
c5.SaveAs(savedir2 + "electronMisId_MVA_WP90.png")
c5.SaveAs(savedir2 + "electronMisId_MVA_WP90.pdf")

c6.SaveAs(savedir2 + "electronMisId_MVA_WP80.root")
c6.SaveAs(savedir2 + "electronMisId_MVA_WP80.png")
c6.SaveAs(savedir2 + "electronMisId_MVA_WP80.pdf")
