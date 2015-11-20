from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2 import *
#from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *

from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from tracks import *
#from makeTable import *
#from limitCalc import *
#from dmt import *

ROOT.gStyle.SetOptStat(0);


setEventListToChains(samples,['w','s'],sr1Loose)


getPlots2(samples,plots, sr1Loose , sampleList=[], plotList=[])



saveDir='/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/tracks/eff/'
effPlots={}


if False:
  for p in samples.s.cuts.sr1Loose.keys():
    if not "trk" in p.lower():
      continue
    savePath=saveDir+"/%s.png"%p
    sHist = getattr(samples.s.cuts.sr1Loose,p)
    bHist = getattr(samples.w.cuts.sr1Loose,p)
    effPlots[p] = getEffFomPlot(sHist,bHist,savePath=savePath)
  srtKeys = sorted(effPlots,key = lambda x: effPlots[x]['max']['maxFOM'],reverse=True)
  res = [ (x,effPlots[x]['max']) for x in srtKeys]


rocPlots={}
if False:
  ROOT.gStyle.SetPaintTextFormat("5.2f")
  dOpt = "p"
  first = True

  
  for p in samples.s.cuts.sr1Loose.keys():
    if not "trk" in p.lower():
      continue
    sHist = getattr(samples.s.cuts.sr1Loose,p)
    bHist = getattr(samples.w.cuts.sr1Loose,p)
    
    roc = getROC(sHist,bHist)
    rocPlots[p] = roc['roc'] 
    rocPlots[p].SetMarkerStyle(7)
    rocPlots[p].SetMarkerSize(1)

    if "OppJet" in p:
      print p, ROOT.kViolet
      rocPlots[p].SetMarkerColor(ROOT.kViolet)
    elif "Opp90Jet" in p:
      rocPlots[p].SetMarkerColor(ROOT.kBlue)
    elif "Opp60Jet" in p:
      rocPlots[p].SetMarkerColor(ROOT.kRed)
    else:
      rocPlots[p].SetMarkerColor(ROOT.kBlack)


    if "_1p5" in p:
      rocPlots[p].SetMarkerStyle(24)
    elif p.endswith("_2"):
      rocPlots[p].SetMarkerStyle(25)
    elif p.endswith("_2p5"):
      rocPlots[p].SetMarkerStyle(26)

    if first:
      fom = ROOT.TH2F("FOM","FOM",10,0,1,10,0,1)
      sTot = roc['sTot']
      bTot = roc['bTot']
      for X in range(1,11):
        x=X/10.
        for Y in range(1,11):
          y=(Y-1)/10.
          fom.SetBinContent(X,Y, fomFuncs['AMSSYS'](sTot*x,bTot*(1-y) ))
      fom.Draw("COLZTEXT")
      first = False
    rocPlots[p].Draw(dOpt)
    dOpt="psame"

























