cd %~dp0

set skip_key_wait=%1

python.exe -m venv venv
call venv\Scripts\activate.bat

pip install --upgrade -r requirements.txt

pip freeze

if not "%skip_key_wait%"=="true" (
  echo "All complate!!! plass any key..."
  pause
)

deactivate
