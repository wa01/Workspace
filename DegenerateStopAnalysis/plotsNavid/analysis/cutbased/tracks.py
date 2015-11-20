import math
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.cuts import *



## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------





sr1Trk   = CutClass ("sr1Trks",    [
                               ["ntracks_1_3", "ntracks_1 > 3"],
                               ["ntracks_1_5", "ntracks_1  > 5"],
                               ["ntracks_1_7", "ntracks_1 > 7"],
                               ["ntracks_1_9", "ntracks_1 > 9"],
                               ["ntracks_1_11","ntracks_1 > 11"],
                               ["ntracks_1_13","ntracks_1 > 13"],
                               ["ntracks_1_15","ntracks_1 > 15"],
                               ["ntracks_1_17","ntracks_1 > 17"],

                               ["ntracks_2_3", "ntracks_2 > 3"],
                               ["ntracks_2_5", "ntracks_2  > 5"],
                               ["ntracks_2_7", "ntracks_2 > 7"],
                               ["ntracks_2_9", "ntracks_2 > 9"],
                               ["ntracks_2_11","ntracks_2 > 11"],
                               ["ntracks_2_13","ntracks_2 > 13"],
                               ["ntracks_2_15","ntracks_2 > 15"],
                               ["ntracks_2_17","ntracks_2 > 17"],

                               ["ntracks_2p5_3", "ntracks_2p5 > 3"],
                               ["ntracks_2p5_5", "ntracks_2p5  > 5"],
                               ["ntracks_2p5_7", "ntracks_2p5 > 7"],
                               ["ntracks_2p5_9", "ntracks_2p5 > 9"],
                               ["ntracks_2p5_11","ntracks_2p5 > 11"],
                               ["ntracks_2p5_13","ntracks_2p5 > 13"],
                               ["ntracks_2p5_15","ntracks_2p5 > 15"],
                               ["ntracks_2p5_17","ntracks_2p5 > 17"],
                           ] , 
                  baseCut = sr1Loose,
                  )


  

sr1TrkJ1   = CutClass ("sr1TrksJ1",    [
                               ["ntrackOppJet1_1_3", "ntrackOppJet1_1 > 3"],
                               ["ntrackOppJet1_1_5", "ntrackOppJet1_1  > 5"],
                               ["ntrackOppJet1_1_7", "ntrackOppJet1_1 > 7"],
                               ["ntrackOppJet1_1_9", "ntrackOppJet1_1 > 9"],
                               ["ntrackOppJet1_1_11","ntrackOppJet1_1 > 11"],
                               ["ntrackOppJet1_1_13","ntrackOppJet1_1 > 13"],
                               ["ntrackOppJet1_1_15","ntrackOppJet1_1 > 15"],
                               ["ntrackOppJet1_1_17","ntrackOppJet1_1 > 17"],

                               ["ntrackOppJet1_2_3", "ntrackOppJet1_2 > 3"],
                               ["ntrackOppJet1_2_5", "ntrackOppJet1_2  > 5"],
                               ["ntrackOppJet1_2_7", "ntrackOppJet1_2 > 7"],
                               ["ntrackOppJet1_2_9", "ntrackOppJet1_2 > 9"],
                               ["ntrackOppJet1_2_11","ntrackOppJet1_2 > 11"],
                               ["ntrackOppJet1_2_13","ntrackOppJet1_2 > 13"],
                               ["ntrackOppJet1_2_15","ntrackOppJet1_2 > 15"],
                               ["ntrackOppJet1_2_17","ntrackOppJet1_2 > 17"],

                               ["ntrackOppJet1_2p5_3", "ntrackOppJet1_2p5 > 3"],
                               ["ntrackOppJet1_2p5_5", "ntrackOppJet1_2p5  > 5"],
                               ["ntrackOppJet1_2p5_7", "ntrackOppJet1_2p5 > 7"],
                               ["ntrackOppJet1_2p5_9", "ntrackOppJet1_2p5 > 9"],
                               ["ntrackOppJet1_2p5_11","ntrackOppJet1_2p5 > 11"],
                               ["ntrackOppJet1_2p5_13","ntrackOppJet1_2p5 > 13"],
                               ["ntrackOppJet1_2p5_15","ntrackOppJet1_2p5 > 15"],
                               ["ntrackOppJet1_2p5_17","ntrackOppJet1_2p5 > 17"],
                           ] , 
                  baseCut = sr1Loose,
                  )






