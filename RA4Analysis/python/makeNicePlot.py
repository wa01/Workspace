import ROOT

def DrawNicePlot(plot1,plot1name,yaxis,xaxis,path,fileName):

  can = ROOT.TCanvas("c",plot1name,800,800)
  can.cd()
  plot1.SetTitle(plot1name)
  plot1.SetStats(0)
  #plot1.SetLineColor(ROOT.ROOT.kAzure+10)
  plot1.SetLineColor(ROOT.ROOT.kBlack)
  plot1.SetLineWidth(2)
  #plot1.SetAxisRange(0.1,(plot1.GetMaximum())*(plot1.GetMaximum()),"Y")
  plot1.Draw()
  plot1.GetYaxis().SetTitle(yaxis)
  plot1.GetYaxis().SetTitleSize(20)
  plot1.GetYaxis().SetTitleFont(43)
  plot1.GetYaxis().SetTitleOffset(1.55)
  plot1.GetYaxis().SetLabelFont(43)
  plot1.GetYaxis().SetLabelSize(15)
  plot1.GetXaxis().SetTitle(xaxis)
  leg = ROOT.TLegend(0.7,0.8,0.9,0.9)
  leg.AddEntry(plot1, plot1name,"l")
  leg.SetFillColor(0)
  leg.Draw()
  can.SetLogy()  
#can.setLogy()
  can.SetGridx()
  #can.Update()
  can.SaveAs(path+fileName)
