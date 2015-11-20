import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_Spring15_soft import *
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_Spring15_v2 import *
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
from Workspace.DegenerateStopAnalysis.navidTools.Sample import Sample, Samples

data_lumi = data_lumi
mc_lumi   = 10000

TTSample    = getChain(TTJets['inc'],histname='') 
T2DegSample = getChain(T2DegStop_300_270['inc'],histname='')
WSample     = getChain(WJets['inc'],histname='')

data_mu     = getChain(data_mu_25ns,histname='')
sampleDict={
          'tt':             {'tree':TTSample        ,'name':"TTJets"  , 'color':ROOT.kAzure-5            , 'isSignal':0 , 'isData':0     ,"weight":"(weight)"  ,"lumi":mc_lumi  },
          'w':              {'tree': WSample        ,'name':"WJets"   , 'color':ROOT.kSpring-5          , 'isSignal':0 , 'isData':0     ,"weight":"(weight)"  ,"lumi":mc_lumi  },
          "s":              {'tree':T2DegSample     ,'name':"S300_270", 'color':ROOT.kRed      , 'isSignal':1 , 'isData':0    ,"weight":"(weight)"  ,"lumi":mc_lumi   },
          "d":              {'tree':data_mu         ,'name':"data"    , 'color':ROOT.kBlack    , 'isSignal':0 , 'isData':1    ,"weight":"(1)"  ,'lumi':data_lumi },
          #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
       }
for s in sampleDict:
  sampleDict[s]['tree'].SetLineColor(sampleDict[s]['color'])


#sampleDict2= {
#          "tt":  Sample(**{'tree':TTSample        ,'name':"TTJets"  , 'color':31          ,'lineColor':1   , 'isSignal':0 , 'isData':0       }   ), 
#          "w" :  Sample(**{'tree': WSample        ,'name':"WJets"   , 'color':424         ,'lineColor':1   , 'isSignal':0 , 'isData':0       }   ),
#          "s" :  Sample(**{'tree':T2DegSample     ,'name':"S300_270", 'color':ROOT.kRed  , 'lineColor':1   , 'isSignal':1 , 'isData':0       }   ),
#         }

sampleDict2 = {}
for samp in sampleDict:
  sampleDict2[samp]=Sample(**sampleDict[samp])

samples = Samples(**sampleDict2)
