#!/bin/bash

if [ $# -eq 0 ]; then
    echo "ERROR: Please specify your COE username when invoking this script:"
    echo
    echo "  $0 [coe_username] "
    echo
    exit
fi

echo "Creating SSH tunnel to VaporEngine server running on test1..."
echo
echo "Point your browser at:"
echo "  http://localhost:12321/"
echo 
echo "[Kill this script when you want to close the tunnel]"
ssh $1@external.hltcoe.jhu.edu -L 12321:kb.ad.hltcoe.jhu.edu:12321 -N
