#eleMisEff_combined.py
import ROOT
import os, sys
import math
from array import *
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *

#Input options
inputSample = "signal" # "signal" "WJets" "TTJets"
zoom = True

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
#data_path = "/data/nrad/cmgTuples/RunII/7412pass2/RunIISpring15xminiAODv2"

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
#deltaR = "sqrt((genLep_eta - LepGood_eta)^2 + (genLep_phi - LepGood_phi)^2)"
#deltaRtau = "sqrt((genLepFromTau_eta - LepGood_eta)^2 + (genLepFromTau_phi - LepGood_phi)^2)"

#deltaP = "abs((genLep_pt - LepGood_pt)/genLep_pt)" #pt difference: gen wrt. reco in %

deltaRcut = 0.3
#deltaPcut = 0.5 #in '%'

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

recoSel = "abs(LepGood_pdgId == 11)"
misMatchSel = "LepGood_mcMatchId == 0"
cutSel = "LepGood_SPRING15_25ns_v1 >="

#MVA IDs
WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

#Generated electrons
hists_total = []
hists_passed = []

for i in range(1,7):
   hists_total.append(emptyHistVarBins("misID_total" + str(i), bins))
   hists_passed.append(emptyHistVarBins("misID_passed" + str(i), bins))

Events.Draw(">>eList", "")
elist = ROOT.gDirectory.Get("eList")
nEvents = elist.GetN()

#Event Loop
for i in range(nEvents):
   #if i == 100000: break
   Events.GetEntry(elist.GetEntry(i))

   #Number of generated and reconstructed leptons
   #ngenLep = Events.GetLeaf("ngenLep").GetValue()
   nLep = Events.GetLeaf("nLepGood").GetValue()
   if nLep == 0: continue
   
   #print "nlepgood: ", nLep
   #Looping over generated leptons 
   for ilep in range(int(nLep)):
      lepId = Events.GetLeaf("LepGood_pdgId").GetValue(ilep)   
      lepEta = Events.GetLeaf("LepGood_eta").GetValue(ilep)
      lepPhi = Events.GetLeaf("LepGood_phi").GetValue(ilep)
      lepPt = Events.GetLeaf("LepGood_pt").GetValue(ilep)
      lepMatchId = Events.GetLeaf("LepGood_mcMatchId").GetValue(ilep)
      cutID = Events.GetLeaf("LepGood_SPRING15_25ns_v1").GetValue(ilep)
      mvaID = Events.GetLeaf("LepGood_mvaIdSpring15").GetValue(ilep)
      
      if abs(lepId) != 11 or abs(lepEta) > 2.5: continue #picking out electrons within acceptance (add pt > 5?)
       
      #Histogram filling   
      #MVA ID cut (dependent on electron pt and detector region)
      if lepPt <= ptSplit:
         if lepEta < ebSplit:
            MVA_min1 = WPs['WP90']['EB1_lowPt']
            MVA_min2 = WPs['WP80']['EB1_lowPt']
         elif lepEta >= ebSplit and lepEta < ebeeSplit:
            MVA_min1 = WPs['WP90']['EB2_lowPt']
            MVA_min2 = WPs['WP80']['EB2_lowPt']
         elif lepEta >= ebeeSplit: # < 2.5 (applied already in LepGood)
            MVA_min1 = WPs['WP90']['EE_lowPt']
            MVA_min2 = WPs['WP80']['EE_lowPt']
      elif lepPt > ptSplit:
         if lepEta < ebSplit:
            MVA_min1 = WPs['WP90']['EB1']
            MVA_min2 = WPs['WP80']['EB1']
         elif lepEta >= ebSplit and lepEta < ebeeSplit:
            MVA_min1 = WPs['WP90']['EB2']
            MVA_min2 = WPs['WP80']['EB2']
         elif lepEta >= ebeeSplit: # < 2.5 (applied already in LepGood)
            MVA_min1 = WPs['WP90']['EE']
            MVA_min2 = WPs['WP80']['EE']
      
      #Generated Electron Pt
      if abs(lepId) == 11 and abs(lepEta) < 2.5:
         #Cut ID
         for i in range(1,5):
            if cutID >= i:
               hists_total[i-1].Fill(lepPt)
               if lepMatchId == 0: hists_passed[i-1].Fill(lepPt) 
         
         #MVA ID   
         if mvaID >= MVA_min1:
            hists_total[4].Fill(lepPt)
            if lepMatchId == 0: hists_passed[4].Fill(lepPt)
         if mvaID >= MVA_min2:
            hists_total[5].Fill(lepPt)
            if lepMatchId == 0: hists_passed[5].Fill(lepPt)

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

hists_total[0].SetName("recoEle")
hists_total[0].SetTitle("Fake (Non-Prompt) Electron p_{T} for Various IDs (Veto, Loose, Medium, Tight, MVA)")
hists_total[0].GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
hists_total[0].SetFillColor(ROOT.kBlue-9)
hists_total[0].SetLineColor(ROOT.kBlack)
hists_total[0].SetLineWidth(3)
hists_total[0].Draw()
ROOT.gPad.SetLogy()
ROOT.gPad.Update()
hists_total[0].GetXaxis().SetTitleOffset(1.2)
hists_total[0].GetYaxis().SetTitleOffset(1.2)
alignStats(hists_total[0])

#Veto ID
hists_passed[0].SetName("electrons_veto")
hists_passed[0].SetLineColor(ROOT.kGreen+3)

#Loose ID
hists_passed[1].SetName("electrons_loose")
hists_passed[1].SetLineColor(ROOT.kBlue+1)

