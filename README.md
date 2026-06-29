# FinTrack

### Plataforma web de gestão financeira pessoal com dashboard, autenticação, API JWT e testes automatizados

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-44%20passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

> Projeto full-stack desenvolvido para demonstrar entrega de produto real: backend, frontend server-rendered, regras de negócio, segurança, isolamento de dados por usuário e deploy.

## Visão geral

O **FinTrack** é uma aplicação web para controle financeiro pessoal. O usuário consegue cadastrar contas, organizar categorias, registrar receitas e despesas, acompanhar saldo e visualizar um dashboard com resumo das movimentações.

A intenção do projeto não é um CRUD simples. O projeto foi pensado e estruturado para mostrar capacidade de construir uma solução completa com:

- arquitetura modular por apps Django
- autenticação com sessão e JWT
- interface responsiva com foco em usabilidade
- regras de saldo entre contas e transações via Django signals
- logs de auditoria
- testes automatizados cobrindo os fluxos principais

## Destaques

- **Produto de ponta a ponta:** experiência web funcional com login, cadastro, dashboard, perfil, contas, categorias e transações.
- **Backend com regra de negócio real:** controle de saldo automático via signals, filtros, autenticação, serialização e isolamento de dados por usuário.
- **Boa base de engenharia:** Django 5.2, DRF, `django-filter`, JWT, `Whitenoise`, `Waitress` e configuração por variáveis de ambiente.
- **Qualidade validada:** suite com **44 testes automatizados** cobrindo os principais fluxos da aplicação.
- **Visão de deploy:** projeto preparado para SQLite no desenvolvimento e PostgreSQL por configuração de ambiente.

## Principais funcionalidades

- Dashboard com saldo total, receitas do mês, despesas do mês, contas ativas e últimas transações.
- Cadastro e gestão de contas financeiras com tipo, cor, limite e status ativo/inativo.
- Cadastro de categorias para receitas ou despesas com cor personalizada.
- Registro de transações com filtros por período, tipo, conta e categoria.
- **Atualização automática de saldo** da conta na criação, edição e exclusão de transações (via Django signals).
- Área de usuário com login por username ou e-mail, cadastro, perfil, avatar, troca de senha e recuperação de senha.
- Verificação de e-mail no cadastro com link tokenizado.
- Logs de auditoria para eventos relevantes do sistema (login, logout, registro, reset de senha).

## Stack utilizada

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.10+, Django 5.2, Django REST Framework 3.16 |
| Autenticação | Session Auth + JWT (`djangorestframework-simplejwt`) |
| Filtros | `django-filter` |
| Frontend | Django Templates, Bootstrap 5, Bootstrap Icons, JavaScript |
| Banco de dados | SQLite (desenvolvimento), PostgreSQL (produção) |
| Deploy | Waitress 3.0, Whitenoise 6.8 |
| Configuração | `python-decouple` |
| Imagens | Pillow |

## Estrutura do projeto

```text
fin-track/
├── fin_track_project/
│   ├── manage.py
│   ├── run_server.bat              # Script de inicialização com Waitress (Windows)
│   ├── fin_track_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py                # Dashboard e views globais
│   │   └── tests.py
│   ├── apps/
│   │   ├── user/                   # Autenticação, perfil, senha
│   │   ├── accounts/               # Contas financeiras
│   │   ├── categories/             # Categorias de transações
│   │   └── transactions/           # Transações e sinais de saldo
│   ├── templates/
│   ├── static/
│   └── logs/                       # Audit trail
├── scripts/
│   └── fin_track_clean.ps1         # Automação de setup (Windows)
├── requirements.txt
├── .env.exemplo
└── README.md
```

## Arquitetura por módulos

| App | Responsabilidade |
|---|---|
| `user` | Autenticação, cadastro, perfil, senha e recuperação |
| `accounts` | Contas bancarias e de controle financeiro |
| `categories` | Classificação das transações |
| `transactions` | Receitas, despesas, filtros e atualização automática de saldo |
| `fin_track_project` | Dashboard, views globais, configuração principal e testes do núcleo |

## Modelos de dados

```
Admin (usuário)
 ├── Account (contas)
 │    └── Transaction (transações)
 │         └── Category (categoria)
 └── Category
```

| Modelo | Campos principais |
|---|---|
| `Admin` | username, email, password, avatar (binary), email_verified |
| `Account` | name, bank, type, account_color, balance, credit_limit, is_active |
| `Category` | name, type (receita/despesa), category_color |
| `Transaction` | account, category, transaction_type, value, date, payment_method |

**Tipos de conta:** corrente, poupança, cartão de crédito, investimento, dinheiro

