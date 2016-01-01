import ROOT
import os
import math
import pickle



from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.getRatioPlot import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *




def saveCanvas(canv,name,plotDir="./",format=".gif"):
  canv.SaveAs(plotDir+"/"+name+format)

def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorateAxis(hist,xAxisTitle='x title',yAxisTitle='y title',title=''):
  axis = hist.GetXaxis()
  axis.SetTitle(xAxisTitle)
#  axis.SetTitleOffSet(1)
  axis = hist.GetYaxis()
  axis.SetTitle(yAxisTitle)
#  axis.SetTitleOffSet(1)
#  axis.SetTitleFont(62) 
  if title:  hist.SetTitle(title)
  return 


def addToLeg(legend,hist,RMS=1,Mean=1,RMSError=0,MeanError=0,pName=''):
  if RMS:
    rmsString='  RMS={RMS:.2f}'.format(RMS=hist.GetRMS())
    if RMSError: rmsString += ' #pm {0:.2f}'.format(hist.GetRMSError())
  else: rmsString=''
  if Mean:
    meanString='  Mean={MEAN:.2f}'.format(MEAN=hist.GetMean())
    if MeanError: meanString += ' #pm {0:.2f}'.format(hist.GetMeanError())
  else: meanString=''
  if pName: nameString=pName

  else: nameString=hist.GetName()
  legString= nameString + rmsString + meanString
  legend.AddEntry(hist,legString)
  return legend



def getChainFromChunks( samples, treeName):
  c = ROOT.TChain("tree")
  if type(samples)!=type([]):
    sampleList=[0]
    sampleList[0]=samples
  else:
    sampleList=samples
  nTot=0
  for sample in sampleList:
    fList, niTot = getChunks(sample,treeName)
    for f in fList:
      c.Add(f['file'])
    #print fList
    nTot += niTot
    print c.GetEntries(), nTot, niTot
  return c, nTot 

def getChainFromDir( dir, treeName='tree'):
  c=ROOT.TChain(treeName)
  c.Add(dir+"/*.root")
  return c


getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "!>=|<$&@$%[]{}#();'\"")


#getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "Kl13@$%[]{}();'\"")

def getGoodPlotFromChain(c, var, binning,varName='', cutString='(1)', weight='weight', color='', lineWidth='',fillColor='',histTitle='',  binningIsExplicit=False, addOverFlowBin=''): 
  ret=  getPlotFromChain(c, var, binning, cutString=cutString, weight=weight, binningIsExplicit=binningIsExplicit, addOverFlowBin=addOverFlowBin) 
  if not varName:
    varName=getAllAlph(var)
    print varName
  if not histTitle:
    histTitle = varName
  ret.SetTitle(histTitle)
  ret.SetName(varName)
  if color:
    #ret.SetLineColor(color)
    ret.SetLineColor(color)
  if lineWidth:
    ret.SetLineWidth(lineWidth)
  if fillColor:
    ret.SetFillColor(fillColor)
    ret.SetLineColor(ROOT.kBlack)
  return ret

def getStackFromHists(histList,sName=None,scale=None):
  if sName:
    stk=ROOT.THStack(sName,sName)
  else:
    stk=ROOT.THStack()
  for h in histList:
    if scale:
      h.Scale(scale)
    stk.Add(h)
  return stk



def matchListToDictKeys(List,Dict):
  rej=[]
  if not List:
    List=Dict.keys()
  else:
    if type(List)==type([]) or  type(List)==type(()):
      pass
    else:
      List=List.rsplit()
    for l in List:
      if l not in Dict.keys():
        print "WARNING: Item \' %s \' will be ignored because it is not found in the dictionary keys:"%(l) , Dict.keys()
        rej.append(l)
        List.pop(List.index(l))
  return List



