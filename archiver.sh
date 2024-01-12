#!/bin/bash
DSTRING=$(date +%F)
# first, strip underscores
CLEAN=${DSTRING//_/}
# next, replace spaces with underscores
CLEAN=${CLEAN// /_}
# now, clean out anything that's not alphanumeric or an underscore
CLEAN=${CLEAN//[^a-zA-Z0-9_]/}
# finally, lowercase with TR
CLEAN=`echo -n $CLEAN | tr A-Z a-z`
cp ap.html archive/$CLEAN.html
