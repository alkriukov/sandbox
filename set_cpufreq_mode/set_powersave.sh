#!/bin/sh -e

cpufreq-set -g powersave
cpufreq-set -f 800000

exit 0

