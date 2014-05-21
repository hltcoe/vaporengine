import os
import pysox

settings = {}

buckeye = {}
buckeye['DB_HOST'] = 'r4n7'
buckeye['DB_NAME'] = 'buckeye'
buckeye['DB_PORT'] = 27017
buckeye['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye['WAV_PATH'] = '/home/hltcoe/ajansen/aren_local/BUCKEYE'
#buckeye['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
buckeye['ZRL_CLUSTERS'] = 'matches/master_graph.dedups.80'
buckeye['ZRL_PATH'] = '/home/hltcoe/ajansen/discovery/exp/buckeye-T25/'
settings['buckeye'] = buckeye

buckeye_localhost = {}
buckeye_localhost['DB_HOST'] = 'localhost'
buckeye_localhost['DB_NAME'] = 'buckeye'
buckeye_localhost['DB_PORT'] = 27017
buckeye_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye_localhost['WAV_PATH'] = os.path.join(os.getenv('HOME'), 'BUCKEYE')
buckeye_localhost['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
buckeye_localhost['ZRL_PATH'] = os.path.join(os.getenv('HOME'), 'buckeye-T25/')
settings['buckeye_localhost'] = buckeye_localhost

fisher_spanish = {}
fisher_spanish['DB_HOST'] = 'r4n7'
fisher_spanish['DB_NAME'] = 'fisher_spanish'
fisher_spanish['DB_PORT'] = 27017
fisher_spanish['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
fisher_spanish['WAV_PATH'] = '/home/hltcoe/ajansen/discovery/exp/fishsp200'
fisher_spanish['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
fisher_spanish['ZRL_PATH'] = '/home/hltcoe/ajansen/discovery/exp/fishsp200/'
settings['fisher_spanish'] = fisher_spanish


tagolog = {}
tagolog['DB_HOST'] = 'r4n7'
tagolog['DB_NAME'] = 'tagolog'
tagolog['DB_PORT'] = 27017
tagolog['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
tagolog['WAV_PATH'] = '/home/hltcoe/ajansen/discovery/exp/tagolog300'
tagolog['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
tagolog['ZRL_PATH'] = '/home/hltcoe/ajansen/discovery/exp/tagolog300/'
settings['tagolog'] = tagolog

current_corpora = ['buckeye', 'fisher_spanish', 'tagolog']
