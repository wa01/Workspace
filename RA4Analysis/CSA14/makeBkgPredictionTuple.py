import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID
from math import sqrt, cos, sin, atan2
from Workspace.RA4Analysis.helpers import deltaPhi

from Workspace.RA4Analysis.stage2Tuples import *
c = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
#mode='dilep'
c.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
mode='dilep'
relIso = 0.3
effUp = 1.1
effDown = 0.9
small = False
maxN=50000

if mode=='had':
  leptonEffMap = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_vetoLeptonEfficiencyMap.pkl'))
  #leptonEffMap = pickle.load(file('/data/easilar/results2014/tauTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso0.3.pkl'))
  doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_genTau.pkl'))
  ofile =                      '/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTauTryBtag110.root'
if mode=='lep':
  leptonEffMap = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_vetoLeptonEfficiencyMap.pkl'))
  doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_lepGenTau.pkl'))
  ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_lepGenTau.root'
if mode=='dilep':
  leptonEffMap = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
  leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso)
  doubleLeptonPreselection = "ngNuMuFromW==2&&ngNuEFromW==0&&ngoodMuons>=1&&Sum$("+leptonID+")==2&&nvetoElectrons==0"
  ofile =                    '/data/easilar/results2014/muonTuples/CSA14_TTJets_dilep_New_relIso'+str(relIso)+'.root'

if mode=='had' or mode=='lep':
  for ptk in templates.keys():
    for etak in templates[ptk].keys():
      templates[ptk][etak].Scale(1./templates[ptk][etak].Integral())
      res=[]
      for b in range(1, 1+templates[ptk][etak].GetNbinsX()):
        res.append({'frac':templates[ptk][etak].GetBinCenter(b), 'weight':templates[ptk][etak].GetBinContent(b)})
      templates[ptk][etak]=res

def getTwoMuons(c):
  nmuCount = int(getVarValue(c, 'nmuCount' ))
  res=[]
  nt=0
  nl=0
  for i in range(nmuCount):
    l=getLooseMuStage2(c, i)
    isTight=tightPOGMuID(l)
    isLoose=vetoMuID(l, relIso=relIso)
    l['isTight'] = isTight 
    l['isLoose'] = isLoose
    if isTight:nt+=1
    if isLoose:nl+=1
    if isTight or isLoose: res.append(l)
    if isTight and not isLoose:
      print "Warning!! Tight but not loose!!",l
  if len(res)!=2: print "Warning: found",len(res),'muons -> inconsistent with preselection!!'
  if not (nt>=1 and nl==2):print "Warning! Not >=1 tight and ==2 loose -> Inconsistent w/ preselection"
  return res

def getTypeStr(s):
  if s=='l': return 'ULong64_t'
  if s=='F': return 'Float_t'
  if s=='I': return 'Int_t'

copyVars  = ['event/l','nbtags/I', 'njets/I', 'ht/F', 'met/F', 'metphi/F', 'nvetoMuons/I']
newVars   = ['njetsPred/I', 'muPtLoose/F','muPhiLoose/F','htPred/F','muPtPred/F','muPhiPred/F','wPhiPred/F','wPtPred/F','stPred/F' ,'metPred/F', 'metphiPred/F','weightPred/F', 'mTPred/F', 'weight/F', 'scaleLEff/F','scaleLEffUp/F','scaleLEffDown/F','deltaPhiPred/F']
vars      = copyVars+newVars  

structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+="}"   
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
dir=ROOT.gDirectory.func()

f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v) 
dir.cd()

c.Draw(">>eList", doubleLeptonPreselection)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
if small:
  if number_events>maxN:
    number_events=maxN
number_events=min(number_events, eList.GetN())
countLeptons=0
for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  s.event = long(c.GetLeaf('event').GetValue())
  for v in copyVars[1:]:
    n=v.split('/')[0]
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  muons = getTwoMuons(c)
  assert len(muons)==2, "Problem in event "+str(int(c.GetLeaf('event').GetValue()))
  if muons[0]['isTight'] and muons[1]['isTight']:
    combFac=0.5
  else:
    combFac=1.
  for perm in [muons, reversed(muons)]:
    m,m2 = perm
    if m2['isTight']:
#      print iperm, m['isTight'],m2['isTight']
#      print "pt",m['pt'],m['phi'],m['eta']
      abseta=abs(m['eta'])
      if abseta>2.1:continue
      countLeptons+=1
