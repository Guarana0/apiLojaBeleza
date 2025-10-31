<h1 align="center">API do Dashboard - Loja de Beleza</h1>

<div align="center">
  <strong>🐳 ⚙️ 🌐</strong>
</div>
<div align="center">
  Um projeto de API RESTful feito Django,PostgreSQL e Django Rest Framework
</div>

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de que você tenha as seguintes ferramentas instaladas em sua máquina:

- Python 🐍
- Git 🐈
- PIP 

## 🚀 Passo a passo interativo

Siga os passos abaixo para iniciar o projeto em seu ambiente local:

1️⃣ **Clone o repositório**

   Clique no botão "Clone" acima ou execute o seguinte comando no terminal:

   ```bash
   git clone https://github.com/Guarana0/apiLojaBeleza.git
   ```

   Isso criará uma cópia local do repositório em seu ambiente.

2️⃣ **Crie e ative um ambiente virtual**

   É uma boa prática isolar as dependências do projeto.

   ```bash
    # Criar o ambiente virtual
    python -m venv venv
    # Ativar no Windows
    .\venv\Scripts\activate
    # Ativar no macOS/Linux
    source venv/bin/activate
  ````

   🐳 Isso cria o ambiente virtual e não atrapalha nenhum outro projeto seu

3️⃣ **Baixe as Dependências do Projeto**

  O arquivo `requirements.txt` contém todas as bibliotecas que o projeto precisa.

  ```bash
    pip install -r requirements.txt
  ````

4️⃣ **Configure as variáveis de ambiente:**

   Este projeto usa um arquivo `.env` para gerenciar chaves e configurações sensíveis. Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis (ajuste conforme necessário):

       ```env
    DB_NAME= nome do seu banco de dados
    DB_USER= usuario do banco de dados
    DB_PASSWORD= senha do banco de dados
    DB_HOST= host do banco de dados 
    DB_PORT= porta do banco de dados (gerlamente 5432)
    ```

5️⃣ **Aplique as Migrações no Banco de dados**

  Este comando cria as tabelas no banco de dados com base nos seus `models`.
  
    ```bash
    python manage.py migrate
    ```
    
6️⃣ **Inicie o servidor**

    ```bash
    python manage.py runserver
    ```
    
    O servidor estará rodando em `http://127.0.0.1:8000/`.

   7️⃣ **Criar Superusuario**

   ```bash
  python manage.py createsuperuser
   ```

Isso é nescessario para a url `/admin/` e `/auth/login/`

## Rotas da API

A API está disponível sob o prefixo `/api/`.

## Como Testar

Após iniciar o servidor, você pode testar os endpoints de duas formas:

1.  **API Navegável do DRF:** Simplesmente acesse `http://127.0.0.1:8000/api/vendedores/` no seu navegador para ver a interface interativa. (é nescessario fazer login com um super usuario para acessar)
2.  **Ferramentas de Cliente API:** Use ferramentas como [Postman](https://www.postman.com/) ou [Insomnia](https://insomnia.rest/) para fazer requisições `GET`, `POST`, `PUT`, `DELETE`, etc.
