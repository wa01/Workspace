#ratioPt_combined.py

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
   hist.SetFillColor(ROOT.kGreen+3)
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

sample = "TTJets" #"signal" #"WJets" 
print makeLine()
print "Using", sample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

for f in getChunks(TTJets_LO)[0]: Events.Add(f['file']) #allSignals[0] #WJetsToLNu

#Bin size 
nbins = 100
min = 0 
max = 10

#Selection criteria
deltaR = "sqrt((genLep_eta - LepGood_eta)^2 + (genLep_phi - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt - LepGood_pt)/genLep_pt)" #pt difference: gen wrt. reco in %

#deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

genSel = "ngenLep == 1 && abs(genLep_pdgId) == 11 && abs(genLep_eta) < 2.5" #nLepGood == 1 biases your efficiency
matchSel = "abs(LepGood_pdgId) == 11 && LepGood_mcMatchId != 0 &&" + "Min$(" + deltaR +")" 
cutSel = "LepGood_SPRING15_25ns_v1 >="


#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)

h1 = makehist(Events, "LepGood_pt/genLep_pt", genSel, nbins, min, max) 
h1.SetName("ratioPt_0")
h1.SetTitle("Ratio of Reconstructed and Generated Electron p_{T}")
h1.GetXaxis().SetTitle("recoPt/genPt")
h1.GetXaxis().SetTitleOffset(1.2)
h1.GetYaxis().SetTitleOffset(1.2)
h1.Draw()
h1.SetFillColor(ROOT.kBlue-9)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(3)

l1 = makeLegend()
l1.AddEntry("ratioPt_0", "recoPt/genPt (no ID)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

#Veto ID
h2 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "1", nbins, min, max) 
h2.SetName("ratioPt_veto")
h2.GetXaxis().SetTitle("recoPt/genPt")
h2.GetXaxis().SetTitleOffset(1.2)
h2.GetYaxis().SetTitleOffset(1.2)
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kGreen+3)
h2.SetLineWidth(3)
l1.AddEntry("ratioPt_veto", "Veto ID", "F")

#Loose ID
h3 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "2", nbins, min, max) 
h3.SetName("ratioPt_loose")
h3.GetXaxis().SetTitle("recoPt/genPt")
h3.GetXaxis().SetTitleOffset(1.2)
h3.GetYaxis().SetTitleOffset(1.2)
h3.Draw("same")
h3.SetFillColor(0)
h3.SetLineColor(ROOT.kBlue+1)
h3.SetLineWidth(3)
l1.AddEntry("ratioPt_loose", "Loose ID", "F")

#Medium ID
h4 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "3", nbins, min, max) 
h4.SetName("ratioPt_medium")
h4.GetXaxis().SetTitle("recoPt/genPt")
h4.GetXaxis().SetTitleOffset(1.2)
h4.GetYaxis().SetTitleOffset(1.2)
h4.Draw("same")
h4.SetFillColor(0)
h4.SetLineColor(ROOT.kOrange-2)
h4.SetLineWidth(3)
l1.AddEntry("ratioPt_medium", "Medium ID", "F")

#Tight ID
h5 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + cutSel + "4", nbins, min, max)
h5.SetName("ratioPt_tight")
h5.GetXaxis().SetTitle("recoPt/genPt")
h5.GetXaxis().SetTitleOffset(1.2)
h5.GetYaxis().SetTitleOffset(1.2)
h5.Draw("same")
h5.SetFillColor(0)
h5.SetLineColor(ROOT.kRed+1)
h5.SetLineWidth(3)
l1.AddEntry("ratioPt_tight", "Tight ID", "F")

#MVA IDs
WP = "WP90"

mvaSel1 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" 

h6 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + mvaSel1, nbins, min, max)
h6.SetName("ratioPt_wp90")
h6.GetXaxis().SetTitle("recoPt/genPt")
h6.GetXaxis().SetTitleOffset(1.2)
h6.GetYaxis().SetTitleOffset(1.2)
h6.Draw("same")
h6.SetFillColor(0)
h6.SetLineColor(ROOT.kMagenta+2)
h6.SetLineWidth(3)
l1.AddEntry("ratioPt_wp90", "MVA ID (" + WP + ")", "F")

WP = "WP80"

mvaSel2 = "(\
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
(LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
(LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))" 

h7 = makehist(Events, "LepGood_pt/genLep_pt", genSel + "&&" + matchSel + "&&" + mvaSel2, nbins, min, max)
h7.SetName("ratioPt_wp80")
h7.GetXaxis().SetTitle("recoPt/genPt")
h7.GetXaxis().SetTitleOffset(1.2)
h7.GetYaxis().SetTitleOffset(1.2)
h7.Draw("same")
h7.SetFillColor(0)
h7.SetLineColor(ROOT.kAzure+5)
h7.SetLineWidth(3)
l1.AddEntry("ratioPt_wp80", "MVA ID (" + WP + ")", "F")

l1.Draw()

c1.Modified()
c1.Update()

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/combined/ratioPt/" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "electronID_ratioPt_" + sample + ".root")
c1.SaveAs(savedir + "electronID_ratioPt_" + sample + ".png")
c1.SaveAs(savedir + "electronID_ratioPt_" + sample + ".pdf")