#      print template 
      s.weight=c.GetLeaf('weight').GetValue()
      lEffb = leptonEffMap.FindBin( m['pt'], m['eta'])
      lEffi = leptonEffMap.GetBinContent(lEffb)
      if lEffi>0.5:
        lEffUp = max((lEffi*effUp)-(effUp-1),0)
        lEffDown = min((lEffi*effDown)+(1-effDown),1)
        lEff = lEffi
        if mode=='dilep':
          s.scaleLEff = (1-lEff)/lEff
          s.scaleLEffUp = (1-lEffUp)/lEffUp
          #print s.scaleLEffUp
          s.scaleLEffDown = (1-lEffDown)/lEffDown 
          metx = s.met*cos(s.metphi)+cos(m['phi'])*m['pt']
          mety = s.met*sin(s.metphi)+sin(m['phi'])*m['pt']
          s.njetsPred = s.njets
          s.htPred   = s.ht
          s.muPtPred     = m2['pt']  
          s.muPhiPred    = m2['phi']
          s.muPtLoose    = m['pt']
          s.muPhiLoose   = m['phi']
          s.weightPred = s.weight
          s.metPred = sqrt(metx**2+mety**2)
          s.metphiPred = atan2(mety,metx)
          s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
          wx = s.metPred*cos(s.metphiPred) + m2['pt']*cos(m2['phi'])
          wy = s.metPred*sin(s.metphiPred) + m2['pt']*sin(m2['phi'])
          s.wPhiPred     = atan2(wy,wx)
          s.wPtPred      = sqrt((wx)**2+(wy)**2)
          s.stPred       = sqrt((s.wPtPred)**2+(s.mTPred)**2) 
          s.deltaPhiPred = deltaPhi(s.wPhiPred,m2['phi'])
          t.Fill()
      if mode=='had' or mode=='lep':
        template=None
        for ptb in gTauPtBins:
          if m['pt']>=ptb[0] and (m['pt']<ptb[1] or ptb[1]<0):
            for etab in gTauAbsEtaBins:
              if abseta>=etab[0] and abseta<etab[1]:
                template=templates[ptb][etab]
                break
            if template:break
        assert template, "No template found for muon: %r" % repr(m)
#        if lEff>0:
        s.scaleLEff = 1./lEff
#        else:
#          s.scaleLEff = 1.
        for p in template:
          metpar    = p['frac']*m['pt']
          MEx = s.met*cos(s.metphi)+cos(m['phi'])*metpar
          MEy = s.met*sin(s.metphi)+sin(m['phi'])*metpar
          wx = MEx+cos(m2['phi'])*m2['pt']
          wy = MEy+sin(m2['phi'])*m2['pt'] 
          if mode=='had':
            s.weightPred = p['weight']*s.weight
  #          s.nvetoMuonsPred = s.nvetoMuons 
            jetpt =  (1.-p['frac'])*m['pt']
            if jetpt>30.:
              s.njetsPred = s.njets+1
              s.htPred    = s.ht+jetpt
            else:
              s.njetsPred = s.njets
              s.htPred    = s.ht
            s.metPred      = sqrt(MEx**2+MEy**2)
            s.metphiPred   = atan2(MEy,MEx)
            s.mTPred       = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
            s.wPtPred      = sqrt(wx**2+wy**2)
            s.wPhiPred     = atan2(wy,wx)
            s.stPred       = sqrt((s.wPtPred)**2+(s.mTPred)**2)
            s.deltaPhiPred = deltaPhi(s.wPhiPred,m2['phi'])
            t.Fill()
          if mode=='lep':
            s.njetsPred = s.njets
            s.htPred   = s.ht
            leppt =  (1.-p['frac'])*m['pt']
            if leppt>15.:
              nlEffb = leptonEffMap.FindBin(leppt, m['eta'])
              nlEff = leptonEffMap.GetBinContent(nlEffb) #Consider the event not contributing if the lepton from the tau hits the lepton veto
              weightFac = 1-nlEff
            else:
              weightFac = 1.
              
            s.weightPred = p['weight']*s.weight*weightFac
            MEx += leppt*cos(m['phi'])
            MEy += leppt*sin(m['phi'])
            s.metPred = sqrt(MEx**2+MEy**2)
            s.metphiPred = atan2(MEy,MEx)
            s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
            t.Fill()
  #              #lepton reconstructed ->not filled
  ##              s.nvetoMuonsPred = s.nvetoMuons + 1 
  #              s.weightPred = p['weight']*s.weight*nlEff
  #              s.metPred = sqrt(MEx**2+MEy**2)
  #              s.metphiPred = atan2(MEy,MEx)
  #              s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
  #              t.Fill()
                #lepton lost
  #              s.nvetoMuonsPred = s.nvetoMuons  


f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

