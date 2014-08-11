#include "Workspace/HEPHYCMSSWTools/plugins/multMETCorrInfoWriter.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include <string>

multMETCorrInfoWriter::multMETCorrInfoWriter( const edm::ParameterSet & cfg ): moduleLabel_(cfg.getParameter<std::string>("@module_label"))
{
  edm::Service<TFileService> fs;

  pflowToken_ = consumes<std::vector<reco::PFCandidate> >(cfg.getParameter<edm::InputTag>("srcPFlow"));

  cfgCorrParameters_ = cfg.getParameter<std::vector<edm::ParameterSet> >("parameters");
//  etaNBins_.clear();
  etaMin_.clear();
  etaMax_.clear();
  type_.clear();
  nbins_.clear();
  counts_.clear();
  MEx_.clear();
  MEy_.clear();
  for (std::vector<edm::ParameterSet>::const_iterator v = cfgCorrParameters_.begin(); v!=cfgCorrParameters_.end(); v++) {
    int etaNBins = v->getParameter<int>("etaNBins");
    double etaMin = v->getParameter<double>("etaMin");
    double etaMax = v->getParameter<double>("etaMax");
    int phiNBins = v->getParameter<int>("phiNBins");
    double phiMin = v->getParameter<double>("phiMin");
    double phiMax = v->getParameter<double>("phiMax");
    int nMin = v->getParameter<int>("nMin");
    int nMax = v->getParameter<int>("nMax");
    int nbins = v->getParameter<double>("nbins");
//    etaNBins_.push_back(etaNBins);
    etaMin_.push_back(etaMin);
    etaMax_.push_back(etaMax);
    nbins_.push_back(nbins);
    type_.push_back(v->getParameter<int>("type"));
    counts_.push_back(0);
    MEx_.push_back(0.);
    MEy_.push_back(0.);
//    std::cout<<" n/min/max "<<nbins<<" "<<etaMin<<" "<<etaMax<<std::endl;
    profile_x_.push_back(fs->make<TProfile>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_Px").c_str(),"Px", nbins, nMin, nMax, -300,300));
    profile_y_.push_back(fs->make<TProfile>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_Py").c_str(),"Py", nbins, nMin, nMax, -300,300));

    occupancy_.push_back(fs->make<TH2F>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_occupancy").c_str(),"occupancy",  etaNBins, etaMin, etaMax, phiNBins, phiMin, phiMax));
    energy_.push_back(fs->make<TH2F>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_energy").c_str(),"energy",           etaNBins, etaMin, etaMax, phiNBins, phiMin, phiMax));
    pt_.push_back(fs->make<TH2F>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_pt").c_str(),"pt",                       etaNBins, etaMin, etaMax, phiNBins, phiMin, phiMax));

    multiplicity_.push_back(fs->make<TH1F>(std::string(moduleLabel_).append("_").append(v->getParameter<std::string>("name")).append("_multiplicity").c_str(),"multiplicity", nbins, nMin, nMax));
  }
}

void multMETCorrInfoWriter::analyze( const edm::Event& evt, const edm::EventSetup& setup) {

  for (unsigned i=0;i<counts_.size();i++) {
    counts_[i]=0;
    MEx_[i]=0.;
    MEy_[i]=0.;
  } 
//  typedef std::vector<reco::PFCandidate>  pfCand;
  edm::Handle<std::vector<reco::PFCandidate> > particleFlow;
  evt.getByToken(pflowToken_, particleFlow);
  for (unsigned i = 0; i < particleFlow->size(); ++i) {
    const reco::PFCandidate& c = particleFlow->at(i);
    for (unsigned j=0; j<type_.size(); j++) {
      if (c.particleId()==type_[j]) {
        if ((c.eta()>etaMin_[j]) and(c.eta()<etaMax_[j])) {
          counts_[j]+=1;
          MEx_[j]-=c.px();
          MEy_[j]-=c.py();

          pt_[j]->Fill(c.eta(), c.phi(), c.pt()); 
          energy_[j]->Fill(c.eta(), c.phi(), c.energy()); 
          occupancy_[j]->Fill(c.eta(), c.phi()); 
        }
      }
    }
  }
  for (std::vector<edm::ParameterSet>::const_iterator v = cfgCorrParameters_.begin(); v!=cfgCorrParameters_.end(); v++) {
    unsigned j=v-cfgCorrParameters_.begin();
//    std::cout<<"j "<<j<<" "<<v->getParameter<std::string>("name")<<" "<<counts_[j]<<" "<<MEx_[j]<<" "<<MEy_[j]<<std::endl;
    profile_x_[j]->Fill(counts_[j], MEx_[j]);
    profile_y_[j]->Fill(counts_[j], MEy_[j]);
    multiplicity_[j]->Fill(counts_[j]);
  }
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(multMETCorrInfoWriter);
