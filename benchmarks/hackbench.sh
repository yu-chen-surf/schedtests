#!/bin/bash
#####################
#hackbench config
#####################
hackbench_job_list="3 6 9 12"
hackbench_iterations=10
hackbench_sleep_time=10
hackbench_log_path=$test_path/logs/hackbench

#####################
#hackbench parameters
#####################
hackbench_work_type="process threads"
hackbench_ipc_mode="pipe sockets"
hackbench_work_loops=10000
hackbench_data_size=100
hackbench_pattern_cmd="grep Time"

run_hackbench_pre()
{
	for job in $hackbench_job_list; do
		for wt in $hackbench_work_type; do
			for im in $hackbench_ipc_mode; do
				mkdir -p $hackbench_log_path/$wt-$im/group-$job/$kernel_name
			done
		done
	done

}

run_hackbench_post()
{
	for job in $hackbench_job_list; do
		for wt in $hackbench_work_type; do
			for im in $hackbench_ipc_mode; do
				log_file=$hackbench_log_path/$wt-$im/group-$job/$kernel_name/hackbench.log
				cat $log_file | $hackbench_pattern_cmd > \
					$hackbench_log_path/$wt-$im/group-$job/$kernel_name.log
			done
		done
	done

}
run_hackbench_single()
{
	local job=$1
	local wt=$2
	local im=$3	
	if [ $im == "pipe" ]; then
		hackbench -g $job --$wt --$im -l $hackbench_work_loops -s $hackbench_data_size
	elif [ $im == "sockets" ]; then
		hackbench -g $job --$wt -l $hackbench_work_loops -s $hackbench_data_size
	else
		echo "hackbench: wrong IPC mode!"
	fi
}

run_hackbench_iterations()
{
	local job=$1
	local wt=$2
	local im=$3	

	for i in $(seq 1 $hackbench_iterations); do
		echo "Group:" $job " - Type:" $wt " - Mode:" $im " - Iterations:" $i
		run_hackbench_single $job $wt $im >> $hackbench_log_path/$wt-$im/group-$job/$kernel_name/hackbench.log
		sleep 1
	done
}

run_hackbench()
{
	for job in $hackbench_job_list; do
		for wt in $hackbench_work_type; do
			for im in $hackbench_ipc_mode; do
				run_hackbench_iterations $job $wt $im
				echo "Wait 10 seconds for the next case"
				sleep $hackbench_sleep_time
			done
		done
	done
}

run_hackbench_pre
run_hackbench
run_hackbench_post
