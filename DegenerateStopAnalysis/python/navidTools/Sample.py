
import ROOT
import math
from Plot import Plot, Plots


class Sample(dict):
  #def __init__(self, *args, **kwargs):
  #  super(Sample, self).__init__(*args, **kwargs)
  def __init__(self, name,tree,isSignal=0,isData=0,color=0,lineColor=0,weight="weight", **kwargs):
    super(Sample, self).__init__(name=name,tree=tree,isSignal=isSignal, isData=isData,color=color ,weight=weight,**kwargs)
    self.__dict__ = self 
    self.tree.SetLineColor(self.color)
    self.plots=Plots()



class Samples(dict):
  def __init__(self,  **kwargs):
    super(Samples, self).__init__(**kwargs)
    self.__dict__=self
 
    data= [samp for samp in self.__dict__ if  self[samp].isData ]
    print data 



    if len(data)>0:
      data_lumi = self[data[0]]['lumi']
      print "--------- Samples include data" 
      print "--------- data_weight will be created for MC samples using the data lumi:  %s fb-1 "%data_lumi
      includes_data= True
      for samp in self:
        if not self[samp].isData:
          self[samp].data_weight = "({w})*({dlumi})/({mclumi})".format(w=self[samp].weight, dlumi=data_lumi, mclumi=self[samp].lumi)
      

  def bkgs(self):
    return 0 


 
    #self.iterall = self.all.itervalues
  def doStuff(self):    #### not sure how to add these without messing with the class/dict structre  
    print [ self[samp].isData for samp in self.__dict__ ]
    self.all = [samp for samp in self.__dict__ ] 
    self.bkgs = [samp for samp in self.all if not self[samp].isData and not self[samp].isSignal ]
    self.sigs = [samp for samp in self.all if self[samp].isSignal ]
    self.data= [samp for samp in self.all if  self[samp].isData ]
    if any( [self[samp].isData and self[samp].isSignal for samp in self.all ] ):
      assert "A sample is Signal and Data??!... nice try, but no!"

    if len(ndata)>0:
      print "Samples include data", "MC will be reweighted based on data lumi"
      self.includes_data= True
      
    else:
      self.includes_data= False
  




