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
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Take a user ste as input, generate 5GC official ste")
    parser.add_argument("-ste", "--steFolder", metavar="<STE exported folder>",
        help="Exported STE folder")
    parser.add_argument("-o", "--outputSte", metavar="<Output Name Suffix>",
        help="resulting 5GC session will have name COAST99.9.<outputSte>.")
    parser.add_argument("-dir", "--dirWorking", metavar="<Working dir>",
        help="Working dir")
    return parser.parse_args()

def getLibraryId(inputSte):
    if 'CO_' in inputSte or 'CO-' in inputSte or 'CO_' in inputSte or 'CO-' in inputSte:
        return '-510'
    elif 'CP_' in inputSte or 'CP-' in inputSte or 'CP_' in inputSte or 'CP-' in inputSte:
        return '-511'
    elif 'PF_' in inputSte or 'PF-' in inputSte or 'PF_' in inputSte or 'PF-' in inputSte:
        return '-511'
    elif 'CUSA_' in inputSte or 'CUSA-' in inputSte:
        return '-513'
    elif 'RUSA_' in inputSte or 'RUSA-' in inputSte or 'DUSA_' in inputSte or 'DUSA-' in inputSte or 'E-ORAN_' in inputSte or 'E-ORAN-' in inputSte:
        return '-514'
    elif 'SA_' in inputSte or 'SA-' in inputSte or 'SA_' in inputSte or 'SA-' in inputSte:
        return '-515'
    else:
        print ('Unknown test type: Please use CO_, CP_, PF_, SA_, CUSA_, RUSA_, DUSA_, or E-ORAN_ in the input ste name.')
        exit()

def getSurfix(inputSte):
    if 'CO_' in inputSte or 'CO-' in inputSte or 'CO_' in inputSte or 'CO-' in inputSte:
        return 'CO_'
    elif 'CP_' in inputSte or 'CP-' in inputSte or 'CP_' in inputSte or 'CP-' in inputSte:
        return 'CP_'
    elif 'PF_' in inputSte or 'PF-' in inputSte or 'PF_' in inputSte or 'PF-' in inputSte:
        return 'PF_'
    elif 'CUSA_' in inputSte or 'CUSA-' in inputSte:
        return 'CUSA_'
    elif 'RUSA_' in inputSte or 'RUSA-' in inputSte:
        return 'RUSA_'
    elif  'DUSA_' in inputSte or 'DUSA-' in inputSte:
        return 'DUSA_'
    elif 'E-ORAN_' in inputSte or 'E-ORAN-' in inputSte:
        return 'E-ORAN_'
    elif 'SA_' in inputSte or 'SA-' in inputSte or 'SA_' in inputSte or 'SA-' in inputSte:
        return 'SA_'
    else:
        print ('Unknown test type: Please use CO_, CP_, PF_, SA_, CUSA_, RUSA_, DUSA_, or E-ORAN_ in the input ste name.')
        exit()

