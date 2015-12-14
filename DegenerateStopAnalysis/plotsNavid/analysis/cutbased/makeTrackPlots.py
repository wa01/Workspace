from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.cuts import *
#from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2 import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from makeTable import *
from limitCalc import *

from tracks import *


######## Track Validation commands ######
testvalidtrackinfo=False
if testvalidtrackinfo:

  trkJetPt="Jet_pt[track_matchedJetIndex]"
  trkJetEta="Jet_eta[track_matchedJetIndex]"
  trkJetPhi="Jet_phi[track_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(track_eta-%s)**2 )"%(minAngle(trkJetPhi,"track_phi") ,trkJetEta)
  f.Draw("track_matchedJetDr:%s"%dr,"track_matchedJetIndex>0","COLZ")
  f.Draw("ntrack_2p5:Sum$(track_pt > 2.5 && abs(track_dxy)<0.02 && abs(track_dz)<0.5 && abs(track_eta)<2.5 && abs(track_pdgId)!=11 && abs(track_pdgId) != 13 &&(track_matchedJetDr > 0.4 || Jet_pt[track_matchedJetIndex] < 30 ) )")
  
  trkJetPt="Jet_pt[Tracks_matchedJetIndex]"
  trkJetEta="Jet_eta[Tracks_matchedJetIndex]"
  trkJetPhi="Jet_phi[Tracks_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(Tracks_eta-%s)**2 )"%(minAngle(trkJetPhi,"Tracks_phi") ,trkJetEta)
  f.Draw("Tracks_matchedJetDr:%s"%dr,"Tracks_matchedJetIndex>0","COLZ")
  f.Draw("nTracks_2p5:Sum$(Tracks_pt > 2.5 && abs(Tracks_dxy)<0.02 && abs(Tracks_dz)<0.5 && abs(Tracks_eta)<2.5 && abs(Tracks_pdgId)!=11 && abs(Tracks_pdgId) != 13 &&(Tracks_matchedJetDr > 0.4 || Jet_pt[Tracks_matchedJetIndex] < 30 ) )")


nTrk = lambda trkPt, jetPt: "Sum$(track_pt > {trkPt} && abs(track_dxy)<0.02 && abs(track_dz)<0.5 && abs(track_eta)<2.5 && abs(track_pdgId)!=11 && abs(track_pdgId) != 13 &&(track_matchedJetDr > 0.4 || Jet_pt[track_matchedJetIndex] < {jetPt}) )".format(trkPt=2.5, jetPt=50)



  trkJetPt="GenJet_pt[GenTracks_matchedJetIndex]"
  trkJetEta="GenJet_eta[GenTracks_matchedJetIndex]"
  trkJetPhi="GenJet_phi[GenTracks_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(GenTracks_eta-%s)**2 )"%(minAngle(trkJetPhi,"GenTracks_phi") ,trkJetEta)
  f.Draw("GenTracks_matchedJetDr:%s"%dr,"GenTracks_matchedJetIndex>0","COLZ")
  f.Draw("nGenTracks_2p5:Sum$(GenTracks_pt > 2.5 && abs(GenTracks_dxy)<0.02 && abs(GenTracks_dz)<0.5 && abs(GenTracks_eta)<2.5 && abs(GenTracks_pdgId)!=11 && abs(GenTracks_pdgId) != 13 &&(GenTracks_matchedJetDr > 0.4 || Jet_pt[GenTracks_matchedJetIndex] < 30 ) )")


saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/tracks'

trkCutList = [sr1Trk,sr1TrkJ1,sr1TrkJ12,sr1TrkJAll, sr1TrkOpp60JAll , sr1TrkOpp90JAll , sr1TrkOpp60J12, sr1TrkOpp90J12, sr1TrkOpp90J1]

#trkCutList = [sr1TrkOpp60JAll, sr1TrkOpp90JAll]


cutList=[]
pklDir="./pkl/trks/"
for trkCut in trkCutList:
  cutList.append({
              "cutInst":trkCut,
              "pklDir":"./pkl/trks/",
              "name":trkCut.name,
              "cutOpt":"list",
                })



ROOT.gStyle.SetOptStat(0)

#setEventListToChains(samples,['tt','w','s','d'],presel)
if not samples.s.tree.GetEventList():
  setEventListToChains(samples,['w','s'],sr1Loose)


yDict={}
for trkCut in cutList:
  yDict[ trkCut['name'] ] = Yields( samples,['w','s'], trkCut['cutInst'] , cutOpt= trkCut['cutOpt'], tableName='{cut}_tracks',pklOpt=True,pklDir=trkCut['pklDir'] )
  JinjaTexTable(yDict[trkCut['name']],pdfDir=saveDir+"/tables/")




canvas={}

sample = samples.s.tree.Clone()


pickleFiles = glob.glob(pklDir+"/*.pkl")

if len(pickleFiles)==0:
  print "############   WARNING    no pickle files found!  #####"
else:
  print "############ %s pickle files ound: "%len(pickleFiles),
  print pickleFiles

limitDict={}
yields={}

yieldInstPickleFiles = [x for x in pickleFiles if "YieldInstance" in x]
for pickleFile in yieldInstPickleFiles:
  filename = splitext(basename(pickleFile))[0].replace("YieldInstance_","")
  print "############ making a limit card for %s"%filename
  yields[filename]=pickle.load(open(pickleFile,"rb") )
  bins = yields[filename].cutLegend[0][1:]
  limitDict[filename] = getLimit(yields[filename])


nLimits = len(limitDict)
limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
canv2 = ROOT.TCanvas("canv2","canv2")


best = sorted(limitDict,key= lambda x: limitDict[x][1]['0.500'] )
#for i,fname in enumerate(sorted(limitDict),1):
for i,fname in enumerate(best,1):
  limit=limitDict[fname][1]['0.500']
  limitPlot.GetXaxis().SetBinLabel(i,fname)
  limitPlot.SetBinContent(i,limit)

limitPlot.GetYaxis().SetTitle("r")
limitPlot.SetTitle("Median Expected Limits")
limitPlot.Draw()
canv2.SaveAs(saveDir+"/%s_ExpectedLimits.png"%"trackMultip")


bestList= [(x,limitDict[x][1]['0.500']) for x in best]
print bestList

