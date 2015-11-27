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
from dmt import *




regs=[
      # {"r":r1_regions, "name": "r1", 'pklDir':"./pkl/dmt_regions/r1/", "cut":"cut1_ptbin"},
      # {"r":r2_regions, "name": "r2", 'pklDir':"./pkl/dmt_regions/r2/", "cut":"cut2_ptbin"},
      # {"r":r3_regions, "name": "r3", 'pklDir':"./pkl/dmt_regions/r3/", "cut":"cut3_ptbin"},
       {"r":r1_regions, "name": "r1", 'pklDir':"./pkl/dmt_regions/r1/", "cut":"cut1_ptbin"},
       {"r":r2_regions, "name": "r2", 'pklDir':"./pkl/dmt_regions/r2/", "cut":"cut2_ptbin"},
       {"r":r3_regions, "name": "r3", 'pklDir':"./pkl/dmt_regions/r3/", "cut":"cut3_ptbin"},
      ]

ind = 2 
regions = regs[ind]['r']
regsname = regs[ind]['name']
pklDir = regs[ind]['pklDir']
cut= regs[ind]['cut']

ROOT.gStyle.SetOptStat(0)

#setEventListToChains(samples,['tt','w','s','d'],presel)
if not samples.s.tree.GetEventList():
  setEventListToChains(samples,['w','s'],sr1Loose)

print "Getting Plots:"
if not hasattr(samples.s,"cuts"):
  getPlots2(samples,plots,sr1Loose,sampleList=['w','s'],plotList=["dmt"])
print "Getting FOM hist"
fomHistW = getFOMFromTH2F(samples.s.cuts.sr1Loose.DMT, samples.w.cuts.sr1Loose.DMT)
fomHistW.SetTitle("FOM")
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
#regDict={}
print "Getting Yields for different regions:"
for r in regions:
    name=r[0]
    canv={}
    #regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
    #print "----------------------------------------------------------------"
    #print getattr(regDict[name],cut).list
    #print "----------------------------------------------------------------"
    yDict[name]=  Yields(samples,['w','s'], getattr(regDict[name],cut), cutOpt='list', tableName='{cut}_dmt',pklOpt=True,pklDir=pklDir )   
    #JinjaTexTable(yDict[name])
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
#limitList = sorted(limitDict.keys())
limitList = best
#for i,fname in enumerate(sorted(limitDict),1):
for i,fname in enumerate(limitList,1):
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





## Draw 2D plot Variation in Each DMT Region

DrawVariationsInDMTRegions=False
if DrawVariationsInDMTRegions:

  regDict={}
  canv2= ROOT.TCanvas("cdmt","cdmt",800,800)

  fomHistW.Draw("COLZ")
  for r in r1_regions:
    name=r[0]
    regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
    regDict[name].r1.r.Draw("same")
    regDict[name].r2.r.Draw("same")
    regDict[name].r3.r.Draw("same")
  canv2.SaveAs(saveDir+"/%s.png"%"allDMTr1Regions")

  fomHistW.Draw("COLZ")
  for r in r2_regions:
    name=r[0]
    regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
    regDict[name].r1.r.Draw("same")
    regDict[name].r2.r.Draw("same")
    regDict[name].r3.r.Draw("same")
  canv2.SaveAs(saveDir+"/%s.png"%"allDMTr2Regions")

  fomHistW.Draw("COLZ")
  for r in r3_regions:
    name=r[0]
    regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
    regDict[name].r1.r.Draw("same")
    regDict[name].r2.r.Draw("same")
    regDict[name].r3.r.Draw("same")
  canv2.SaveAs(saveDir+"/%s.png"%"allDMTr3Regions")



## Yields for each DMT Regions
if True:
  dmtYields={}
  for dmtCut in [dmtRegions, dmtR1, dmtR2, dmtR3 ]:
    dmtYields[dmtCut.name]=   Yields(samples,['w','s'], dmtCut, cutOpt='list', tableName='{cut}',pklOpt=True,pklDir= "./pkl/dmt_regions/" )
    JinjaTexTable(dmtYields[dmtCut.name])    







