from Workspace.DegenerateStopAnalysis.navidTools.PlotDict import *
from Workspace.DegenerateStopAnalysis.navidTools.Yields import *
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *
from Workspace.DegenerateStopAnalysis.cuts import *
#from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2_GenTracks import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from makeTable import *
from limitCalc import *

from Tracks import *

from trackPlotDict import *

from Workspace.DegenerateStopAnalysis.navidTools.getRatioPlot import *



######## Track Validation commands ######
testvalidtrackinfo=False
if testvalidtrackinfo:

  trkJetPt="Jet_pt[track_matchedJetIndex]"
  trkJetEta="Jet_eta[track_matchedJetIndex]"
  trkJetPhi="Jet_phi[track_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(track_eta-%s)**2 )"%(minAngle(trkJetPhi,"track_phi") ,trkJetEta)
  f.Draw("track_matchedJetDr:%s"%dr,"track_matchedJetIndex>0","COLZ")
  f.Draw("ntrack_2p5:Sum$(track_pt > 2.5 && abs(track_dxy)<0.02 && abs(track_dz)<0.5 && abs(track_eta)<2.5 && abs(track_pdgId)!=11 && abs(track_pdgId) != 13 &&(track_matchedJetDr > 0.4 || Jet_pt[track_matchedJetIndex] < 30 ) )")
  
  trkJetPt="Jet_pt[Tracks_matchedJetIndex]"
  trkJetEta="Jet_eta[Tracks_matchedJetIndex]"
  trkJetPhi="Jet_phi[Tracks_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(Tracks_eta-%s)**2 )"%(minAngle(trkJetPhi,"Tracks_phi") ,trkJetEta)
  f.Draw("Tracks_matchedJetDr:%s"%dr,"Tracks_matchedJetIndex>0","COLZ")
  f.Draw("nTracks_2p5:Sum$(Tracks_pt > 2.5 && abs(Tracks_dxy)<0.02 && abs(Tracks_dz)<0.5 && abs(Tracks_eta)<2.5 && abs(Tracks_pdgId)!=11 && abs(Tracks_pdgId) != 13 &&(Tracks_matchedJetDr > 0.4 || Jet_pt[Tracks_matchedJetIndex] < 30 ) )")

  nTrk = lambda trkPt, jetPt: "Sum$(track_pt > {trkPt} && abs(track_dxy)<0.02 && abs(track_dz)<0.5 && abs(track_eta)<2.5 && abs(track_pdgId)!=11 && abs(track_pdgId) != 13 &&(track_matchedJetDr > 0.4 || Jet_pt[track_matchedJetIndex] < {jetPt}) )".format(trkPt=2.5, jetPt=50)

  trkJetPt="GenJet_pt[GenTracks_matchedJetIndex]"
  trkJetEta="GenJet_eta[GenTracks_matchedJetIndex]"
  trkJetPhi="GenJet_phi[GenTracks_matchedJetIndex]"
  minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)
  dr="sqrt( (%s)**2+(GenTracks_eta-%s)**2 )"%(minAngle(trkJetPhi,"GenTracks_phi") ,trkJetEta)
  f.Draw("GenTracks_matchedJetDr:%s"%dr,"GenTracks_matchedJetIndex>0","COLZ")
  f.Draw("nGenTracks_2p5:Sum$(GenTracks_pt > 2.5 && abs(GenTracks_dxy)<0.02 && abs(GenTracks_dz)<0.5 && abs(GenTracks_eta)<2.5 && abs(GenTracks_pdgId)!=11 && abs(GenTracks_pdgId) != 13 &&(GenTracks_matchedJetDr > 0.4 || Jet_pt[GenTracks_matchedJetIndex] < 30 ) )")


#saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/GenTracks/1stIter'
saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/GenTracks/Multip/1stIter'