**Métodos de pagamento:** dinheiro, cartão de crédito, cartão de débito, Pix, boleto, transferência, outros

### Regra de saldo automático

Os sinais `post_save` e `post_delete` em `transactions/signals.py` atualizam o campo `balance` da conta automaticamente:

- Receita criada → `balance += value`
- Despesa criada → `balance -= value`
- Transação deletada → operação inversa aplicada

## Como executar localmente

### 1. Clone o repositório

```bash
git clone <repo-url>
cd fin-track
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

Use o arquivo `.env.exemplo` como base e crie o seu `.env` na raiz do projeto:

```bash
copy .env.exemplo .env
```

Preencha as variáveis de acordo com a tabela abaixo:

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | Sim | Chave secreta do Django (gere uma aleatória) |
| `DEBUG` | Sim | `true` para desenvolvimento, `false` para produção |
| `DB_ENGINE` | Não | Engine do banco (padrão: `django.db.backends.sqlite3`) |
| `DB_NAME` | Não* | Nome do banco de dados (*obrigatório para PostgreSQL) |
| `DB_USER` | Não* | Usuário do banco |
| `DB_PASSWORD` | Não* | Senha do banco |
| `DB_HOST` | Não* | Host do banco |
| `DB_PORT` | Não* | Porta do banco |
| `ALLOWED_HOSTS` | Sim | Hosts permitidos separados por vírgula (`localhost,127.0.0.1`) |
| `CSRF_TRUSTED_ORIGINS` | Sim | Origins confiáveis para CSRF (`http://localhost:8000`) |
| `EMAIL_HOST_HOMO` | Não | Host do servidor SMTP de homologação (padrão: `localhost`) |
| `EMAIL_PORT_HOMO` | Não | Porta SMTP de homologação (padrão: `8025`) |
| `EMAIL_BACKEND_HOMO` | Não | Backend de e-mail de homologação |
| `DEFAULT_FROM_EMAIL_HOMO` | Não | E-mail remetente em homologação |
| `EMAIL_HOST` | Não | Host SMTP de produção (ex: `smtp.gmail.com`) |
| `EMAIL_PORT` | Não | Porta SMTP de produção (ex: `587`) |
| `EMAIL_HOST_USER` | Não | Usuário SMTP |
| `EMAIL_HOST_PASSWORD` | Não | Senha SMTP (use senha de app para Gmail) |
| `EMAIL_USE_TLS` | Não | `True` para TLS |
| `DEFAULT_FROM_EMAIL` | Não | E-mail remetente padrão em produção |
| `DJANGO_SUPERUSER_USERNAME` | Não | Username do superusuário (usado pelo script de setup) |
| `DJANGO_SUPERUSER_PASSWORD` | Não | Senha do superusuário |
| `DJANGO_SUPERUSER_EMAIL` | Não | E-mail do superusuário |

> Para desenvolvimento com `DEBUG=true` e SQLite, apenas `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` são obrigatórias.

### 5. Rode a aplicação

```bash
cd fin_track_project
python manage.py migrate
python manage.py runserver
```

Acesse em:

```
http://127.0.0.1:8000/
```

## Execução no Windows com Waitress

Para iniciar o projeto com `Waitress` e coletar estáticos automaticamente no Windows:

```bat
cd fin_track_project
run_server.bat
```

O script realiza automaticamente: verificação de dependências, migrações, coleta de estáticos e inicialização com 4 threads.

Ou manualmente:

```bash
waitress-serve --port=8000 --threads=4 fin_track_project.wsgi:application
```

## Script de automação

O projeto possui um utilitário em [`scripts/fin_track_clean.ps1`](scripts/fin_track_clean.ps1) para acelerar setup e limpeza do ambiente no Windows.

Esse script pode:

- limpar pastas `__pycache__`
- limpar arquivos de `migrations`
- remover o banco SQLite
- carregar variáveis do `.env`
- executar `makemigrations`, `migrate` e `createsuperuser`

### Como executar

Na raiz do projeto:

```powershell
.\scripts\fin_track_clean.ps1
```

Se o PowerShell bloquear a execução, rode antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Parâmetros disponíveis

| Parâmetro | Descrição |
|---|---|
| `-DeleteDB` | Remove o banco SQLite antes do setup |
| `-SkipCache` | Não limpa os diretórios `__pycache__` |
| `-SkipMigrations` | Não limpa os arquivos de migration |
| `-SkipEnv` | Não carrega variáveis do arquivo `.env` |
| `-DryRun` | Apenas simula o que seria executado |
| `-Help` | Exibe a ajuda do script |

