#!/bin/bash



#for MASS in  0 100 125 150 175 200 225 50; do
#  echo "LSP$MASS"
#  python mergeLHEs.py --lhedir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2  --lhepattern="*LSP$MASS*.lhe" --outputdir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2/merged/ --output="stop_stop300_LSP$MASS.lhe" &
#  done


#python mergeLHEs.py --lhedir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2/merged --lhepattern="*LSP*.lhe" --outputdir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2/merged/ --output="stop_stop300_LSPMIXED.lhe"
python mergeLHEs.py --lhedir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2/  --lhepattern="*.lhe" --outputdir=/afs/hephy.at/data/nrad01/lhe/T2tt_v2/merged_all/ --output="stop_stop300_LSPMIXED_2.lhe"


