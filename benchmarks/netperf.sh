#!/bin/bash
#####################
#netperf config
#####################
: "${netperf_job_list:="48 96 144 192"}"
: "${netperf_iterations:=10}"
: "${netperf_run_time:=100}"

#####################
#netperf parameters
#####################
netperf_work_mode="TCP_RR UDP_RR"
netperf_host_ip=127.0.0.1
netperf_sleep_time=10
pattern_cmd="grep $netperf_run_time.00"
netperf_log_path=$test_path/logs/netperf

run_netperf_pre()
{
	echo "start netperf server"
	pgrep netserver && killall netserver
	sleep 1
	netserver
	sleep 1
	for job in $netperf_job_list; do
		for wm in $netperf_work_mode; do
			mkdir -p $netperf_log_path/$wm/thread-$job/$kernel_name
		done
	done
}

run_netperf_post()
{
	for job in $netperf_job_list; do
		for wm in $netperf_work_mode; do
			log_file=$netperf_log_path/$wm/thread-$job/$kernel_name/netperf.log
			cat $log_file | $pattern_cmd > \
				$netperf_log_path/$wm/thread-$job/$kernel_name.log
		done
	done
}

run_netperf_single()
{
	local job=$1
	local wm=$2
	for i in $(seq 1 $job); do
		netperf -4 -H $netperf_host_ip -t $wm -c -C -l $netperf_run_time &
	done
	wait
}

run_netperf_iterations()
{
	local job=$1
	local wm=$2

	for i in $(seq 1 $netperf_iterations); do
		echo "Thread:" $job " - Mode:" $wm " - Iterations:" $i
		run_netperf_single $job $wm >> $netperf_log_path/$wm/thread-$job/$kernel_name/netperf.log
		sleep 1
	done
}

run_netperf()
{
	for job in $netperf_job_list; do
		for wm in $netperf_work_mode; do
			echo "Wait 10 seconds for the next case"
			sleep $netperf_sleep_time
			run_netperf_iterations $job $wm
		done
	done
	echo -e "\nnetperf testing completed"
}

run_netperf_pre
run_netperf
run_netperf_post
