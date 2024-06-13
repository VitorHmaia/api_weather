# Weather API

![Django Logo](https://static.djangoproject.com/img/logos/django-logo-negative.png)
![MongoDB Logo](https://webassets.mongodb.com/_com_assets/cms/mongodb_logo1-76twgcu2dm.png)

## Visão Geral

A Weather API é uma aplicação que permite o gerenciamento de dados meteorológicos. Ela foi construída utilizando Django, Django REST Framework e MongoDB. A API oferece endpoints para criar, ler, atualizar e deletar dados meteorológicos, além de funcionalidades para gerar dados aleatórios e limpar o banco de dados.

## Tecnologias Utilizadas

- **Django**: Framework web utilizado para construir a aplicação.
- **Django REST Framework**: Utilizado para criar APIs RESTful de forma simples e rápida.
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar os dados meteorológicos.
- **PyMongo**: Biblioteca utilizada para conectar e interagir com o MongoDB.
- **JWT (JSON Web Token)**: Utilizado para autenticação e controle de acesso.

## Configuração do Projeto

### Variáveis de Ambiente

Certifique-se de configurar as seguintes variáveis de ambiente para proteger suas chaves e strings de conexão:

```bash
export SECRET_KEY='your-secret-key'
export MONGO_CONNECTION_STRING='your-mongo-connection-string'
export MONGO_DATABASE_NAME='your-database-name'
```

## Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Configuração do MongoDB 

Certifique-se de que o MongoDB esteja instalado e rodando. Ajuste a variável de ambiente `MONGO_CONNECTION_STRING` para apontar para sua instância do MongoDB.

### Configuração do Django

Crie um arquivo `.env` na raiz do seu projeto com o seguinte conteúdo:

```bash
SECRET_KEY=your-secret-key
MONGO_CONNECTION_STRING=mongodb://localhost:27017/
MONGO_DATABASE_NAME=weather_maia
```

### Endpoints

#### Autenticação

A API utiliza JWT para autenticação. Você pode obter um token JWT e renová-lo usando os seguintes endpoints:

- Obter Token JWT: /api/token/

  - Método: POST
  - Payload:
  ```json
  {
  "username": "your-username",
  "password": "your-password"
  }
  ```

- Renovar Token JWT: /api/token/refresh/

  - Método: POST
  - Payload:
  ```json
  {
  "refresh": "your-refresh-token"
  }
  ```

### Weather Endpoints

Todos os endpoints de Weather requerem autenticação.

- Obter Todos os Dados Meteorológicos: /

  - Método: GET

- Gerar Dados Meteorológicos Aleatórios: `/generate/`

  - Método: GET

- Inserir Dados Meteorológicos: /insert/

  - Método: POST
  - Payload:
  ```json
  {
    "temperature": 25,
    "date": "2023-06-12T14:30:00Z",
    "atmospheric_pressure": 1012,
    "humidity": 60,
    "city": "São Paulo",
    "weather": "Ensolarado"
  }
  ```

- Limpar Banco de Dados: `/clear/`

  - Método: GET

- Editar Dados Meteorológicos: /edit/`<str:id>/`

  - Método: POST
  - Payload:
  ```json
  {
    "temperature": 28,
    "date": "2023-06-12T14:30:00Z",
    "atmospheric_pressure": 1005,
    "humidity": 65,
    "city": "Rio de Janeiro",
    "weather": "Nublado"
  }
  ```

- Remover Dados Meteorológicos: `/remove/<str:id>/`

  - Método: GET

### Testando a API

Você pode testar a API utilizando ferramentas como Postman ou curl. Certifique-se de incluir o token JWT no cabeçalho de autorização para endpoints que requerem autenticação.

#### Exemplo de Requisição com Curl
```bash
# Obter token JWT
curl -X POST http://localhost:8000/api/token/ -d '{"username": "your-username", "password": "your-password"}' -H "Content-Type: application/json"

# Usar token JWT para acessar endpoint protegido
curl -X GET http://localhost:8000/ -H "Authorization: Bearer your-access-token"
```

### Conexão com MongoDB
A conexão com o MongoDB é gerenciada pela classe `WeatherRepository` que utiliza a biblioteca `PyMongo` para realizar operações CRUD no banco de dados. Certifique-se de que o MongoDB esteja rodando e que a string de conexão esteja configurada corretamente no arquivo de configurações do Django.

### Licença
Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo LICENSE para mais detalhes.




