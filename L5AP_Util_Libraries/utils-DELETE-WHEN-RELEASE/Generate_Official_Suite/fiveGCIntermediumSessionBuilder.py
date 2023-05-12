#!/usr/bin/python3
##########################################################################
#  Generate 5GC tests in official libraries
#  TL uses this script to get intermedium tests
#
#  Input: single ste including the tests in the SAME library
#         SuiteReader.jar from latest LS
#         TestSuiteBuilder.jar from latest LS
#  Output: official ste including only tests in the input ste
#  Note: no XML will be generted, no perforce access required
##########################################################################

import os,sys,argparse
from os.path import exists
from datetime import date
import time

verbose = False

def parse_args():
	parser = argparse.ArgumentParser(description="Take a user ste as input, generate 5GC official ste")
	parser.add_argument("inputSte", metavar="<User Ste>",
			help="user 5GC test sessions in ste.")
	parser.add_argument("suiteReader", metavar="<SuiteReader.jar>",
			help="path to SuiteReader.jar from latest LS")
	parser.add_argument("testSuiteBuilder", metavar="<TestSuiteBuilder.jar>",
			help="path to TestSuiteBuilder.jar from latest LS")
	parser.add_argument("-o", "--outputSte", metavar="<Output Name Suffix>",
			help="resulting 5GC session will have name COAST99.9.<outputSte>.")
	parser.add_argument("--verbose", default=False, action='store_true',
			help="print more debug lines")
	return parser.parse_args()


def verbose_print (_str):
	global verbose
	if verbose:
		print (_str)

