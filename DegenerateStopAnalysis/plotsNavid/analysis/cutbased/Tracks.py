import math
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.cuts import *



## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------







sr1Trk   = CutClass ("sr1Trks",    
                               [[ "nTracks_pt2_%s"%x,  "nTracks_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracks_pt2p5_%s"%x,  "nTracks_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracks_pt3_%s"%x,  "nTracks_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )
  

sr1TrkJ1   = CutClass ("sr1TrksJ1",    
                               [[ "nTracksOppJet1_pt2_%s"%x,    "nTracksOppJet1_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJet1_pt2p5_%s"%x,  "nTracksOppJet1_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJet1_pt3_%s"%x,    "nTracksOppJet1_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkJ12   = CutClass ("sr1TrksOppJ12",    
                               [[ "nTracksOppJet12_pt2_%s"%x,  "nTracksOppJet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJet12_pt2p5_%s"%x,  "nTracksOppJet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJet12_pt3_%s"%x,  "nTracksOppJet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkJAll   = CutClass ("sr1TrksOppJAll",    

                               [[ "nTracksOppJetAll_pt2_%s"%x,  "nTracksOppJetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJetAll_pt2p5_%s"%x,  "nTracksOppJetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOppJetAll_pt3_%s"%x,  "nTracksOppJetAll_3 > %s"%x     ] for x in range(12) ]

                  ,baseCut = sr1Loose,
                  )

sr1TrkOpp60JAll   = CutClass ("sr1TrksOpp60JAll",    
                               [[ "nTracksOpp60JetAll_pt2_%s"%x,  "nTracksOpp60JetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp60JetAll_pt2p5_%s"%x,  "nTracksOpp60JetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp60JetAll_pt3_%s"%x,  "nTracksOpp60JetAll_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkOpp90JAll   = CutClass ("sr1TrksOpp90JAll",    
                               [[ "nTracksOpp90JetAll_pt2_%s"%x,  "nTracksOpp90JetAll_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90JetAll_pt2p5_%s"%x,  "nTracksOpp90JetAll_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90JetAll_pt3_%s"%x,  "nTracksOpp90JetAll_3 > %s"%x     ] for x in range(12) ]
                  , baseCut = sr1Loose,
                  )

sr1TrkOpp90J12   = CutClass ("sr1TrksOpp90J12",    
                               [[ "nTracksOpp90Jet12_pt2_%s"%x,  "nTracksOpp90Jet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90Jet12_pt2p5_%s"%x,  "nTracksOpp90Jet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90Jet12_pt3_%s"%x,  "nTracksOpp90Jet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkOpp60J12   = CutClass ("sr1TrksOpp60J12",   
                               [[ "nTracksOpp60Jet12_pt2_%s"%x,  "nTracksOpp60Jet12_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp60Jet12_pt2p5_%s"%x,  "nTracksOpp60Jet12_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp60Jet12_pt3_%s"%x,  "nTracksOpp60Jet12_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )

sr1TrkOpp90J1   = CutClass ("sr1TrksOpp90J1",    
                               [[ "nTracksOpp90Jet1_pt2_%s"%x,  "nTracksOpp90Jet1_2 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90Jet1_pt2p5_%s"%x,  "nTracksOpp90Jet1_2p5 > %s"%x     ] for x in range(12) ]+
                               [[ "nTracksOpp90Jet1_pt3_%s"%x,  "nTracksOpp90Jet1_3 > %s"%x     ] for x in range(12) ]
                  ,baseCut = sr1Loose,
                  )


#import dmt
#
#dmtBM1Trk       = CutClass ("dmtR1Trk",
#                               [[ "nTracksOpp90Jet12_pt2_%s"%x,  "nTracksOpp90Jet12_2 > %s"%x     ] for x in range(12) ]+
#                               [[ "nTracksOpp90Jet12_pt2p5_%s"%x,  "nTracksOpp90Jet12_2p5 > %s"%x     ] for x in range(12) ]+
#                               [[ "nTracksOpp90Jet12_pt3_%s"%x,  "nTracksOpp90Jet12_3 > %s"%x     ] for x in range(12) ]
#                          
#                              ,baseCut = dmtBM1R1
#                          )
#




