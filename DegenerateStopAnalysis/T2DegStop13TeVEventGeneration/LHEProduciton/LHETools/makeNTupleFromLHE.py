
import sys, os, copy
import re, array, gzip
import glob
from ROOT import *


from optparse import OptionParser
parser = OptionParser()

parser.add_option("--lhedir", dest="lhedir", default="./", type="string", action="store", help="Directory for the lhe's to be merged")
parser.add_option("--lhepattern", dest="lhepattern", default="", type="string", action="store", help="Pattern for the LHE file to merge (i.e *stop300*.lhe )")

parser.add_option("--outputdir", dest="outputdir", default="./", type="string", action="store", help="Output directory for the root file")
parser.add_option("--output", dest="output", default="output_merged.lhe", type="string", action="store", help="Name of the root file")
parser.add_option("--tag", dest="tag", default="", type="string", action="store", help="Tag")

#parser.add_option("--overwrite", dest="overwrite", action="store_true", default=False, help="THIS DOESNT DO ANYTHING")

(options, args) = parser.parse_args()

lhedir = options.lhedir
outputdir = options.outputdir
output = options.output
tag=options.tag




lheFilesIn= lambda dir : [dir+fn for fn in os.listdir(dir) if any([fn.endswith(ext) for ext in ['.lhe'] ])];
    
if not options.lhepattern:
  filelist = glob.glob("%s/*.lhe"%lhedir)
else:
  filelist = glob.glob("%s/%s"%(lhedir,options.lhepattern))

print "Looking in Dir: %s"%lhedir 
print "     For files matching pattern: %s" %options.lhepattern
print "         Found %s LHE files "%(len(filelist))
print filelist

if not len(filelist):
  print "No Files Found"
  assert False

# filename can be xxx.lhe or xxx.lhe.gz
#filename = sys.argv[1]
#outfile = sys.argv[2]

#tag = sys.argv[1]
#dirname = "/afs/cern.ch/work/n/nrad/private/T2DegStop/lhe_processed/"+tag+"/"
#dirname = "/afs/cern.ch/work/n/nrad/private/T2DegStop/suchita/"+tag+"/"
#outfile = "/afs/cern.ch/work/n/nrad/private/T2DegStop/lheroot/lheroot_"+tag+"_lhe.root"
#files=lheFilesIn('/afs/cern.ch/work/n/nrad/private/T2DegStop/lhe_processed/{0}'.format(tag))
#files=['file:'+x for x in files]

outfile = outputdir +"/"+"lheroot_"+tag+"_lhe.root"



particles = ["pr", "st", "bq", "fd", "fu", "no", "je"]

varsI = ["event", "nj"]
varsD = []

pvarsI = ["Id", "C1", "C2", "He"]
ipvarsI = [0, 4, 5, 12]
pvarsD = ["Px", "Py", "Pz", "En", "Ma"]
ipvarsD = [6, 7, 8, 9, 10]

for par in particles:
  for im in range(1,3):
    for var in pvarsI:
      varsI.append(par+str(im)+var)
    for var in pvarsD:
      varsD.append(par+str(im)+var)

structString = "struct lhe_t { "
for var in varsI:
  structString += "Int_t "+var+";"
for var in varsD:
  structString += "Double_t "+var+";"
structString += " };"

gROOT.ProcessLine(structString)
lhe = lhe_t()
f = TFile( outfile, 'RECREATE' )
t = TTree( 't', '' )
for var in varsI:
    t.Branch(var, AddressOf(lhe,var), var+'/I' )
for var in varsD:
    t.Branch(var, AddressOf(lhe,var), var+'/D' )

nevent = 0

def fillTree(filename):
   global nevent

   if( not os.path.isfile(filename) ):
     print "File not found"
     return
   switch = 0
   inev = -1
   print 'opening file ',filename
   if(filename[-3:] == ".gz"):
       filehandle = gzip.open(filename)
   else:
       filehandle = open(filename)
   for line in filehandle.readlines():
     if( re.match('\<event\>', line) ):
       switch=1
       nevent+=1
       lhe.event = nevent
       inev = -1
       if( not(lhe.event % 10000) ):
#           break
         print lhe.event
     if( re.match('\<\/event\>',line) ):
       switch=0
       t.Fill()
       for var in varsI:
    #exec('lhe.'+var+' = 0')
          setattr(lhe,var,0)
       for var in varsD:
          setattr(lhe,var,0)
         #exec('lhe.'+var+' = 0.')
     if(switch):
       l = filter( lambda x: x, re.split('\s+', line) )
       if( len(l)!=13 ):
         continue
       inev += 1
       if( re.match('^\-?24$',l[0]) ):
         inev -= 1
         continue
       if( inev==0 or inev==1 ):
         indpar = 0
         im = (inev % 2) + 1
       elif( inev==2 or inev==3 ):
         indpar = 1
         im = 1
         if( re.match('-1000006',l[0]) ):
           im = 2
       elif( inev>3 and inev<12 ):
         indpar = ( (inev-4) % 4 ) + 2
         im = int((inev-4) / 4) + 1
       else:
         indpar = 6
         im = inev - 12 + 1
         lhe.nj += 1   

       for ivar, var in enumerate(pvarsI):
         exec('lhe.'+particles[indpar]+str(im)+var+' = int(float(l['+str(ipvarsI[ivar])+']))')
       for ivar, var in enumerate(pvarsD):
         exec('lhe.'+particles[indpar]+str(im)+var+' = float(l['+str(ipvarsD[ivar])+'])')

#         print line, particles[indpar], str(im)
   print 'read ',nevent,' events'

#   t.Print()
   t.Write()
   
   
#### 
   
#ldir = os.listdir(dirname)
print filelist
for fname in filelist:
    if fname[-3:] == "lhe":
        print fname 
        fillTree(fname)