def main(argv):
	global verbose

	# Read input ste, output ste name suffix
	opts = parse_args()

	verbose = opts.verbose
	print ('verbose:',opts.verbose)

	# sanity check for input ste
	inputSte = opts.inputSte
	if 'CO_' in inputSte or 'CO-' in inputSte or 'CO_' in inputSte or 'CO-' in inputSte:
		library = '-510'
	elif 'CP_' in inputSte or 'CP-' in inputSte or 'CP_' in inputSte or 'CP-' in inputSte:
		library = '-511'
	elif 'PF_' in inputSte or 'PF-' in inputSte or 'PF_' in inputSte or 'PF-' in inputSte:
		library = '-511'
	elif 'CUSA_' in inputSte or 'CUSA-' in inputSte:
		library = '-513'
	elif 'RUSA_' in inputSte or 'RUSA-' in inputSte or 'DUSA_' in inputSte or 'DUSA-' in inputSte or 'E-ORAN_' in inputSte or 'E-ORAN-' in inputSte:
		library = '-514'
	elif 'SA_' in inputSte or 'SA-' in inputSte or 'SA_' in inputSte or 'SA-' in inputSte:
		library = '-515'
	else:
		print ('Unknown test type: Please use CO_, CP_, PF_, SA_, CUSA_, RUSA_, DUSA_, or E-ORAN_ in the input ste name.')
		exit()

	if inputSte[0] != "/":
		# not absolute path, convert to absolute path
		inputSte = os.path.join(os.getcwd(), inputSte)
	if not exists(inputSte):
		print ('Error: User ste ' + inputSte + ' does not exist')
		exit()	


	# sanity check for suiteReader
	suiteReader = opts.suiteReader
	if suiteReader[0] != "/":
		# not absolute path, convert to absolute path
		suiteReader = os.path.join(os.getcwd(), suiteReader)
	if not exists(suiteReader):
		print ('Error: ' + suiteReader + ' does not exist')
		exit()	

	# sanity check for testSuiteBuilder
	testSuiteBuilder = opts.testSuiteBuilder
	if testSuiteBuilder[0] != "/":
		# not absolute path, convert to absolute path
		testSuiteBuilder = os.path.join(os.getcwd(), testSuiteBuilder)
	if not exists(testSuiteBuilder):
		print ('Error: ' + testSuiteBuilder + ' does not exist')
		exit()	

	# save current directory
	prevPath = os.getcwd()
	if not prevPath.endswith('/'):
		prevPath = prevPath + '/'

	# construct suffix for output ste filename
	outputSuffix = opts.outputSte
	if outputSuffix is None:
		today = date.today()
		# mm-dd
		outputSuffix = today.strftime("%m-%d")
	print ('Using "' + outputSuffix + '" as suffix in output ste name.')

	#create temp directorie
	temp_dir = 'temp' + outputSuffix
	cmd = 'mkdir ' + temp_dir
	print (cmd)
	if os.system(cmd) != 0:
		verbose_print ('ERROR: cannot create ' + temp_dir)
		exit()

	cmd = 'cd ' + temp_dir
	print (cmd)
	if os.system(cmd) != 0:
		verbose_print ('ERROR: cannot enter ' + temp_dir)
		exit()

	# change dir to the temp dir
	os.chdir(temp_dir)
	work_dir = os.getcwd()
	if not work_dir.endswith('/'):
		work_dir = work_dir + '/'
	
	verbose_print ('work_dir is:' + work_dir)

	#create mandatory directory for TestSuiteBuilder
	cmd = 'mkdir tcl'
	print (cmd)
	if os.system(cmd) != 0:
		verbose_print ('ERROR: cannot create mandatory folder tcl')
		exit()

	status = 0
	# run SuiteReader for this ste file
	print ('Processing ', inputSte, '...')
	cmd = "echo -ne '\n' | java -jar " + suiteReader + ' ' + inputSte + ' ' + library 
	if os.system(cmd)!=0:
		print ('ERROR: execute ', suiteReader, 'failed.')
		status = 1
	
	session_dir_tmp = work_dir + 'sessions'
	sessiondmf_dir_tmp = work_dir + 'sessiondmfs'
	dmf_dir_tmp = work_dir + 'dmfs'
	vsa_dir_tmp = work_dir + 'vsas'
	# for tdfs, SuiteReader only generate subdirectories
	# with names like tdfs-510 
	tdf_dir = work_dir + 'tdf'
	if exists(session_dir_tmp):
		print ('5GC session XML files generated successfully')
	else:
		print ('Failed to parse ' + inputSte)
		status = 1

	if status == 0:
		# rename sessions->session sessiondmfs->sessiondmf, etc
		cmd = 'mv sessions session'
		if os.system(cmd)!=0:
			print ('ERROR: failed to rename temp session directory')
			status = 1
	if exists(sessiondmf_dir_tmp):
		cmd = 'mv sessiondmfs sessiondmf'
		if os.system(cmd)!=0:
			print ('ERROR: failed to rename temp sessiondmf directory')
			status = 1
	if exists(dmf_dir_tmp):
		cmd = 'mv dmfs dmf'
		if os.system(cmd)!=0:
			print ('ERROR: failed to rename temp dmf directory')
			status = 1
	if exists(vsa_dir_tmp):
		cmd = 'mv vsas vsa'
		if os.system(cmd)!=0:
			print ('ERROR: failed to rename temp vsa directory')
			status = 1
	# check tdf folders
	for aFile in os.scandir(work_dir):
		if aFile.is_dir():
			dirName = aFile.name
			if 'tdfs' in dirName:
				# create tdf folder, put this tdfs folder under and rename
				if not exists(tdf_dir):
					cmd = 'mkdir ' + tdf_dir
					print (cmd)
					if os.system(cmd)!=0:
						print ('ERROR: failed to create temp tdf directory')
						status = 1
				if status == 0:
					newName = dirName.replace('tdfs', 'tdf')
					cmd = 'mv ' + aFile.path + ' ' + os.path.join(tdf_dir, newName)
					if os.system(cmd)!=0:
						print ('ERROR: failed to mv temp tdf directory ' + dirName)
						status = 1					

	if status == 0:
		# Build output ste
		cmd = 'java -Xmx356m -jar ' + testSuiteBuilder + ' -version=99.9.0.' + outputSuffix + ' .'
		print (cmd)
		if os.system(cmd) != 0:
			print ('ERROR: Failed to build offcial ste')
			status = 1

	# copy output ste to prevPath
	if status == 0:
		cmd = 'cp *.ste ' + prevPath
		if os.system(cmd) != 0:
			print ('ERROR: Failed to copy offcial ste')
		else:
			print ('COAST.99.9.0.' + outputSuffix + '.ste copied to ' + prevPath)

	# Change path back, remove temp directories
	os.chdir(prevPath)
	verbose_print ('now path:' + os.getcwd())

	# remove temporary directories
	cmd  = 'rm -rf ' + temp_dir
	verbose_print (cmd)
	if os.system(cmd)!=0:
		print ('ERROR: failed to remove temporary folder ' + temp_dir) 
	
if __name__ == "__main__":
  main(sys.argv[1:])