#trkCutList = [sr1Trk,sr1TrkJ1,sr1TrkJ12,sr1TrkJAll, sr1TrkOpp60JAll , sr1TrkOpp90JAll , sr1TrkOpp60J12, sr1TrkOpp90J12, sr1TrkOpp90J1]

#trkCutList = [sr1TrkOpp60JAll, sr1TrkOpp90JAll]


sampleList=['s','w']
#plotList=[ x for x in plotDict if "_2p5" in x]
plotList=[]

if not samples.s.tree.GetEventList():
  setEventListToChains(samples,sampleList,sr1Loose)


getPlotOpt=False
if getPlotOpt:
    print "Getting Plots:"
    if not hasattr(samples.s,"cuts"):
        getPlots2(samples,trackPlots,sr1Loose,sampleList=sampleList,plotList=plotList)
#print "Getting FOM hist"
#fomHistW = getFOMFromTH2F(samples.s.cuts.sr1Loose.DMT, samples.w.cuts.sr1Loose.DMT)
#fomHistW.SetTitle("FOM")
#fomHistW.SetMinimum(0)



def drawPlot(samples,sampleList=['s','w'],plot='',min=False,logy=0,save=True,fom=True):
    canv = ROOT.TCanvas(plot,plot,600,600)
    if logy: canv.SetLogy(1)
    sigHist = getattr(samples.s.cuts.sr1Loose,plot)
    bkgHist = getattr(samples.w.cuts.sr1Loose,plot)
    bkgHist.Draw("hist")
    if min: bkgHist.SetMinimum(min)
    sigHist.Draw("same")
    canv.SetLogy(1)
    if save:
        canv.SaveAs(saveDir+"/%s.png"%plot)
    if fom:
        fomHist=getFOMFromTH1F(sigHist,bkgHist)
        fomCanv=ROOT.TCanvas("FOM_%s"%plot,"FOM_%s"%plot ,600,200)
        fomHist.Draw()
    return canv, fomHist, fomCanv