def getPlots__(sampleDict,plotDict,treeList='',varList='',cutList=''):
  """Use: getPlots(sampleDict,plotDict,treeList='',varList='',cutList=''):"""
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  
  print treeList
  print varList
  for s in treeList:
    if sampleDict[s].has_key("weight") and sampleDict[s]["weight"]:
      weight = str(sampleDict[s]["weight"])
      print "For sample %s, using weight in sampleDict, weight= %s"%(s,weight) 
    else: weight="weight"
    if not sampleDict[s].has_key('plots'):
      sampleDict[s]['plots']={}
    for p in varList:
      lineWidth=plotDict[p]['lineWidth']
      if plotDict[p]['color'] == type("") and plotDict[p]['color'].lower()=="fill" and not sampleDict[s]['isSignal']:
        #color = ROOT.kBlack
        color = sampleDict[s]['color']
        fcolor = sampleDict[s]['color']
      else:
        color  = sampleDict[s]['color']
        fcolor = 0 
        if sampleDict[s]['isSignal']:
          lineWidth=2
      if cutList:
        if type(cutList)==type(()) or type(cutList)==type([]):
          cutString=cutList[1]
          cutName=cutList[0]
          plotName = "%s_%s"%(p,cutName)
          if not plotDict.has_key(plotName):
            plotDict[plotName]=plotDict[p].copy()
            plotDict[plotName]['cut']=cutString
            plotDict[plotName]['presel']="(1)"
          title = plotDict[p]['title'].replace("{SAMPLE}",s).replace("{CUT}",cutName)
          print "*******************************************"
          print title 
          #plotDict[plotName]['title']= title 
          print "Using cut %s : %s"%(cutName,cutString)
        else:
          cutString=cutList
          cutName=getAllAlph(cutList)
          print "Using cut %s : %s "%(cutName,cutString)
          print "Try using cutList=[cutName,cutString] as an input"
          plotName = "%s_%s"%(p,cutName)
          title = plotName
      else:
        cutString="(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
        cutName=getAllAlpha(cutString)
        print "Using default cut values for var. cut:  %s"%(cutString)
        plotName=p
        title = plotName
      print "Sample:" , s , "Getting Plot: ", p, "with cut:  " , cutName
      sampleDict[s]['plots'][plotName] = getGoodPlotFromChain(sampleDict[s]['tree'] , plotDict[p]['var'], plotDict[p]['bin'],\
                                                       varName     = p  ,
                                                       histTitle   = title, 
                                                       cutString   = cutString, 
                                                       color       = color,
                                                       fillColor   = fcolor,
                                                       lineWidth   = lineWidth,
                                                       weight      = weight
                                                       #weight      = str(sampleDict[s]['weight'])
                                                       )
  return

def getBkgSigStacks(sampleDict, plotDict, varList='',treeList=''):
  """Get stacks for signal and backgrounds. make vars in varlist are available in sampleDict. no stacks for 2d histograms.   """
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  #treeList=sampleDict.keys()
  #varList=plotDict.keys()
  #sampleDict=sampleDict
  bkgStackDict={}
  sigStackDict={}
  for v in varList:
    if len(plotDict[v]['bins'])!=6:
      bkgStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if not sampleDict[t]['isSignal']])
      sigStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if sampleDict[t]['isSignal']])
  return (bkgStackDict,sigStackDict)