#Medium ID
hists_passed[2].SetName("electrons_medium")
hists_passed[2].SetLineColor(ROOT.kOrange-2)

#Tight ID
hists_passed[3].SetName("electrons_tight")
hists_passed[3].SetLineColor(ROOT.kRed+1)

hists_passed[4].SetName("electrons_mva_WP80")
hists_passed[4].SetLineColor(ROOT.kAzure+5)

hists_passed[5].SetName("electrons_mva_WP90")
hists_passed[5].SetLineColor(ROOT.kMagenta+2)

for i in range(0,6): #hists 1-4
   hists_passed[i].SetFillColor(0)
   hists_passed[i].SetLineWidth(3)
   hists_passed[i].Draw("same")


l1 = makeLegend()
l1.AddEntry("recoEle", "Reconstructed Electron p_{T}", "F")
l1.AddEntry("electrons_veto", "Veto ID", "F")
l1.AddEntry("electrons_loose", "Loose ID", "F")
l1.AddEntry("electrons_medium", "Medium ID", "F")
l1.AddEntry("electrons_tight", "Tight ID", "F")
l1.AddEntry("electrons_mva_WP80", "MVA ID (WP80)", "F")
l1.AddEntry("electrons_mva_WP90", "MVA ID (WP90)", "F")
l1.Draw()

#Total Efficiencies
#eff1 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + cutSel + "1"))/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100 #added generated pt cut to match LepGood collection
#eff2 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + cutSel + "2"))/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100
#eff3 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + cutSel + "3"))/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100
#eff4 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + cutSel + "4"))/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100
#eff5 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + mvaSel1))/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100
#eff6 = float(Events.GetEntries(genSel + "&&" + matchSel + "&&" + mvaSel2)/float(Events.GetEntries(genSel + "&&" + "genLep_pt[0] > 5"))*100

#box1 = makeBox()
#box1.AddText("Total Efficiencies:")
#box1.AddText("#bf{Veto ID: }" + str("%0.1f"%eff1) + "%")
#box1.AddText("#bf{Loose ID: }" + str("%0.1f"%eff2) + "%")
#box1.AddText("#bf{Medium ID: }" + str("%0.1f"%eff3) + "%")
#box1.AddText("#bf{Tight ID: }" + str("%0.1f"%eff4) + "%")
#box1.AddText("#bf{MVA ID (WP90): }" + str("%0.1f"%eff5) + "%")
#box1.AddText("#bf{MVA ID (WP80): }" + str("%0.1f"%eff6) + "%")
#box1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)
l2 = makeLegend()

effs = []

#Efficiency Veto
for i in range (0, 6):
   effs.append(ROOT.TEfficiency(hists_passed[i], hists_total[i])) #(passed, total)
   effs[i].SetMarkerStyle(33)
   effs[i].SetMarkerSize(1.5)
   effs[i].SetLineWidth(2)

effs[0].SetTitle("Electron Mismatch Efficiency for Various IDs ; Reconstructed Electron p_{T} / GeV ; Counts")
effs[0].SetName("eff1")
effs[0].SetMarkerColor(ROOT.kGreen+3)
effs[0].SetLineColor(ROOT.kGreen+3)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
effs[0].Draw("AP") 
ROOT.gPad.Update()
effs[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#effs[0].GetPaintedGraph().GetXaxis().SetNdivisions(510, 1)
effs[0].GetPaintedGraph().GetXaxis().CenterTitle()
effs[0].GetPaintedGraph().GetYaxis().CenterTitle()

#Efficiency Loose
effs[1].SetName("eff2")
effs[1].SetMarkerColor(ROOT.kBlue+1)
effs[1].SetLineColor(ROOT.kBlue+1)
effs[1].Draw("sameP") 

#Efficiency Medium
effs[2].SetName("eff3")
effs[2].SetMarkerColor(ROOT.kOrange-2)
effs[2].SetLineColor(ROOT.kOrange-2)
effs[2].Draw("sameP") 

#Efficiency Tight
effs[3].SetName("eff4")
effs[3].SetMarkerColor(ROOT.kRed+1)
effs[3].SetLineColor(ROOT.kRed+1)
effs[3].Draw("sameP") 


#Efficiency WP80
effs[4].SetName("eff6")
effs[4].SetMarkerColor(ROOT.kAzure+5)
effs[4].SetMarkerStyle(22)
effs[4].SetMarkerSize(1)
effs[4].Draw("sameP")
effs[4].SetLineColor(ROOT.kAzure+5)

#Efficiency WP90
effs[5].SetName("eff5")
effs[5].SetMarkerColor(ROOT.kMagenta+2)
effs[5].SetMarkerStyle(22)
effs[5].SetMarkerSize(1)
effs[5].Draw("sameP")
effs[5].SetLineColor(ROOT.kMagenta+2)

ROOT.gPad.Update()

l2.AddEntry("eff1", "Veto ID", "P")
l2.AddEntry("eff2", "Loose ID", "P")
l2.AddEntry("eff3", "Medium ID", "P")
l2.AddEntry("eff4", "Tight ID", "P")
l2.AddEntry("eff5", "MVA ID (WP80)", "P")
l2.AddEntry("eff6", "MVA ID (WP90)", "P")
l2.Draw()
#box1.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/combined/misId/loop/" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "electronMisId_loop_" + inputSample + z + ".root")
c1.SaveAs(savedir + "electronMisId_loop_" + inputSample + z + ".png")
c1.SaveAs(savedir + "electronMisId_loop_" + inputSample + z + ".pdf")
