#eleIdEff.py

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

sample = "WJets"
print makeLine()
print "Using", sample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

for f in getChunks(WJetsToLNu)[0]: Events.Add(f['file']) #allSignals[0]

deltaR = "sqrt((genLep_eta - LepGood_eta)^2 + (genLep_phi - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt - LepGood_pt)/genLep_pt)" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

#Bin size 
nbins = 100 #80
min = 0 #GeV
max = 500 # 20 #GeV 

#Zoom
zoom = True
z = ""
if zoom == True:
   nbins = 80
   max = 20
   z = "lowPt/"

#Selection criteria
genSel = "ngenLep == 1 && abs(genLep_pdgId) == 11 && abs(genLep_eta) < 2.5" #nLepGood == 1 biases your efficiency & 5 GeV cut in LepGood
matchSel = "abs(LepGood_pdgId) == 11 && LepGood_mcMatchId != 0 &&" + "Min$(" + deltaR +") &&" + deltaR + "<" + str(deltaRcut)
cutSel = "LepGood_SPRING15_25ns_v1 >="

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Generated selection
h1 = makehist(Events, "genLep_pt", genSel, nbins, min, max) #match gen cuts to LepGood cuts (eta, pt) 
h1.SetName("genEle")
h1.SetTitle("Electron p_{T} for Various IDs (Veto, Loose, Medium, Tight)")
h1.GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
h1.GetXaxis().SetTitleOffset(1.2)
h1.GetYaxis().SetTitleOffset(1.2)
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)

l1 = makeLegend()
l1.AddEntry("genEle", "Generated Electron p_{T}", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

h2 = makehist(Events, "genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "1", nbins, min, max)
h2.SetName("electrons_veto")
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)

l1.AddEntry("electrons_veto", "Electron p_{T} (Veto ID)", "F")
l1.Draw()

#Efficiency Veto
c1.cd(2)
efficiency1 = ROOT.TEfficiency(h2, h1) #(passed, total)
efficiency1.SetTitle("Electron Efficiency for Veto ID ; Generated Electron p_{T} / GeV ; Counts")
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
h1.Draw()

l2 = makeLegend()
l2.AddEntry("genEle", "Generated Electron p_{T}", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

h3 = makehist(Events, "genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "2", nbins, min, max)
h3.SetName("electrons_loose")
h3.Draw("same")
h3.SetFillColor(0)
h3.SetLineColor(ROOT.kAzure+7)
h3.SetLineWidth(4)

l2.AddEntry("electrons_loose", "Electron p_{T} (Loose ID)", "F")
l2.Draw()

#Efficiency Loose
c2.cd(2)
efficiency2 = ROOT.TEfficiency(h3, h1) #(passed, total)
efficiency2.SetTitle("Electron Efficiency for Loose ID ; Generated Electron p_{T} / GeV ; Counts")
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
h1.Draw()

l3 = makeLegend()
l3.AddEntry("genEle", "Generated Electron p_{T}", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

h4 = makehist(Events, "genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "3", nbins, min, max)
h4.SetName("electrons_medium")
h4.Draw("same")
h4.SetFillColor(0)
h4.SetLineColor(ROOT.kAzure+7)
h4.SetLineWidth(4)

l3.AddEntry("electrons_medium", "Electron p_{T} (Medium ID)", "F")
l3.Draw()

#Efficiency Medium
c3.cd(2)
efficiency3 = ROOT.TEfficiency(h4, h1) #(passed, total)
efficiency3.SetTitle("Electron Efficiency for Medium ID ; Generated Electron p_{T} / GeV ; Counts")
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
h1.Draw()

l4 = makeLegend()
l4.AddEntry("genEle", "Generated Electron p_{T}", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

h5 = makehist(Events, "genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "4", nbins, min, max)
h5.SetName("electrons_tight")
h5.Draw("same")
h5.SetFillColor(0)
h5.SetLineColor(ROOT.kAzure+7)
h5.SetLineWidth(4)

l4.AddEntry("electrons_tight", "Electron p_{T} (Tight ID)", "F")
l4.Draw()

c4.cd(2)
efficiency4 = ROOT.TEfficiency(h5, h1) #(passed, total)
efficiency4.SetTitle("Electron Efficiency for Tight ID ; Generated Electron p_{T} / GeV ; Counts")
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

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/efficiency/cut/" + sample + "/" + z #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "electronIDeff_veto.root")
c1.SaveAs(savedir + "electronIDeff_veto.png")
c1.SaveAs(savedir + "electronIDeff_veto.pdf")

c2.SaveAs(savedir + "electronIDeff_loose.root")
c2.SaveAs(savedir + "electronIDeff_loose.png")
c2.SaveAs(savedir + "electronIDeff_loose.pdf")

c3.SaveAs(savedir + "electronIDeff_medium.png")
c3.SaveAs(savedir + "electronIDeff_medium.root")
c3.SaveAs(savedir + "electronIDeff_medium.pdf")

c4.SaveAs(savedir + "electronIDeff_tight.root")
c4.SaveAs(savedir + "electronIDeff_tight.png")
c4.SaveAs(savedir + "electronIDeff_tight.pdf")
