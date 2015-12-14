from Workspace.DegenerateStopAnalysis.navidTools.Plot import Plot, Plots
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import makeDecorHistFunc, makeDecorAxisFunc
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.cuts import *


import ROOT
import math



hemiList    =   [ 180, 90, 60 ]
hemicos=lambda x: round( math.cos(math.pi- 0.5*(x* math.pi/180)),3)
cosines = {  x:hemicos(x) for x in hemiList }   ### corresponding to 90, 135, 150 degree diff between jet and track


def trackCut(trk="Tracks",trkPt=2.5,trkEta=2.5 ,pdgs=[13],jetPt=30,jetOpt="",dxy=0.2, dz=0.2, hemi=0, opp="12"):
    trackCuts = []
    if trk=="Tracks":
        jt= "Jet"
        if dz:
            trackCuts.append("abs(Tracks_dz)<%s"%dz)
        if dxy:
            trackCuts.append("abs(Tracks_dxy)<%s"%dxy)
    elif trk=="GenTracks":
        jt= "GenJet"
    trackCuts.extend(["abs(%s_pdgId)!=%s"%(trk,pdgId) for pdgId in pdgs])
    trackCuts.append( "%s_pt>%s"%(trk,trkPt)   )
    trackCuts.append( "%s_eta<%s"%(trk,trkEta) )

    if hemi and opp:
        if not opp in ["12", "1", "All"] : assert False 
        trackCuts.append( "{trk}_CosPhiJet{opp} < {hemicos}".format(trk=trk,opp=opp, hemicos=hemicos(hemi) ) ) 
    if jetOpt.lower()=='veto':  ## veto tracks associated to a jet with pt greater than jetpt
        trackCuts.append( "({trk}_matchedJetDr > 0.4 || {jt}_pt[{trk}_matchedJetIndex] < {jetPt} )".format( jt=jt ,trk=trk, jetPt=jetPt))
    elif jetOpt.lower()=='only':  ## only include tracks associated to a jet with pt greater than jetPt
        trackCuts.append( "({trk}_matchedJetDr >=0.4 || {jt}_pt[{trk}_matchedJetIndex] >= {jetPt} )".format( jt=jt ,trk=trk, jetPt=jetPt))
    #trackCuts.append( "( {%s}_CosPhiJet12 < 0.5  )" )
    return "(%s)"%" && ".join(trackCuts) 


def trkSelName ( d ):
    name = "n{trk}_Pt{trkPt}_{jetOpt}JetTrks_Opp{hemi}Jet{opp}".format( **d) 
    name = name.replace(".","p")
    #name = "n{trk}_Pt{trkPt}_{jetOpt}Jets_Opp{hemi}Jet{opp}".format( trk=trk, trkPt=trkPt, jetPt=jetPt, jetOpt=jetOpt, hemi=hemi, opp=opp )
    return name

def nTracks(trk="Tracks",trkPt=2.5,trkEta=2.5 ,pdgs=[13],jetPt=30,jetOpt="veto",dxy=0.1, dz=0.1, hemi=0, opp="12",makeName=False, gt=None):
    trackCuts = trackCut(trk=trk,trkPt=trkPt, trkEta=trkEta, pdgs=pdgs, jetPt=jetPt,jetOpt=jetOpt, dxy=dxy, dz=dz, hemi=hemi, opp=opp)
    nTrks = "Sum$(%s)"%trackCuts 
    if gt:
        nTrks = "(%s > %s)"%(nTrks,gt)
    if makeName:
        name = trkSelName({}) 
        return [name, nTrks ]
    else:
        return nTrks


sr1TrkDicts = [ 
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
 
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  

                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  

                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
 
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
 
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':180, 'opp':"12"  } ,  

                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':90, 'opp':"12"  } ,  

                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':45,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"",'dxy':0.1, 'dz':0.1,     'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"only",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
              ] 
 

sr1TrkCuts= {}
for trkCut in sr1TrkDicts: 
    trkCutName = trkSelName(trkCut)
    sr1TrkCuts[trkCutName]={}
    sr1TrkCuts[trkCutName]['bin'] = [30,0,60]
    if "_JetTrks" in trkCutName:
        sr1TrkCuts[trkCutName]['bin'] = [60,0,60]
    if "_onlyJetTrks" in trkCutName:
        sr1TrkCuts[trkCutName]['bin'] = [60,0,60]
    if any([ x in trkCutName for x in  ["_Opp270","_Opp180","_Opp90"]]):
        sr1TrkCuts[trkCutName]['bin'] = [30,0,30]


    maxNTrk = sr1TrkCuts[trkCutName]['bin'][2]
    sr1TrkCuts[trkCutName]['params']=trkCut
    sr1TrkCuts[trkCutName]['var'] = nTracks(**trkCut)
    sr1TrkCuts[trkCutName]['cut'] = CutClass( trkCutName, 
                                    [ [ trkCutName+" $>$ %s"%x, nTracks(gt=x, **trkCut)   ] for x in range(maxNTrk) ]                        
                        ,baseCut = sr1Loose 
                        )  






