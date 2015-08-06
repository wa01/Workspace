#redEffMap.py script 

import ROOT
import os
import numpy as np
#from array import array
#import scipy

#Root options

#ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Default") #Plain = sets empty TStyle

#ROOT.gStyle.SetOptStat(1) #prints statistics on plots
#ROOT.gStyle.SetOptFit(0) #gStyle->SetOptFit(1111); //prints fit results of plot
#ROOT.gStyle.SetTitleX(0.15) #sets x-coord of title
#gStyle->SetFuncWidth(1) #sets width of fit line
#gStyle->SetFuncColor(9) #sets colours of fit line
#gStyle->SetLineWidth(2)
#gStyle->SetOptTitle(0) #suppresses title box

#ROOT.gStyle.SetCanvasBorderMode(0);
#ROOT.gStyle.SetPadBorderMode(0);
#ROOT.gStyle.SetPadColor(0);
#ROOT.gStyle.SetCanvasColor(0);
#ROOT.gStyle.SetTitleColor(0);
#ROOT.gStyle.SetStatColor(0);

path = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/ROI/"

#if not os.path.exists(path):
#   os.makedirs(path)

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

files = []
buffer = []
redFactor1 = []; redFactor2 = []; redFactor3 = []; redFactor4 = []
effReco1 = []; effReco2 = []; effReco3 = []; effReco4 = []
cutsMET = []; cutsISR = []

#Gets all file paths with filter results
for dirname in sorted(os.listdir(path)): 
   if dirname.startswith("filter"):
      print dirname
      buffer = dirname.split("_")
      filename = 'reductionEfficiency_' + buffer[1] + '_' + buffer[2]  + '.txt'
      files.append(os.path.join(path,dirname,filename))

#Extraction of data from file
for filename in files:
   infile = open(filename, 'r') #.read() #opens data file
   print "Opening: ", infile.name

   #infile.seek(offset, [from]) # offset = number of bytes to be moved | [from] ref position from where bytes to be moved

   #infile.tell() #position in file

   for line in infile:
         #print line
         line = infile.next() 
         print line
         buffer = line.split()
         cutsMET.append(buffer[0]) #gMET cut
         cutsISR.append(buffer[1]) #gISR cut
         redFactor1.append(buffer[2]) #MET 1
         effReco1.append(buffer[3]) #MET 1
         redFactor2.append(buffer[4]) #MET 2
         effReco2.append(buffer[5]) #MET 2
         redFactor3.append(buffer[6]) # ISR 1
         effReco3.append(buffer[7]) #ISR 1
         redFactor4.append(buffer[8]) #ISR 2
         effReco4.append(buffer[9]) #ISR 2
   infile.close()

#Canvas 1: MET 1
c1 = ROOT.TCanvas("c1", "Generator Cut Optimisation")
c1.Divide(2)

#c1.SetGrid() #adds a grid to the canvas
#c1.SetFillColor(42)
#c1.GetFrame().SetFillColor(21)
#c1.GetFrame().SetBorderSize(12)
c1.cd(1) 
gr1 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(effReco2, 'float64')*np.array(effReco4, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("Total Filter Efficiency at Reco Cut Values vs Both Generator Cuts")
 
#gr1.SetMarkerColor(ROOT.kBlue)
#gr1.SetMarkerStyle(ROOT.kFullCircle)
#gr1.SetMarkerSize(1)
gr1.GetHistogram()
gr1.GetXaxis().SetTitle("genMET Cut / GeV")
gr1.GetYaxis().SetTitle("genISR Cut / GeV")
gr1.GetZaxis().SetTitle("Total Filter Efficiency at both Reco Cut Values")
gr1.GetXaxis().SetTitleOffset(1.2)
gr1.GetYaxis().SetTitleOffset(1.2)
gr1.GetZaxis().SetTitleOffset(1.2)
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()
gr1.GetZaxis().CenterTitle()

#gr1.SetContour(nlevels, levels array) #default: n = 20 + equidistant #or TStyle.SetNumberContours()
ROOT.gStyle.SetPalette(1) #55
gr1.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
#ROOT.gPad.Update()
#gr1.SetMaximum(1.0)
#gr1.SetMinimum(0.9)
gr1.GetZaxis().SetRangeUser(0.9, 1)
gr1.GetXaxis().SetRangeUser(100, 165)
gr1.GetYaxis().SetRangeUser(60, 100)
#gr1.GetZaxis().SetNdivisions(520)

#totalReduction
c1.cd(2)
gr2 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(redFactor2, 'float64')) #graph object with error bars using arrays of data
gr2.SetTitle("Total Reduction Factor for Both Generator Cuts")
 
#gr2.SetMarkerColor(ROOT.kBlue)
#gr2.SetMarkerStyle(ROOT.kFullCircle)
#gr2.SetMarkerSize(1)
gr2.GetHistogram()
gr2.GetXaxis().SetTitle("genMET Cut / GeV")
gr2.GetYaxis().SetTitle("genISR Cut / GeV")
gr2.GetZaxis().SetTitle("Reduction Factor at both Reco Cut Values")
gr2.GetXaxis().SetTitleOffset(1.2)
gr2.GetYaxis().SetTitleOffset(1.2)
gr2.GetZaxis().SetTitleOffset(1.2)
gr2.GetXaxis().CenterTitle()
gr2.GetYaxis().CenterTitle()
gr2.GetZaxis().CenterTitle()
#gr2.GetYaxis()->SetTicks("-"); //sets x-axis ticks

#ROOT.gStyle.SetPalette(55) #55
gr2.Draw("COLZ") #CONT1-5 #plots the graph with axes and points #try opt. 0 (for min/max bins)
#gr2.SetMaximum(4)
#gr2.SetMinimum(6)
gr2.GetZaxis().SetRangeUser(4, 6)
gr2.GetXaxis().SetRangeUser(100, 165)
gr2.GetYaxis().SetRangeUser(60, 100)

c1.Update()
#pad1->Update();
c1.SaveAs(path + "reductionEfficiency/redEffMapROI.root")
c1.SaveAs(path + "reductionEfficiency/redEffMapROI.png")
c1.SaveAs(path + "reductionEfficiency/redEffMapROI.pdf")