def drawPlots_old(sampleDict,plotDict,varList='',treeList='',plotDir='',dOpt=""):
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)

  bkgStackDict, sigStackDict =  getBkgSigStacks(sampleDict,plotDict, varList=varList,treeList=treeList)
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      c1=ROOT.TCanvas("c1","c1")
      bkgStackDict[v].Draw()
      bkgStackDict[v].SetMinimum(1)
      sigStackDict[v].Draw("samenostack")
      decorateAxis(bkgStackDict[v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
    #plotDict[v]['yAxis']
      c1.SetLogy(plotDict[v]['yLog'])
      c1.SetLogx(plotDict[v]['xLog'])
      c1.Update()
      saveCanvas(c1,v,plotDir=plotDir)
      saveCanvas(c1,v,plotDir=plotDir+"/pdf/",format=".pdf")  
      saveCanvas(c1,v,plotDir=plotDir+"/root/",format=".root")
      
      del c1
    ### 2D plots:
    elif len(plotDict[v]['bin'])==6:
      for t in treeList:
        c1=ROOT.TCanvas("c1","c1")
        #sampleDict[t]['plots'][v].SetTitle(t+"_"+plotDict[v]['title'])
        
        sampleDict[t]['plots'][v].Draw("colz%s"%dOpt)
        decorateAxis(sampleDict[t]['plots'][v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
        c1.SetLogx(plotDict[v]['xLog'])
        c1.SetLogy(plotDict[v]['yLog'])
        c1.SetLogz(plotDict[v]['zLog'])
        saveCanvas(c1,v+"_"+t,plotDir=plotDir)
        saveCanvas(c1,v+"_"+t,plotDir=plotDir+"/pdf/",format=".pdf")
        saveCanvas(c1,v+"_"+t,plotDir=plotDir+"/root/",format=".root")
        del c1



###############################################################################
###############################################################################
###############################################################################
###############################################################################


addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))



def getEventListFromFile(eListName,tmpDir=None,opt="read"):
  if opt.lower() in ["read","r"]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    f=ROOT.TFile(eListPath,"open") 
    eList = f.Get(eListName)
    eList.SetDirectory(0) 
  return eList

def getEventListFromChain(tree,cut,eListName="",tmpDir="./",opt="write"):
  if not eListName or eListName.lower()=="elist" : 
    print "WARNING: Using Default eList Name, this could be dangerous! eList name should be customized by the sample name and cut" 
    eListName="eList" 
  tree.SetEventList(0) 
  tree.Draw(">>%s"%eListName,cut) 
  eList=ROOT.gDirectory.Get(eListName)
  if opt.lower() in ["write", "w", "save", "s" ]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    print "EventList saved in: %s"%eListPath
    f = ROOT.TFile(eListPath,"recreate")
    eList.Write()
    f.Close()
  return eList

def setEventListToChain(tree,cut,eListName="",verbose=True,tmpDir=None,opt="read"): 
  if not tmpDir:
    tmpDir = os.getenv("CMSSW_BASE")+"/src/Workspace/DegenerateStopAnalysis/plotsNavid/tmp/"
  eListPath="%s/%s.root"%(tmpDir,eListName)
  if opt.lower() in ["read","r"]: 
    if os.path.isfile(eListPath):
      eList = getEventListFromFile(eListName=eListName,tmpDir=tmpDir,opt=opt)
    else:
      print "eList was not found in:%s "%eListPath
      opt="write"
  if opt.lower() in ["make","m","write", "w","s","save"] : 
    if True: print "Creating EList", eListName 
    eList = getEventListFromChain(tree,cut,eListName,tmpDir=tmpDir,opt=opt)
  if verbose: print "Setting EventList to Chain: ", tree, "Reducing the raw nEvents from ", tree.GetEntries(), " to ", 
  tree.SetEventList(eList) 
  assert eList.GetN() == tree.GetEventList().GetN() 
  return eList

def setEventListToChains(sampleDict,treeList,cutInst,verbose=True,opt="read"):
  if cutInst:
    if isinstance(cutInst,CutClass):
      cutName   = cutInst.name
      cutString = cutInst.combined
    else:
      cutName, cutString = cutInst
    if verbose:
      print "Setting eventlists using cut:"
      print cutName, cutString
    for tree in treeList:
      eListName="eList_%s_%s"%(tree,cutName)
      setEventListToChain(sampleDict[tree]['tree'],cutString,eListName=eListName,verbose=False,opt=opt)
      if verbose:
        if sampleDict[tree]['tree'].GetEventList():
          print "     Sample:", tree,   "Reducing the raw nEvents from ", sampleDict[tree]['tree'].GetEntries(), " to ", sampleDict[tree]['tree'].GetEventList().GetN()
        else:
          print "FAILED Setting EventList to Sample", tree, sampleDict[tree]['tree'].GetEventList() 
  else:
    print "no cut... no EventList was set to trees" 






def setEventListToChainSimple(tree,cut,eListName="",verbose=True):
  if not eListName:
    print "WARNING: Using Default eList Name, this could be dangerous!"
    eListName="eList"
  if verbose: print "Setting EventList to Chain: ", tree, "Reducing the raw nEvents from ", tree.GetEntries(), " to ",
  tree.SetEventList(0)
  tree.Draw(">>%s"%eListName,cut)
  eList = getattr(ROOT,eListName)
  tree.SetEventList(eList )
  if verbose: print eList.GetN()
  assert eList.GetN() == tree.GetEventList().GetN()
  del eList



def makeDecorHistFunc(title='',x='',y="",color='',width='',fillColor=''):
  def decorateFunc(h):
    if color: h.SetLineColor(color)
    if width: h.SetLineWidth(width)
    if title: h.SetTitle(title)
    if title: h.SetName(getAllAlph(title))
    if fillColor: h.SetFillColor(fillColor)
    if x : h.GetXaxis().SetTitle(x)
    if y : h.GetYaxis().SetTitle(y)
  return decorateFunc


def makeDecorCanvFunc(xlog=0,ylog=0,zlog=0):
  def decorateFunc(canv):
    if xlog: canv.SetLogx(xlog)
    if ylog: canv.SetLogy(zlog)
    if zlog: canv.SetLogz(ylog)
  return decorateFunc

def makeDecorAxisFunc(axis,title,titleSize,titleFont,titleOffset,nDiv,labelSize):
  def decorateFunc(hist):
    if axis.lower=="x":
      ax = hist.GetXaxis()
    elif axis.lower=="y":
      ax = hist.GetYaxis()
    else:
      print "Choose either X or Y axis to decorate!"
    ax.SetTitle(title)
    ax.SetTitleSize(titleSize)
    ax.SetTitleFont(titleFont)
    ax.SetTitleOffset(titleOffset)
    ax.SetLabelSize(labelSize)
    ax.SetNdivisions(nDiv)
  return decorateFunc



class Dict(dict):
  def __init__(self,*arg,**kw):
      super(Dict, self).__init__(*arg, **kw)
      self.__dict__ = self


###############################


def decorHist(samp,cut,hist,decorDict):
  dd=decorDict
  if dd.has_key("title"):
    hist.SetName(getAllAlph(dd["title"]))
    hist.SetTitle(getAllAlph(dd["title"]))
  if dd.has_key("color") and dd['color']:
    hist.SetLineColor(dd['color'])
  elif not samp.isData and not samp.isSignal:
    hist.SetFillColor(samp['color'])
    hist.SetLineColor(ROOT.kBlack)
  elif samp.isSignal:
    hist.SetLineColor(samp['color'])
  else:
    print "default color used for:", samp, cut, hist, decorDict
  if dd.has_key("x") and dd['x']:
    hist.GetXaxis().SetTitle(dd['x'])
  if dd.has_key("y") and dd['y']:
    hist.GetYaxis().SetTitle(dd['y'])


def getPlot2(sample,plot,cut,cutOpt="combined"):
  
  c   = sample.tree

  var = plot.var
  try:
    cutString = getattr(cut,cutOpt)
  except AttributeError:
    assert False

  hist = getPlotFromChain(sample.tree,plot.var,plot.bins,cutString,weight=sample.weight)
  #plot.decorHistFunc(p)
  decorHist(sample,cut,hist,plot.decor) 
  sample.plots[plot.name]=hist
  
def getPlot(sample,plot,cut,weight="(weight)", nMinus1=""):
  c   = sample.tree
  var = plot.var
  if nMinus1:
    cutString = cut.nMinus1(nMinus1)
  else:
    cutString = cut.combined

  if weight:
    w = weight
  else:
    print "No Weight is being applied"
    w = "(1)"

  hist = getPlotFromChain(sample.tree,plot.var,plot.bins,cutString,weight=w)
  #plot.decorHistFunc(p)
  decorHist(sample,cut,hist,plot.decor) 
  plotName=plot.name + "_"+ cut.name
  sample.plots[plotName]=hist
  if not sample.has_key("cuts"):
    sample.cuts=Dict()
  if not sample.cuts.has_key(cut.name):
    sample.cuts[cut.name]=Dict()
  sample.cuts[cut.name][plot.name]=hist



def getPlots(samples,plots,cut):
  for sample in samples.itervalues():
    for plot in plots.itervalues():
      getPlot(sample,plot,cut)


def getPlots2(samples,plots,cut,sampleList=[],plotList=[],weight="(weight)",nMinus1=""):
  for sample in samples.iterkeys():
    if sample in sampleList or not sampleList:
      if weight.endswith("_weight"):
        if samples[sample].has_key(weight):
          weight_str = samples[sample][weight]     
          print "Sample: %s, weight: %s"%(sample,weight_str)
          #print sample, weight_str, samples[sample]
        elif samples[sample].isData:
          weight_str = "(1)"
        else:
          print "not sure what weight to use!", sample, weight_str,  samples[sample]
          assert False
          #w = "(weight)"
      else:
        weight_str = weight
      for plot in plots.iterkeys():
        if plot in plotList or not plotList:
          getPlot(samples[sample],plots[plot],cut,weight=weight_str,nMinus1=nMinus1)


def drawPlots(samples,plots):
  canv=ROOT.TCanvas()
  for plot in plots.itervalues():
    drawOpt=""
    for sample in samples.itervalues():
      sample.plots[plot.name].Draw(drawOpt)
      drawOpt="same"
  return canv

          

def drawPlot(samples,sampleList=['s','w'],plot='',min=False,logy=0,save=True,fom=True):
    canv = ROOT.TCanvas(plot,plot,600,600)
    if logy: canv.SetLogy(1)
    sigHist = getattr(samples.s.cuts.sr1Loose,plot)
    bkgHist = getattr(samples.w.cuts.sr1Loose,plot)
    bkgHist.Draw("hist")
    if min: bkgHist.SetMinimum(min)
    sigHist.Draw("same")
    canv.SetLogy(1)
    if save:
        canv.SaveAs(saveDir+"/%s.png"%plot)
    if fom:
        fomHist=getFOMFromTH1F(sigHist,bkgHist)
        fomCanv=ROOT.TCanvas("FOM_%s"%plot,"FOM_%s"%plot ,600,200)
        fomHist.Draw()
    return canv, fomHist, fomCanv






def getAndDraw_old(samples,name,var,cut="(1)",bins=[],weight="weight",sampleList=['w'],min=False,logy=0,fom="AMSSYS",fomOpt=True,save=False):
    binning = "(%s)"%",".join([str(x) for x in bins]) if bins else ''
    ret={}

    #bkgList=['tt','w']
    bkgList=sampleList
    bkgHists={}
    for bkg in bkgList:
        bkgHists[bkg]={}
        bkgHistName= bkg+"_"+name
        bkgHists[bkg]['name']=bkgHistName
        bkgTree=samples[bkg].tree
        if hasattr(ROOT,bkgHistName) and getattr(ROOT,bkgHistName):
            hist=getattr(ROOT,bkgHistName)
            #print hist, "already exist, will try to delete it!"
            #hist.IsA().Destructor(hist)
            del hist
        bkgTree.Draw(var+">>hTmp%s"%(binning) ,  "(%s)*(%s)"%(weight,cut), "goff")
        bkgHists[bkg]['hist'] = ROOT.hTmp.Clone(bkgHistName)
        del ROOT.hTmp
        bkgHists[bkg]['hist'].SetFillColor(bkgHists[bkg]['hist'].GetLineColor())
        bkgHists[bkg]['hist'].SetLineColor(1)
        bkgHists[bkg]['hist'].SetTitle(name)
    bkgStack = getStackFromHists( [bkgHists[bkg]['hist'] for bkg in bkgList] )
    bkgStack.SetTitle(name)

    
    sigHistName="s_%s"%name
    samples.s.tree.Draw(var+">>hTmp2%s"%(binning), "(%s)*(%s)"%(weight,cut), "goff")
    sigHist = ROOT.hTmp2.Clone(sigHistName)
    del ROOT.hTmp2

    nBins  = sigHist.GetNbinsX()
    lowBin = sigHist.GetBinLowEdge(1)
    hiBin  = sigHist.GetBinLowEdge(sigHist.GetNbinsX()+1)

    stackHist=ROOT.TH1F("stack_hist","stack_hist",nBins,lowBin,hiBin)
    stackHist.Merge(bkgStack.GetHists())

    if min:
        bkgStack.SetMinimum(min)
    ret.update({'sHist':sigHist, 'bkgHists':bkgHists, "bkgStack":bkgStack, "stackHist":stackHist } )

    if fom:
        c1,p1,p2 = makeCanvasPads("%s"%name,600,600)
        p2.cd()


        if str(fom)  == "ratio": 
            ratio = getRatio(sigHist,stackHist,normalize=True, min=0.01,max=2.0)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getRatio(sigHist, bkgHists[bkg]['hist'] ,normalize=True, min=0.01,max=2.0)
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        else:
            ratio=getFOMFromTH1FIntegral(sigHist,stackHist,fom=fom)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getFOMFromTH1FIntegral(sigHist, bkgHists[bkg]['hist'], fom=fom )
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        dOpt=''
        if not fomOpt:
            for bkg in bkgList:
                bkgHists[bkg]['ratio'].SetLineColor( bkgHists[bkg]['hist'].GetFillColor() )
                bkgHists[bkg]['ratio'].SetLineWidth(2)

                if not dOpt:
                    firstHist = bkgHists[bkg]['ratio']
                bkgHists[bkg]['ratio'].Draw(dOpt)
                dOpt="same"
        else:
            firstHist = ratio
            ratio.SetTitle(name)
            ratio.Draw(dOpt)

        firstHist.SetStats(0)
        x = firstHist.GetXaxis()
        x.SetTitleSize(20)
        x.SetTitleFont(43)
        x.SetTitleOffset(4.0)
        x.SetLabelFont(43)
        x.SetLabelSize(15)
        y = firstHist.GetYaxis()
        y.SetTitle(fom)
        y.SetNdivisions(505)
        y.SetTitleSize(20)
        y.SetTitleFont(43)
        y.SetTitleOffset(1)
        y.SetLabelFont(43)
        y.SetLabelSize(15)
               
 
        ratio.SetLineColor(ROOT.kSpring+4)
        ratio.SetMarkerColor(ROOT.kSpring+4)
        ratio.SetLineWidth(2)
        if "ratio" in fom.lower():
          ratio.SetMinimum(0)
          ratio.SetMaximum(2)
        else:
          ratio.SetMinimum(0.5)
          ratio.SetMaximum(2)
        print "getting ratio"
        Func = ROOT.TF1('Func',"[0]",sigHist.GetBinLowEdge(1),sigHist.GetBinLowEdge( sigHist.GetNbinsX()+1) )
        Func.SetParameter(0,1)
        Func.SetLineColor(ROOT.kRed)
        Func.Draw('same')
        c1.Update()
        p1.Update()
        ret.update({'ratio':ratio, 'canv': (c1,p1,p2), 'func':Func } )
    else:
        p1 = ROOT.TCanvas(name,name,600,600)
        ret.update({'canv': (p1) } )
        #bkgHist.Draw("hist")
        #sigHist.Draw("same")
    p1.cd()

    bkgStack.Draw("hist")
    bkgStack.GetYaxis().SetTitle("nEvents")
    sigHist.Draw("same")
    if logy:
        p1.SetLogy(1)
    if save:
        if fom:
            c1.SaveAs(save+"/%s.png"%name)
        else:
            p1.SaveAs(save+"/%s.png"%name)
    return ret 







def getAndDraw(samples, plots, cutInst, weight="weight", sampleList=['w'], min=False,logy=0,fom="AMSSYS",fomOpt=True,save=False):


    bkgList=sampleList
    bkgHists={}
    for bkg in bkgList:
        bkgHists[bkg]={}
        bkgHistName= bkg+"_"+name
        bkgHists[bkg]['name']=bkgHistName
        bkgTree=samples[bkg].tree
        if hasattr(ROOT,bkgHistName) and getattr(ROOT,bkgHistName):
            hist=getattr(ROOT,bkgHistName)
            #print hist, "already exist, will try to delete it!"
            #hist.IsA().Destructor(hist)
            del hist
        bkgTree.Draw(var+">>hTmp%s"%(binning) ,  "(%s)*(%s)"%(weight,cut), "goff")
        bkgHists[bkg]['hist'] = ROOT.hTmp.Clone(bkgHistName)
        del ROOT.hTmp
        bkgHists[bkg]['hist'].SetFillColor(bkgHists[bkg]['hist'].GetLineColor())
        bkgHists[bkg]['hist'].SetLineColor(1)
        bkgHists[bkg]['hist'].SetTitle(name)
    bkgStack = getStackFromHists( [bkgHists[bkg]['hist'] for bkg in bkgList] )
    bkgStack.SetTitle(name)

    
    sigHistName="s_%s"%name
    samples.s.tree.Draw(var+">>hTmp2%s"%(binning), "(%s)*(%s)"%(weight,cut), "goff")
    sigHist = ROOT.hTmp2.Clone(sigHistName)
    del ROOT.hTmp2

    nBins  = sigHist.GetNbinsX()
    lowBin = sigHist.GetBinLowEdge(1)
    hiBin  = sigHist.GetBinLowEdge(sigHist.GetNbinsX()+1)

    stackHist=ROOT.TH1F("stack_hist","stack_hist",nBins,lowBin,hiBin)
    stackHist.Merge(bkgStack.GetHists())

    if min:
        bkgStack.SetMinimum(min)
    ret.update({'sHist':sigHist, 'bkgHists':bkgHists, "bkgStack":bkgStack, "stackHist":stackHist } )

    if fom:
        c1,p1,p2 = makeCanvasPads("%s"%name,600,600)
        p2.cd()


        if str(fom)  == "ratio": 
            ratio = getRatio(sigHist,stackHist,normalize=True, min=0.01,max=2.0)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getRatio(sigHist, bkgHists[bkg]['hist'] ,normalize=True, min=0.01,max=2.0)
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        else:
            ratio=getFOMFromTH1FIntegral(sigHist,stackHist,fom=fom)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getFOMFromTH1FIntegral(sigHist, bkgHists[bkg]['hist'], fom=fom )
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        dOpt=''
        if not fomOpt:
            for bkg in bkgList:
                bkgHists[bkg]['ratio'].SetLineColor( bkgHists[bkg]['hist'].GetFillColor() )
                bkgHists[bkg]['ratio'].SetLineWidth(2)

                if not dOpt:
                    firstHist = bkgHists[bkg]['ratio']
                bkgHists[bkg]['ratio'].Draw(dOpt)
                dOpt="same"
        else:
            firstHist = ratio
            ratio.SetTitle(name)
            ratio.Draw(dOpt)

        firstHist.SetStats(0)
        x = firstHist.GetXaxis()
        x.SetTitleSize(20)
        x.SetTitleFont(43)
        x.SetTitleOffset(4.0)
        x.SetLabelFont(43)
        x.SetLabelSize(15)
        y = firstHist.GetYaxis()
        y.SetTitle(fom)
        y.SetNdivisions(505)
        y.SetTitleSize(20)
        y.SetTitleFont(43)
        y.SetTitleOffset(1)
        y.SetLabelFont(43)
        y.SetLabelSize(15)
               
 
        ratio.SetLineColor(ROOT.kSpring+4)
        ratio.SetMarkerColor(ROOT.kSpring+4)
        ratio.SetLineWidth(2)
        if "ratio" in fom.lower():
          ratio.SetMinimum(0)
          ratio.SetMaximum(2)
        else:
          ratio.SetMinimum(0.5)
          ratio.SetMaximum(2)
        print "getting ratio"
        Func = ROOT.TF1('Func',"[0]",sigHist.GetBinLowEdge(1),sigHist.GetBinLowEdge( sigHist.GetNbinsX()+1) )
        Func.SetParameter(0,1)
        Func.SetLineColor(ROOT.kRed)
        Func.Draw('same')
        c1.Update()
        p1.Update()
        ret.update({'ratio':ratio, 'canv': (c1,p1,p2), 'func':Func } )
    else:
        p1 = ROOT.TCanvas(name,name,600,600)
        ret.update({'canv': (p1) } )
        #bkgHist.Draw("hist")
        #sigHist.Draw("same")
    p1.cd()

    bkgStack.Draw("hist")
    bkgStack.GetYaxis().SetTitle("nEvents")
    sigHist.Draw("same")
    if logy:
        p1.SetLogy(1)
    if save:
        if fom:
            c1.SaveAs(save+"/%s.png"%name)
        else:
            p1.SaveAs(save+"/%s.png"%name)
    return ret 






