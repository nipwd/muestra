@ECHO OFF
start "C:\Program Files\Google\Chrome\Application"  "http://127.0.0.1:8000/prueba/"
start wsl.exe  /home/main/miniconda3/envs/directml/bin/python /home/main/WOLFMARKET/manage.py runserver && /home/main/WOLFMARKET/python && /home/main/miniconda3/envs/directml/bin/python:
