#!/bin/sh
sleep 30
cd /home/aubrey/work/schedtests
touch complete_list

task_list="hackbench netperf tbench schbench"

for task in $task_list; do
	if [ `grep -c $task complete_list` -eq '0' ]; then
		./run-schedtests.sh $task > cron.log 2>&1
		echo "$task" >> complete_list
		systemctl start kexec.target
		exit
	fi
done
./run-schedtests.sh complete
