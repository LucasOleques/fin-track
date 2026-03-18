@echo off

REM Diretorio base do script
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo Diretorio do projeto: %PROJECT_ROOT%

echo Ativando ambiente virtual...

REM Tenta usar conda do PATH (mais generico)
call conda activate fin-track 2>nul
if errorlevel 1 (
    echo Conda falhou, tentando venv...
    call %PROJECT_ROOT%\.venv\Scripts\activate
)

echo Ambiente ativado.

REM Ir para o projeto
cd /d %PROJECT_ROOT%\fin_track_project

echo Executando makemigrations do Django...
python manage.py makemigrations user transactions categories accounts

echo Executando migrate do Django...
python manage.py migrate

echo Migracoes realizadas e Banco de dados criado.

echo Criando usuario Admin...
set DJANGO_SUPERUSER_PASSWORD=admin
python manage.py createsuperuser --username admin --email admin@admin.com --noinput