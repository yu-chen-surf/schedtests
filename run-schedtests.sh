#!/bin/bash
rela_path=`dirname $0`
test_path=`cd "$rela_path" && pwd`

pepc.standalone pstates config --governor performance
pepc.standalone pstates config --turbo off
pepc.standalone cstates config --disable C6
echo 1 > /proc/sys/kernel/sched_schedstats
echo 1 > /sys/kernel/debug/tracing/events/sched/sched_update_sd_lb_stats/enable
pepc.standalone cpu-hotplug offline --packages 1

sleep 10

run_name=`uname -r`
# 25% 50% 75% 100% 125% 150% 175% 200%
min_job=$(($(nproc) / 4))
joblist="$min_job $(($min_job * 2)) $(($min_job * 3)) $(($min_job * 4)) $(($min_job * 5)) $(($min_job * 6)) $(($min_job * 7)) $(($min_job * 8))"
runtime=60
iterations=3

start_hackbench()
{
	hackbench_job_list="1 2 4 8"
	hackbench_iterations=$iterations
	. $test_path/benchmarks/hackbench.sh
}

start_netperf()
{
	netperf_job_list=$joblist
	netperf_run_time=$runtime
	netperf_iterations=$iterations
	. $test_path/benchmarks/netperf.sh
}

start_tbench()
{
	tbench_job_list=$joblist
	tbench_run_time=$runtime
	tbench_iterations=$iterations
	. $test_path/benchmarks/tbench.sh
}

start_schbench()
{
	schbench_job_list="1 2 4 8"
	schbench_run_time=$runtime
	schbench_iterations=$iterations
	. $test_path/benchmarks/schbench.sh
}

[ $# = 0 ] && {
        start_hackbench
        start_netperf
        start_tbench
        start_schbench
        exit
}

benchmark=$1

if [ -n "$2" ]; then
	joblist=$2
fi

case "$benchmark" in
	'hackbench'	) start_hackbench	;;
	'netperf'	) start_netperf	;;
	'tbench'	) start_tbench	;;
	'schbench'	) start_schbench	;;
esac
