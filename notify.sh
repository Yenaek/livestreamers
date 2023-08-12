#!/bin/sh
SCRIPT_DIR=$(dirname $(readlink -f $0))
OLD_LIVE=/tmp/livestreamers/live
NEW_LIVE=/tmp/livestreamers/new_live

# create tmp dir
mkdir -p /tmp/livestreamers

# update live streamers
python3 $SCRIPT_DIR/live.py > $NEW_LIVE

# get old and new live channels
OLD_LIVE_CHANNELS=$(cat $OLD_LIVE | awk -F '\t' '{print $1}')
NEW_LIVE_CHANNELS=$(cat $NEW_LIVE | awk -F '\t' '{print $1}')

# get new live channels
NEW_CHANNELS=$(echo "$NEW_LIVE_CHANNELS" | grep -v -F -x -f <(echo "$OLD_LIVE_CHANNELS"))

# notify new live channels
for CHANNEL in $NEW_CHANNELS; do
    GAME=$(cat $NEW_LIVE | grep -F -w "$CHANNEL" | awk -F '\t' '{print $2}')
    TITLE=$(cat $NEW_LIVE | grep -F -w "$CHANNEL" | awk -F '\t' '{print $3}')
    notify-send "$CHANNEL is now playing $GAME" "$TITLE"
done

# write new live to old live
mv $NEW_LIVE $OLD_LIVE
