import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_Spring15_GenTracks import *
from Workspace.DegenerateStopAnalysis.navidTools.Sample import Sample, Samples


#-------------------------



#data_lumi = data_lumi
mc_lumi   = 10000
#data_lumi_blinded = 1330
#data_lumi_blinded = 553.149950870
data_lumi_unblinded = 135.21
data_lumi_blinded = 1547.74

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
#WJetsHTSample.Add(T2DegSample)
#WJetsHTSample.Add(T2DegSample)

#ZJetsHTSample = getChain(ZJetsHT['inc'],histname='')






TTJetsHT0   =   getChain(TTJetsHT0to600['inc'],histname='') 
TTJetsHT1   =   getChain(TTJetsHT600to800['inc'],histname='')
TTJetsHT2   =   getChain(TTJetsHT800toInf['inc'],histname='')


TTJetsSample = TTJetsHT0.Clone()
TTJetsSample.Add(TTJetsHT1)
TTJetsSample.Add(TTJetsHT2)
##WJetsSample = getChain(WJetsInc['inc'],histname='')
#
#METDataOct05 = getChain(MET_Run2015D_05Oct2015_v1['inc'],histname='')
#METDataBlind       = getChain(MET_Run2015D_PromptReco_v4['inc'],histname='')
#METDataBlind.Add(METDataOct05)
#METDataUnblind = METDataBlind.CopyTree("run<=257599")
#



sampleDict={
          #'z':          {'tree':ZJetsHTSample         ,'name':'ZJets'     ,'color':ROOT.kSpring+10           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
          'w':          {'tree':WJetsHTSample         ,'name':'WJets'     ,'color':ROOT.kSpring-5           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
          "s":          {'tree':T2DegSample           ,'name':'S300_270'  ,'color':ROOT.kRed                , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
          #"d":          {'tree':METDataUnblind        ,'name':"data"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"weight":"(1)"  ,'lumi': data_lumi_unblinded  },
          #"dblind":     {'tree':METDataBlind          ,'name':"dblind" , 'color':ROOT.kBlack          , 'isSignal':0 ,'isData':1    ,"weight":"(1)"  ,'lumi': data_lumi_blinded  },
          'tt':         {'tree':TTJetsSample          ,'name':'TTJets'  ,'color':ROOT.kAzure-5              , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      }
       }

getWTau=False
if getWTau:
    print "Creating a sample for the Tau Component of WJets ... this might take some time"
    WTau=WJetsHTSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)>=1")
    WNoTau=WJetsHTSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)==0")
    sampleDict.update({
        'wtau':          {'tree':WTau    ,'name':'WTau'     ,'color':ROOT.kViolet           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      } ,
        'wnotau':          {'tree':WNoTau    ,'name':'WNoTau'     ,'color':ROOT.kViolet           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      }, 
        })


sampleDict2 = {}

for samp in sampleDict:
  sampleDict2[samp]=Sample(**sampleDict[samp])
samples = Samples(**sampleDict2)








