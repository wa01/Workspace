import math
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.cuts import *



## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------





sr1Trk   = CutClass ("sr1Trks",    
                               [[ "ntrack_pt2_%s"%x,  "ntrack_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrack_pt2p5_%s"%x,  "ntrack_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrack_pt3_%s"%x,  "ntrack_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )


  

sr1TrkJ1   = CutClass ("sr1TrksJ1",    
                               [[ "ntrackOppJet1_pt2_%s"%x,    "ntrackOppJet1_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJet1_pt2p5_%s"%x,  "ntrackOppJet1_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJet1_pt3_%s"%x,    "ntrackOppJet1_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )






sr1TrkJ12   = CutClass ("sr1TrksOppJ12",    
                               [[ "ntrackOppJet12_pt2_%s"%x,  "ntrackOppJet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJet12_pt2p5_%s"%x,  "ntrackOppJet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJet12_pt3_%s"%x,  "ntrackOppJet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkJAll   = CutClass ("sr1TrksOppJAll",    

                               [[ "ntrackOppJetAll_pt2_%s"%x,  "ntrackOppJetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJetAll_pt2p5_%s"%x,  "ntrackOppJetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOppJetAll_pt3_%s"%x,  "ntrackOppJetAll_3 > %s"%x     ] for x in range(12) ]

                  ,baseCut = sr1Loose,
                  )



sr1TrkOpp60JAll   = CutClass ("sr1TrksOpp60JAll",    
                               [[ "ntrackOpp60JetAll_pt2_%s"%x,  "ntrackOpp60JetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp60JetAll_pt2p5_%s"%x,  "ntrackOpp60JetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp60JetAll_pt3_%s"%x,  "ntrackOpp60JetAll_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkOpp90JAll   = CutClass ("sr1TrksOpp90JAll",    
                               [[ "ntrackOpp90JetAll_pt2_%s"%x,  "ntrackOpp90JetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90JetAll_pt2p5_%s"%x,  "ntrackOpp90JetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90JetAll_pt3_%s"%x,  "ntrackOpp90JetAll_3 > %s"%x     ] for x in range(12) ]
                  , baseCut = sr1Loose,
                  )



sr1TrkOpp90J12   = CutClass ("sr1TrksOpp90J12",    
                               [[ "ntrackOpp90Jet12_pt2_%s"%x,  "ntrackOpp90Jet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet12_pt2p5_%s"%x,  "ntrackOpp90Jet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet12_pt3_%s"%x,  "ntrackOpp90Jet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )




sr1TrkOpp60J12   = CutClass ("sr1TrksOpp60J12",   
                               [[ "ntrackOpp60Jet12_pt2_%s"%x,  "ntrackOpp60Jet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp60Jet12_pt2p5_%s"%x,  "ntrackOpp60Jet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp60Jet12_pt3_%s"%x,  "ntrackOpp60Jet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )




sr1TrkOpp90J1   = CutClass ("sr1TrksOpp90J1",    
                               [[ "ntrackOpp90Jet1_pt2_%s"%x,  "ntrackOpp90Jet1_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet1_pt2p5_%s"%x,  "ntrackOpp90Jet1_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet1_pt3_%s"%x,  "ntrackOpp90Jet1_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )



import dmt

dmtBM1Trk       = CutClass ("dmtR1Trk",
                               [[ "ntrackOpp90Jet12_pt2_%s"%x,  "ntrackOpp90Jet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet12_pt2p5_%s"%x,  "ntrackOpp90Jet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "ntrackOpp90Jet12_pt3_%s"%x,  "ntrackOpp90Jet12_3 > %s"%x     ] for x in range(12) ]
                          
                              ,baseCut = dmtBM1R1
                          )





