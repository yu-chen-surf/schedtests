#!/usr/bin/python3
import os
import sys
import numpy as np
import pandas as pd

benchmark_list = [
		{"name":"hackbench",	"better":"less"},
		{"name":"netperf",	"better":"bigger"},
		{"name":"tbench",	"better":"bigger"},
		{"name":"schbench",	"better":"less"},
		]

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
		#self.table.sort_values(by=['case', 'patch-avg'], ascending=True, inplace=True)

	def report(self, baseline, patch, better):
		self.data_process(baseline, patch)
		print('{0:16s}\t{1:8s}\t{2}({3})\t{4} ({5:>6s})'.format('case','load','baseline','std%','patch%','std%'))
		for i in range(len(self.table)):
			if better == 'less':
				change = round((1 - self.table['patch-avg'][i]/self.table['baseline-avg'][i]) * 100.0, 2)
			else:
				change = round((self.table['patch-avg'][i]/self.table['baseline-avg'][i] - 1) * 100.0, 2)
			print('{0:16s}\t{1:8s}\t{2:5.2f} ({3:6.2f})\t{4:>+6.2f} ({5:6.2f})'.format(self.table['case'][i],
								    self.table['load'][i],
								    1.0,
								    self.table['baseline-std'][i],
								    change,
								    self.table['patch-std'][i]))

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("log file argument missing")
		sys.exit()
	baseline = sys.argv[1]
	patch = sys.argv[2]
	for i in range(len(benchmark_list)):
		name = benchmark_list[i]['name']
		better = benchmark_list[i]['better']
		task = benchmark(name)
		print("\n{0}\n".format(name))
		task.report(baseline, patch, better)
