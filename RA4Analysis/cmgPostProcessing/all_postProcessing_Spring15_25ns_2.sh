#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=DYJetsToLL_M_10to50_25ns
#python cmgPostProcessing.py --skim="HT500ST250"  --samples=DYJetsToLL_M_50_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DYJetsToLL_M_50_HT100to200_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DYJetsToLL_M_50_HT200to400_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DYJetsToLL_M_50_HT400to600_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DYJetsToLL_M_50_HT600toInf_25ns
