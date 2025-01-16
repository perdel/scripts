#!/bin/bash

nflag=
lflag=
tflag=
while getopts nlt: opts
do
    case $opts in
        n) nflag=1;;
        l) lflag=1;;
        t) tflag=1
           tval="$OPTARG";;
        ?) printf "Usage: %s: [-n] [-l] [-t] TIME\n" $0
           exit;;
    esac
done

shift $((OPTIND-1))

# The source path to backup. Can be local or remote.
SOURCE=$1/

# Where to store the incremental backups
DESTBASE=$2

MORE_OPTS=

if [ ! -z "$nflag" ]; then
    MORE_OPTS+="--dry-run "

fi
if [ ! -z "$lflag" ]; then
    MORE_OPTS+="--copy-links"
fi

if [ ! -z "$tflag" ]; then
    # Where to store current backup
    DEST="$DESTBASE/$(hostnamectl hostname)-work-$(date +%${tval}_%y)"
    # Where to find last backup
    LAST="$DESTBASE/$(hostnamectl hostname)-work-$(date -d "last year" +%W_%y)/"
else
    # Where to store this week's backup
    DEST="$DESTBASE/$(hostnamectl hostname)-work-$(date +%W_%y)"
    # Where to find last week's backup
    LAST="$DESTBASE/$(hostnamectl hostname)-work-$(date -d "last week" +%W_%y)/"
fi

# Use yesterday's backup as the incremental base if it exists
if [ -d "$LAST" ]
then
    OPTS="--link-dest $LAST"
fi

# Run the rsync
rsync -av $OPTS $MORE_OPTS "$SOURCE" "$DEST"
