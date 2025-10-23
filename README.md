# 🪙 Fin-Track: API RESTful para Gestão Financeira Pessoal
Uma aplicação backend desenvolvida com Django e Django REST Framework (DRF) para gerenciar finanças pessoais, incluindo funcionalidades como gestão de usuários, controle de finanças pessoais, controle de cartões de crédito e débito, categorização de despesas e receitas, além de planejamento financeiro.

## 🚀 Funcionalidades de Negócio Implementadas
* **Gestão Completa de Usuários:** Autenticação segura baseada em token e endpoints para CRUD de usuários.
* **Controle de Transações Financeiras:** API para registro de receitas e despesas.
* **Organização Financeira:** Suporte para categorização de transações e gerenciamento de múltiplas contas.
* **Planejamento e Orçamento:** Estrutura para implementar orçamentos e metas financeiras.
* **Relatórios Financeiros:** Endpoints para geração de relatórios financeiros básicos.

## 🛠️ Tecnologias Utilizadas
- **Django:** Framework web de alto nível para desenvolvimento rápido e seguro.
- **Django REST Framework (DRF):** Biblioteca poderosa e flexível para construir APIs web.
- **PostgreSQL:** Banco de dados relacional para armazenamento de dados.

## 🧩 Estrutura do Projeto
A estrutura do projeto é organizada para facilitar a manutenção e escalabilidade, seguindo as melhores práticas do Django e DRF.

### Diretórios e Arquivos:
```bash
fin-track/
├── fin_track_project/
│   ├── __init__.py
│   ├── settings.py           # Configurações globais do Django
│   ├── urls.py               # Rotas URL globais da API
│   └── wsgi.py               # Configuração WSGI para deploy
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
│   │   └── views.py          # Lógica de negócio (ViewSets) para transações
│   ├── categories/           # Módulo de gestão de categorias de transações
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para categorias
│   │   ├── serializers.py    # Serializadores DRF para categorias
│   │   ├── urls.py           # Rotas URL específicas para categorias
│   │   └── views.py          # Lógica de negócio (ViewSets) para categorias
├── manage.py                 # Utilitário de linha de comando do Django
├── requirements.txt          # Dependências do projeto
├── .env.example              # Exemplo de arquivo de variáveis de ambiente
└── README.md                 # Documentação principal do projeto
```

## 📡 Documentação da API:
Principais endpoints da API RESTful para gestão financeira pessoal.

### Usuários
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/user/` | Registra um novo usuário no sistema. |
| `POST` | `/api/user/login/` | Autentica um usuário e retorna um `Auth Token`. |
| `GET` | `/api/user/{id}/` | Retorna os detalhes de um usuário específico. |
| `PUT` | `/api/user/{id}/` | Atualiza todos os dados de um usuário. |
| `DELETE` | `/api/user/{id}/` | Remove um usuário específico. |
---

### Contas (Accounts)
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/accounts/` | Cria uma nova conta. |
| `GET` | `/api/accounts/{id}/` | Retorna os detalhes de uma conta específica. |
| `PUT` | `/api/accounts/{id}/` | Atualiza todos os dados de uma conta. |
| `DELETE` | `/api/accounts/{id}/` | Remove uma conta específica. |
---

### Transações
| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/transactions/` | Registra uma nova transação financeira. |
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

## ⚙️ Como Iniciar (Developer Onboarding)
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


# 🤝 Contribuindo

Pull requests são bem-vindos!  
Siga o padrão de commits convencionais e abra uma issue antes de propor novas features.

```bash
git checkout -b feature/nome-da-feature
git commit -m "feat: adiciona suporte a categorias personalizadas"
git push origin feature/nome-da-feature
```

# 📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.