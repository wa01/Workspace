#!/usr/bin/env python

import os
import glob




from optparse import OptionParser
parser = OptionParser()

parser.add_option("--lhedir", dest="lhedir", default="./", type="string", action="store", help="Directory for the lhe's to be merged")
parser.add_option("--lhepattern", dest="lhepattern", default="", type="string", action="store", help="Pattern for the LHE file to merge (i.e *stop300*.lhe )")

parser.add_option("--outputdir", dest="outputdir", default="./", type="string", action="store", help="Output directory for the merged lhefile")
parser.add_option("--output", dest="output", default="output_merged.lhe", type="string", action="store", help="Name of the merged lhefile")
parser.add_option("--pretend", dest="pretend" , action="store_true", help="Name of the merged lhefile")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", default=False, help="THIS DOESNT DO ANYTHING")

(options, args) = parser.parse_args()

pretend=False

lhedir = options.lhedir
outputdir = options.outputdir
output = options.output
#overwrite = options.overwrite





#f = open('list1.txt')
#fout = open('T2DegStop2j_300_270_merged.lhe', 'w')
outname= outputdir+"/"+output
fout = open(outname, 'w')

nFiles=0

#dir = './testLHEfiles/'
#lhedir = '/afs/cern.ch/work/n/nrad/public/T2DegStop/lhe_processed/T2DegStop2j/'

if not options.lhepattern:
  filelist = glob.glob("%s/*.lhe"%lhedir)
else: 
  filelist = glob.glob("%s/%s"%(lhedir,options.lhepattern))

print "Found %s LHE files to merge in dir %s:"%(len(filelist),lhedir)
print filelist

if options.pretend:
  assert False, "pretending"

#for file in os.listdir(lhedir):
for file in filelist:
  if not file[-3:] == 'lhe':
    print file, 'not lhe file'
    continue 

  nFiles+=1
  print 'File number:', nFiles, "File Name", file
  #f = open(lhedir+file)
  f = open(file)
  if nFiles==1:
  
    print 'Using the header of', file
    for line in f.xreadlines():
      if "</LesHouchesEvents>" in line:
        print "reached end"
        break
      else:
        fout.write(line)
       #'tests/file/myword' in line:
       #   f1.write(line) 
  else:
    print 'ignoring the header of', file
    startCopy=0

    for line in f.xreadlines():
      
      if startCopy==0:
        if "<event>" in line:
          startCopy=1

      if startCopy==1:
        if "</LesHouchesEvents>" in line:
          print "reached end of", file
          break
        else:
          fout.write(line)


  f.close()

#for line in f.readlines():
#
#    if 'tests/file/myword' in line:
#        doIHaveToCopyTheLine=True
#
#    if doIHaveToCopyTheLine:
#        f1.write(line)
#

#w.writelines([item for item in lines[:-1]])

#f1.close()

fout.write("</LesHouchesEvents>")
fout.close()

print "Output: %s"%outname
