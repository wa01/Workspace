import copy, os, sys


data_ele={\
"name" : "SingleElectron_Run2015B",
"chunkString" : "SingleElectron_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_mu={\
"name" : "SingleMuon_Run2015B",
"chunkString" : "SingleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir' : "/data/easilar/cmgTuples/",
}

DYJetsToLL_M_50={\
"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dir':"/data/easilar/cmgTuples/crab_Spring15/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dbsName':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT100to200={\
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT200to400={\
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT400to600={\
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600toInf={\
"name" : "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_sch={\
"name" : "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"chunkString":"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dbsName" : "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch={\
"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"chunkString":"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dbsName" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch={\
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"chunkString":"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dbsName" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch={\
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"chunkString":"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dbsName" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TTJets={\
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dbsName" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
