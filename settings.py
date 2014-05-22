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
buckeye_localhost['WAV_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/BUCKEYE')
buckeye_localhost['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
buckeye_localhost['ZRL_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/buckeye-T25/')
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

fisher_spanish_localhost = {}
fisher_spanish_localhost['DB_HOST'] = 'localhost'
fisher_spanish_localhost['DB_NAME'] = 'fisher_spanish'
fisher_spanish_localhost['DB_PORT'] = 27017
fisher_spanish_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
fisher_spanish_localhost['WAV_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/FISHSPwav/')
fisher_spanish_localhost['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
fisher_spanish_localhost['ZRL_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/fishsp200/')
settings['fisher_spanish_localhost'] = fisher_spanish_localhost

tagalog = {}
tagalog['DB_HOST'] = 'r4n7'
tagalog['DB_NAME'] = 'tagalog'
tagalog['DB_PORT'] = 27017
tagalog['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
tagalog['WAV_PATH'] = '/home/hltcoe/ajansen/discovery/exp/tagalog300'
tagalog['ZRL_CLUSTERS'] = 'matches/master_graph.dedups'
tagalog['ZRL_PATH'] = '/home/hltcoe/ajansen/discovery/exp/tagalog300/'
settings['tagalog'] = tagalog

current_corpora = ['buckeye', 'fisher_spanish', 'tagalog']
