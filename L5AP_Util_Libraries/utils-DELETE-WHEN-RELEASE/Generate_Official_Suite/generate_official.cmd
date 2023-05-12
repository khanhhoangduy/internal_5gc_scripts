@echo off
:: ---------------------  Configure  -----------------------------------------
set mypath=%cd%
set additional_dmf_path=
echo Current path: "%mypath%"

if not exist "%mypath%\TestSuiteBuilder.jar" EXIT /b
if not exist "%mypath%\SuiteReader.jar" EXIT /b

set /p suite_name="Enter ste file name: "
if not exist "%mypath%\%suite_name%" EXIT /b

set /p library_id="Choose library: -510:[5G Compliance] -511: [5G Capacity and Performance] -512: [5G Service Based] Select: "
if %library_id%==-510 echo "5G Compliance"
if %library_id%==-511 echo "5G Capacity and Performance"
if %library_id%==-512 echo "5G Service Based"

:: ----------------------------------------------------------------------------

:: Additional DMFs
set /p additional_dmf_path="Input absolute path to mainline/tc/dmf directory: "

:: ----------------------------------------------------------------------------
if not exist "tcl" mkdir "tcl"
if not exist "session" mkdir "session"
if not exist "sessiondmf" mkdir "sessiondmf"
if not exist "dmf" mkdir "dmf"
if not exist "tdf" mkdir "tdf"
if not exist "tdf\tdf%library_id%" mkdir "tdf\tdf%library_id%"
if exist %additional_dmf_path% xcopy "%additional_dmf_path%\*.*" "%mypath%\dmf"

:: ---------------------  execute SuiteReader.jar -----------------------------
start javaw -jar SuiteReader.jar %suite_name% %library_id%
timeout /t 10

:: ---------------------  Repairing for TestSuiteBuilder ----------------------
if exist "sessions" del "%mypath%\sessions\*.tcl" /s /q /f
if exist "sessions" xcopy "%mypath%\sessions\*.xml" "%mypath%\session"
if exist "sessiondmfs" del "%mypath%\sessiondmfs\*.tcl" /s /q /f
if exist "sessiondmfs" xcopy "%mypath%\sessiondmfs" "%mypath%\sessiondmf"
if exist "tdf%library_id%" xcopy "%mypath%\tdf%library_id%" "%mypath%\tdf\tdf%library_id%"

:: ---------------------  Create temp folder ----------------------------------
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%%MM%%DD%" & set "timestamp=%HH%%Min%%Sec%"
set "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

if not exist "%mypath%\%fullstamp%" mkdir "%mypath%\%fullstamp%"

:: ---------------------  Execute TestSuiteBuilder ----------------------------
start javaw -Xmx300m -jar TestSuiteBuilder.jar -version=99.9.0.official_%fullstamp% "%mypath%"
timeout /t 10

:: ---------------------  Move all files to temp folder  ----------------------
move "%mypath%\*%fullstamp%*.ste" "%mypath%\%fullstamp%\"

if exist "%mypath%\tcl" move "%mypath%\tcl" "%mypath%\%fullstamp%"
if exist "%mypath%\session" move "%mypath%\session" "%mypath%\%fullstamp%"
if exist "%mypath%\sessions" move "%mypath%\sessions" "%mypath%\%fullstamp%"
if exist "%mypath%\sessiondmf" move "%mypath%\sessiondmf" "%mypath%\%fullstamp%"
if exist "%mypath%\sessiondmfs" move "%mypath%\sessiondmfs" "%mypath%\%fullstamp%"
if exist "%mypath%\dmf" move "%mypath%\dmf" "%mypath%\%fullstamp%"
if exist "%mypath%\dmfs" move "%mypath%\dmfs" "%mypath%\%fullstamp%"
if exist "%mypath%\tdf%library_id%" move "%mypath%\tdf%library_id%" "%mypath%\%fullstamp%"
if exist "%mypath%\tdfs%library_id%" move "%mypath%\tdfs%library_id%" "%mypath%\%fullstamp%"
if exist "%mypath%\tdf" move "%mypath%\tdf" "%mypath%\%fullstamp%"
if exist "%mypath%\tdfs" move "%mypath%\tdfs" "%mypath%\%fullstamp%"
if exist "%mypath%\SavedTCs.xml" move "%mypath%\SavedTCs.xml" "%mypath%\%fullstamp%\"
if exist "%mypath%\Sessions.xml" move "%mypath%\Sessions.xml" "%mypath%\%fullstamp%"
if exist "%mypath%\vsas" move "%mypath%\vsas" "%mypath%\%fullstamp%"

if exist "%mypath%\%suite_name%" xcopy "%mypath%\%suite_name%" "%mypath%\%fullstamp%"

:: ---------------------  Delete if need  ----------------------
if exist "%mypath%\tcl" @RD /q "%mypath%\tcl"
if exist "%mypath%\session" @RD /q "%mypath%\session"
if exist "%mypath%\sessions" @RD /q "%mypath%\sessions"
if exist "%mypath%\sessiondmf" @RD /q "%mypath%\sessiondmf"
if exist "%mypath%\dmf" @RD /q "%mypath%\dmf"
if exist "%mypath%\dmfs" @RD /q "%mypath%\dmfs"
if exist "%mypath%\sessiondmfs" @RD /q "%mypath%\sessiondmfs"
if exist "%mypath%\tdf" @RD /q "%mypath%\tdf"
if exist "%mypath%\tdf%library_id%" @RD /q "%mypath%\tdf%library_id%"
if exist "%mypath%\tdfs" @RD /q "%mypath%\tdfs"
if exist "%mypath%\tdfs%library_id%" @RD /q "%mypath%\tdfs%library_id%"
if exist "%mypath%\SavedTCs.xml" del "%mypath%\SavedTCs.xml" /q
if exist "%mypath%\Sessions.xml" del "%mypath%\Sessions.xml" /q 
if exist "%mypath%\vsas" @RD /q "%mypath%\vsas"

echo Complete. Check official in "%fullstamp%"
pause