sr1TrkJ12   = CutClass ("sr1TrksOppJ12",    [
                               ["ntrackOppJet12_1_3", "ntrackOppJet12_1 > 3"],
                               ["ntrackOppJet12_1_5", "ntrackOppJet12_1  > 5"],
                               ["ntrackOppJet12_1_7", "ntrackOppJet12_1 > 7"],
                               ["ntrackOppJet12_1_9", "ntrackOppJet12_1 > 9"],
                               ["ntrackOppJet12_1_11","ntrackOppJet12_1 > 11"],
                               ["ntrackOppJet12_1_13","ntrackOppJet12_1 > 13"],
                               ["ntrackOppJet12_1_15","ntrackOppJet12_1 > 15"],
                               ["ntrackOppJet12_1_17","ntrackOppJet12_1 > 17"],
                               ["ntrackOppJet12_2_3", "ntrackOppJet12_2 > 3"],
                               ["ntrackOppJet12_2_5", "ntrackOppJet12_2  > 5"],
                               ["ntrackOppJet12_2_7", "ntrackOppJet12_2 > 7"],
                               ["ntrackOppJet12_2_9", "ntrackOppJet12_2 > 9"],
                               ["ntrackOppJet12_2_11","ntrackOppJet12_2 > 11"],
                               ["ntrackOppJet12_2_13","ntrackOppJet12_2 > 13"],
                               ["ntrackOppJet12_2_15","ntrackOppJet12_2 > 15"],
                               ["ntrackOppJet12_2_17","ntrackOppJet12_2 > 17"],
                               ["ntrackOppJet12_2p5_3", "ntrackOppJet12_2p5 > 3"],
                               ["ntrackOppJet12_2p5_5", "ntrackOppJet12_2p5  > 5"],
                               ["ntrackOppJet12_2p5_7", "ntrackOppJet12_2p5 > 7"],
                               ["ntrackOppJet12_2p5_9", "ntrackOppJet12_2p5 > 9"],
                               ["ntrackOppJet12_2p5_11","ntrackOppJet12_2p5 > 11"],
                               ["ntrackOppJet12_2p5_13","ntrackOppJet12_2p5 > 13"],
                               ["ntrackOppJet12_2p5_15","ntrackOppJet12_2p5 > 15"],
                               ["ntrackOppJet12_2p5_17","ntrackOppJet12_2p5 > 17"],
                           ] , 
                  baseCut = sr1Loose,
                  )


sr1TrkJAll   = CutClass ("sr1TrksOppJAll",    [
                               ["ntrackOppJetAll_1_3", "ntrackOppJetAll_1 > 3"],
                               ["ntrackOppJetAll_1_5", "ntrackOppJetAll_1  > 5"],
                               ["ntrackOppJetAll_1_7", "ntrackOppJetAll_1 > 7"],
                               ["ntrackOppJetAll_1_9", "ntrackOppJetAll_1 > 9"],
                               ["ntrackOppJetAll_1_11","ntrackOppJetAll_1 > 11"],
                               ["ntrackOppJetAll_1_13","ntrackOppJetAll_1 > 13"],
                               ["ntrackOppJetAll_1_15","ntrackOppJetAll_1 > 15"],
                               ["ntrackOppJetAll_1_17","ntrackOppJetAll_1 > 17"],
                               ["ntrackOppJetAll_2_3", "ntrackOppJetAll_2 > 3"],
                               ["ntrackOppJetAll_2_5", "ntrackOppJetAll_2  > 5"],
                               ["ntrackOppJetAll_2_7", "ntrackOppJetAll_2 > 7"],
                               ["ntrackOppJetAll_2_9", "ntrackOppJetAll_2 > 9"],
                               ["ntrackOppJetAll_2_11","ntrackOppJetAll_2 > 11"],
                               ["ntrackOppJetAll_2_13","ntrackOppJetAll_2 > 13"],
                               ["ntrackOppJetAll_2_15","ntrackOppJetAll_2 > 15"],
                               ["ntrackOppJetAll_2_17","ntrackOppJetAll_2 > 17"],
                               ["ntrackOppJetAll_2p5_3", "ntrackOppJetAll_2p5 > 3"],
                               ["ntrackOppJetAll_2p5_5", "ntrackOppJetAll_2p5  > 5"],
                               ["ntrackOppJetAll_2p5_7", "ntrackOppJetAll_2p5 > 7"],
                               ["ntrackOppJetAll_2p5_9", "ntrackOppJetAll_2p5 > 9"],
                               ["ntrackOppJetAll_2p5_11","ntrackOppJetAll_2p5 > 11"],
                               ["ntrackOppJetAll_2p5_13","ntrackOppJetAll_2p5 > 13"],
                               ["ntrackOppJetAll_2p5_15","ntrackOppJetAll_2p5 > 15"],
                               ["ntrackOppJetAll_2p5_17","ntrackOppJetAll_2p5 > 17"],
                           ] , 
                  baseCut = sr1Loose,
                  )
