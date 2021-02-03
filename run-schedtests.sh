#!/bin/bash
test_path=`pwd`
kernel_name=`uname -r`
email_address="aubrey.li@intel.com"

iterations=2
runtime=10

run_hackbench()
{
	hackbench_job_list="6 12"
	hackbench_iterations=$iterations
	. $test_path/benchmarks/hackbench.sh
}

run_netperf()
{
	netperf_job_list="52 104"
	netperf_iterations=$iterations
	netperf_run_time=$runtime
	. $test_path/benchmarks/netperf.sh
}

run_tbench()
{
	tbench_job_list="52 104"
	tbench_iterations=$iterations
	tbench_run_time=$runtime
	. $test_path/benchmarks/tbench.sh
}

run_schbench()
{
	schbench_job_list="4 8"
	schbench_iterations=$iterations
	schbench_run_time=$runtime
	. $test_path/benchmarks/schbench.sh
}

run_complete()
{
	echo `date` | mutt -s "[schedtests]: Testing completed" $email_address
}

benchmark=$1

case "$benchmark" in
	'hackbench'	) run_hackbench	;;
	'netperf'	) run_netperf	;;
	'tbench'	) run_tbench	;;
	'schbench'	) run_schbench	;;
	'complete'	) run_complete	;;
esac
