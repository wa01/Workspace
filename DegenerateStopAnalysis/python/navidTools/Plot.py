
import ROOT
import math

from Workspace.DegenerateStopAnalysis.navidTools.plotTools import *



class Plot(dict):
  def __init__(self, name, var, bins, decor={},cut=''):
    super(Plot, self).__init__( name=name, var=var, bins=bins,decor=decor,cut='')
    self.__dict__ = self 
    #if not all([x in self.__dict__ for x in ['name','tree']]):
    #  assert False,  "Cannot create sample.... Usage:  Sample(name='name', tree=ROOT.TChain, isData=0, isSignal=0, color=ROOT.kBlue)"
    #for attr in defdict:
    #  if attr not in self.__dict__:
    #    self[attr]=defdict[attr]
    if len(self.bins)==3:
      self.is1d = True
    else: self.is1d=  False
    if len(self.bins)==6:
      self.is2d = True
    else: self.is2d = False
    if "hists" not in self.__dict__:
      self.hists=Dict()
  def decorate(hist,decorDict):
    pass


class Plots(dict):
  def __init__(self,  **kwargs):
    super(Plots, self).__init__(**kwargs)
    self.__dict__=self


 
 
 
