#!/bin/sh

# python keyboard library does not handle keyboard connection and disconnection events
# so this service monitors the keyboards and restarts the mediakey service when it detects
# a change in the number of connected keyboards

last_num_kbds=0

while true; do
    # get number of connected keyboards
    curr_num_kbds=$(lsusb -v 2>/dev/null | grep -i keyboard | awk '{ print $2 }')
    [[ -z "${num_keyboards}" ]] && num_keyboards=0

    # if # of kbds has changed
    if [[ ${curr_num_kbds} -ne ${last_num_kbds} ]]; then
        # restart service 
    fi 

    last_num_kbds=curr_num_kbds

done

