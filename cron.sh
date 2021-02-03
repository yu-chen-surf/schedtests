#!/bin/sh
task_list="hackbench netperf tbench schbench"
email_address="aubrey.li@intel.com"

sleep 30

cd /home/aubrey/work/schedtests
touch state_machine

for task in $task_list; do
	if [ `grep -c $task state_machine` -eq '0' ]; then
		echo `date` | mutt -s "[schedtests]: $task started" $email_address
		./run-schedtests.sh $task > cron.log 2>&1
		echo `date` | mutt -s "[schedtests]: $task completed" $email_address
		echo "$task" >> state_machine
		systemctl start kexec.target
		exit
	fi
done

echo `date` | mutt -s "[schedtests]: Testing completed" $email_address
