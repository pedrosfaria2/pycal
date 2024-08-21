
# Event Manager API

## Descrição do Projeto

Esta API foi desenvolvida como parte de um desafio técnico para a criação de um sistema de gerenciamento de eventos. O projeto foi implementado utilizando o framework FastAPI, com validação de dados usando Pydantic, integração com MySQL via SQLAlchemy, e um pipeline CI/CD configurado com GitHub Actions.

## Requisitos

### Dependências:

- **Python 3.12+**
- **Docker** (para rodar o MySQL server)
- **Poetry** (para gerenciamento de dependências)

## Explicação do Projeto

### Estrutura do Projeto:

- **`app/`**: Contém todo o código-fonte da aplicação, dividido em vários módulos:
  - **`crud/`**: Implementação das operações CRUD (Create, Read, Update, Delete) para o modelo `Event`.
  - **`database.py`**: Configuração do banco de dados e gerenciamento de sessões.
  - **`exceptions/`**: Handlers para exceções personalizadas e tratamento de erros.
  - **`logging_config.py`**: Configuração do sistema de logging.
  - **`middleware/`**: Contém middlewares para tratamento de exceções e controle de throttling.
  - **`models/`**: Definição dos modelos do banco de dados.
  - **`routers/`**: Definição das rotas da API.
  - **`schemas/`**: Definição dos schemas Pydantic para validação de dados.
  - **`config.py`**: Configurações gerais da aplicação.
  - **`main.py`**: Ponto de entrada da aplicação FastAPI.
- **`tests/`**: Contém testes para a aplicação.
  - **`conftest.py`**: Configura o ambiente de testes.
  - **`test_crud.py`**: Testa as operações de CRUD diretamente, utilizando a camada de banco de dados.
  - **`test_events.py`**: Teste as rotas da API.
  - **`test_validation.py`**: Foca na validação de dados, testando cenários de erro e garantindo que dados inválidos sejam rejeitados.
  - **`test_throttling.py`**: Testa o throttle imposto na API.
  - **`test_health_check.py`**: Testa o endpoint de saúde criado. 
  
### Escolhas Técnicas:

- **FastAPI**: Escolhi o FastAPI devido à sua performance, facilidade de uso, e suporte embutido para validação de dados e documentação automática.
  
- **Pydantic**: Utilizado para validação de dados, assegurando que todos os inputs e outputs estejam no formato correto e que dados inválidos sejam identificados e tratados de forma apropriada.

- **SQLAlchemy**: Optado como ORM para facilitar a manipulação do banco de dados de forma orientada a objetos, mantendo o código limpo e modularizado.

- **Docker**: Utilizado para garantir que o ambiente de banco de dados seja consistente e fácil de configurar, independentemente do ambiente de desenvolvimento.

- **Poetry**: Escolhido para gerenciamento de dependências, permitindo um controle preciso das bibliotecas utilizadas e facilitando a instalação e o gerenciamento do ambiente de desenvolvimento.

- **Pytest**: Selecionado como framework de testes para garantir a robustez e a qualidade do código. Os testes implementados cobrem tanto as funcionalidades da API quanto as validações de dados, assegurando que a aplicação se comporte conforme o esperado.

- **CI/CD com GitHub Actions**: Configurei um pipeline de CI/CD para garantir que os testes sejam executados automaticamente a cada novo commit, mantendo a integridade do código e a qualidade do projeto.

## Como Rodar o Projeto

1. **Inicie o MySQL com Docker:**

   Certifique-se de que o MySQL está rodando com Docker:

   ```bash
   docker-compose up -d
   ```

2. **Instale as Dependências:**
    
    Utilize o Poetry para instalar todas as dependências do projeto:

   ```bash
   poetry install
   ```

3. **Ative o Ambiente Virtual:**

    Ative o ambiente virtual criado pelo Poetry:

    ```bash
   poetry shell
   ```


4. **Execute as Migrações:**

   Use o Alembic para aplicar as migrações necessárias ao banco de dados:

   ```bash
   poetry run alembic upgrade head
   ```

5. **Inicie a Aplicação:**

   Inicie o servidor FastAPI:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

6. **Acesse a API:**

   Abra seu navegador e acesse:

   ```
   http://127.0.0.1:8000
   ```

   A documentação interativa da API estará disponível em:

   ```
   http://127.0.0.1:8000/docs
   ```

## Testes

O projeto inclui uma série de testes unitários, de integração e de validação, que garantem a correta funcionalidade das operações CRUD (Create, Read, Update, Delete) e a integridade dos dados processados pela API. Esses testes também cobrem o controle de throttling e a verificação do endpoint de saúde, assegurando que a API lida corretamente com limites de requisição e a conexão ao banco de dados. Os testes foram implementados utilizando o framework pytest e cobrem tanto o comportamento das rotas quanto a lógica interna do CRUD. Para rodar os testes localmente, utilize:
```bash
poetry run pytest
```

Isso garantirá que todas as funcionalidades estão cobertas e funcionando como esperado.

## Considerações Finais

Este projeto foi desenvolvido com o objetivo de cobrir todos os requisitos obrigatórios do desafio, incluindo a utilização de um framework web moderno (FastAPI), validação de dados (Pydantic), manipulação de banco de dados com ORM (SQLAlchemy), testes automatizados e controle de throttling para gerenciar o tráfego da API e evitar abusos. Além disso, a maior parte dos requisitos opcionais foi implementada, especialmente aqueles que impactam diretamente as funcionalidades da API e demonstram boas práticas de desenvolvimento, como a integração contínua (CI/CD) e a cobertura de testes.

A escolha das tecnologias foi baseada em sua eficiência e compatibilidade com o cenário proposto. Docker foi utilizado para garantir um ambiente de banco de dados consistente, enquanto Poetry foi escolhido para o gerenciamento de dependências, assegurando um ambiente de desenvolvimento controlado e fácil de replicar.

Embora a segurança não tenha sido o foco principal nesta versão do projeto, ela foi identificada como uma área de melhoria para futuras iterações. O projeto está preparado para expansões, incluindo a adição de mecanismos de autenticação e autorização, que podem ser incorporados conforme a evolução das necessidades da aplicação.

Adicionalmente, embora ferramentas de monitoramento não tenham sido integradas diretamente ao projeto, foi exposto um endpoint de verificação de saúde (`/health`) que permite a fácil integração com sistemas de monitoramento externos. Esse endpoint verifica a conectividade com o banco de dados e o estado geral da aplicação.