### Exemplos de uso

```powershell
.\scripts\fin_track_clean.ps1 -Help
.\scripts\fin_track_clean.ps1 -DeleteDB
.\scripts\fin_track_clean.ps1 -SkipCache -SkipMigrations
.\scripts\fin_track_clean.ps1 -DeleteDB -DryRun
```

## Testes automatizados

O projeto possui cobertura dos fluxos principais da aplicação:

| Suite | O que testa |
|---|---|
| `fin_track_project/tests.py` | Dashboard, views globais, isolamento de dados |
| `apps/user/tests.py` | Login, cadastro, verificação de e-mail, perfil, avatar |
| `apps/accounts/tests.py` | CRUD de contas, filtros, validação de propriedade |
| `apps/categories/tests.py` | CRUD de categorias, filtro por tipo |
| `apps/transactions/tests.py` | Criação de transações, signals de saldo, filtros |

Para rodar os testes (com variáveis de ambiente mínimas no PowerShell):

```powershell
$env:DEBUG='true'
$env:SECRET_KEY='test-secret'
$env:DB_ENGINE='django.db.backends.sqlite3'
$env:EMAIL_HOST_HOMO='localhost'
$env:EMAIL_PORT_HOMO='25'
$env:EMAIL_BACKEND_HOMO='django.core.mail.backends.locmem.EmailBackend'
$env:DEFAULT_FROM_EMAIL_HOMO='test@example.com'
cd fin_track_project
python manage.py test
```

## Endpoints

### Interface web

| Método | URL | Descrição |
|---|---|---|
| GET | `/` | Entrada da aplicação |
| GET | `/dashboard/` | Dashboard principal |
| GET/POST | `/user/login/` | Login |
| GET | `/user/logout/` | Logout |
| GET/POST | `/user/register/` | Cadastro |
| GET/POST | `/user/profile/` | Perfil do usuário |
| GET/POST | `/user/password_reset/` | Solicitar reset de senha |
| GET | `/user/verify-email/<uidb64>/<token>/` | Verificar e-mail |
| GET | `/accounts/list/` | Listar contas |
| GET | `/accounts/detail/<id>/` | Detalhe da conta |
| GET/POST | `/accounts/create/` | Criar conta |
| GET/POST | `/accounts/edit/<id>/` | Editar conta |
| POST | `/accounts/delete/<id>/` | Excluir conta |
| GET | `/categories/list/` | Listar categorias |
| GET/POST | `/categories/create/` | Criar categoria |
| GET/POST | `/categories/edit/<id>/` | Editar categoria |
| POST | `/categories/delete/<id>/` | Excluir categoria |
| GET | `/transactions/list/` | Listar transações (com filtros) |
| GET/POST | `/transactions/create/` | Criar transação |
| GET/POST | `/transactions/edit/<id>/` | Editar transação |
| POST | `/transactions/delete/<id>/` | Excluir transação |

### API REST (JSON)

| Método | URL | Descrição |
|---|---|---|
| POST | `/api/token/` | Obter token JWT |
| POST | `/api/token/refresh/` | Renovar token JWT |
| GET/POST | `/api/accounts/` | Contas (listagem e criação) |
| GET/POST | `/api/transactions/` | Transações (listagem e criação) |
| GET/POST | `/api/categories/` | Categorias (listagem e criação) |

## Segurança

- Isolamento completo de dados por usuário (toda query filtra por `request.user`)
- Verificação de e-mail obrigatória na ativação da conta
- Reset de senha via token com expiração
- CSRF protection com lista de origins confiáveis
- HSTS habilitado em produção (`SECURE_HSTS_SECONDS=31536000`)
- SSL redirect em produção (`SECURE_SSL_REDIRECT`)
- Cookies seguros em produção (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- `X_FRAME_OPTIONS: DENY`
- Avatar armazenado como `BinaryField` (sem exposição de path de arquivo)

## Acesso externo com Cloudflare Tunnel (opcional)

Para expor a aplicação localmente via Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:8000
```

Adicione o domínio gerado em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` no `.env`.

## Por que este projeto se destaca

O FinTrack mostra capacidade de entregar um sistema com mentalidade de produto e não apenas de exercício técnico. Ele combina interface, backend, autenticação, organização modular, preocupação com segurança, configuração para deploy e testes automatizados em uma única base coesa.

Em um contexto de avaliação técnica, este projeto evidencia:

- domínio de Django e DRF
- organização de código por contexto de negócio
- cuidado com experiência do usuário
- preocupação com manutenção e validação automatizada
- capacidade de evoluir um MVP para um produto mais robusto

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE).
