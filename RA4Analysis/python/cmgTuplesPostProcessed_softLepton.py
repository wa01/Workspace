import copy, os, sys

def makeSample(sample):
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s}

ttJets=makeSample({\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})
WJetsHTToLNu=makeSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})
TTVH=makeSample({\
"name" : "TTVH",
"bins" : ["TTH", "TTWJets", "TTZJets"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})
singleTop=makeSample({\
"name" : "singleTop",
"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})
DY=makeSample({\
"name" : "DY",
"bins" : ["DYJetsToLL_M50_HT100to200", "DYJetsToLL_M50_HT200to400", "DYJetsToLL_M50_HT400to600", "DYJetsToLL_M50_HT600toInf"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})
QCD=makeSample({\
"name" : "QCD",
"bins" : ["QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
})


#T1qqqq_1400_325_300={\
#"name" : "T1qqqq_1400_325_300",
#"bins": ["T1qqqq_1400_325_300"],
#'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1200_1000_800={\
#"name" : "T5Full_1200_1000_800",
#"bins": ["T5Full_1200_1000_800"],
#'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1500_800_100={\
#"name" : "T5Full_1500_800_100",
#"bins": ["T5Full_1500_800_100"],
#'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v0/singleLepton/",
#}


allSignalStrings=[\
#"SMS_T1tttt_2J_mGl1200_mLSP800",
#"SMS_T1tttt_2J_mGl1500_mLSP100",
#"SMS_T2tt_2J_mStop425_mLSP325",
#"SMS_T2tt_2J_mStop500_mLSP325",
#"SMS_T2tt_2J_mStop650_mLSP325",
#"SMS_T2tt_2J_mStop850_mLSP100",
#"SMS_T5qqqqWW_Gl1200_Chi1000_LSP800",
#"SMS_T5qqqqWW_Gl1500_Chi800_LSP100",
#"T1ttbbWW_mGo1000_mCh725_mChi715",
#"T1ttbbWW_mGo1000_mCh725_mChi720",
#"T1ttbbWW_mGo1300_mCh300_mChi290",
#"T1ttbbWW_mGo1300_mCh300_mChi295",
#"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
#"T5ttttDeg_mGo1000_mStop300_mChi280",
#"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
#"T5ttttDeg_mGo1300_mStop300_mChi280",
"T5qqqqWWDeg_mGo800_mCh305_mChi300",
"T5qqqqWWDeg_mGo1000_mCh310_mChi300",
"T5qqqqWWDeg_mGo1000_mCh315_mChi300",
"T5qqqqWWDeg_mGo1000_mCh325_mChi300",
"T5qqqqWWDeg_mGo1400_mCh315_mChi300",
"T5qqqqWW_mGo1000_mCh800_mChi700",

]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : "/data/dspitzbart/cmgTuples/postProcessed_v1_Phys14V3/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")
  exec("allSignals.append(s)")
  
