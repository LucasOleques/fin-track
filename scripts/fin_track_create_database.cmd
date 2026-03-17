@echo off

echo Ativando ambiente virtual...
call C:\Users\lucas\miniconda3\Scripts\activate
call conda activate fin-track
echo Ambiente ativado.

cd C:\Users\lucas\IdeaProjects VSCode\fin-track\fin_track_project

echo Executando makemigrations do Django...
python manage.py makemigrations user transactions categories accounts

echo Executando migrate do Django...
python manage.py migrate

echo Migracoes realizadas e Banco de dados criado.

cd C:\Users\lucas\IdeaProjects VSCode\fin-track\fin_track_project

echo Criando usuario Admin...
set DJANGO_SUPERUSER_PASSWORD=admin
python manage.py createsuperuser --username admin --email admin@admin.com --noinput

echo Usuario Admin criado com sucesso.