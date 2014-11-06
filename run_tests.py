#!/usr/bin/env python

import os
import glob
import subprocess
import difflib

def run_test(fname_cxx):
	fname_rs = os.path.splitext(fname_cxx)[0] + ".rs"
	with open(fname_rs) as f:
		expected_output = f.read().split()

	cmd = ['./cxx2rs.py', fname_cxx]
	actual_output = subprocess.check_output(cmd).split()
	
	different = False
	diff = difflib.unified_diff(actual_output, expected_output)
	for line in diff:
		if not different:
			print '================ "%s" test failed. diff begin ================' % os.path.basename(fname_cxx)
			different = True
		print line

	if different:
		print '================  "%s" test failed. diff end  ================' % os.path.basename(fname_cxx)
		print
	else:
		print 'Test "%s" succeeded.' % os.path.basename(fname_cxx)


def main():
	basepath = os.path.dirname(__file__)
	testpath = os.path.join(basepath, './tests/*.c*')

	for fname_cxx in glob.glob(testpath):
		with open(fname_cxx, 'r') as f:
			first_line = f.readline()

			if first_line.lower().strip() == '// skip':
				print 'Skipping test "%s".' % os.path.basename(fname_cxx)
				continue

			print 'Running test "%s"...' % os.path.basename(fname_cxx)
			run_test(fname_cxx)

if __name__ == "__main__":
	main()