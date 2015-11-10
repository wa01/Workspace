from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from makeTable import *
from limitCalc import *
from dmt import *



regions = r1_regions
name    = "r1"

regs=[
       {"r":r1_regions, "name": "r1", 'pklDir':"./pkl/dmt_regions/r1/", "cut":"cut1_ptbin"}

      ]


ind = 0
regions = regs[ind]['r']
regsname = regs[ind]['name']
pklDir = regs[ind]['pklDir']
cut= regs[ind]['cut']

ROOT.gStyle.SetOptStat(0)

#setEventListToChains(samples,['tt','w','s','d'],presel)
if not samples.s.tree.GetEventList():
  setEventListToChains(samples,['w','s'],sr1Loose)

getPlots(samples,plots,sr1Loose)
fomHistW = getFOMFromTH2F(samples.s.cuts.sr1Loose.DMT, samples.w.cuts.sr1Loose.DMT)
fomHistW.SetMinimum(0)


#fomHistTT = getFOMFromTH2F(samples.s.plots.DMT, samples.tt.plots.DMT)
#
#bkgDMT = samples.tt.plots.DMT.Clone()
#bkgDMT.Add(samples.w.plots.DMT)
#fomHistBkg = getFOMFromTH2F(samples.s.plots.DMT, bkgDMT)
#
saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions'

canvas={}

plotQCOSregions=False
#sample = samples.s.tree
sample = samples.s.tree.Clone()
#setEventListToChain(sample,presel.combined, "presel")


yDict={}
regDict={}
for r in regions:
  name=r[0]
  canv={}
  regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
  yDict[name]=  Yields(samples,['w','s'], getattr(regDict[name],cut), cutOpt='list', tableName='{cut}_dmt',pklOpt=True,pklDir=pklDir )   
  JinjaTexTable(yDict[name])
  canv[name]=ROOT.TCanvas(name,name,800,800)
  fomHistW.Draw("COLZ")
  regDict[name].r1.r.Draw("same")
  regDict[name].r2.r.Draw("same")
  regDict[name].r3.r.Draw("same")
  canv[name].SaveAs(saveDir+"/%s.png"%name)

    


################################### Combined Limit TOOL

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
#ROOT.c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/ExpectedLimits.png")
canv2.SaveAs(saveDir+"/%s_ExpectedLimits.png"%regsname)


bestList= [(x,limitDict[x][1]['0.500']) for x in best]
print bestList

