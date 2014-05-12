import os
import pysox

buckeye = {}
buckeye['DB_HOST'] = 'r4n7'
buckeye['DB_NAME'] = 'buckeye'
buckeye['DB_PORT'] = 27017
buckeye['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye['WAV_PATH'] = '/home/hltcoe/ajansen/aren_local/BUCKEYE'
buckeye['ZRL_PATH'] = '/home/hltcoe/ajansen/discovery/exp/buckeye-T25/'

buckeye_localhost = {}
buckeye_localhost['DB_HOST'] = 'localhost'
buckeye_localhost['DB_NAME'] = 'buckeye'
buckeye_localhost['DB_PORT'] = 27017
buckeye_localhost['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye['WAV_PATH'] = os.path.join(os.getenv('HOME'), 'BUCKEYE')
buckeye_localhost['ZRL_PATH'] = os.path.join(os.getenv('HOME'), 'buckeye-T25/')
