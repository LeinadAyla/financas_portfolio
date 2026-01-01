
# 🛡️ Configuração de Autenticação e Hardening (SELinux)
 
# 💰 Sistema de Gestão Financeira Personalizado - Finanças 2026

Este é um ecossistema completo de gestão financeira desenvolvido com **Python (Flask)** e **PostgreSQL**, focado em alta performance, segurança de dados (Multi-tenancy) e visualização moderna de indicadores.

## 🚀 Novidades da Versão 1.2 (Stability & UX Update)

-   **Localização BRL (Novo):** Sistema inteligente de filtros Jinja2 para formatação de moeda brasileira (Ex: R$ 1.500,00).
    
-   **Busca & Filtros Dinâmicos:** Motor de busca por descrição e filtros temporais (Mês Atual) integrados ao Dashboard.
    
-   **Resiliência (Error Handling):** Implementação de página 404 personalizada para garantir a retenção do usuário em rotas inexistentes.
    
-   **Dashboards Interativos:** Visualização dinâmica de receitas e despesas com **Chart.js**.
    
-   **Gestão de Metas (Budgeting):** Sistema de barra de progresso em tempo real baseado em limites de gastos definidos pelo usuário.
    

## 🛠️ Stack Tecnológica

-   **Backend:** Python 3.12+ (Flask)
    
-   **Banco de Dados:** PostgreSQL 15 (Docker Container)
    
-   **Segurança:** Flask-Login para sessões e Werkzeug para Hashing de senhas.
    
-   **Frontend:** HTML5, CSS3 (Modern Grid/Flexbox), JavaScript (ES6).
    
-   **Data Viz:** Chart.js para indicadores financeiros.
    

## 💎 Diferenciais Técnicos (Boas Práticas)

-   **Clean Code:** Lógica de negócio separada por rotas e filtros reutilizáveis.
    
-   **ORM SQLAlchemy:** Abstração completa de banco de dados, protegendo a aplicação contra SQL Injection.
    
-   **UX/UI Dark Mode:** Interface otimizada para redução de fadiga visual e foco nos dados financeiros.
    
-   **Mobile Friendly:** Layout responsivo adaptável para dispositivos móveis.
    

## 📦 Como Rodar o Projeto

### 1. Requisitos Prévios

-   Docker & Docker Compose instalado.
    
-   Python 3.12+ (opcional para rodar fora do container).
    

### 2. Clonar e Configurar Ambiente

Bash

```
git clone https://github.com/LeinadAyla/financas_portfolio.git
cd financas_portfolio/projeto_financas_v1

```

### 3. Subir Banco de Dados e Aplicação

Bash

```
# Iniciar o container PostgreSQL
docker-compose up -d

# Instalar dependências (dentro do venv)
pip install -r requirements.txt

# Executar a aplicação
python app/main.py
```

  

---

*Notas de laboratório - Atividade 4.1 e 4.2 - Hackers do Bem.*