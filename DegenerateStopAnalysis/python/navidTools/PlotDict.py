from Workspace.DegenerateStopAnalysis.navidTools.Plot import Plot, Plots
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import makeDecorHistFunc, makeDecorAxisFunc
import ROOT

plotDict =\
      {
        'LepPt':          {'var':"lepPt",         'name':"LepPt"    ,"bins":[5,0,35]              ,"decor":{"title":"LeptonPt", "x":"Pt"       ,"y":"Events"}  },
        'dmt':            {'var':"Q80:CosLMet",   'name':"DMT"      ,"bins":[20,-1,1,20,-3,1]     ,"decor":{"title":"DeconstMT","x":"CosLepMet","y":"Q80"   }  }, 

        "nTrk_1p5":           {'var':"ntrack_1p5",   'name':"nTrks_1p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"Track Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrk_2":           {'var':"ntrack_2",   'name':"nTrks_2"    ,"bins":[20,0,20]                                         ,"decor":{"title":"Track Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrk_2p5":           {'var':"ntrack_2p5",   'name':"nTrks_2p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"Track Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ1_1p5":           {'var':"ntrackOppJet1_1p5",   'name':"nTrksOppJet1_1p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Opp to Jet 1 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ1_2":           {'var':"ntrackOppJet1_2",   'name':"nTrksOppJet1_2"    ,"bins":[20,0,20]                       ,"decor":{"title":"Track Opp to Jet 1 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ1_2p5":           {'var':"ntrackOppJet1_2p5",   'name':"nTrksOppJet1_2p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Opp to Jet 1 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ12_1p5":           {'var':"ntrackOppJet12_1p5",   'name':"nTrksOppJet12_1p5"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Opp to Jet 1&2 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ12_2":           {'var':"ntrackOppJet12_2",   'name':"nTrksOppJet12_2"    ,"bins":[20,0,20]                    ,"decor":{"title":"Track Opp to Jet 1&2 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJ12_2p5":           {'var':"ntrackOppJet12_2p5",   'name':"nTrksOppJet12_2p5"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Opp to Jet 1&2 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJAll_1p5":           {'var':"ntrackOppJetAll_1p5",   'name':"nTrksOppJetAll_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp to Jet All Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJAll_2":           {'var':"ntrackOppJetAll_2",   'name':"nTrksOppJetAll_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Opp to Jet All Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOppJAll_2p5":           {'var':"ntrackOppJetAll_2p5",   'name':"nTrksOppJetAll_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp to Jet All Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },

        "nTrkOpp90J1_1p5":           {'var':"ntrackOpp90Jet1_1p5",   'name':"nTrksOpp90Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp90 to Jet 1 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90J1_2":           {'var':"ntrackOpp90Jet1_2",   'name':"nTrksOpp90Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Opp90 to Jet 1 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90J1_2p5":           {'var':"ntrackOpp90Jet1_2p5",   'name':"nTrksOpp90Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp90 to Jet 1 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90J12_1p5":           {'var':"ntrackOpp90Jet12_1p5",   'name':"nTrksOpp90Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Opp90 to Jet 1&2 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90J12_2":           {'var':"ntrackOpp90Jet12_2",   'name':"nTrksOpp90Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Opp90 to Jet 1&2 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90J12_2p5":           {'var':"ntrackOpp90Jet12_2p5",   'name':"nTrksOpp90Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Opp90 to Jet 1&2 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90JAll_1p5":           {'var':"ntrackOpp90JetAll_1p5",   'name':"nTrksOpp90JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Opp90 to Jet All Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90JAll_2":           {'var':"ntrackOpp90JetAll_2",   'name':"nTrksOpp90JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp90 to Jet All Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp90JAll_2p5":           {'var':"ntrackOpp90JetAll_2p5",   'name':"nTrksOpp90JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Opp90 to Jet All Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },

        "nTrkOpp60J1_1p5":           {'var':"ntrackOpp60Jet1_1p5",   'name':"nTrksOpp60Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp60 to Jet 1 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60J1_2":           {'var':"ntrackOpp60Jet1_2",   'name':"nTrksOpp60Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Opp60 to Jet 1 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60J1_2p5":           {'var':"ntrackOpp60Jet1_2p5",   'name':"nTrksOpp60Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp60 to Jet 1 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60J12_1p5":           {'var':"ntrackOpp60Jet12_1p5",   'name':"nTrksOpp60Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Opp60 to Jet 1&2 Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60J12_2":           {'var':"ntrackOpp60Jet12_2",   'name':"nTrksOpp60Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Opp60 to Jet 1&2 Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60J12_2p5":           {'var':"ntrackOpp60Jet12_2p5",   'name':"nTrksOpp60Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Opp60 to Jet 1&2 Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60JAll_1p5":           {'var':"ntrackOpp60JetAll_1p5",   'name':"nTrksOpp60JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Opp60 to Jet All Multip pt > 1.5"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60JAll_2":           {'var':"ntrackOpp60JetAll_2",   'name':"nTrksOpp60JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Opp60 to Jet All Multip pt > 2.0"  ,"x":"nTrks","y":"nEvents"   }  },
        "nTrkOpp60JAll_2p5":           {'var':"ntrackOpp60JetAll_2p5",   'name':"nTrksOpp60JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Opp60 to Jet All Multip pt > 2.5"  ,"x":"nTrks","y":"nEvents"   }  },




        #'tauMu_dmt':    {'var':lepTauDmt,          "presel":"(1)", "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":"{SAMPLE}_dmt_{CUT}"    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0 ,"zLog":1        },
      }


plotDict2={}
for p in plotDict:
  plotDict2[p]=Plot(**plotDict[p])

plots=Plots(**plotDict2)



