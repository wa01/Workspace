import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain


from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.cuts import *
#from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2 import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *

#from Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns_fromArtur import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *

import math


saveDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/DataPlots/1stIter"

cmsbase = os.getenv("CMSSW_BASE")
print "cmsbase", cmsbase
ROOT.gROOT.LoadMacro(cmsbase+"/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

#lumi =1260 ##fb
MCScale = 0.81 ## 0.8
#MCScale = 6.955
#MCLumi = 10000




def setPadMargins(pad,t=None,b=None,l=None,r=None):
  if t: pad.SetTopMargin(t)
  if b: pad.SetBottomMargin(b)
  if l: pad.SetLeftMargin(l)
  if r: pad.SetRightMargin(r)

#def makePlot(samples,plots,plot,cut):
#def drawDataPlot(sigHists,bkgHists,dataHist,name="Name"):
#def drawDataPlot(sigHists,bkgHists,dataHist,name="Name"):
def drawData(title,data,bkgs=[],sigs=[],MCScale=1):
  ''' bkgHists = [ {'name':"WJets", 'hist':ROOT.TH1F , "name":"WJets", "color":color } , 
                   {'name':"TTJets", .....  }
                  ]
      same with sigHists

    ''' 


  #sigHists=[samples.s.plots.LepPt];bkgHists=[samples.tt.plots.LepPt, samples.w.plots.LepPt]; dataHist=samples.d.plots.LepPt;name="NNAMEE"
  

 


  #### Preparing Stacks
  bkgList  = [samp['name'] for samp in bkgs]
  sigList  = [samp['name'] for samp in sigs]
  bkgHists = [samp['hist'].Clone() for samp in bkgs]
  sigHists = [samp['hist'].Clone() for samp in sigs]
  bkgStack = getStackFromHists(bkgHists,"bkgStack",scale=1)
  sigStack = getStackFromHists(sigHists,"sigStack",scale=1)
  dataHist = data['hist'].Clone()
  data_lumi = data['lumi']
  nBins  = dataHist.GetNbinsX()
  lowBin = dataHist.GetBinLowEdge(1)
  hiBin  = dataHist.GetBinLowEdge(dataHist.GetNbinsX()+1)


  print "Plotting starts.."
  can = ROOT.TCanvas(title,title,800,800)
  can.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.05)
  latex.SetTextAlign(11)

  leg = ROOT.TLegend(0.75,0.6,0.9,0.9)
  leg.SetBorderSize(1)

  Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
  Pad1.SetLogy()
  setPadMargins(Pad1,0.06,0,0.1,0.06)

  Pad1.Draw()
  Pad1.cd()

  
  #for hist in sigHists + bkgHists:
  #  hist.Scale(1./MCScale)  


  for bkg in bkgs:
    #leg.AddEntry(samples[bkg].cuts[cut.name][plotName], samples[bkg].name,"f")
    leg.AddEntry( bkg['hist'], bkg['name'],"f")
  for sig in sigs:
    leg.AddEntry( sig['hist'], sig['name'],"l")

  #bkgStack.Draw("hist")
  bkgStack.SetMaximum(data_lumi)
  bkgStack.SetMinimum(0.1)

  color = ROOT.kBlack
  #dataHist = ROOT.TH1F(str(histo) ,str(histo),p['bin'][0],p['bin'][1],p['bin'][2])
  #data.Draw(p['var']+'>>'+str(histoname),cut['cut'])
  dataHist.SetMarkerStyle(20)
  dataHist.SetMarkerSize(1.2)
  dataHist.SetMarkerColor(ROOT.kBlack)
  dataHist.SetLineColor(color)
  print "pass draw : ) "
  #dataHist.SetMarkerStyle(20)
  #dataHist.GetXaxis().SetTitle(p['xaxis'])
  #dataHist.SetTitle("")
  dataHist.GetYaxis().SetTitleSize(0.05)
  dataHist.GetYaxis().SetLabelSize(0.05)
  #dataHist.SetMarkerSize(2)
  #dataHist.SetMaximum(3000)
  #dataHist.SetMinimum(0.11)
  bkgStack.Draw("Histo")
  sigStack.Draw("histsame")
  dataHist.Draw("E1PSame")
  #histo.Draw("E1")
  #histo.Draw("E1PSame")
  #histo.GetYaxis().SetTitle(p['yaxis'])

  

  stack_hist=ROOT.TH1F("stack_hist","stack_hist",nBins,lowBin,hiBin)
  stack_hist.Merge(bkgStack.GetHists())
  print "Integral of BKG:" , stack_hist.Integral()
  print "Integral of Data:" , dataHist.Integral()
  leg.AddEntry(dataHist, "data","PL")
  leg.SetFillColor(0)
  leg.Draw()
  latex.DrawLatex(0.1,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
  latex.DrawLatex(0.72,0.958,"#bf{L=%0.2f fb^{-1} (13 TeV)}"%(data_lumi/1000.) )
  #latex.DrawLatex(0.6,0.8,"#bf{H_{T}>500 GeV}")
  #latex.DrawLatex(0.6,0.75,"#bf{L_{T}>250 GeV}")
  #latex.DrawLatex(0.6,0.7,"#bf{N_{bjets}==1}")
  latex.DrawLatex(0.6,0.8,"#bf{MC scale=%s}"%MCScale)

  Pad1.RedrawAxis()
  can.cd()

  Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
  setPadMargins(Pad2,0,0.5,0.1,0.05)
  #Pad2.SetTopMargin(0)
  #Pad2.SetBottomMargin(0.5)
  #Pad2.SetLeftMargin(0.16)
  #Pad2.SetRightMargin(0.05)

  print "--------------------------------"
  Pad2.Draw()
  Pad2.cd()
  Func = ROOT.TF1('Func',"[0]",lowBin,hiBin)
  Func.SetParameter(0,1)
  Func.SetLineColor(2)
  h_ratio = dataHist.Clone('h_ratio')
  h_ratio.SetMinimum(0.0)
  h_ratio.SetMaximum(1.99)
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(stack_hist)
  h_ratio.SetTitle("")
  h_ratio.GetYaxis().SetTitle("Data/Pred. ")
  h_ratio.GetYaxis().SetTitleSize(0.1)
  #h_ratio.GetXaxis().SetTitle(p['xaxis'])
  h_ratio.GetYaxis().SetTitleFont(20)
  h_ratio.GetYaxis().SetTitleOffset(0.6)
  h_ratio.GetXaxis().SetTitleOffset(1)
  h_ratio.GetYaxis().SetNdivisions(505)
  h_ratio.GetXaxis().SetTitleSize(0.2)
  h_ratio.GetXaxis().SetLabelSize(0.13)
  h_ratio.GetYaxis().SetLabelSize(0.1)
  h_ratio.Draw("E1")
  #h_ratio.Draw()
  Func.Draw("same")
  #Func.Draw()
  #can.SaveAs(path+p['varname']+'.png')
  #can.SaveAs(path+p['varname']+'.pdf')
  #can.SaveAs(path+p['varname']+'.root')
  #can.Clear()
  #return can
  can.Draw()
  can.SaveAs(saveDir+"/%s.png"%title)
  return can,bkgStack, sigStack, data , (sigHists,bkgHists), Pad1, Pad2 



if __name__=="__main__":

  plotName="MET"
  cut=presel
  title=plotName



  sigList=[samp for samp in samples if samples[samp].isSignal]
  bkgList=[samp for samp in samples if not samples[samp].isSignal and not samples[samp].isData]
  d= "dblind"

  #getPlots2(samples,plots,cut , sampleList=[], plotList=[plotName], weight="%s_weight"%d)
  getPlots2(samples,plots,cut , sampleList=[], plotList=[plotName], weight="%s_weight"%d, nMinus1='met')
  #data   =[samp for samp in samples if samples[samp].isData][0]


  bkgs =  [ {'name': samples[samp].name   ,'hist': samples[samp].cuts[cut.name][plotName]  } for samp in bkgList  ] 
  sigs =  [ {'name': samples[samp].name   ,'hist': samples[samp].cuts[cut.name][plotName]  } for samp in sigList    ] 
  data =    { 'name':  samples[d]['name']   ,'hist':samples[d].cuts[cut.name][plotName]  , 'lumi':samples[d]['lumi'] }


  can=drawData(title,data,bkgs,sigs)
