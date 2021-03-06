import ROOT
import pickle
import copy, os, sys

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from math import *

signalRegion = signalRegion3fb

#add the path where the pickle files are located
path = '/data/'+username+'/results2015/rCS_0b/'

def getNumString(n,ne, acc=2):    ##For printing table 
  if type(n) is float and type(ne) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ ne

def getQCDfraction(Bkg, Bkg_err, QCD, QCD_err):
  if QCD>0 and Bkg>0:
    res = QCD/Bkg
    res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  else:
    res = float('nan')
    res_err = float('nan')
  return res, res_err

#side band for tt+jets estimation 4-5j, 1b
ttCRbtb = (1,1)

#get the ratios from the Lp template fit
#side band for QCD estimation 3-4j, 0b
CR = (3,4)  
btb = (0,0)
ratio={}
for srNJet in sorted(signalRegion):
  ratio[srNJet] = {}
  for stb in sorted(signalRegion[srNJet]):
    ratio[srNJet][stb] = {}
    for htb in sorted(signalRegion[srNJet][stb]):
      res = pickle.load(file(path+'QCDyieldFromTemplateFit_'+nameAndCut(stb, htb, CR, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'_pkl'))
      ratio[srNJet][stb][htb] = {'F_seltoantisel':res[htb][stb][CR][btb]['F_seltoantisel'], 'F_seltoantisel_err':res[htb][stb][CR][btb]['F_seltoantisel_err'],\
                                 'NQCDSelMC':res[htb][stb][CR][btb]['NQCDSelMC'], 'NQCDSelMC_err':res[htb][stb][CR][btb]['NQCDSelMC_err'],\
                                 'NQCDFit':res[htb][stb][CR][btb]['QCD']['yield'], 'NQCDFit_err':sqrt(res[htb][stb][CR][btb]['QCD']['yieldVar']),\
                                 'NdataSel':res[htb][stb][CR][btb]['NdataSel'], 'NdataSel_err':res[htb][stb][CR][btb]['NdataSel_err']}

nAntiSel = pickle.load(file(path+'RcsQCD3fb-1_pkl'))
nCRAntiSel = pickle.load(file(path+'RcsQCD_4-5j_1b_3fb-1_pkl'))

rowsNJet = {}
rowsSt = {}
for srNJet in sorted(signalRegion):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegion[srNJet]):
    rows += len(signalRegion[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegion[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegion[srNJet]), 'n':rows}

#print only yields and ratios from the CR
print " QCD estimation and ratios in CR"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{9}{c|}{QCD multijets}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}&\multicolumn{3}{c|}{$F_{sel-to-antisel}$}\\\\\hline'
print '\\hline'
print '\multirow{'+str(len(ratio))+'}{*}{\\begin{sideways}$'+varBin(CR)+'$\end{sideways}}'
for njb in sorted(ratio):
  for stb in sorted(ratio[njb]):
    print '&\multirow{'+str(len(ratio[njb]))+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(ratio[njb][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(ratio[njb][stb][htb]['NQCDFit'],ratio[njb][stb][htb]['NQCDFit_err'])\
           +' & '+getNumString(ratio[njb][stb][htb]['NQCDSelMC'],ratio[njb][stb][htb]['NQCDSelMC_err'])\
           +' & '+getNumString(ratio[njb][stb][htb]['F_seltoantisel'],ratio[njb][stb][htb]['F_seltoantisel_err'])+'\\\\'
print '\\hline'
print '\\hline\end{tabular}}\end{center}\caption{Closure and Ratio for QCD background in the CR, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpredCR}\end{table}'

print 'Results QCD in 4-5j, 1b CR'
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{QCD multijets in 4-5j,1b CR}&\multicolumn{3}{c|}{$N^{MC}_{Bkg.}/N^{MC}_{QCD}$}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{}\\\\\hline'
#print yields in the CR 4-5j,1b
print '\\hline'
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      res, res_err = getQCDfraction(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataSel'],nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataSel_err'],nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelMC'],nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelMC_err'])
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(ratio[srNJet][stb][htb]['F_seltoantisel']*nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel'],\
                 sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel']**2)+(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2)))\
           +' & '+getNumString(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelMC'], nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelMC_err'])\
           +' & '+getNumString(res,res_err)+'\\\\'
print '\\hline\end{tabular}}\end{center}\caption{Closure table for QCD background , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpred}\end{table}'

#print RCS factors in the CR 4-5j, 1b
print 'RCS in CR 4-5j,1b'
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT & \DF    &\multicolumn{6}{c|}{Transfer factors in 4-5j,1b CR}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c}{$R^{antiselected}_{CS}$}&\multicolumn{3}{c|}{$R^{selected}_{CS}$}\\\\\hline'
print '\\hline'
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
      print ' & '+getNumString(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsQCDantisel'], nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsQCDantiselErr_sim'],3)\
           +' & '+getNumString(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsSel'], nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsSelErr_sim'],3)+'\\\\'
