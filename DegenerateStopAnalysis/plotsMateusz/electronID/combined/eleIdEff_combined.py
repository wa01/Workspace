#eleIdEff_combined.py
import ROOT
import os, sys
from array import *
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *

#Input options
inputSample = "WJets" # "signal" "WJets" "TTJets"
zoom = False

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

bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax,10)) #Variable bin size

#Zoom
z = ""
if zoom == True:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax,2))
   z = "_lowPt"

#Selection criteria
deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
#deltaP = "abs((genLep_pt[0] - LepGood_pt[0])/genLep_pt[0])" #pt difference: gen wrt. reco in %

deltaRcut = 0.1
#deltaPcut = 0.5 #in '%'

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
#genSel = "ngenLep == 1 && abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < 2.5" #nLepGood == 1 biases your efficiency & 5 GeV cut in LepGood
genSel = "Sum$(abs(genLep_pdgId == 11 && abs(genLep_eta) < 2.5)) == 1" # == ngenLep
matchSel = "Min$(" + deltaR +"*(abs(LepGood_pdgId) == 11 && LepGood_mcMatchId != 0)) <" + str(deltaRcut) + "&& Min$(" + deltaR +"*(abs(LepGood_pdgId) == 11 && LepGood_mcMatchId != 0)) != 0"
cutSel = "LepGood_SPRING15_25ns_v1 >="

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Generated electrons
hists = []

#hist1 = ROOT.TH1F("hist", "Histogram", len(xbins)-1, xbins)
#Events.Draw("genLep_pt[0]" + ">>hist", genSel)
#hists.append(hist1)

hists.append(makeHistVarBins(Events, "genLep_pt[0]", genSel, bins)) #match gen cuts to LepGood cuts (eta, pt) 
hists[0].SetName("genEle")
hists[0].SetTitle("Electron p_{T} for Various IDs")
hists[0].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
hists[0].GetXaxis().SetTitleOffset(1.2)
hists[0].GetYaxis().SetTitleOffset(1.2)
hists[0].Draw()
hists[0].SetFillColor(ROOT.kBlue-9)
hists[0].SetLineColor(ROOT.kBlack)
hists[0].SetLineWidth(3)

l1 = makeLegend()
l1.AddEntry("genEle", "Generated Electron p_{T}", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(hists[0])

for i in range(1,5): #hists 1-4
   hists.append(makeHistVarBins(Events, "genLep_pt[0]", genSel + "&&" + matchSel + "&&" + cutSel + str(i), bins))
   hists[i].SetFillColor(0)
   hists[i].SetLineWidth(3)
   hists[i].Draw("same")

#Veto ID
hists[1].SetName("electrons_veto")
hists[1].SetLineColor(ROOT.kGreen+3)
l1.AddEntry("electrons_veto", "Veto ID", "F")

#Loose ID
hists[2].SetName("electrons_loose")
hists[2].SetLineColor(ROOT.kBlue+1)
l1.AddEntry("electrons_loose", "Loose ID", "F")

#Medium ID
hists[3].SetName("electrons_medium")
hists[3].SetLineColor(ROOT.kOrange-2)
l1.AddEntry("electrons_medium", "Medium ID", "F")

#Tight ID
hists[4].SetName("electrons_tight")
hists[4].SetLineColor(ROOT.kRed+1)
l1.AddEntry("electrons_tight", "Tight ID", "F")

ROOT.gPad.Update()

#MVA IDs
WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

for WP in WPs:
   mvaSel = "(\
   (LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
   (LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
   (LepGood_pt <=" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& LepGood_eta <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebSplit) + "&& LepGood_eta <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& LepGood_eta >=" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))"
   
   hists.append(makeHistVarBins(Events, "genLep_pt[0]", genSel + "&&" + matchSel + "&&" + mvaSel, bins))
   
hists[5].SetName("electrons_mva_wp90")
hists[5].Draw("same")
hists[5].SetFillColor(0)
hists[5].SetLineColor(ROOT.kMagenta+2)
hists[5].SetLineWidth(3)
l1.AddEntry("electrons_mva_wp90", "MVA ID (WP90)", "F")

hists[6].SetName("electrons_mva_wp80")
hists[6].Draw("same")
hists[6].SetFillColor(0)
hists[6].SetLineColor(ROOT.kAzure+2)
hists[6].SetLineWidth(3)
l1.AddEntry("electrons_mva_wp80", "MVA ID (WP80)", "F")

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
for i in range (1, 7):
   effs.append(ROOT.TEfficiency(hists[i], hists[0])) #(passed, total)
   effs[i-1].SetMarkerStyle(33)
   effs[i-1].SetMarkerSize(1.5)
   effs[i-1].SetLineWidth(2)

effs[0].SetTitle("Electron Efficiencies for Various IDs (Veto, Loose, Medium, Tight, MVA) ; Generated Electron p_{T} / GeV ; Counts")
effs[0].SetName("eff1")
effs[0].SetMarkerColor(ROOT.kGreen+3)
effs[0].SetLineColor(ROOT.kGreen+3)
effs[0].Draw("AP") 
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
effs[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#effs[0].GetPaintedGraph().GetXaxis().SetNdivisions(510, 1)
effs[0].GetPaintedGraph().GetXaxis().CenterTitle()
effs[0].GetPaintedGraph().GetYaxis().CenterTitle()
l2.AddEntry("eff1", "Veto ID", "P")

#Efficiency Loose
effs[1].SetName("eff2")
effs[1].SetMarkerColor(ROOT.kBlue+1)
effs[1].SetLineColor(ROOT.kBlue+1)
effs[1].Draw("sameP") 
ROOT.gPad.Update()
l2.AddEntry("eff2", "Loose ID", "P")

#Efficiency Medium
effs[2].SetName("eff3")
effs[2].SetMarkerColor(ROOT.kOrange-2)
effs[2].SetLineColor(ROOT.kOrange-2)
effs[2].Draw("sameP") 
ROOT.gPad.Update()
l2.AddEntry("eff3", "Medium ID", "P")

#Efficiency Tight
effs[3].SetName("eff4")
effs[3].SetMarkerColor(ROOT.kRed+1)
effs[3].SetLineColor(ROOT.kRed+1)
effs[3].Draw("sameP") 
ROOT.gPad.Update()
l2.AddEntry("eff4", "Tight ID", "P")

#Efficiency WP90
effs[4].SetName("eff5")
effs[4].SetMarkerColor(ROOT.kMagenta+2)
effs[4].SetMarkerStyle(22)
effs[4].SetMarkerSize(1)
effs[4].Draw("sameP")
effs[4].SetLineColor(ROOT.kMagenta+2)
ROOT.gPad.Update()
l2.AddEntry("eff5", "MVA ID (WP90)", "P")

#Efficiency WP80
effs[5].SetName("eff6")
effs[5].SetMarkerColor(ROOT.kAzure+5)
effs[5].SetMarkerStyle(22)
effs[5].SetMarkerSize(1)
effs[5].Draw("sameP")
effs[5].SetLineColor(ROOT.kAzure+5)
ROOT.gPad.Update()
l2.AddEntry("eff6", "MVA ID (WP80)", "P")

l2.Draw()
#box1.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/combined/efficiency/" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency

if not os.path.exists(savedir):
   os.makedirs(savedir)

#Save to Web
c1.SaveAs(savedir + "electronIDeff_" + inputSample + z + ".root")
c1.SaveAs(savedir + "electronIDeff_" + inputSample + z + ".png")
c1.SaveAs(savedir + "electronIDeff_" + inputSample + z + ".pdf")
