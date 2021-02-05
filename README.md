# schedtests

A lightweight benchmarking framework primarily aimed at Linux kernel scheduler
testing. It provides a reasonable coverage within one night, to compare the
difference between a baseline kernel and a testing kernel.

## Basic Installation

### schedtests includes 4 benchmarks:
- hackbench (apt install rt-tests)
- netperf (apt install netperf)
- tbench (apt install dbench)
- schbench (https://git.kernel.org/pub/scm/linux/kernel/git/mason/schbench.git)

Note, schbench is expected to be installed at /usr/bin.

### result process and report:
- python3 (apt install python3.x)
- numpy (pip3 install numpy)
- pandas (pip3 install pandas)

### [optional] email notification:
- mutt (apt install mutt)
- msmtp (apt install msmtp)

mutt and msmtp is expected to be properly configured.

## Configuration
