@echo off
set /p a=Please enter Artifact Evaluation folder file path :
echo Starting linear...
start python "%a%\Artifact Evaluation\test\main.py"
