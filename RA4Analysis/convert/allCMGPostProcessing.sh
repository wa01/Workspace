#!/bin/sh 
########Spring15###############
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT100to200 &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT200to400 &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT400to600 &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT600toInf &
#
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=DYJetsToLL_M_50  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=TToLeptons_sch  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=TToLeptons_tch  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=TBar_tWch  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=T_tWch  &

#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=data_mu  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=data_ele  &

#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt10to15_50ns    
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt15to30_50ns
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt30to50_50ns
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt50to80_50ns      &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt80to120_50ns     &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt120to170_50ns    &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt170to300_50ns    &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt300to470_50ns    &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt470to600_50ns    &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt600to800_50ns    &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt800to1000_50ns   &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt1000to1400_50ns  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt1400to1800_50ns  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt1800to2400_50ns  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt2400to3200_50ns  &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=QCD_Pt3200toInf_25ns   &

#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=DYJetsToLL_M_50_25ns   &

python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT100to200   &
python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT200to400   &
python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT400to600   &
python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT600toInf   &

#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT600to800   &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT800to1200   &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT1200to2500   &
#python cmgPostProcessing.py --leptonSelection=hard --inputTreeName="" --samples=WJetsToLNu_HT2500toInf   &


#########Phys14###############
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T5qqqqWW_Gl1500_Chi800_LSP100  $2   &  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T5qqqqWW_Gl1200_Chi1000_LSP800 $2    &   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1tttt_2J_mGl1500_mLSP100 $2          &   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1tttt_2J_mGl1200_mLSP800 $2           &  #--skim=HT400ST150 
###python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1bbbb_2J_mGl1000_mLSP900 $2 & 
###python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1qqqq_2J_mGl1000_mLSP800 $2 & 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T2tt_2J_mStop425_mLSP325 $2  
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T2tt_2J_mStop500_mLSP325 $2  
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T2tt_2J_mStop650_mLSP325 $2  
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T2tt_2J_mStop850_mLSP100 $2  
###python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T5qqqqWW_2J_mGo1400_mCh315_mChi300 $2&
####python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T6qqWW_mSq950_mChi325_mLSP300 $2
###python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1tttt_2J_mGl1300_mLSP100 $2
###python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T1tttt_2J_mGl800_mLSP450 $2
##
###python cmgPostProcessing.py --leptonSelection=$1 --samples=T1ttbb_mGo1500_mChi100 $2
###python cmgPostProcessing.py --leptonSelection=$1 --samples=T6ttWW_mSbot600_mCh425_mChi50 $2
###python cmgPostProcessing.py --leptonSelection=$1 --samples=T6ttWW_mSbot650_mCh150_mChi50 $2
##
#####python cmgPostProcessing.py --leptonSelection=$1 --samples=T1ttbbWW_mGo1000_mCh725_mChi715     $2    &     
#####python cmgPostProcessing.py --leptonSelection=$1 --samples=T1ttbbWW_mGo1000_mCh725_mChi720     $2 &
#####python cmgPostProcessing.py --leptonSelection=$1 --samples=T1ttbbWW_mGo1300_mCh300_mChi290     $2 &
#####python cmgPostProcessing.py --leptonSelection=$1 --samples=T1ttbbWW_mGo1300_mCh300_mChi295     $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1000_mStop300_mCh285_mChi280 $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1000_mStop300_mChi280  $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1300_mStop300_mCh285_mChi280 $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1300_mStop300_mChi280  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1000_mCh800_mChi700  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1000_mCh800_mChi700_dilep  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1200_mCh1000_mChi800  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1200_mCh1000_mChi800_cmg  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1200_mCh1000_mChi800_dilep  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5qqqqWW_mGo1500_mCh800_mChi100  $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1000_mStop300_mCh285_mChi280  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_dil  $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1000_mStop300_mChi280  $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1300_mStop300_mCh285_mChi280  $2 &
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_dil  $2 &
##python cmgPostProcessing.py --leptonSelection=$1 --samples=T5ttttDeg_mGo1300_mStop300_mChi280  $2 &

#python cmgPostProcessing.py --leptonSelection=$1 --samples=ttJets_PU20bx25                      $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=WJetsToLNu_HT100to200_PU20bx25       $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=WJetsToLNu_HT200to400_PU20bx25       $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=WJetsToLNu_HT400to600_PU20bx25       $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=WJetsToLNu_HT600toInf_PU20bx25       $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=ttWJets_PU20bx25                     $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=ttZJets_PU20bx25                     $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=ttH_PU20bx25                         $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=DYJetsToLL_M50_HT100to200_PU20bx25   $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=DYJetsToLL_M50_HT200to400_PU20bx25   $2  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=DYJetsToLL_M50_HT400to600_PU20bx25   $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=DYJetsToLL_M50_HT600toInf_PU20bx25   $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=QCD_HT_100To250_PU20bx25             $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=QCD_HT_250To500_PU20bx25             $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=QCD_HT_500To1000_PU20bx25            $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=QCD_HT_1000ToInf_PU20bx25            $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=TBarToLeptons_sChannel_PU20bx25      $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=TBarToLeptons_tChannel_PU20bx25      $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=TToLeptons_sChannel_PU20bx25         $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=TToLeptons_tChannel_PU20bx25         $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=T_tWChannel_PU20bx25                 $2   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=TBar_tWChannel_PU20bx25              $2   #--skim=HT400ST150 
