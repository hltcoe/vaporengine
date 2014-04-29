import sys, codecs, math, re, pickle, marshal, os, io

# Load data from Aren Jansen's Zero Resource Psuedo-term generator.
# 
# 4/28/14 Paul McNamee

# "Documentation" from Aren via Glen
#
# matches/master_graph.nodes: node file
# matches/master_graph.dedups: deduped cluster file
# matches/master_graph.feats: hard PT counts
#
# formats (divide frames by 100 to get seconds):
#
# nodes: file start_frame end_frame score ignore ignore
# dedups: one line per PT cluster, containing list of node ids
# (correspond to nodes line #s)
# feats: one line per cut, list of (PTID,count) pairs, where PTID is the line # in dedups file

# Desired functionality:
# DOCS[w] -> list of PTs
# PT[x] -> list of all audio frags
# AFRAG[y] -> (aren-idx, file, start, end)

# Just a utility method to load a file in memory
def slurp(fname, encoding='utf-8'):
    lines = []
    #f = open(fname, 'r')
    #f = codecs.open(fname, 'r', encoding)
    f = io.open(fname, 'r', encoding=encoding, newline='\n')
    ## NB: io.open ignores \u2028 and \u2029 (thankfully)
    try:
        lines = f.readlines()
        #for (idx, x) in enumerate(lines):
        #if x.endswith(('\u2028', '\u2029')):
        #lines
    finally:
        f.close()
    return lines


# Loads master_graph.nodes and master_graph.dedups files.  The former
# gives all information about audio events/fragments and the later
# gives the equivalence information about the psuedo-terms (PTs)
    #ZRL = ZRLoader('/home/hltcoe/ajansen/discovery/exp/buckeye-T25/matches/master_graph.nodes', '/home/hltcoe/ajansen/discovery/exp/buckeye-T25/matches/master_graph.dedups');


class ZRLoader:
    def __init__(self, prefix, audiofragments='master_graph.nodes', clusters='master_graph.dedups'):
        self.docs = {}
        self.pts = {}
        self.afrags = {}
        self.load(prefix+audiofragments, prefix+clusters)

    def AllUtterances(self):
        return self.docs.keys()

    def PTIDsForUtterance(self, utterance):
        return self.docs.get(utterance,[])

    def AudioEventIDsForPTID(self, ptid):
        return self.pts.get(ptid,())

    def AudioEventDataForAEID(self, aeid):
        return self.afrags.get(aeid,())
        
    def load(self, audiofragments, clusters):
        frags = slurp(audiofragments)
        for (fragid, line) in enumerate(frags, start=1):
            (file, start, end, score, ig1, ig2) = line.split();
            self.afrags[fragid] = (file, int(start), int(end))
        clusts = slurp(clusters)
        for (ptid, line) in enumerate(clusts, start=1):
            self.pts[ptid] = tuple([int(x) for x in line.split()])

        for (ptid,pttuple) in self.pts.iteritems():
            for fragid in pttuple:
                fragtuple = self.afrags[fragid]
                # fragtuple looks like (docid,start,end)
                docid = fragtuple[0]
                #print "PUT: %s %s" % (docid, ptid)
                self.docs.setdefault(docid,[]).append(ptid)


if __name__ == '__main__':  
    # unicode in python stinks
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdout.encoding = 'utf-8'

    ZRL = ZRLoader('/home/hltcoe/ajansen/discovery/exp/buckeye-T25/matches/')

    for docid in ZRL.AllUtterances()[0:1]:
        for ptid in ZRL.PTIDsForUtterance(docid):
            for aeid in ZRL.AudioEventIDsForPTID(ptid):
                print "%s %s %s %s" % (docid, ptid, aeid, ZRL.AudioEventDataForAEID(aeid))



    # for x in [1+x for x in range(5)]:
    #     print "PT[%s]: %s" % (x, ZRL.pts[x])
    # for x in [1+x for x in range(5)]:
    #     print "AFRAGS[%s]: %s" % (x, ZRL.afrags[x])
    # for docid in ZRL.AllUtterances()[0:5]:
    #     print "DOC[%s]: %s" % (docid, ZRL.docs[docid])
    # for x in [1+x for x in range(5)]:
    #     print "PT[%s]: %s" % (x, ZRL.pts[x])
    # for x in [1+x for x in range(5)]:
    #     print "AFRAGS[%s]: %s" % (x, ZRL.afrags[x])


    
# end o' file
