#data_path = "/data/nrad/cmgTuples/RunII/7412pass2/Data25ns" 
data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v2/Data25nsRun2015D_Nov13Json"


SingleMuon_Run2015D_v4 ={\
"chunkString":"",
"name" : "SingleMuon_Run2015D-PromptReco-v4_Data25ns",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}

SingleMuon_Run2015D_05Oct ={\
"chunkString":"",
"name" : "SingleMuon_Run2015D-05Oct2015-v1_Data25ns",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}

SingleElectron_Run2015D_v4 ={\
"chunkString":"",
"name" : "SingleElectron_Run2015D-PromptReco-v4_Data25ns",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
SingleElectron_Run2015D_05Oct ={\
"chunkString":"",
"name" : "SingleElectron_Run2015D-05Oct2015-v1_Data25ns",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
MET_Run2015D_v4 ={\
"chunkString":"",
"name" : "MET_Run2015D-PromptReco-v4_Data25ns",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
MET_Run2015D_05Oct ={\
"chunkString":"",
"name" : "MET_Run2015D-05Oct2015-v1_Data25ns",
"dir": data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True,
}


samples = [MET_Run2015D_05Oct, MET_Run2015D_v4, SingleElectron_Run2015D_05Oct, SingleElectron_Run2015D_v4, SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_v4]

for sample in samples:
  sample['dir'] = sample['dir']+"/"+sample['name']