def getAndDraw(name,var,cut="(1)",bins=[],weight="weight",sampleList=['w'],min=False,logy=0,fom="AMSSYS",fomOpt=True,save=False):
    binning = "(%s)"%",".join([str(x) for x in bins]) if bins else ''
    ret={}

    #bkgList=['tt','w']
    bkgList=sampleList
    bkgHists={}
    for bkg in bkgList:
        bkgHists[bkg]={}
        bkgHistName= bkg+"_"+name
        bkgHists[bkg]['name']=bkgHistName
        bkgTree=samples[bkg].tree
        if hasattr(ROOT,bkgHistName) and getattr(ROOT,bkgHistName):
            hist=getattr(ROOT,bkgHistName)
            #print hist, "already exist, will try to delete it!"
            #hist.IsA().Destructor(hist)
            del hist
        bkgTree.Draw(var+">>hTmp%s"%(binning) ,  "(%s)*(%s)"%(weight,cut), "goff")
        bkgHists[bkg]['hist'] = ROOT.hTmp.Clone(bkgHistName)
        del ROOT.hTmp
        bkgHists[bkg]['hist'].SetFillColor(bkgHists[bkg]['hist'].GetLineColor())
        bkgHists[bkg]['hist'].SetLineColor(1)
        bkgHists[bkg]['hist'].SetTitle(name)
    bkgStack = getStackFromHists( [bkgHists[bkg]['hist'] for bkg in bkgList] )
    bkgStack.SetTitle(name)


    
    sigHistName="s_%s"%name
    samples.s.tree.Draw(var+">>hTmp2%s"%(binning), "(%s)*(%s)"%(weight,cut), "goff")
    sigHist = ROOT.hTmp2.Clone(sigHistName)
    del ROOT.hTmp2

    nBins  = sigHist.GetNbinsX()
    lowBin = sigHist.GetBinLowEdge(1)
    hiBin  = sigHist.GetBinLowEdge(sigHist.GetNbinsX()+1)

    stackHist=ROOT.TH1F("stack_hist","stack_hist",nBins,lowBin,hiBin)
    stackHist.Merge(bkgStack.GetHists())

    if min:
        bkgStack.SetMinimum(min)
    ret.update({'sHist':sigHist, 'bkgHists':bkgHists, "bkgStack":bkgStack, "stackHist":stackHist } )

    if fom:
        c1,p1,p2 = makeCanvasPads("%s"%name,600,600)
        p2.cd()


        if str(fom)  == "ratio": 
            ratio = getRatio(sigHist,stackHist,normalize=True, min=0.01,max=2.0)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getRatio(sigHist, bkgHists[bkg]['hist'] ,normalize=True, min=0.01,max=2.0)
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        else:
            ratio=getFOMFromTH1FIntegral(sigHist,stackHist,fom=fom)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getFOMFromTH1FIntegral(sigHist, bkgHists[bkg]['hist'], fom=fom )
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        dOpt=''
        if not fomOpt:
            for bkg in bkgList:
                bkgHists[bkg]['ratio'].SetLineColor( bkgHists[bkg]['hist'].GetFillColor() )
                bkgHists[bkg]['ratio'].SetLineWidth(2)

                if not dOpt:
                    firstHist = bkgHists[bkg]['ratio']
                bkgHists[bkg]['ratio'].Draw(dOpt)
                dOpt="same"
        else:
            firstHist = ratio
            ratio.SetTitle(name)
            ratio.Draw(dOpt)

        firstHist.SetStats(0)
        x = firstHist.GetXaxis()
        x.SetTitleSize(20)
        x.SetTitleFont(43)
        x.SetTitleOffset(4.0)
        x.SetLabelFont(43)
        x.SetLabelSize(15)
        y = firstHist.GetYaxis()
        y.SetTitle(fom)
        y.SetNdivisions(505)
        y.SetTitleSize(20)
        y.SetTitleFont(43)
        y.SetTitleOffset(1)
        y.SetLabelFont(43)
        y.SetLabelSize(15)
               
 
        ratio.SetLineColor(ROOT.kSpring+4)
        ratio.SetMarkerColor(ROOT.kSpring+4)
        ratio.SetLineWidth(2)
        if "ratio" in fom.lower():
          ratio.SetMinimum(0)
          ratio.SetMaximum(2)
        else:
          ratio.SetMinimum(0)
          ratio.SetMaximum(3)
        print "getting ratio"
        Func = ROOT.TF1('Func',"[0]",sigHist.GetBinLowEdge(1),sigHist.GetBinLowEdge( sigHist.GetNbinsX()+1) )
        Func.SetParameter(0,1)
        Func.SetLineColor(ROOT.kRed)
        Func.Draw('same')
        c1.Update()
        p1.Update()
        ret.update({'ratio':ratio, 'canv': (c1,p1,p2), 'func':Func } )
    else:
        p1 = ROOT.TCanvas(name,name,600,600)
        ret.update({'canv': (p1) } )
        #bkgHist.Draw("hist")
        #sigHist.Draw("same")
    p1.cd()

    bkgStack.Draw("hist")
    bkgStack.GetYaxis().SetTitle("nEvents")
    sigHist.Draw("same")
    if logy:
        p1.SetLogy(1)
    if save:
        if fom:
            c1.SaveAs(saveDir+"/%s.png"%name)
        else:
            p1.SaveAs(saveDir+"/%s.png"%name)
    return ret 

#getAndDraw("trackPt", "Tracks_pt", cut="(1)",bins=[50,0,50] ,logy=1,fom=True)

