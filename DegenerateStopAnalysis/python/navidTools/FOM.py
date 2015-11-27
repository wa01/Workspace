import math 
import ROOT

## --------------------------------------------------------------
##                        Figure of Merit Tools
## --------------------------------------------------------------

def AMSSYS (s,b,sysUnc=0.2):
  #print s, b
  sysUnc2=sysUnc*sysUnc
  b2 = b*b 
  if s==0: 
    return 0
  if b<=0: 
    return -1
  #return (lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sysUnc*b))/(b2+(s+b)*sysUnc*b))  - b2/(sysUnc*b)*math.log(1+sysUnc*b*s/(b*(b+sysUnc*b))) )) if b!=0 else -1)(s,b)
  ret = math.sqrt(2*( (s+b)*math.log(((s+b)*(b+ (sysUnc2*b2) ))/(b2+(s+b)* (sysUnc2*b2) ))  - b2/( (sysUnc2*b2) )*math.log(1+ (sysUnc2*b2) *s/(b*(b+ (sysUnc2*b2) ))))) 
  return ret 


def AMS1 (s,b,sysUnc=0.2):
  sysUnc2= sysUnc*sysUnc
  b0 = 0.5*( b - sysUnc2 + math.sqrt( (b-sysUnc2)*(b-sysUnc2)+4*(s+b)*(sysUnc2)   )  ) 
  ams1 = math.sqrt(2*((s+b)*math.log((s+b)/b0)-s-b+b0 )+ (b-b0)*(b-b0)/sysUnc2  )
  return ams1

fomFuncs= {
                "SOB"         : lambda s,b,sysUnc  : s/math.sqrt(b) if b!=0 else -1 ,
                "SOBSYS"      : lambda s,b,sysUnc : s/math.sqrt(b+(sysUnc*sysUnc*b*b) ) if b!=0 else -1 ,
                "AMS"         : lambda s,b,sysUnc : math.sqrt(2*((s+b)*math.log(1+1.*s/b)-s) ) if b!=0 else -1 ,
                "AMSSYS"      : AMSSYS ,
                "AMS1"        : AMS1   ,
            }

def calcFOMs(s,b,sysUnc=0.2,fom=None):
  if fom: 
    return fomFuncs[fom](s,b,sysUnc)
  else:
    ret = {}
    for f in fomFuncs:
      ret[f]=fomFuncs[f](s,b,sysUnc)
    return ret




def getFOMFromTH2F(sHist,bHist,fom="AMSSYS",sysUnc=0.2): 
  assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match" 
  assert sHist.GetNbinsY() == bHist.GetNbinsY(), "yBins don't match" 
  nBinX= sHist.GetNbinsX() 
  nBinY= sHist.GetNbinsY() 

  fomHist=sHist.Clone() 
  fomHist.Reset() 
  fomHist.SetMarkerSize(0.8) 
  fomHist.SetName("FOM_%s_"%fom+fomHist.GetName() ) 
  for x in range(1,nBinX+1): 
    for y in range(1,nBinY+1): 
      s=sHist.GetBinContent(x,y) 
      b=bHist.GetBinContent(x,y) 
      #print s,b,
      fomVal= fomFuncs[fom](s,b,sysUnc) 
      #print fomVal
      fomHist.SetBinContent(x,y,fomVal) 
  return fomHist   

def getFOMFromTH1F(sHist,bHist,fom="AMSSYS",sysUnc=0.2): 
  assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match" 
  nBinX= sHist.GetNbinsX() 
  fomHist=sHist.Clone() 
  fomHist.Reset() 
  fomHist.SetMarkerSize(0.8) 
  fomHist.SetName("FOM_%s_"%fom+fomHist.GetName() ) 
  for x in range(1,nBinX+1): 
      s=sHist.GetBinContent(x) 
      b=bHist.GetBinContent(x) 
      #print s,b,
      fomVal= fomFuncs[fom](s,b,sysUnc) 
      #print fomVal
      fomHist.SetBinContent(x,fomVal) 
  return fomHist   


