#!/usr/bin/env python

import pysox

INPUT_FILES = ['0003.wav', '0004.wav']
OUTPUT_FILE = 'out.wav'

outfile = pysox.CSoxStream(
    OUTPUT_FILE,
    'w',
    pysox.CSignalInfo(8000.0,1,14))  # TODO: Don't hard-code sample rate

for input_filename in INPUT_FILES:
    START_OFFSET = b'25'
    DURATION = b'3'

    infile = pysox.CSoxStream(input_filename)
    chain = pysox.CEffectsChain(infile, outfile)
    chain.add_effect(pysox.CEffect('trim', [START_OFFSET, DURATION]))
    chain.flow_effects()
    infile.close()

outfile.close()
