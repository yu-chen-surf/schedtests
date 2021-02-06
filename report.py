#!/usr/bin/python3
import os
import sys
import getopt
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
		self.table = pd.DataFrame(columns = ['case', 'load', 'baseline-avg', 'baseline-std', 'compare-avg', 'compare-std'])

	def parse_logfile(self, logfile):
		indicator = []
		fd = open(logfile, 'r')
		for line in fd.readlines():
			items = line.strip().split()
			indicator.append(float(items[0]))
		fd.close()
		return indicator

	def data_process(self, baseline, compare):
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
					if compare in log:
						compare_avg = avg
						compare_std = std
				self.table = self.table.append({'case':case,
								'load':load,
								'baseline-avg':baseline_avg,
								'baseline-std':baseline_std,
								'compare-avg':compare_avg,
								'compare-std':compare_std},
                                                                ignore_index=True)
		self.table['sort'] = self.table['load'].str.extract('(\d+)', expand=False).astype(int)
		self.table.sort_values(by=['case', 'sort'], inplace=True, ascending=True)
		self.table = self.table.drop('sort', axis=1).reset_index(drop=True)

	def report(self, baseline, compare, better):
		self.data_process(baseline, compare)
		print('{0:16s}\t{1:8s}\t{2}({3})\t{4}({5:>5s})'.format('case','load','baseline','std%','compare%','std%'))
		for i in range(len(self.table)):
			if better == 'less':
				change = round((1 - self.table['compare-avg'][i]/self.table['baseline-avg'][i]) * 100.0, 2)
			else:
				change = round((self.table['compare-avg'][i]/self.table['baseline-avg'][i] - 1) * 100.0, 2)
			print('{0:16s}\t{1:8s}\t{2:5.2f} ({3:6.2f})\t{4:>+6.2f} ({5:6.2f})'.format(self.table['case'][i],
								    self.table['load'][i],
								    1.0,
								    self.table['baseline-std'][i],
								    change,
								    self.table['compare-std'][i]))
def usage():
	print("./report.py usage:")
	print("\t-t (--testname) test case name")
	print("\t-b (--baseline) baseline run name")
	print("\t-c (--compare) compare run name")

if __name__ == "__main__":

	try:
		opts, args = getopt.getopt(sys.argv[1:], '-h-t:-b:-c:', ['help','testname','baseline','compare'])
	except getopt.GetoptError:
		usage()
		sys.exit()

	testname = ""
	baseline = ""
	compare = ""
	for opt_name, opt_value in opts:
		if opt_name in ('-h', '--help'):
			usage()
			sys.exit()
		if opt_name in ('-t', '--testname'):
			testname = opt_value
		if opt_name in ('-b', '--baseline'):
			baseline = opt_value
		if opt_name in ('-c', '--compare'):
			compare = opt_value

	if not baseline or not compare:
		usage()
		sys.exit()

	for i in range(len(benchmark_list)):
		name = benchmark_list[i]['name']
		if testname and testname not in name:
			continue
		better = benchmark_list[i]['better']
		task = benchmark(name)
		print("\n{0}".format(name))
		print("==========")
		task.report(baseline, compare, better)
