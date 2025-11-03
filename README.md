# 🪙 Fin-Track: API REST para Gestão Financeira Pessoal

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0+-green?style=for-the-badge&logo=django)
![Django REST Framework](https://img.shields.io/badge/Django_Rest_Framework-3.15-red?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?style=for-the-badge&logo=postgresql)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green.svg?style=for-the-badge)

Uma aplicação backend desenvolvida com Django e Django REST Framework (DRF) para o gerenciamento de finanças pessoais. O sistema conta com o gerenciamento de usuários, contas bancárias, transações financeiras e as categorias das transações.

## Funcionalidades de Negócio Implementadas
* **Gestão Completa de Usuários:** Autenticação segura baseada em token e endpoints para CRUD de usuários.
* **Controle de Transações Financeiras:** API para registro de receitas e despesas.
* **Organização Financeira:** Suporte para categorização de transações e gerenciamento de múltiplas contas.
* **Segurança e Isolamento de Dados:** Cada usuário só pode acessar e gerenciar seus próprios dados.

## Tecnologias Utilizadas
- **Python:** A linguagem de programação principal do projeto.
- **Django:** O robusto framework web que serve como espinha dorsal da aplicação, gerenciando a lógica de negócio, modelos e rotas.
- **Django REST Framework (DRF):** Toolkit essencial para a construção rápida e flexível de APIs RESTful, cuidando da serialização, autenticação e viewsets.
- **PostgreSQL:** Um sistema de gerenciamento de banco de dados objeto-relacional poderoso e de código aberto, escolhido por sua robustez e escalabilidade.
- **DRF Token Authentication:** Para a implementação de um sistema de autenticação seguro baseado em tokens.
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
│   └── wsgi.py               # Configuração WSGI para deploy (em andamento)
├── apps/
│   ├── user/                # Módulo de gestão de usuários
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para usuários
│   │   ├── serializers.py    # Serializadores DRF para usuários
│   │   ├── urls.py           # Rotas URL específicas para usuários
│   │   └── views.py          # Lógica de negócio (ViewSets) para usuários
│   ├── accounts/             # Módulo de gestão de contas bancárias
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para contas
│   │   ├── serializers.py    # Serializadores DRF para contas
│   │   ├── urls.py           # Rotas URL específicas para contas
│   │   └── views.py          # Lógica de negócio (ViewSets) para contas
│   ├── transactions/         # Módulo de gestão de transações financeiras
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para transações
│   │   ├── serializers.py    # Serializadores DRF para transações
│   │   ├── urls.py           # Rotas URL específicas para transações
│   │   └── views.py          # Lógica de negócio para transações
│   ├── categories/           # Módulo de gestão de categorias de transações
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para categorias
│   │   ├── serializers.py    # Serializadores DRF para categorias
│   │   ├── urls.py           # Rotas URL específicas para categorias
│   │   └── views.py          # Lógica de negócio para categorias
├── manage.py                 # Utilitário de linha de comando do Django
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal do projeto
```

## Documentação da API:
Principais endpoints da API RESTful para gestão financeira pessoal.

### Usuários
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/user/` | Registra um novo usuário. |
| `POST` | `/api/auth_token/` | Autentica um usuário e retorna um `Auth Token`. |
| `GET` | `/api/user/manage/` | Retorna os detalhes do usuário logado. |
| `PUT` | `/api/user/manage/` | Atualiza todos os dados do usuário logado. |
| `PATCH` | `/api/user/manage/` | Atualiza parcialmente os dados do usuário logado. |
| `DELETE` | `/api/user/manage/` | Remove um usuário específico. |

#### Exemplo de corpo para autenticação (`POST /api/auth_token/`):
```JSON
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```
---

### Contas (Accounts)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/accounts/` | Cria uma nova conta. |
| `GET` | `/api/accounts/` | Lista todas as contas do usuário logado. |
| `GET` | `/api/accounts/{id}/` | Retorna os detalhes de uma conta específica. |
| `PUT` | `/api/accounts/{id}/` | Atualiza todos os dados de uma conta. |
| `DELETE` | `/api/accounts/{id}/` | Remove uma conta específica. |

---

### Transações
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/transactions/` | Registra uma nova transação financeira. |
| `GET` | `/api/transactions/` | Lista todas as transações do usuário. Permite filtros. |
| `GET` | `/api/transactions/{id}/` | Retorna os detalhes de uma transação específica. |
| `PUT` | `/api/transactions/{id}/` | Atualiza todos os dados de uma transação. |
| `DELETE` | `/api/transactions/{id}/` | Remove uma transação específica. |

---

### Categorias (Categories)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/categories/` | Cria uma nova categoria. |
| `GET` | `/api/categories/{id}/` | Retorna os detalhes de uma categoria específica. |
| `PUT` | `/api/categories/{id}/` | Atualiza uma categoria. |
| `DELETE` | `/api/categories/{id}/` | Remove uma categoria específica. |
---

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