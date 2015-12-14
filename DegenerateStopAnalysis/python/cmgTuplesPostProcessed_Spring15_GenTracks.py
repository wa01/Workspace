import copy, os, sys
#spring15_soft_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15/"
#spring15_inc_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15_vasile_v1/"
 
#sample_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_7412pass2_v2"
sample_path = "/afs/hephy.at/data/nrad01/cmgTuples/GenTracks_v0"


def makeSample(sample):
  i = copy.deepcopy(sample)
  i['dir']=i['dir']+'/inc/'
  #s = copy.deepcopy(sample)
  #s['dir']=s['dir']+'/soft/'
  #return {'inc':i, 'soft':s}
  return {'inc':i }



TTJetsHT800toInf=makeSample({\
"name" : "TTJets",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [

            #"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
            #"TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
            "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",

         ],
'dir' : sample_path
})

TTJetsHT0to600=makeSample({\
"name" : "TTJets",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
            "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
         ],
'dir' : sample_path+"/lhehtlow/"
})
TTJetsHT600to800=makeSample({\
"name" : "TTJets",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
              "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/"
         ],
'dir' : sample_path+"/lhehthi/"
})


#
#
#
#
#
#
WJetsHT=makeSample({\
"name" : "WJets",
"bins" : [
            "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
    

            #"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/",
        ],
'dir' : sample_path
})
WJetsInc=makeSample({\
"name" : "WJetsInc",
"bins" : [
            "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : sample_path
})



#ZJetsHT=makeSample({\
#"name" : "ZJets",
#"bins" : [
#            "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/"
#            "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/",
#            "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/",
#            "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/",
#            "ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/",
#        ],
#'dir' : sample_path
#})





allSignalStrings=[\
"T2DegStop_300_270",
]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : sample_path,
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")






allSignalStrings=[\
"T2DegStop_300_270",
]




############################################# DATA Samples ######################################################





MET_Run2015D_05Oct2015_v1              = makeSample({'dir':sample_path,  "name":"METblind",  "bins":  ["MET_Run2015D-05Oct2015-v1_Data25ns"    ]   } )
MET_Run2015D_PromptReco_v4             = makeSample({'dir':sample_path,  "name":"MET",  "bins":  ["MET_Run2015D-PromptReco-v4_Data25ns" ]   } )
SingleElectron_Run2015D_05Oct2015_v1   = makeSample({'dir':sample_path,  "name":"SingleElblind",  "bins":  ["SingleElectron_Run2015D-05Oct2015-v1_Data25ns" ]   } )
SingleElectron_Run2015D_PromptReco_v4  = makeSample({'dir':sample_path,  "name":"SingleEl",  "bins":  ["SingleElectron_Run2015D-PromptReco-v4_Data25ns" ]   } )
SingleMuon_Run2015D_05Oct2015_v1       = makeSample({'dir':sample_path,  "name":"SingleMublind",  "bins":  ["SingleMuon_Run2015D-05Oct2015-v1_Data25ns" ]   } )
SingleMuon_Run2015D_PromptReco_v4      = makeSample({'dir':sample_path,  "name":"SingleMu",  "bins":  ["SingleMuon_Run2015D-PromptReco-v4_Data25ns" ]   } )


for data in [ MET_Run2015D_05Oct2015_v1, MET_Run2015D_PromptReco_v4, SingleElectron_Run2015D_05Oct2015_v1, SingleElectron_Run2015D_PromptReco_v4, SingleMuon_Run2015D_05Oct2015_v1, SingleMuon_Run2015D_PromptReco_v4]:
  data.update({"dir":sample_path})
