import ROOT



def getRatio(hist1, hist2,normalize=False,min=False,max=False):
  ret = hist1.Clone("Ratio")
  h2  = hist2.Clone()
  if normalize:
    ret.Scale(1./ret.Integral())
    h2.Scale(1./h2.Integral())
  ret.SetLineColor(ROOT.kBlack)
  ret.SetMarkerStyle(21)
  ret.SetTitle("")
  if min:   ret.SetMinimum(min)
  if max:   ret.SetMaximum(max)
  # Set up plot for markers and errors
  ret.Sumw2()
  ret.SetStats(0)
  ret.Divide(h2)
  # Adjust y-axis settings
  y = ret.GetYaxis()
  y.SetTitle("Ratio")
  y.SetNdivisions(505)
  y.SetTitleSize(20)
  y.SetTitleFont(43)
  y.SetTitleOffset(1.55)
  y.SetLabelFont(43)
  y.SetLabelSize(15)
  # Adjust x-axis settings
  x = ret.GetXaxis()
  x.SetTitleSize(20)
  x.SetTitleFont(43)
  x.SetTitleOffset(4.0)
  x.SetLabelFont(43)
  x.SetLabelSize(15)
  return ret


def makeCanvasPads(c1name="canvas",c1ww=600,c1wh=600):
  c = ROOT.TCanvas(c1name,c1name,c1ww,c1wh)
  # Upper histogram plot is pad1
  pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0)  # joins upper and lower plot
  pad1.SetGridx()
  pad1.Draw()
  # Lower ratio plot is pad2
  c.cd()  # returns to main canvas before defining pad2
  pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
  pad2.SetTopMargin(0)  # joins upper and lower plot
  pad2.SetBottomMargin(0.2)
  pad2.SetGridx()
  pad2.Draw()
  return c, pad1, pad2


def makeRatioPlot(h1,h2): 
  # create required parts 
  h3 = createRatio(h1, h2) 
  c, pad1, pad2 = createCanvasPads() 
 
  # draw everything 
  pad1.cd() 
  h1.Draw() 
  h2.Draw("same") 
  # to avoid clipping the bottom zero, redraw a small axis 
  h1.GetYaxis().SetLabelSize(0.0) 
  axis = ROOT.TGaxis(-5, 20, -5, 220, 20, 220, 510, "") 
  axis.SetLabelFont(43) 
  axis.SetLabelSize(15) 
  axis.Draw() 
  pad2.cd() 
  h3.Draw("ep") 




