import math 


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


