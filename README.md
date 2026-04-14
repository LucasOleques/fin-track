# FinTrack

### Plataforma web de gestao financeira pessoal com dashboard, autenticacao, API JWT e testes automatizados

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-44%20passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

> Projeto full-stack desenvolvido para demonstrar entrega de produto real: backend, frontend server-rendered, regras de negocio, seguranca, isolamento de dados por usuario e deploy.

## Visao geral

O **FinTrack** é uma aplicacao web para controle financeiro pessoal. O usuario consegue cadastrar contas, organizar categorias, registrar receitas e despesas, acompanhar saldo e visualizar um dashboard com resumo das movimentacoes.

A intenção do projeto, não é um CRUD simples. O projeto foi pensado e estruturado para mostrar capacidade de construir uma solucao completa com:

- arquitetura modular por apps Django
- autenticacao com sessao e JWT
- interface responsiva com foco em usabilidade
- regras de saldo entre contas e transacoes
- logs de auditoria
- testes automatizados cobrindo os fluxos principais

## Destaques

- **Produto de ponta a ponta:** experiencia web funcional com login, cadastro, dashboard, perfil, contas, categorias e transacoes.
- **Backend com regra de negocio real:** controle de saldo, filtros, autenticacao, serializacao, sinais e isolamento de dados por usuario.
- **Boa base de engenharia:** Django, DRF, `django-filter`, JWT, `Whitenoise`, `Waitress` e configuracao por variaveis de ambiente.
- **Qualidade validada:** suite com **44 testes automatizados** cobrindo os principais fluxos da aplicacao.
- **Visao de deploy:** projeto preparado para SQLite no desenvolvimento e PostgreSQL por configuracao de ambiente.

## Principais funcionalidades

- Dashboard com saldo total, receitas do mes, despesas do mes, contas ativas e ultimas transacoes.
- Cadastro e gestao de contas financeiras com tipo, cor, limite e status ativo/inativo.
- Cadastro de categorias para receitas ou despesas.
- Registro de transacoes com filtros por periodo, tipo, conta e categoria.
- Atualizacao automatica de saldo da conta em criacao e exclusao de transacoes.
- Area de usuario com login por username ou e-mail, cadastro, perfil, avatar, troca de senha e recuperacao de senha.
- Logs de auditoria para eventos relevantes do sistema.

## Stack utilizada

- **Backend:** Python, Django, Django REST Framework
- **Autenticacao:** Session Auth + JWT (`djangorestframework-simplejwt`)
- **Filtros:** `django-filter`
- **Frontend:** Django Templates, Bootstrap 5, Bootstrap Icons, JavaScript
- **Banco de dados:** SQLite no dev, PostgreSQL por configuracao
- **Deploy / execucao web:** Waitress + Whitenoise
- **Configuracao:** `python-decouple`
- **Imagens:** Pillow

## Estrutura do projeto

```text
fin-track/
|-- fin_track_project/
|   |-- manage.py
|   |-- fin_track_project/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- views.py
|   |   `-- tests.py
|   |-- apps/
|   |   |-- user/
|   |   |-- accounts/
|   |   |-- categories/
|   |   `-- transactions/
|   |-- templates/
|   |-- static/
|   |-- logs/
|   `-- run_server.bat
|-- scripts/
|-- requirements.txt
|-- .env.exemplo
`-- README.md
```

## Arquitetura por modulos

- `user`: autenticacao, cadastro, perfil, senha e recuperacao.
- `accounts`: contas bancarias e de controle financeiro.
- `categories`: classificacao das transacoes.
- `transactions`: receitas, despesas, filtros e atualizacao de saldo.
- `fin_track_project`: dashboard, views globais, configuracao principal e testes do nucleo.

## Como executar localmente

### 1. Clone o repositorio

```bash
git clone <repo-url>
cd fin-track
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependencias

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

Use o arquivo `.env.exemplo` como base e crie o seu `.env`.

```bash
copy .env.exemplo .env
```

Campos importantes:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- configuracoes de banco
- configuracoes de e-mail

> Importante: em `DEBUG`, use `true` ou `false`.

### 5. Rode a aplicacao

```bash
cd fin_track_project
python manage.py migrate
python manage.py runserver
```

Abra no navegador:

```text
http://127.0.0.1:8000/
```

## Execucao no Windows com Waitress

Para iniciar o projeto com `Waitress` e coletar estaticos automaticamente no Windows:

```bat
cd fin_track_project
run_server.bat
```

## Script de automacao

O projeto tambem possui um utilitario em [scripts/fin_track_clean.ps1](c:/Users/lucas/IdeaProjects%20VSCode/fin-track/scripts/fin_track_clean.ps1) para acelerar setup e limpeza do ambiente no Windows.

Esse script pode:

- limpar pastas `__pycache__`
- limpar arquivos de `migrations`
- remover o banco SQLite
- carregar variaveis do `.env`
- executar `makemigrations`, `migrate` e `createsuperuser`

### Como executar

Na raiz do projeto:

```powershell
.\scripts\fin_track_clean.ps1
```

Se o PowerShell bloquear a execucao, rode antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Parametros disponiveis

- `-DeleteDB`: remove o banco SQLite antes do setup.
- `-SkipCache`: nao limpa os diretorios `__pycache__`.
- `-SkipMigrations`: nao limpa os arquivos de migration.
- `-SkipEnv`: nao carrega variaveis do arquivo `.env`.
- `-DryRun`: apenas simula o que seria executado.
- `-Help`: exibe a ajuda do script.

### Exemplos de uso

```powershell
.\scripts\fin_track_clean.ps1 -Help
.\scripts\fin_track_clean.ps1 -DeleteDB
.\scripts\fin_track_clean.ps1 -SkipCache -SkipMigrations
.\scripts\fin_track_clean.ps1 -DeleteDB -DryRun
```

## Testes automatizados

O projeto possui cobertura dos fluxos principais da aplicacao:

- dashboard e views globais
- contas
- categorias
- transacoes
- autenticacao e perfil de usuario

Para rodar os testes:

```bash
cd fin_track_project
python manage.py test
```

## Endpoints e acessos principais

- `GET /` -> entrada da aplicacao
- `GET /dashboard/` -> dashboard principal
- `GET /user/login/` -> login
- `GET /accounts/list/` -> contas
- `GET /categories/list/` -> categorias
- `GET /transactions/list/` -> transacoes
- `POST /api/token/` -> obtencao de token JWT
- `POST /api/token/refresh/` -> refresh de token JWT

## Por que este projeto se destaca

O FinTrack mostra capacidade de entregar um sistema com mentalidade de produto e nao apenas de exercicio tecnico. Ele combina interface, backend, autenticacao, organizacao modular, preocupacao com seguranca, configuracao para deploy e testes automatizados em uma unica base coesa.

Em um contexto de avaliacao tecnica, este projeto evidencia:

- dominio de Django e DRF
- organizacao de codigo por contexto de negocio
- cuidado com experiencia do usuario
- preocupacao com manutencao e validacao automatizada
- capacidade de evoluir um MVP para um produto mais robusto

## Licenca

Este projeto esta sob a licenca MIT. Consulte o arquivo [LICENSE](LICENSE).
