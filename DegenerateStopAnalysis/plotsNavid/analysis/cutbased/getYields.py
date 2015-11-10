from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.navidPlotTools import setEventListToChains
from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import sampleDict


from makeTable import *

yields=[
            #{ "name":"presel",  "cut":presel,     "opt":"flow" },
            { "name":"sr1",     "cut":sr1,        "opt":"flow" },
            { "name":"sr1abc",  "cut":sr1abc,     "opt":"list" },
            { "name":"sr2",     "cut":sr2,        "opt":"flow" },
            { "name":"sr2pt",     "cut":sr2pt,        "opt":"list" },
         ]


if False:
  setEventListToChains(sampleDict,['tt','w','s'], presel.combinedList)

  for yDict in yields:
    yDict['y']=Yields( sampleDict,['tt', 'w','s'], yDict['cut'] , cutOpt=yDict['opt'] ,tableName='{cut}',pklOpt=3)
    #yDict['y']=pickle.load(open("./pkl/YieldInstance_%s.pkl"%yDict['cut'].name,"rb"))
    yDict['table']=JinjaTexTable(yDict['y'])


if False:

  yieldDict={}

  #cutInst=presel
  #setEventListToChains(sampleDict,['tt','w','s'], cutInst.baseCut)
  #y=Yields(sampleDict,['tt', 'w','s'],cutInst,tableName='{cut}',pklOpt=3);
  cutInst=sr1
  setEventListToChains(sampleDict,['tt','w','s'], cutInst.baseCut)
  yields[cutInst.name]={}
  y=pickle.load(open("./pkl/YieldInstance_sr1.pkl","rb"))
  #yields[cutInst.name]['y']=Yields(sampleDict,['tt', 'w','s'],cutInst,tableName='{cut}',pklOpt=3);
  yields[cutInst.name]['table'] = JinjaTexTable(y)

  

