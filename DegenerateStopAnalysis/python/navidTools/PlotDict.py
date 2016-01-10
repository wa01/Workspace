from Workspace.DegenerateStopAnalysis.navidTools.Plot import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
import ROOT

plotDict =\
      {
        #'LepPtCR':          {'var':"lepPt",         'name':"LepPtCR"    ,"bins":[30,30,300]              ,"decor":{"title":"LeptonPt", "x":"p_{T}(\mu)[GeV]"       ,"y":"Events"}  },
        #'LepPt':          {'var':"lepPt",         'name':"LepPt"    ,"bins":[8,0,40]              ,"decor":{"title":"LeptonPt", "x":"P_{T}(\mu)[GeV]"       ,"y":"Events"}  },
        #'MET':          {'var':"met",         'name':"MET"    ,"bins":[50,0,1000]              ,"decor":{"title":"MET", "x":"E_{T}^{miss} [GeV]"       ,"y":"Events"}  },
        #'MT':          {'var':"mt",         'name':"MT"    ,"bins":[20,0,140]              ,"decor":{"title":"MT", "x":"m_{T} [GeV]"       ,"y":"Events"}  },
        #'dmt':            {'var':"Q80:CosLMet",   'name':"DMT"      ,"bins":[20,-1,1,20,-3,1]     ,"decor":{"title":"DeconstMT","x":"CosLepMet","y":"Q80"   }  }, 




        "nTrks_1p5":           {'var':"ntrack_1p5",   'name':"nTrks_1p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"Track Count  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_2":           {'var':"ntrack_2",   'name':"nTrks_2"    ,"bins":[20,0,20]                                         ,"decor":{"title":"Track Count  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_2p5":           {'var':"ntrack_2p5",   'name':"nTrks_2p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"Track Count  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet1_1p5":           {'var':"ntrackOppJet1_1p5",   'name':"nTrksOppJet1_1p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Count Opp to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet1_2":           {'var':"ntrackOppJet1_2",   'name':"nTrksOppJet1_2"    ,"bins":[20,0,20]                       ,"decor":{"title":"Track Count Opp to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet1_2p5":           {'var':"ntrackOppJet1_2p5",   'name':"nTrksOppJet1_2p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Count Opp to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet12_1p5":           {'var':"ntrackOppJet12_1p5",   'name':"nTrksOppJet12_1p5"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Count Opp to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet12_2":           {'var':"ntrackOppJet12_2",   'name':"nTrksOppJet12_2"    ,"bins":[20,0,20]                    ,"decor":{"title":"Track Count Opp to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJet12_2p5":           {'var':"ntrackOppJet12_2p5",   'name':"nTrksOppJet12_2p5"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Count Opp to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJetAll_1p5":           {'var':"ntrackOppJetAll_1p5",   'name':"nTrksOppJetAll_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJetAll_2":           {'var':"ntrackOppJetAll_2",   'name':"nTrksOppJetAll_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Count Opp to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOppJetAll_2p5":           {'var':"ntrackOppJetAll_2p5",   'name':"nTrksOppJetAll_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nTrksOpp90Jet1_1p5":           {'var':"ntrackOpp90Jet1_1p5",   'name':"nTrksOpp90Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp90 to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90Jet1_2":           {'var':"ntrackOpp90Jet1_2",   'name':"nTrksOpp90Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Count Opp90 to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90Jet1_2p5":           {'var':"ntrackOpp90Jet1_2p5",   'name':"nTrksOpp90Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp90 to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90Jet12_1p5":           {'var':"ntrackOpp90Jet12_1p5",   'name':"nTrksOpp90Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Count Opp90 to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90Jet12_2":           {'var':"ntrackOpp90Jet12_2",   'name':"nTrksOpp90Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Count Opp90 to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90Jet12_2p5":           {'var':"ntrackOpp90Jet12_2p5",   'name':"nTrksOpp90Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Count Opp90 to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90JetAll_1p5":           {'var':"ntrackOpp90JetAll_1p5",   'name':"nTrksOpp90JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Count Opp90 to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90JetAll_2":           {'var':"ntrackOpp90JetAll_2",   'name':"nTrksOpp90JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp90 to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp90JetAll_2p5":           {'var':"ntrackOpp90JetAll_2p5",   'name':"nTrksOpp90JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Count Opp90 to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nTrksOpp60Jet1_1p5":           {'var':"ntrackOpp60Jet1_1p5",   'name':"nTrksOpp60Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp60 to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60Jet1_2":           {'var':"ntrackOpp60Jet1_2",   'name':"nTrksOpp60Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"Track Count Opp60 to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60Jet1_2p5":           {'var':"ntrackOpp60Jet1_2p5",   'name':"nTrksOpp60Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp60 to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60Jet12_1p5":           {'var':"ntrackOpp60Jet12_1p5",   'name':"nTrksOpp60Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Count Opp60 to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60Jet12_2":           {'var':"ntrackOpp60Jet12_2",   'name':"nTrksOpp60Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"Track Count Opp60 to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60Jet12_2p5":           {'var':"ntrackOpp60Jet12_2p5",   'name':"nTrksOpp60Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"Track Count Opp60 to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60JetAll_1p5":           {'var':"ntrackOpp60JetAll_1p5",   'name':"nTrksOpp60JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Count Opp60 to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60JetAll_2":           {'var':"ntrackOpp60JetAll_2",   'name':"nTrksOpp60JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"Track Count Opp60 to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrksOpp60JetAll_2p5":           {'var':"ntrackOpp60JetAll_2p5",   'name':"nTrksOpp60JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"Track Count Opp60 to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },







        "nGenTrks_1p5":           {'var':"nGenTrack_1p5",   'name':"nGenTrks_1p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"GenTrack Count  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_2":           {'var':"nGenTrack_2",   'name':"nGenTrks_2"    ,"bins":[20,0,20]                                         ,"decor":{"title":"GenTrack Count  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_2p5":           {'var':"nGenTrack_2p5",   'name':"nGenTrks_2p5"    ,"bins":[20,0,20]                                   ,"decor":{"title":"GenTrack Count  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet1_1p5":           {'var':"nGenTrackOppJet1_1p5",   'name':"nGenTrksOppJet1_1p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"GenTrack Count Opp to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet1_2":           {'var':"nGenTrackOppJet1_2",   'name':"nGenTrksOppJet1_2"    ,"bins":[20,0,20]                       ,"decor":{"title":"GenTrack Count Opp to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet1_2p5":           {'var':"nGenTrackOppJet1_2p5",   'name':"nGenTrksOppJet1_2p5"    ,"bins":[20,0,20]                 ,"decor":{"title":"GenTrack Count Opp to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet12_1p5":           {'var':"nGenTrackOppJet12_1p5",   'name':"nGenTrksOppJet12_1p5"    ,"bins":[20,0,20]              ,"decor":{"title":"GenTrack Count Opp to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet12_2":           {'var':"nGenTrackOppJet12_2",   'name':"nGenTrksOppJet12_2"    ,"bins":[20,0,20]                    ,"decor":{"title":"GenTrack Count Opp to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJet12_2p5":           {'var':"nGenTrackOppJet12_2p5",   'name':"nGenTrksOppJet12_2p5"    ,"bins":[20,0,20]              ,"decor":{"title":"GenTrack Count Opp to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJetAll_1p5":           {'var':"nGenTrackOppJetAll_1p5",   'name':"nGenTrksOppJetAll_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJetAll_2":           {'var':"nGenTrackOppJetAll_2",   'name':"nGenTrksOppJetAll_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"GenTrack Count Opp to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOppJetAll_2p5":           {'var':"nGenTrackOppJetAll_2p5",   'name':"nGenTrksOppJetAll_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nGenTrksOpp90Jet1_1p5":           {'var':"nGenTrackOpp90Jet1_1p5",   'name':"nGenTrksOpp90Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp90 to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90Jet1_2":           {'var':"nGenTrackOpp90Jet1_2",   'name':"nGenTrksOpp90Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"GenTrack Count Opp90 to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90Jet1_2p5":           {'var':"nGenTrackOpp90Jet1_2p5",   'name':"nGenTrksOpp90Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp90 to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90Jet12_1p5":           {'var':"nGenTrackOpp90Jet12_1p5",   'name':"nGenTrksOpp90Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"GenTrack Count Opp90 to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90Jet12_2":           {'var':"nGenTrackOpp90Jet12_2",   'name':"nGenTrksOpp90Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"GenTrack Count Opp90 to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90Jet12_2p5":           {'var':"nGenTrackOpp90Jet12_2p5",   'name':"nGenTrksOpp90Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"GenTrack Count Opp90 to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90JetAll_1p5":           {'var':"nGenTrackOpp90JetAll_1p5",   'name':"nGenTrksOpp90JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"GenTrack Count Opp90 to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90JetAll_2":           {'var':"nGenTrackOpp90JetAll_2",   'name':"nGenTrksOpp90JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp90 to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp90JetAll_2p5":           {'var':"nGenTrackOpp90JetAll_2p5",   'name':"nGenTrksOpp90JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"GenTrack Count Opp90 to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nGenTrksOpp60Jet1_1p5":           {'var':"nGenTrackOpp60Jet1_1p5",   'name':"nGenTrksOpp60Jet1_1p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp60 to Jet 1  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60Jet1_2":           {'var':"nGenTrackOpp60Jet1_2",   'name':"nGenTrksOpp60Jet1_2"    ,"bins":[20,0,20]                 ,"decor":{"title":"GenTrack Count Opp60 to Jet 1  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60Jet1_2p5":           {'var':"nGenTrackOpp60Jet1_2p5",   'name':"nGenTrksOpp60Jet1_2p5"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp60 to Jet 1  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60Jet12_1p5":           {'var':"nGenTrackOpp60Jet12_1p5",   'name':"nGenTrksOpp60Jet12_1p5"    ,"bins":[20,0,20]        ,"decor":{"title":"GenTrack Count Opp60 to Jet 1&2  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60Jet12_2":           {'var':"nGenTrackOpp60Jet12_2",   'name':"nGenTrksOpp60Jet12_2"    ,"bins":[20,0,20]              ,"decor":{"title":"GenTrack Count Opp60 to Jet 1&2  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60Jet12_2p5":           {'var':"nGenTrackOpp60Jet12_2p5",   'name':"nGenTrksOpp60Jet12_2p5"    ,"bins":[20,0,20]        ,"decor":{"title":"GenTrack Count Opp60 to Jet 1&2  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60JetAll_1p5":           {'var':"nGenTrackOpp60JetAll_1p5",   'name':"nGenTrksOpp60JetAll_1p5"    ,"bins":[20,0,20]     ,"decor":{"title":"GenTrack Count Opp60 to Jet All  TrkPt > 1.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60JetAll_2":           {'var':"nGenTrackOpp60JetAll_2",   'name':"nGenTrksOpp60JetAll_2"    ,"bins":[20,0,20]           ,"decor":{"title":"GenTrack Count Opp60 to Jet All  TrkPt > 2.0"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrksOpp60JetAll_2p5":           {'var':"nGenTrackOpp60JetAll_2p5",   'name':"nGenTrksOpp60JetAll_2p5"    ,"bins":[20,0,20]     ,"decor":{"title":"GenTrack Count Opp60 to Jet All  TrkPt > 2.5"  ,"x":"Track Multiplicity","y":"nEvents"   }  },




        #'tauMu_dmt':    {'var':lepTauDmt,          "presel":"(1)", "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":"{SAMPLE}_dmt_{CUT}"    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0 ,"zLog":1        },
      }


plotDict2={}
for p in plotDict:
  plotDict2[p]=Plot(**plotDict[p])

plots=Plots(**plotDict2)



