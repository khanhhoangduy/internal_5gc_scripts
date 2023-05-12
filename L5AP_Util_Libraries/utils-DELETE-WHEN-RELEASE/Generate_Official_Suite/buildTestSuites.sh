#!/bin/bash

now=`date +"%m-%d-%y"`
SUITE_READER="SuiteReader.jar"
TEST_SUITE_BUILDER="TestSuiteBuilder.jar"
SUITE_READER_EXIST="No"
TEST_SUITE_BUILDER_EXIST="No"
STE_EXIST="No"
CONT_TEST_SUITE_BUILDER="No"
SESSIONS="sessions"
SESSION="session"
SESSION_DMFS="sessiondmfs"
SESSION_DMF="sessiondmf"
TDF="tdf"
TDFS="tdfs"
TCL="tcl"

# to build official Test Suite
echo "-------------------Building Official Test Suite------------------"
echo "                   Date:$now                         "
echo "-----------------------------------------------------------------"


read -p "Input absolute path to your test directory: " ABS_PATH

read -p "Input absolute path to mainline/tc/dmf directory: " ABS_PATH_DMF

# where is the .ste file for input?
read -p "Input .ste name: " INPUT_STE_NAME

read -p "Enter a name for the official test suite: " TEST_SUITE_NAME

echo "Library IDs: "
echo "input -510 for 5G Compliance"
echo "input -511 for 5G Capacity and Performance"
echo "input -512 for 5G Service Based"
read -p "Input Library ID: " INPUT_LIBRARY_ID

# check to see if SuiteReader.jar exist
if find $AB_PATH -name $SUITE_READER
then
  echo "$SUITE_READER exist"
  SUITE_READER_EXIST="Yes"
  echo "Exit 1"
else
  echo "$SUITE_READER does not exists. Please copy the file to $ABS_PATH"
  echo "Exit 2"
fi

# check to see if TestSuiteBuilder.jar exist
if find $ABS_PATH -name $TEST_SUITE_BUILDER
then
  echo "$TEST_SUITE_BUILDER exist"
  TEST_SUITE_BUILDER_EXIST="Yes"
  echo "Exit 3"
else
  echo "$TEST_SUITE_BUILDER does not exist. Please copy the file to $ABS_PATH"
  echo "Exit 4"
fi

# find .ste file
if find $ABS_PATH -name $INPUT_STE_NAME
then
  echo "$INPUT_STE_NAME exist"
  STE_EXIST="Yes"
  echo "Exit 5"
else
  echo "$INPUT_STE_NAME does not exist"
  echo "Exit 6"
fi

# Start processing the .ste file
echo "--------------Processing .ste file--------------"
echo "------------------------------------------------"

if (((($SUITE_READER_EXIST == "Yes")) && (($STE_EXIST == "Yes")) && (($TEST_SUITE_BUILDER_EXIST == "Yes"))))
then
  echo "SuiteReader.jar , TestSuiteReader.jar, and .ste exist"
  cd $ABS_PATH
  chmod -R 777 $INPUT_STE_NAME
  echo "Creating session, sessiondmf,dmf, and tdf directories ...."
  mkdir $TCL
  mkdir $SESSION
  mkdir $SESSION_DMF
  mkdir $TDF
  cd $TDF
  mkdir $TDF$INPUT_LIBRARY_ID
  cd ..
  mkdir dmf
  echo "Copying DMF files"
  cp -Rf $ABS_PATH_DMF/* $ABS_PATH/dmf/ 
  #cd ..
  echo -ne '\n' | java -jar ./SuiteReader.jar $INPUT_STE_NAME $INPUT_LIBRARY_ID
  sleep 5
  echo "Exit 7"
else
  echo "SuiteReader.jar, TestSuiteBuilder, and/or .ste does not exist"
  echo "Exit 8"
fi

if find $ABS_PATH -name "sessions"
then
  echo "sessions directory exist"
  rm -rf $ABS_PATH/$SESSIONS/*.tcl -R
  cp -Rf $ABS_PATH/$SESSIONS/* $ABS_PATH/$SESSION/
  echo "Exit 9"
else
  echo "sessions directory not found"
  echo "Exit 10"
fi

if find $ABS_PATH -name "sessiondmfs"
then
  echo "sessiondmfs directory exist"
  rm -rf $ABS_PATH/$SESSION_DMFS/*.tcl -R
  echo $ABS_PATH_SESSIONDMF
  cp -Rf $ABS_PATH/$SESSION_DMFS/* $SESSION_DMF/
  # for file1 in $ABS_PATH/$SESSION_DMFS/*; do
  #     for file2 in $ABS_PATH_SESSIONDMF/*; do
  #       name1="$(basename "$file1")"
  #       name2="$(basename "$file2")"
  #       if [ "$name1" == "$name2" ]
  #       then
  #         echo "WARNING: DUPLICATE DMF -"$name1" EXIST."
  #         echo "WARNING: PLEASE RENAME THE DMF AS IT COULD BE OVERWRITING EXISTING DMFs"
  #         echo "WARNING: PLEASE RESTART THE PROCESS AFTER RENAMING THE DMF"
  #       fi
  #     done
  # done
  echo "Exit 11"
else
  echo "sessiondmfs not found"
  echo "Exit 12"
fi

if find $ABS_PATH -name "tdfs"
then
  echo "tdfs$INPUT_LIBRARY_ID directory found"
  chmod -R 777 tdfs$INPUT_LIBRARY_ID
  cp -Rf $TDFS$INPUT_LIBRARY_ID/* $TDF/$TDF$INPUT_LIBRARY_ID/
  echo "Exit 13"
else
  echo "tdf directory is not found"
  echo "Exit 14"
fi

echo "--------------Building Test Suites--------------"
echo "------------------------------------------------"
pwd

java -Xmx356m -jar TestSuiteBuilder.jar -version=99.9.0.$TEST_SUITE_NAME $ABS_PATH/
echo "Completed"
