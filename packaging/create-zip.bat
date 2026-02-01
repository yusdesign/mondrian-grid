@echo off
echo Creating Mondrian Grid extension distribution package...
echo.

REM Create temp directory
mkdir dist-temp 2>nul

REM Copy essential files
echo Copying extension files...
copy extension\mondriangrid_v3.inx dist-temp\
copy extension\mondriangrid_v3.py dist-temp\
copy README.md dist-temp\
copy LICENSE dist-temp\
copy INSTALL.md dist-temp\

REM Create ZIP
echo Creating ZIP archive...
cd dist-temp
"C:\Program Files\7-Zip\7z.exe" a -tzip ..\mondrian-grid.zip * >nul
cd ..

REM Cleanup
rmdir /s /q dist-temp

echo.
echo ✅ Package created: mondrian-grid.zip
echo.
echo Files included:
echo   - mondriangrid_v3.inx (extension definition)
echo   - mondriangrid_v3.py (main code)
echo   - README.md (documentation)
echo   - LICENSE (MIT)
echo   - INSTALL.md (installation guide)
echo.
pause