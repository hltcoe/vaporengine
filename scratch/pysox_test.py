#!/usr/bin/env python

import os
import tempfile

import pysox

INPUT_FILES = ['0003.wav', '0004.wav']
OUTPUT_FILE = 'out.wav'

# Create a temporary directory
tmp_directory = tempfile.mkdtemp()
tmp_filename = os.path.join(tmp_directory, 'combined_clips.wav')

# The first argument to CSoxStream must be a filename with a '.wav' extension.
#
# If the output file does not have a '.wav' extension, pysox will raise
# an "IOError: No such file" exception.
outfile = pysox.CSoxStream(
    tmp_filename,
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

# Read in audio data from temporary file
wav_data = open(tmp_filename, 'rb').read()
open(OUTPUT_FILE, 'wb').write(wav_data)

# Clean up temporary files
os.remove(tmp_filename)
os.rmdir(tmp_directory)
