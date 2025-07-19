#!/bin/sh -e

# For system-wide scope on Ubuntu - put this content into /etc/rc.local
cpufreq-set -g powersave
cpufreq-set -f 800000

exit 0

