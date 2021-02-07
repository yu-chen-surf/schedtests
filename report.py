#!/usr/bin/python3
import os
import sys
import getopt
import numpy as np
import pandas as pd

#global benchmark_list
bmk_list = [
    {"name":"hackbench","metrics":"Time",    "better":"-"},
    {"name":"netperf",  "metrics":"Trans/s", "better":"+"},
    {"name":"tbench",   "metrics":"Tput/s",  "better":"+"},
    {"name":"schbench", "metrics":"Lat_99th","better":"-"},
]

class benchmark:
    curr_path = os.getcwd()

    def __init__(self, name):

        # the relative log path is ./logs
        self.log_path = os.path.join(benchmark.curr_path, "logs/" + name)

        # metrics extracted as the first column in the log file
        self.metrics_pos = 0

        # benchmark core table
        self.table = pd.DataFrame(columns =
                    ['case', 'load', 'b_avg', 'b_std', 'c_avg', 'c_std'])

    def _parse_logfile(self, logfile):

        metrics = []

        fd = open(logfile, 'r')

        for line in fd.readlines():
            items = line.strip().split()
            metrics.append(float(items[self.metrics_pos]))

        fd.close()
	# return metrics list
        return metrics

    def _data_process(self, baseline, compare):
        for case in os.listdir(self.log_path):
            case_path = os.path.join(self.log_path,case)
            for load in os.listdir(case_path):
                load_path = os.path.join(case_path, load)
                baseline_avg = 0.0
                baseline_std = 0.0
                compare_avg = 0.0
                compare_std = 0.0
                for log in os.listdir(load_path):
                    result = os.path.join(load_path, log)
                    if os.path.isdir(result):
                        continue
                    indicator = self._parse_logfile(result)
                    avg = round(np.mean(indicator), 4)
                    std = round(100 * np.std(indicator) / avg, 2)
                    if baseline in log:
                        baseline_avg = avg
                        baseline_std = std
                    if compare and compare in log:
                        compare_avg = avg
                        compare_std = std
                self.table = self.table.append({'case':case,
                                        'load':load,
                                        'b_avg':baseline_avg,
                                        'b_std':baseline_std,
                                        'c_avg':compare_avg,
                                        'c_std':compare_std},
                                        ignore_index=True)
        self.table['sort'] = self.table['load'].str.extract('(\d+)',
                                        expand=False).astype(int)
        self.table.sort_values(by=['case', 'sort'], inplace=True, ascending=True)
        self.table = self.table.drop('sort', axis=1).reset_index(drop=True)

    def _baseline_report(self, baseline, metrics):
        print('{0:16s}\t{1:8s}\t{2:>12s}\t{3:>8s}'.format(
                                        'case','load',metrics,'std%'))
        for i in range(len(self.table)):
            print('{0:16s}\t{1:8s}\t{2:12.2f}\t({3:6.2f})'.format(
                self.table['case'][i], self.table['load'][i],
                self.table['baseline-avg'][i], self.table['baseline-std'][i]))

    def _compare_report(self, baseline, compare, better):
        print('{0:16s}\t{1:8s}\t{2}({3})\t{4}({5:>5s})'.format('case','load','baseline','std%','compare%','std%'))
        for i in range(len(self.table)):
            if better == '-':
                change = round((1 - self.table['c_avg'][i]/self.table['b_avg'][i]) * 100.0, 2)
            else:
                change = round((self.table['c_avg'][i]/self.table['b_avg'][i] - 1) * 100.0, 2)
            print('{0:16s}\t{1:8s}\t{2:5.2f} ({3:6.2f})\t{4:>+6.2f} ({5:6.2f})'.format(self.table['case'][i],
                    self.table['load'][i], 1.0, self.table['b_std'][i],
                    change, self.table['c_std'][i]))

    def report(self, baseline, compare, metrics, better):
        self._data_process(baseline, compare)
        if not compare:
            self._baseline_report(baseline, metrics)
        else:
            self._compare_report(baseline, compare, better)
def usage():
    print("./report.py [-t testname] -b baseline [-c compare]")
    print("\t-t (--testname) test case name")
    print("\t-b (--baseline) baseline run name")
    print("\t-c (--compare) compare run name")

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], '-h-t:-b:-c:', ['help','testname=','baseline=','compare='])
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

    # baseline is a must
    if not baseline:
        usage()
        sys.exit()

    for i in range(len(bmk_list)):
        name = bmk_list[i]['name']
        if testname and testname not in name:
            continue
        metrics = bmk_list[i]['metrics']
        better = bmk_list[i]['better']
        task = benchmark(name)
        print("\n{0}".format(name))
        print("==========")
        task.report(baseline, compare, metrics, better)
