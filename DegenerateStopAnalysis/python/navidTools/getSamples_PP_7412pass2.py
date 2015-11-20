import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.navidTools.Sample import Sample, Samples


#-------------------------



#data_lumi = data_lumi
mc_lumi   = 10000
data_lumi_blinded = 0.133
data_lumi_unblinded = 0.133 + 1.55

#TTSample    = getChain(TTJets['inc'],histname='') 
#
#data_mu     = getChain(data_mu_25ns,histname='')
#sampleDict={
#          'tt':             {'tree':TTSample        ,'name':"TTJets"  , 'color':ROOT.kAzure-5            , 'isSignal':0 , 'isData':0     ,"weight":"(weight)"  ,"lumi":mc_lumi  },
#          'w':              {'tree': WSample        ,'name':"WJets"   , 'color':ROOT.kSpring-5          , 'isSignal':0 , 'isData':0     ,"weight":"(weight)"  ,"lumi":mc_lumi  },
#          "s":              {'tree':T2DegSample     ,'name':"S300_270", 'color':ROOT.kRed      , 'isSignal':1 , 'isData':0    ,"weight":"(weight)"  ,"lumi":mc_lumi   },
#          "d":              {'tree':data_mu         ,'name':"data"    , 'color':ROOT.kBlack    , 'isSignal':0 , 'isData':1    ,"weight":"(1)"  ,'lumi':data_lumi },
#          #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
#       }
#for s in sampleDict:
#  sampleDict[s]['tree'].SetLineColor(sampleDict[s]['color'])



T2DegSample = getChain(T2DegStop_300_270['inc'],histname='')
#WJets = getChain(WJets['inc'],histname='')
WJetsHTSample = getChain(WJetsHT['inc'],histname='')
#WJetsSample = getChain(WJetsInc['inc'],histname='')

METDataBlinded = getChain(MET_Run2015D_05Oct2015_v1['inc'],histname='')
METData       = getChain(MET_Run2015D_PromptReco_v4['inc'],histname='')
METData.Add(METDataBlinded)

sampleDict={
          'w':          {'tree':WJetsHTSample         ,'name':'WJets'     ,'color':ROOT.kSpring-5           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
          "s":          {'tree':T2DegSample           ,'name':'S300_270'  ,'color':ROOT.kRed                , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
          "d":          {'tree':METDataBlinded        ,'name':"data"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"weight":"(1)"  ,'lumi': data_lumi_blinded},
          #"d":         {'tree':METData               ,'name':"data"     , 'color':ROOT.kBlack              , 'isSignal':0 , 'isData':1    ,"weight":"(1)"  ,'lumi': 1.26 },
          #'TTs': {'tree':getChain(ttJets['soft'],histname=' 'lineColor':1') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
       }
sampleDict2 = {}

for samp in sampleDict:
  sampleDict2[samp]=Sample(**sampleDict[samp])
samples = Samples(**sampleDict2)