trackPlotDict =\
      {
        "nTrks_jetPt30":            {'var':nTracks(jetPt=30)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 30"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_jetPt45":            {'var':nTracks(jetPt=45)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 45"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_jetPt60":            {'var':nTracks(jetPt=60)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 60"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nGenTrks_jetPt30":         {'var':nTracks(trk="GenTracks",jetPt=30)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 30"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_jetPt45":         {'var':nTracks(trk="GenTracks",jetPt=45)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 45"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_jetPt60":         {'var':nTracks(trk="GenTracks",jetPt=60)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 60"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

      }


plotDict2={}
for p in trackPlotDict:
  trackPlotDict[p]['name']=p
  plotDict2[p]=Plot(**trackPlotDict[p])

trackPlots=Plots(**plotDict2)







def getAndDraw(name,var,cut="(1)",bins=[],weight="weight",min=False,logy=0,fom="ratio",fomOpt="All",save=False):
    bkgHistName="w_%s"%name
    sigHistName="s_%s"%name
    ret={}
    if hasattr(ROOT,bkgHistName) and getattr(ROOT,bkgHistName):
        hist=getattr(ROOT,"w_%s"%name)
        #print hist, "already exist, will try to delete it!"
        #hist.IsA().Destructor(hist)
        del hist
    binning = "(%s)"%",".join([str(x) for x in bins]) if bins else ''
    samples.w.tree.Draw(var+">>hTmp%s"%(binning) ,  "(%s)*(%s)"%(weight,cut), "goff")
    bkgHist = ROOT.hTmp.Clone(bkgHistName)
    #bkgHist = getPlotFromChain(samples.w.tree,var,bins,cutString=cut, weight=weight)
    #bkgHist.SetName(bkgHistName)
    #bkgHist.SetFillColor(samples.w.tree.GetLineColor())
    #bkgHist.SetLineColor(1)
    del ROOT.hTmp
    bkgHist.SetFillColor(bkgHist.GetLineColor())
    bkgHist.SetLineColor(1)
    bkgHist.SetTitle(name)
    samples.s.tree.Draw(var+">>hTmp2%s"%(binning), "(%s)*(%s)"%(weight,cut), "goff")
    sigHist = ROOT.hTmp2.Clone(sigHistName)
    del ROOT.hTmp2
    if min:
        bkgHist.SetMinimum(min)
    ret.update({'sHist':sigHist, 'bkgHist':bkgHist } )
    if fom:
        if str(fom).lower() == "ratio": ratio = getRatio(sigHist,bkgHist,normalize=True, min=0.01,max=2.0)
        else: 
            ratio=getFOMFromTH1F(sigHist,bkgHist,fom="AMSSYS")
            x = ratio.GetXaxis()
            x.SetTitleSize(20)
            x.SetTitleFont(43)
            x.SetTitleOffset(4.0)
            x.SetLabelFont(43)
            x.SetLabelSize(15)

        ratio.SetLineColor(ROOT.kSpring+4)
        ratio.SetMarkerColor(ROOT.kSpring+4)
        ratio.SetLineWidth(2)
        print "getting ratio"
        #ratio.Print('all')
        #ratio.Draw()
        c1,p1,p2 = makeCanvasPads("%s"%name,600,600)
        p2.cd()
        Func = ROOT.TF1('Func',"[0]",sigHist.GetBinLowEdge(1),sigHist.GetNbinsX()+1)
        Func.SetParameter(0,1)
        Func.SetLineColor(ROOT.kRed)
        ratio.Draw()        
        Func.Draw('same')
        ratio.Draw('same')        
        ret.update({'ratio':ratio , 'canv': (c1,p1,p2), 'func':Func } )
    else:
        p1 = ROOT.TCanvas(name,name,600,600)
        ret.update({'canv': (p1) } )
        #bkgHist.Draw("hist")
        #sigHist.Draw("same")
    p1.cd()
    bkgHist.Draw("hist")
    sigHist.Draw("same")
    if logy:
        p1.SetLogy(1)
    if save:
        if fom:
            c1.SaveAs(saveDir+"/%s.png"%name)
        else:
            p1.SaveAs(saveDir+"/%s.png"%name)
    return ret 



