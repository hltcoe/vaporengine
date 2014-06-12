import os
import pysox

settings = {}

buckeye = {}
buckeye['DB_HOST'] = 'r4n7'
buckeye['DB_NAME'] = 'buckeye'
buckeye['DB_PORT'] = 27017
buckeye['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
#buckeye['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
buckeye['ZR_CLUSTERS'] = 'matches/master_graph.dedups.80'
buckeye['ZR_PATH'] = '/home/hltcoe/ajansen/discovery/exp/buckeye-T25/'
settings['buckeye'] = buckeye

buckeye_localhost = {}
buckeye_localhost['DB_HOST'] = 'localhost'
buckeye_localhost['DB_NAME'] = 'buckeye'
buckeye_localhost['DB_PORT'] = 27017
buckeye_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye_localhost['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
buckeye_localhost['ZR_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/buckeye-T25/')
settings['buckeye_localhost'] = buckeye_localhost

fisher_spanish = {}
fisher_spanish['DB_HOST'] = 'r4n7'
fisher_spanish['DB_NAME'] = 'fisher_spanish'
fisher_spanish['DB_PORT'] = 27017
fisher_spanish['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
fisher_spanish['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
fisher_spanish['ZR_PATH'] = '/home/hltcoe/ajansen/discovery/exp/fishsp200/'
settings['fisher_spanish'] = fisher_spanish

fisher_spanish_localhost = {}
fisher_spanish_localhost['DB_HOST'] = 'localhost'
fisher_spanish_localhost['DB_NAME'] = 'fisher_spanish'
fisher_spanish_localhost['DB_PORT'] = 27017
fisher_spanish_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
fisher_spanish_localhost['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
fisher_spanish_localhost['ZR_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/fishsp200/')
settings['fisher_spanish_localhost'] = fisher_spanish_localhost

QASW = {}
QASW['DB_HOST'] = 'r4n7'
QASW['DB_NAME'] = 'QASW'
QASW['DB_PORT'] = 27017
QASW['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,14)
QASW['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
QASW['ZR_PATH'] = '/home/hltcoe/ajansen/discovery/exp/QASW'
settings['QASW'] = QASW

QASW_localhost = {}
QASW_localhost['DB_HOST'] = 'localhost'
QASW_localhost['DB_NAME'] = 'QASW'
QASW_localhost['DB_PORT'] = 27017
QASW_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,14)
QASW_localhost['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
QASW_localhost['ZR_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/QASW/')
settings['QASW_localhost'] = QASW_localhost

tagalog = {}
tagalog['DB_HOST'] = 'r4n7'
tagalog['DB_NAME'] = 'tagalog'
tagalog['DB_PORT'] = 27017
tagalog['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
tagalog['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
tagalog['ZR_PATH'] = '/home/hltcoe/ajansen/discovery/exp/tagalog300/'
settings['tagalog'] = tagalog

tagalog_localhost = {}
tagalog_localhost['DB_HOST'] = 'localhost'
tagalog_localhost['DB_NAME'] = 'tagalog'
tagalog_localhost['DB_PORT'] = 27017
tagalog_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(8000.0,1,16)
tagalog_localhost['ZR_CLUSTERS'] = 'matches/master_graph.dedups'
tagalog_localhost['ZR_PATH'] = os.path.join(os.getenv('HOME'), 'zr_datasets/tagalog300/')
settings['tagalog_localhost'] = tagalog_localhost

current_corpora = ['buckeye', 'fisher_spanish', 'QASW', 'tagalog']