def generateSteFile(inputSte, working_dir, suiteReader, testSuiteBuilder, outputSuffix):
    library = getLibraryId(inputSte)
    # save current directory
    prevPath = working_dir
    if not prevPath.endswith('/'):
        prevPath = prevPath + '/'

    #create temp directorie
    temp_dir = 'D:/Documents/Landslide/Scripts/temp' + outputSuffix
    
    if exists(temp_dir):
        cmd  = 'rd /Q /s \"' + temp_dir + "\""
        print(cmd)
        os.system(cmd)
        
    cmd = 'mkdir \"' + temp_dir + "\""
    print (cmd)
    
    if os.system(cmd) != 0:
        verbose_print ('ERROR: cannot create ' + temp_dir)
        exit()

    cmd = 'cd \"' + temp_dir + "\""
    print (cmd)
    if os.system(cmd) != 0:
        verbose_print ('ERROR: cannot enter ' + temp_dir)
        exit()

    # change dir to the temp dir
    os.chdir(temp_dir)
    work_dir = temp_dir
    if not work_dir.endswith('/'):
        work_dir = work_dir + '/'
    
    print ('work_dir is:' + work_dir)

    #create mandatory directory for TestSuiteBuilder
    cmd = 'mkdir tcl'
    print (cmd)
    if os.system(cmd) != 0:
        verbose_print ('ERROR: cannot create mandatory folder tcl')
        exit()

    status = 0
    # run SuiteReader for this ste file
    print ('Processing ', inputSte, '...')
    #cmd = "java -jar " + suiteReader + ' ' + inputSte + ' ' + library 
    #p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
    #p.communicate(input='\n'.encode())
    cmd = "echo -ne '\\n' | java -jar " + suiteReader + ' ' + inputSte + ' ' + library 
    print(cmd)
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
        cmd = 'ren sessions session'
        if os.system(cmd)!=0:
            print ('ERROR: failed to rename temp session directory')
            status = 1
    if exists(sessiondmf_dir_tmp):
        cmd = 'ren sessiondmfs sessiondmf'
        if os.system(cmd)!=0:
            print ('ERROR: failed to rename temp sessiondmf directory')
            status = 1
    if exists(dmf_dir_tmp):
        cmd = 'ren dmfs dmf'
        if os.system(cmd)!=0:
            print ('ERROR: failed to rename temp dmf directory')
            status = 1
    if exists(vsa_dir_tmp):
        cmd = 'ren vsas vsa'
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
                    cmd = 'mkdir \"' + tdf_dir + "\""
                    print (cmd)
                    #p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
                    if os.system(cmd)!=0:
                        print ('ERROR: failed to create temp tdf directory')
                        status = 1
                if status == 0:
                    newName = dirName.replace('tdfs', 'tdf')
                    cmd = 'ren \"' + aFile.name + '\" \"' + newName + "\""
                    print(cmd)
                    #subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
                    if os.system(cmd)!=0:
                        print ('ERROR: failed to mv temp tdf directory ' + dirName)
                        status = 1                    

    if status == 0:
        # Build output ste
        cmd = 'java -Xmx356m -jar ' + testSuiteBuilder + ' -version=21.6.002.' + outputSuffix + ' .'
        print (cmd)
        if os.system(cmd) != 0:
            print ('ERROR: Failed to build offcial ste')
            status = 1
        #subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)

    # copy output ste to prevPath
    surfix = getSurfix(inputSte)
    if status == 0:
        generated_ste_file = 'COAST.21.6.002.' + outputSuffix + '.ste'
        new_generated_ste_file = surfix + generated_ste_file 
        cmd = 'ren "' + generated_ste_file + '" "' + new_generated_ste_file + '"'
        if os.system(cmd) != 0:
            print ('ERROR: Can not rename ste')
        else:
            print ('Rename ' + generated_ste_file + ' to ' + new_generated_ste_file)
            
        cmd = 'copy *.ste \"' + prevPath + "\""
        if os.system(cmd) != 0:
            print ('ERROR: Failed to copy offcial ste')
        else:
            print ('COAST.21.6.002.' + outputSuffix + '.ste copied to ' + prevPath)

    # Change path back, remove temp directories
    os.chdir(prevPath)

    # remove temporary directories
    cmd  = 'rd /Q /s \"' + temp_dir + "\""
    print(cmd)
    os.system(cmd)

def main(argv):
    global verbose

    #working_dir = "D:/Documents/Landslide/Scripts/"
    # Read input ste, output ste name suffix
    opts = parse_args()
    working_dir = opts.dirWorking
    
    cmd = 'cd \"' + working_dir + "\""
    print (cmd)
    if os.system(cmd) != 0:
        verbose_print ('ERROR: cannot enter ' + temp_dir)
        exit()       
    
    ste_dir = opts.steFolder
    
    # sanity check for suiteReader
    suiteReader = "SuiteReader.jar"
    if suiteReader[0] != "/":
        # not absolute path, convert to absolute path
        suiteReader = os.path.join(working_dir, suiteReader)
    if not exists(suiteReader):
        print ('Error: ' + suiteReader + ' does not exist')
        exit()    

    # sanity check for testSuiteBuilder
    testSuiteBuilder = "TestSuiteBuilder.jar"
    if testSuiteBuilder[0] != "/":
        # not absolute path, convert to absolute path
        testSuiteBuilder = os.path.join(working_dir, testSuiteBuilder)
    if not exists(testSuiteBuilder):
        print ('Error: ' + testSuiteBuilder + ' does not exist')
        exit()    

    # construct suffix for output ste filename
    outputSuffix = opts.outputSte
    if outputSuffix is None:
        today = date.today()
        # mm-dd
        outputSuffix = today.strftime("%m-%d")
    print ('Using "' + outputSuffix + '" as suffix in output ste name.')

    for aFile in os.scandir(ste_dir):
        if aFile.is_file():
            steFile = aFile.name
            if steFile.endswith(".ste"):
                inputSte = os.path.join(ste_dir, steFile)
                print(inputSte)
                generateSteFile(inputSte, working_dir, suiteReader, testSuiteBuilder, outputSuffix)
    
if __name__ == "__main__":
    main(sys.argv[1:])