print '\\hline\end{tabular}}\end{center}\caption{$R^{QCD}_{CS} $ factors from anti-selected Data in the 4-5j, 1b CR}\label{tab:1b_QCDrcs}\end{table}'

#print QCD yields in low dPhi region to correct RCS_EWK in the CR 4-5j, 1b
print '$N^{QCD}_{selected}(low \DF)$ in CR 4-5j,1b'
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT & \DF    &\multicolumn{6}{c|}{$N^{QCD}_{selected}(low \DF)$ in 4-5j,1b CR}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}\\\\\hline'
print '\\hline'
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      nQCDpred = ratio[srNJet][stb][htb]['F_seltoantisel']*nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel']
      nQCDpred_err = sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel']**2)\
                         +(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NdataAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2))
      res = nQCDpred/(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsQCDantisel']+1)
      res_err = res * sqrt(nQCDpred_err**2/nQCDpred**2 + nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsQCDantiselErr_sim']**2/(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['RcsQCDantisel']+1)**2)
      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
      print ' & '+getNumString(res, res_err)\
           +' & '+getNumString(nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelLowdPhi'], nCRAntiSel[srNJet][stb][htb][ttCRbtb]['NQCDSelLowdPhi_err'])+'\\\\'
print '\\hline\end{tabular}}\end{center}\caption{$N^{QCD}_{selected}(low \DF)$ to correct $R^{EWK}_{CS}$  in the 4-5j, 1b CR}\label{tab:1b_QCDlowdPhi}\end{table}'


print "Results QCD estimation"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{QCD multijets}&\multicolumn{3}{c|}{$N^{MC}_{Bkg.}/N^{MC}_{QCD}$}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{}\\\\\hline'
#first print yields in the CR 3-4j
print '\\hline'
print '\multirow{'+str(len(ratio))+'}{*}{\\begin{sideways}$'+varBin(CR)+'$\end{sideways}}'
for njb in sorted(ratio):
  for stb in sorted(ratio[njb]):
    print '&\multirow{'+str(len(ratio[njb]))+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(ratio[njb][stb]):
      if not first: print '&'
      first = False
      res, res_err = getQCDfraction(ratio[njb][stb][htb]['NdataSel'],ratio[njb][stb][htb]['NdataSel_err'],ratio[njb][stb][htb]['NQCDSelMC'],ratio[njb][stb][htb]['NQCDSelMC_err'])
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(ratio[njb][stb][htb]['NQCDFit'],ratio[njb][stb][htb]['NQCDFit_err'])\
           +' & '+getNumString(ratio[njb][stb][htb]['NQCDSelMC'],ratio[njb][stb][htb]['NQCDSelMC_err'])\
           +' & '+getNumString(res,res_err)+'\\\\'
print '\\hline'
#print predicted yields in the SR
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      res, res_err = getQCDfraction(nAntiSel[srNJet][stb][htb][btb]['NdataSel'],nAntiSel[srNJet][stb][htb][btb]['NdataSel_err'],nAntiSel[srNJet][stb][htb][btb]['NQCDSelMC'],nAntiSel[srNJet][stb][htb][btb]['NQCDSelMC_err'])
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(ratio[srNJet][stb][htb]['F_seltoantisel']*nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel'],\
                 sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel']**2)+(nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2)))\
           +' & '+getNumString(nAntiSel[srNJet][stb][htb][btb]['NQCDSelMC'], nAntiSel[srNJet][stb][htb][btb]['NQCDSelMC_err'])\
           +' & '+getNumString(res,res_err)+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-9}'

print '\\hline\end{tabular}}\end{center}\caption{Closure table for QCD background , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpred}\end{table}'

print "Results $R^{QCD}_{CS} $"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT & $\Delta\Phi_{cut} $   &\multicolumn{3}{c|}{$R^{antiselected}_{CS}$}&\multicolumn{3}{c|}{$R^{selected}_{CS}$}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c|}{}&\multicolumn{3}{c|}{}\\\\\hline'
print '\\hline'
#print predicted yields in the SR
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
      print ' & '+getNumString(nAntiSel[srNJet][stb][htb][btb]['RcsQCDantisel'],nAntiSel[srNJet][stb][htb][btb]['RcsQCDantiselErr_sim'],3)\
           +' & '+getNumString(nAntiSel[srNJet][stb][htb][btb]['RcsSel'],nAntiSel[srNJet][stb][htb][btb]['RcsSelErr_sim'],3)+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{$R^{QCD}_{CS} $ factors from anti-selected Data , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcs}\end{table}'
