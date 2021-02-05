#!/bin/sh
rela_path=`dirname $0`
test_path=`cd "$rela_path" && pwd`
task_list="hackbench netperf tbench schbench"
email_address="aubrey.li@intel.com"

task_notify()
{
	local task=$1
	local status=$2
	if [ -z "$email_address" ]; then
		return
	fi
	echo `date` `uname -r` `hostname` | mutt -s "[schedtests]: $task $status" $email_address
}

#wait for the system boots up completely
sleep 30

cd $test_path
touch state_machine

for task in $task_list; do
	if [ `grep -c $task state_machine` -eq '0' ]; then
		task_notify $task "started"
		./run-schedtests.sh $task > cron.log 2>&1
		task_notify $task "completed"
		echo "$task" >> state_machine
		# wait for the notification sent out
		sleep 10
		systemctl start kexec.target
		exit
	fi
done

task_notify "Testing" "completed"
