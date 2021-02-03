#!/bin/bash
test_path=`pwd`
kernel_name="5.10.9-upstream"
email_address="aubrey.li@intel.com"

run_hackbench()
{
	. $test_path/benchmarks/hackbench.sh
}

run_netperf()
{
	. $test_path/benchmarks/netperf.sh
}

run_tbench()
{
	. $test_path/benchmarks/tbench.sh
}

run_schbench()
{
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
