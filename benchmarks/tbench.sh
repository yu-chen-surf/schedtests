#!/bin/bash
#####################
#tbench config
#####################
: "${tbench_job_list:="48 96 144 192"}"
: "${tbench_iterations:=10}"
: "${tbench_run_time:=100}"

#####################
#tbench parameters
#####################
tbench_host_ip=127.0.0.1
tbench_work_mode="loopback"
tbench_pattern_cmd="grep Throughput"
tbench_sleep_time=10
tbench_log_path=$test_path/logs/tbench

run_tbench_pre()
{
	echo "start tbench server"
	killall tbench_srv
	sleep 1
	tbench_srv &
	sleep 1
	for job in $tbench_job_list; do
		for wm in $tbench_work_mode; do
			mkdir -p $tbench_log_path/$wm/thread-$job/$kernel_name
		done
	done
}

run_tbench_post()
{
	for job in $tbench_job_list; do
		for wm in $tbench_work_mode; do
			log_file=$tbench_log_path/$wm/thread-$job/$kernel_name/tbench.log
			cat $log_file | $tbench_pattern_cmd > \
				$tbench_log_path/$wm/thread-$job/$kernel_name.log
		done
	done
}

run_tbench_single()
{
	local job=$1

	tbench -t $tbench_run_time $job $tbench_host_ip
}

run_tbench_iterations()
{
	local job=$1
	local wm=$2

	for i in $(seq 1 $tbench_iterations); do
		echo -e "\nThread:" $job " - Mode:" $wm " - Iterations:" $i
		run_tbench_single $job >> $tbench_log_path/$wm/thread-$job/$kernel_name/tbench.log
		sleep 1
	done
}

run_tbench()
{
	for job in $tbench_job_list; do
		for wm in $tbench_work_mode; do
			run_tbench_iterations $job $wm
			echo -e "\nWait 10 seconds for the next case"
			sleep $tbench_sleep_time
		done
	done
}

run_tbench_pre
run_tbench
run_tbench_post
