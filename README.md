# Fin-Track: API RESTful para Gestão Financeira

## Resumo Executivo

O **Fin-Track** é uma API RESTful de back-end, projetada para servir como o núcleo de uma aplicação de gestão financeira pessoal. Construído com tecnologias de ponta e seguindo as melhores práticas de desenvolvimento, este projeto demonstra uma arquitetura limpa, segura e escalável, pronta para ser integrada a qualquer interface de front-end (web ou mobile) e ser expandida com novas funcionalidades.

O objetivo é fornecer uma base sólida e confiável que impressione pela qualidade técnica e pela prontidão para o mercado.

---

## Destaques Técnicos e Arquiteturais

Esta API não é apenas funcional, mas foi construída sobre uma base de tecnologias e padrões que garantem performance, segurança e manutenibilidade. A escolha de cada componente foi deliberada para criar um produto de nível profissional.

| Pilar Arquitetural | Tecnologias Utilizadas (`requirements.txt`) | Vantagens e Justificativas Técnicas |
| :--- | :--- | :--- |
| **Framework Robusto e Moderno** | `Django==5.2.7` | Utilizamos uma versão recente do Django, um dos frameworks mais seguros e completos do mercado. Ele nos permite desenvolver rapidamente, garantindo segurança nativa contra vulnerabilidades comuns (XSS, CSRF, SQL Injection) e fornecendo uma estrutura escalável (ORM, admin, etc.). |
| **API RESTful Padrão de Mercado** | `djangorestframework==3.16.1`, `django-filter==25.2` | A API segue os padrões REST e é construída com o DRF, o padrão-ouro para APIs em Django. Isso garante endpoints limpos, documentação automática e recursos avançados como filtragem de dados dinâmica via `django-filter`, essencial para relatórios e buscas complexas. |
| **Banco de Dados Confiável** | `psycopg2==2.9.11` | A escolha pelo PostgreSQL, acessado via `psycopg2`, reflete a necessidade de consistência e integridade de dados, críticas para uma aplicação financeira. PostgreSQL é renomado por sua robustez e performance em cenários de alta transação. |
| **Configuração Segura (12-Factor App)** | `python-decouple==3.8` | O projeto adere aos princípios do *Twelve-Factor App*, separando estritamente a configuração do código. Isso torna a aplicação mais segura, portátil entre ambientes (desenvolvimento, staging, produção) e fácil de gerenciar por equipes de DevOps. |
| **Suporte a Mídia e Assincronia** | `Pillow==11.3.0`, `asgiref==3.10.0` | A inclusão de `Pillow` prepara a API para funcionalidades de upload de imagens (ex: avatares, comprovantes), enquanto o `asgiref` garante compatibilidade com servidores web modernos e assíncronos (ASGI), otimizando a performance e o consumo de recursos. |

---

## Funcionalidades de Negócio Implementadas

*   **Gestão Completa de Usuários:** Autenticação segura baseada em token e endpoints para CRUD de usuários.
*   **Controle de Transações Financeiras:** API para registro de receitas e despesas.
*   **Organização Financeira:** Suporte para categorização de transações e gerenciamento de múltiplas contas.
*   **Planejamento e Orçamento:** Estrutura pronta para implementação de metas e orçamentos.

---

## Documentação da API (Exemplo: Módulo de Usuários)

A API é auto-documentada através da interface do DRF. Abaixo, um exemplo da clareza e padrão dos endpoints.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/users/` | Registra um novo usuário no sistema. |
| `POST` | `/api/users/login/` | Autentica um usuário e retorna um `Auth Token`. |
| `GET` | `/api/users/{id}/` | Retorna os detalhes de um usuário específico. |
| `PUT` | `/api/users/{id}/` | Atualiza todos os dados de um usuário. |

---

## Como Iniciar (Developer Onboarding)

Um processo de setup rápido e claro é crucial para a produtividade da equipe de desenvolvimento.

1.  **Clone & Configure:**
    ```bash
    git clone <repo-url> && cd fin-track
    pip install -r requirements.txt
    cp .env.example .env # Preencha com suas credenciais
    ```
2.  **Banco de Dados & Execução:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Garantia de Qualidade

O projeto está configurado com um ambiente de testes para garantir a estabilidade e a confiabilidade do código a cada nova alteração.

```bash
# Execute a suíte de testes para validar a integridade da aplicação
python manage.py test apps/
```fin-track/
├── fin_track_project/
│   ├── __init__.py
│   ├── settings.py           # Configurações globais do Django
│   ├── urls.py               # Rotas URL globais da API
│   └── wsgi.py               # Configuração WSGI para deploy
├── apps/
│   ├── users/                # Módulo de gestão de usuários
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para usuários
│   │   ├── serializers.py    # Serializadores DRF para usuários
│   │   ├── urls.py           # Rotas URL específicas para usuários
│   │   └── views.py          # Lógica de negócio (ViewSets) para usuários
│   ├── transactions/         # Módulo de gestão de transações financeiras (ex: receitas, despesas)
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py         # Modelos de dados para transações
│   │   ├── serializers.py    # Serializadores DRF para transações
│   │   ├── urls.py           # Rotas URL específicas para transações
│   │   └── views.py          # Lógica de negócio (ViewSets) para transações
│   └── ...                   # Outros módulos (categorias, contas, orçamentos, etc.)
├── manage.py                 # Utilitário de linha de comando do Django
├── requirements.txt          # Dependências do projeto
├── .env.example              # Exemplo de arquivo de variáveis de ambiente
└── README.md                 # Documentação principal do projeto
