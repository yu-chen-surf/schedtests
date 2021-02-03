#!/usr/bin/python3
import os
import sys
import numpy as np
import pandas as pd

benchmark_list = ["hackbench", "netperf", "tbench", "schbench"]

class benchmark:
	curr_path = os.getcwd()

	def __init__(self, name):
		self.log_path = os.path.join(benchmark.curr_path, "logs/" + name)
		self.table = pd.DataFrame(columns = ['case', 'load', 'baseline-avg', 'baseline-std', 'patch-avg', 'patch-std'])

	def parse_logfile(self, logfile):
		indicator = []
		fd = open(logfile, 'r')
		for line in fd.readlines():
			items = line.strip().split()
			indicator.append(float(items[0]))
		fd.close()
		return indicator

	def data_process(self, baseline, patch):
		for case in os.listdir(self.log_path):
			case_path = os.path.join(self.log_path,case)
			for load in os.listdir(case_path):
				load_path = os.path.join(case_path, load)
				log_column = []
				for log in os.listdir(load_path):
					result = os.path.join(load_path, log)
					if os.path.isdir(result):
						continue
					indicator = self.parse_logfile(result)
					avg = round(np.mean(indicator), 4)
					std = round(100 * np.std(indicator) / avg, 2)
					if baseline in log:
						baseline_avg = avg
						baseline_std = std
					if patch in log:
						patch_avg = avg
						patch_std = std
				self.table = self.table.append({'case':case,
								'load':load,
								'baseline-avg':baseline_avg,
								'baseline-std':baseline_std,
								'patch-avg':patch_avg,
								'patch-std':patch_std},
                                    				ignore_index=True)
	def report(self, baseline, patch):
		self.data_process(baseline, patch)
		print(self.table)
			

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("log file argument missing")
		sys.exit()
	baseline = sys.argv[1]
	patch = sys.argv[2]
	for i in range(len(benchmark_list)):
		name = benchmark_list[i]
		task = benchmark(name)
		print(name)
		task.report(baseline, patch)
