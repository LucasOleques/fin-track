# 🪙 Fin-Track: Gestão Financeira

Uma aplicação backend desenvolvida com Django e Django REST Framework (DRF) para o gerenciamento de finanças. O sistema conta com o gerenciamento de usuários, contas bancárias, transações financeiras e as categorias das transações.

## Funcionalidades de Negócio Implementadas
* **Gestão de Usuários:** Autenticação segura baseada em token e endpoints para CRUD de usuários.
* **Controle de Transações Financeiras:** API para registro de receitas e despesas.
* **Organização Financeira:** Suporte para categorização de transações e gerenciamento de múltiplas contas.
* **Segurança e Isolamento de Dados:** Cada usuário só pode acessar e gerenciar seus próprios dados.

## Tecnologias Utilizadas
- **Python:** A linguagem de programação principal do projeto.
- **Django:** O framework web principal da aplicação, gerenciando a lógica de negócio, modelos e rotas.
- **Django REST Framework (DRF):** Toolkit essencial para a construção rápida e flexível de APIs RESTful, cuidando da serialização, autenticação e viewsets.
- **PostgreSQL:** Um sistema de gerenciamento de banco de dados relacional.
- **JWT:** Para implementar autenticação segura baseada em tokens.
- **django-filter:** Para permitir filtragem avançada e declarativa nos endpoints da API, facilitando a consulta de dados.
- **python-decouple:** Para gerenciar variáveis de ambiente de forma segura, separando as configurações (como chaves de API e credenciais de banco de dados) do código-fonte.



## Pré-requisitos
- Python 3.10+
- Conda (ou outro gerenciador de ambiente virtual como `venv`)
- PostgreSQL 12+

## Estrutura do Projeto
A estrutura do projeto é organizada para facilitar a manutenção e escalabilidade, seguindo as melhores práticas do Django e DRF.

### Diretórios e Arquivos:
```bash
fin-track/
├── fin_track_project/
│   ├── __init__.py
│   ├── settings.py           # Configurações globais do Django
│   ├── urls.py               # Rotas URL globais da API
│   ├── asgi.py               # Configuração ASGI para deploy (em andamento)
│   ├── wsgi.py               # Configuração WSGI para deploy (em andamento)
│   └── apps/
│       ├── user/                # Módulo de gestão de usuários
│       ├── accounts/            # Módulo de gestão de contas bancárias
│       ├── transactions/        # Módulo de gestão de transações financeiras
│       └── categories/          # Módulo de gestão de categorias de transações
├── manage.py                 # Utilitário de linha de comando do Django
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal do projeto
```

## Documentação:
Principais endpoints da API:

### Users (Usuários)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/user/` | Registra um novo usuário. |
| `POST` | `/api/token/` | Autentica um usuário e retorna um token JWT. |
| `GET` | `/api/user/manage/` | Retorna os dados do usuário autenticado. |
| `PUT` | `/api/user/manage/` | Atualiza todos os dados do usuário autenticado. |
| `PATCH` | `/api/user/manage/` | Atualiza parcialmente os dados do usuário autenticado. |
| `DELETE` | `/api/user/manage/` | Remove o próprio usuário autenticado. |

#### Exemplo de corpo para autenticação (`POST /api/token/`):
```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```
---

### Accounts (Contas)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/accounts/` | Cria uma nova conta. |
| `GET` | `/api/accounts/` | Lista todas as contas do usuário autenticado. |
| `GET` | `/api/accounts/{id}/` | Retorna os detalhes de uma conta específica. |
| `PUT` | `/api/accounts/{id}/` | Atualiza todos os dados de uma conta. |
| `PATCH` | `/api/accounts/{id}/` | Atualiza parcialmente uma conta. |
| `DELETE` | `/api/accounts/{id}/` | Remove uma conta específica. |

---

### Transactions (Transações)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/transactions/` | Registra uma nova transação financeira. |
| `GET` | `/api/transactions/` | Lista todas as transações do usuário autenticado. Permite filtros. |
| `GET` | `/api/transactions/{id}/` | Retorna os detalhes de uma transação específica. |
| `PUT` | `/api/transactions/{id}/` | Atualiza todos os dados de uma transação. |
| `PATCH` | `/api/transactions/{id}/` | Atualiza parcialmente uma transação. |
| `DELETE` | `/api/transactions/{id}/` | Remove uma transação específica. |

---

### Categories (Categorias)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/categories/` | Cria uma nova categoria. |
| `GET` | `/api/categories/` | Lista todas as categorias do usuário autenticado. |
| `GET` | `/api/categories/{id}/` | Retorna os detalhes de uma categoria específica. |
| `PUT` | `/api/categories/{id}/` | Atualiza uma categoria. |
| `PATCH` | `/api/categories/{id}/` | Atualiza parcialmente uma categoria. |
| `DELETE` | `/api/categories/{id}/` | Remove uma categoria específica. |
---

## Sobre a Autenticação:
> Todos os endpoints protegidos exigem autenticação JWT. Os dados retornados e manipulados sempre pertencem ao usuário autenticado.

## Como Iniciar (Developer Onboarding)
Configuração para iniciar o projeto localmente.

1.  **Clone do Repositório:**
    ```bash
    git clone <repo-url>
    cd fin-track
    ```
2.  **Ambiente Virtual:**
    ```bash
    conda create -n fin-track
    conda activate fin-track
    ```
3.  **Instalação de Dependências & Configuração do .env:**
    ```bash
    pip install -r requirements.txt
    cp .env.example .env # Preencha com suas credenciais
    ```
4.  **Banco de Dados & Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Iniciar o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
6.  **Acesse a API:**
    Acesse http://localhost:8000/api/ para interagir com a API.

## Script de Limpeza do Projeto

O projeto inclui um script PowerShell para limpeza de arquivos e pastas temporárias, caches e arquivos desnecessários gerados durante o desenvolvimento.

**Script:** `fin_track_clean.ps1`

**Para que serve?**

Remove arquivos `__pycache__`, arquivos `.pyc`, pastas de migrações não essenciais e outros resíduos comuns em projetos Python/Django, facilitando a manutenção e evitando sujeira no versionamento.

**Como executar:**

No terminal do Windows, na raiz do projeto:

```powershell
./fin_track_clean.ps1
```

Se necessário, permita a execução de scripts PowerShell com:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

# Contribuindo

Pull requests são bem-vindos!  
Siga o padrão de commits convencionais e abra uma issue antes de propor novas features.

```bash
git checkout -b feature/nome-da-feature
git commit -m "feat: adiciona suporte a categorias personalizadas"
git push origin feature/nome-da-feature
```

# Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0+-green?style=for-the-badge&logo=django)
![Django REST Framework](https://img.shields.io/badge/Django_Rest_Framework-3.15-red?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?style=for-the-badge&logo=postgresql)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green.svg?style=for-the-badge)