plotList=[
          #{"name":"Tracks_dz",   
          #                   "var":"Tracks_dz",   'cut':trackCut(dxy=0.5,dz=0.5)    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dxy",   
          #                  "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5,dz=0.5)    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dxy",   
          #                  "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5,dz=0.5)    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          {"name":"Tracks_dxy__dz01_vetoJet",   
                            "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5, dz=0.1,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dxy__dz05_vetoJet",   
          #                  "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5, dz=0.5,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy05_vetoJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.5,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy05_onlyJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.5, jetOpt="only")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy01_vetoJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.1,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy01_onlyJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.1, jetOpt="only")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          {"name":"Tracks_pt_onlyJetTracks",   
                            "var":"Tracks_pt",   'cut':trackCut(dz=0.1, dxy=0.1, jetOpt="only")    ,'bins':[100,0,300],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          {"name":"Tracks_pt_vetoJetTracks",   
                            "var":"Tracks_pt",   'cut':trackCut(trkPt=1, dz=0.1, dxy=0.1, jetOpt="veto")    ,'bins':[100,0,50],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 

          {"name":"nTracks_dz__dxy01_onlyJet",   
                            "var":nTracks(dz=0.1,dxy=0.1, jetOpt="veto"),   'cut':"(1)"    ,'bins':[20,0,20],'weight':"weight",'min':0.1,'logy':1,'fom':True,'save':True}, 
          {"name":"nGenTracks_dz__dxy01_onlyJet",   
                            "var":nTracks(trk="GenTracks", jetOpt="veto"),   'cut':"(1)"    ,'bins':[50,0,50],'weight':"weight",'min':0.1,'logy':1,'fom':True,'save':True}, 



          ]

plots={}

plotOpt=False
if plotOpt:
  for p in plotList:
      plots[p['name']]=getAndDraw(**p)




canvs={}
foms={}
fomCanvs={}


drawOpt=False
if drawOpt:
  for plot in plotList:
      canvs[plot]=drawPlot( samples, sampleList, plot,save=True )
      foms[plot]=getFOMFromTH1F(samples.s.cuts.sr1Loose[plot], samples.w.cuts.sr1Loose[plot] )
      foms[plot].GetXaxis().SetTitle("Track Multip > X")
      foms[plot].GetYaxis().SetTitle("FOM")
      fomCanvs[plot]=ROOT.TCanvas( "FOM_%s"%plot, "FOM_%s"%plot, 600, 600)
      foms[plot].SetLineColor(ROOT.kMagenta)
      foms[plot].SetLineWidth(2)
      foms[plot].SetMinimum(0)
      foms[plot].Draw()
      fomCanvs[plot].SaveAs(saveDir+"/%s.png"%"FOM_%s"%plot)

pklDir= "./pkl/Tracks/1stIter/"
#tableDir = saveDir+"/table/" 
tableDir = saveDir+"" 



getYieldsOpt=False
if getYieldsOpt:
    print "Getting Yields:"
    print "Pickle Dir: ", pklDir
    print "Tables: ", tableDir
    yDict={}
    hists={}
    for trkCut in sr1TrkCuts:
        name = trkCut
        cutInst = sr1TrkCuts[trkCut]['cut']
        #canv={}
        #regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
        #print "----------------------------------------------------------------"
        #print getattr(regDict[name],cut).list
        #print "----------------------------------------------------------------"
        yDict[name] =  Yields(samples,['w','s'], cutInst , cutOpt='list', tableName='{cut}',pklOpt=True,pklDir=pklDir )
        JinjaTexTable(yDict[name], pdfDir=tableDir)
        hists[name] = getAndDraw(name, sr1TrkCuts[name]['var'], bins=sr1TrkCuts[name]['bin'],   sampleList=['w'], min=0.1, logy=1, fom='AMSSYS'   , save=True)
        #canv[name]=ROOT.TCanvas(name,name,800,800)
        #fomHistW.Draw("COLZ")
        #regDict[name].r1.r.Draw("same")
        #regDict[name].r2.r.Draw("same")
        #regDict[name].r3.r.Draw("same")
        #canv[name].SaveAs(saveDir+"/%s.png"%name)









