cd %~dp0

set input_path=%1

call venv\Scripts\activate.bat

pip freeze

python launch.py %input_path%

deactivate
