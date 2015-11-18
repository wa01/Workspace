#eleIdEff.py

import os, sys
import ROOT
import math

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

def emptyhist(varname, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F(varname, varname + " Histogram", nbins, min, max)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetYaxis().CenterTitle()
   return hist

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

sample = "WJets" #"Signal"
print makeLine()
print "Using", sample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

for f in getChunks(WJetsToLNu)[0]: Events.Add(f['file'])

#deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt[0] - LepGood_pt[0])/genLep_pt[0])" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
deltaPcut = 0.5 #in '%'

#Bin size 
nbins = 100
min = 0 #GeV
max = 500 #GeV

# There are 6 categories in this MVA. They have to be configured in this strict order
# (cuts and weight files order):
#   0   EB1 (eta<0.8)  pt 5-10 GeV
#   1   EB2 (eta>=0.8) pt 5-10 GeV
#   2   EE             pt 5-10 GeV
#   3   EB1 (eta<0.8)  pt 10-inf GeV
#   4   EB2 (eta>=0.8) pt 10-inf GeV
#   5   EE             pt 10-inf GeV

WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

WP = "WP90"

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

Events.Draw(">>eList", "")
elist = ROOT.gDirectory.Get("eList")
nEvents = elist.GetN()

#deltaR = "math.sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt[0] - LepGood_pt[0])/genLep_pt[0])" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

#Empty histograms
h1 = emptyhist("genEle") 
h2 = emptyhist("MVA_" + WP)

#Event Loop
for i in range(nEvents):
   #if i == 1000: break
   Events.GetEntry(elist.GetEntry(i))

   #Generated Variables
   ngenLep = Events.GetLeaf("ngenLep").GetValue()
   if ngenLep != 1: continue 
   
   genLepId = Events.GetLeaf("genLep_pdgId").GetValue()
   if abs(genLepId) != 11: continue
   
   genLepPt = Events.GetLeaf("genLep_pt").GetValue()
   genLepEta = Events.GetLeaf("genLep_eta").GetValue()
   genLepPhi = Events.GetLeaf("genLep_phi").GetValue()
   
   #Reconstructed Variables 
   nLep = Events.GetLeaf("nLepGood").GetValue()
   
   deltaRmin = 100.0;
   
   for ilep in range(int(nLep)):
      lepId = Events.GetLeaf("LepGood_pdgId").GetValue(ilep)
      if abs(lepId) != 11: continue
      
      lepEta = Events.GetLeaf("LepGood_eta").GetValue(ilep)
      lepPhi = Events.GetLeaf("LepGood_phi").GetValue(ilep)
      
      deltaR = math.sqrt((genLepEta - lepEta)**2 + (genLepPhi - lepPhi)**2)
      if deltaR < deltaRmin:
         deltaRmin = deltaR
         lepPt = Events.GetLeaf("LepGood_pt").GetValue(ilep)
         lepMatchId = Events.GetLeaf("LepGood_mcMatchId").GetValue(ilep)
         mvaEleId = Events.GetLeaf("LepGood_mvaIdSpring15").GetValue(ilep)
   
   #Histogram filling   
   #Generated Electron Pt
   if ngenLep == 1 and abs(genLepId) == 11 and abs(genLepEta) < 2.5:
      h1.Fill(genLepPt)
   
      #MVA Id (dependent on electron pt and detector region)
      if lepPt <= ptSplit:
         if lepEta < ebSplit:
            MVA_min = WPs[WP]['EB1_lowPt'] 
         elif lepEta >= ebSplit and lepEta < ebeeSplit:
            MVA_min = WPs[WP]['EB2_lowPt']
         elif lepEta >= ebeeSplit: # < 2.5 (applied already in LepGood)
            MVA_min = WPs[WP]['EE_lowPt']
      
      elif lepPt > ptSplit:
         if lepEta < ebSplit:
            MVA_min = WPs[WP]['EB1'] 
         elif lepEta >= ebSplit and lepEta < ebeeSplit:
            MVA_min = WPs[WP]['EB2']
         elif lepEta >= ebeeSplit: # < 2.5 (applied already in LepGood)
            MVA_min = WPs[WP]['EE']
      
      if lepMatchId != 0 and deltaRmin < deltaRcut and mvaEleId >= MVA_min:
         h2.Fill(genLepPt)

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)
#h1.SetName("genEle")
h1.SetTitle("Electron p_{T} for MVA ID (" + WP + ")")
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

h2.SetName("electrons_mva")
h2.Draw("same")
h2.SetFillColor(0)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)

l1.AddEntry("electrons_mva", "Electrons (MVA ID " + WP + ")", "F")
l1.Draw()

#Efficiency Veto
c1.cd(2)
efficiency1 = ROOT.TEfficiency(h2, h1) #(passed, total)
efficiency1.SetTitle("Electron Efficiency Plot for MVA ID (" + WP + "); Electron p_{T} / GeV ; Counts")
efficiency1.SetMarkerColor(ROOT.kBlue)
efficiency1.SetMarkerStyle(33)
efficiency1.SetMarkerSize(3)
efficiency1.Draw("AP") 
efficiency1.SetLineColor(ROOT.kBlack)
efficiency1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
efficiency1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
efficiency1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
efficiency1.GetPaintedGraph().GetXaxis().CenterTitle()
efficiency1.GetPaintedGraph().GetYaxis().CenterTitle()

c1.Modified()
c1.Update()

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/efficiency/mva2/" + sample #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "/electronIDeff_mva_" + WP + ".root")
c1.SaveAs(savedir + "/electronIDeff_mva_" + WP + ".png")
c1.SaveAs(savedir + "/electronIDeff_mva_" + WP + ".pdf")