def getHistMax(hist):
  nBinX = hist.GetNbinsX()
  histMax= max( [(x,hist.GetBinContent(x)) for x in range(1, nBinX+1)] , key= lambda f: f[1] )
  return histMax

def getFOMFromTH1FIntegral(sHist,bHist,fom="AMSSYS",sysUnc=0.2):
  assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match"
  nBinX= sHist.GetNbinsX()
  fomHist = sHist.Clone()
  fomHist.Reset()
  for x in range(1,nBinX+1):
    s=sHist.Integral(x,nBinX) 
    b=bHist.Integral(x,nBinX) 
    fomVal = fomFuncs[fom](s,b,sysUnc) 
    fomHist.SetBinContent(x,fomVal)
  return fomHist

def getCutEff(hist,rej=False):
  ''' rej=False will return 1-eff ''' 
  nBinX= hist.GetNbinsX()
  effHist = hist.Clone()
  effHist.Reset()
  tot = hist.Integral()
  #print "tot:", tot
  for x in range(1,nBinX+1):
    eff = hist.Integral(x,nBinX)/float(tot)
    if rej:
      effHist.SetBinContent(x,1-eff)
    else:
      effHist.SetBinContent(x,eff)
  return {"hist":effHist,'tot':tot}


def getEffFomPlot(sHist,bHist,fom="AMSSYS", sysUnc=0.2,savePath=''):
  canv = ROOT.TCanvas()
  sEff = getCutEff(sHist)['hist'] 
  bEff = getCutEff(bHist)['hist'] 
  fom  = getFOMFromTH1FIntegral(sHist,bHist)
  fomMax = getHistMax(fom)
  maxDict = {
             "maxFOM":fomMax[1],
              "bin":fomMax[0],
              "sEff":sEff.GetBinContent(fomMax[0]),
              "bEff":bEff.GetBinContent(fomMax[0]),
            }

  bEff.SetLineColor(bEff.GetFillColor())
  bEff.SetFillColor(0)

  fomColor = ROOT.kRed

  rightmax = 1.1*fom.GetMaximum();
  scale = canv.GetUymax()/rightmax
  fom.Scale(scale)
  bEff.Draw()
  sEff.Draw('same')
  fom.SetLineColor(fomColor)
  fom.Draw('same')

  fom.SetLineWidth(2)
  sHist.SetLineWidth(2)
  bHist.SetLineWidth(2)

  xmin= 20 # (ROOT.gPad.GetUxmax()
  ymin= 0  # ROOT.gPad.GetUymin()
  xmax= 20 # ROOT.gPad.GetUxmax() 
  ymax= 1.05 # ROOT.gPad.GetUymax()
  axis = ROOT.TGaxis( xmin, ymin, xmax, ymax ,0,rightmax,510,"+L")
  axis.SetLabelColor(fomColor)
  axis.SetTitle("FOM")
  axis.SetTitleColor(fomColor)
  axis.Draw()
  print "canv:", canv.GetUxmax()
  print "after:",  (ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax() )
  if savePath:
    canv.SaveAs(savePath)
  return {"canv":canv,"sEff":sEff,"bEff":bEff,"fom":fom,"axis":axis, "max":maxDict }


def getROC(sHist, bHist, fom="AMSSYS", sysUnc=0.2,savePath=''):
  s = getCutEff(sHist)
  b = getCutEff(bHist,rej=True)
  sEffHist = s['hist']
  bRejHist = b['hist']
  sTot = s['tot']
  bTot = b['tot']
  roc = ROOT.TGraph()
  for x in range(1,sEffHist.GetNbinsX()+1):
    sEff = sEffHist.GetBinContent(x)
    bRej = bRejHist.GetBinContent(x)
    roc.SetPoint(x,sEff,bRej)
  return {'roc':roc,'sTot':sTot, 'bTot':bTot}
  #return roc

