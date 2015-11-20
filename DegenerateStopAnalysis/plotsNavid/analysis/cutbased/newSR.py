from dmt import *
from tracks import *
from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2 import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from limitCalc import *
from makeTable import *

tableDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/newVars/tables/"


sr1Trks = CutClass( "sr1Trks" , [ 
                      ["ntrackOppJet12_2p5_5", "ntrackOppJet12_2p5  > 4"],
                               ],
                    baseCut = sr1Loose,
                  )



bm1 = qcosRegionBM1



dmt = CutClass ("dmt", [
                              #["r1","r1BM1"   ],
                                  ["r1_pt1",joinCutStrings([ bm1.r1cut,   btw("lepPt",5,12)]  )],
                                  ["r1_pt2",joinCutStrings([ bm1.r1cut,   btw("lepPt",12,20)] )],
                                  ["r1_pt3",joinCutStrings([ bm1.r1cut,   btw("lepPt",20,30)] )],
                              #["r2","r2BM1"   ],
                                  ["r2_pt1",joinCutStrings([ bm1.r2cut,   btw("lepPt",5,12)]  )],
                                  ["r2_pt2",joinCutStrings([ bm1.r2cut,   btw("lepPt",12,20)] )],
                                  ["r2_pt3",joinCutStrings([ bm1.r2cut,   btw("lepPt",20,30)] )],
                              #["r3","r3BM1"   ],
                                  ["r3_pt1",joinCutStrings([ bm1.r3cut,   btw("lepPt",5,12)]  )],
                                  ["r3_pt2",joinCutStrings([ bm1.r3cut,   btw("lepPt",12,20)] )],
                                  ["r3_pt3",joinCutStrings([ bm1.r3cut,   btw("lepPt",20,30)] )],
                              #  ["rej",   bm1.rej   ],
                                  ["rej_pt1",joinCutStrings([ bm1.rej,   btw("lepPt",5,12)]  )],
                                  ["rej_pt2",joinCutStrings([ bm1.rej,   btw("lepPt",12,20)] )],
                                  ["rej_pt3",joinCutStrings([ bm1.rej,   btw("lepPt",20,30)] )],

                            ] ,
                baseCut=sr1Loose,
                )


newSR = CutClass ("newSR", [
                              ["ntrackOppJet12_2p5_5", "ntrackOppJet12_2p5  > 5"],
                              #["r1","r1BM1"   ],
                                  ["r1_pt1",joinCutStrings([ bm1.r1cut,   btw("lepPt",5,12)]  )],
                                  ["r1_pt2",joinCutStrings([ bm1.r1cut,   btw("lepPt",12,20)] )],
                                  ["r1_pt3",joinCutStrings([ bm1.r1cut,   btw("lepPt",20,30)] )],
                              #["r2","r2BM1"   ],
                                  ["r2_pt1",joinCutStrings([ bm1.r2cut,   btw("lepPt",5,12)]  )],
                                  ["r2_pt2",joinCutStrings([ bm1.r2cut,   btw("lepPt",12,20)] )],
                                  ["r2_pt3",joinCutStrings([ bm1.r2cut,   btw("lepPt",20,30)] )],
                              #["r3","r3BM1"   ],
                                  ["r3_pt1",joinCutStrings([ bm1.r3cut,   btw("lepPt",5,12)]  )],
                                  ["r3_pt2",joinCutStrings([ bm1.r3cut,   btw("lepPt",12,20)] )],
                                  ["r3_pt3",joinCutStrings([ bm1.r3cut,   btw("lepPt",20,30)] )],
                              #  ["rej",   bm1.rej   ],
                                  ["rej_pt1",joinCutStrings([ bm1.rej,   btw("lepPt",5,12)]  )],
                                  ["rej_pt2",joinCutStrings([ bm1.rej,   btw("lepPt",12,20)] )],
                                  ["rej_pt3",joinCutStrings([ bm1.rej,   btw("lepPt",20,30)] )],

                            ] ,
                baseCut=sr1Loose,
                )



dmtTrks = CutClass ("dmtTrks", [
                              #["r1","r1BM1"   ],
                                  ["r1_pt1",joinCutStrings([ bm1.r1cut,   btw("lepPt",5,12)]  )],
                                  ["r1_pt2",joinCutStrings([ bm1.r1cut,   btw("lepPt",12,20)] )],
                                  ["r1_pt3",joinCutStrings([ bm1.r1cut,   btw("lepPt",20,30)] )],
                              #["r2","r2BM1"   ],
                                  ["r2_pt1",joinCutStrings([ bm1.r2cut,   btw("lepPt",5,12)]  )],
                                  ["r2_pt2",joinCutStrings([ bm1.r2cut,   btw("lepPt",12,20)] )],
                                  ["r2_pt3",joinCutStrings([ bm1.r2cut,   btw("lepPt",20,30)] )],
                              #["r3","r3BM1"   ],
                                  ["r3_pt1",joinCutStrings([ bm1.r3cut,   btw("lepPt",5,12)]  )],
                                  ["r3_pt2",joinCutStrings([ bm1.r3cut,   btw("lepPt",12,20)] )],
                                  ["r3_pt3",joinCutStrings([ bm1.r3cut,   btw("lepPt",20,30)] )],
                              #  ["rej",   bm1.rej   ],
                                  ["rej_pt1",joinCutStrings([ bm1.rej,   btw("lepPt",5,12)]  )],
                                  ["rej_pt2",joinCutStrings([ bm1.rej,   btw("lepPt",12,20)] )],
                                  ["rej_pt3",joinCutStrings([ bm1.rej,   btw("lepPt",20,30)] )],

                            ] ,
                baseCut=sr1Trks,
                )



yDict={}
lDict={}

if __name__ == "__main__":
  setEventListToChains(samples,['w','s'],sr1Loose)
  yDict['dmtTrks']=Yields(samples,["w","s"],dmtTrks, "list",pklOpt=True, pklDir="./pkl/newSR/") 
  JinjaTexTable( yDict['dmtTrks'] ,pdfDir = tableDir)
  lDict['dmtTrks'] = getLimit(  yDict['dmtTrks'] )

  yDict['newSR']=Yields(samples,["w","s"],newSR, "list",pklOpt=True, pklDir="./pkl/newSR/") 
  JinjaTexTable( yDict['newSR'],pdfDir = tableDir )
  lDict['newSR'] = getLimit(  yDict['newSR'] )

  yDict['dmt']=Yields(samples,["w","s"],dmt, "list",pklOpt=True, pklDir="./pkl/newSR/") 
  JinjaTexTable( yDict['dmt'],pdfDir = tableDir )
  lDict['dmt'] = getLimit(  yDict['dmt'] )


  yDict['sr1abc']=Yields(samples,["w","s"],sr1abc, "list",pklOpt=True, pklDir="./pkl/newSR/")
  JinjaTexTable( yDict['sr1abc'] ,pdfDir = tableDir)
  lDict['sr1abc'] = getLimit( yDict['sr1abc'] )


