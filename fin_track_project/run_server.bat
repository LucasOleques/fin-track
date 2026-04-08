@echo off
REM Script para iniciar o servidor Waitress no Windows
REM Uso: run_server.bat

echo ================================
echo FinTrack - Servidor Waitress
echo ================================
echo.

REM Verificar se esta no ambiente correto
if not exist "manage.py" (
    echo Erro: Execute este script a partir da pasta fin_track_project
    pause
    exit /b 1
)

REM Instalar waitress (se necessario)
echo Verificando dependências...
pip install waitress > nul 2>&1

REM Executar migracoes
echo.
echo Executando migracoes...
python manage.py migrate

REM Coletar estaticos
echo.
echo Coletando arquivos estaticos...
python manage.py collectstatic --noinput

REM Iniciar servidor
echo.
echo ✅ Iniciando servidor Waitress...
echo.
echo Acesse: http://localhost:8000
echo.

waitress-serve --port=8000 --threads=4 fin_track_project.wsgi:application

pause