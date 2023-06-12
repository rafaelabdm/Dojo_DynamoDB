# DESAFIO - DOJO DYNAMODB

Integrar a API de "dicas de projetos" que vocês fizeram com o DynamoDB usando um emulador
de serviços da AWS chamado LocalStack que permite testarmos serviços localmente sem a 
necessidade de uma conta. Para rodar o LocalStack, usaremos Docker.

## Para isso precisaremos de:
- Docker
- Localstack (imagem)
- AWS CLI (local)
- Python (versão 3.9 para baixo)
- Biblioteca Boto3

## O que faremos?

Temos uma API que quando recebe um request devolve uma dica de projeto. O objetivo é guardar essas
dicas numa tabela no banco de dados. E fazer uma função que consulte essa tabela e devolva uma dica
aleatória!

- Como funciona o DynamoDB?
	o DynamoDB é um banco NoSQL (não relacional), ou seja, ele não funciona como os bancos de dados
	que tem várias tabelas que se relacionam e que podemos fazer esse tipo de busca: 
		```SELECT <attribute> FROM <table_name> WHERE <condition>```
	É um banco de dados em que temos uma grande tabela e apenas 2 chaves de busca. Primary key, chave
	primária e obrigatória na busca. E a Sort Key, chace secundária e opcional para filtrar melhor a busca.
	Juntas elas formam a Partition Key.

- Como desenvolver nossa tabela?
	Modelando um sistema:
	1. Comece com um ERD (Entity Relationship Diagram):
		- Toda dica tem quais atributos? E os atributos tem quais outros atributos?
			EXEMPLO: dica tem um projeto, um projeto tem uma fase e uma fase tem vários projetos...
		- Quais atributos realmente precisamos?
	2. Defina seu padrão de acesso:
		- Qual é o pradrão de acesso na nossa tabela?
			Escrever, em português mesmo quais as consultas serão feitas.
	3. Design da tabela:
		- Qual dos atributos deve ser a partition key?
		- Precisamos de uma sort key?


## Criando a Tabela:
- Primeiro Passo
	Rodar o LocalStack: `docker-compose up`;

- Segundo Passo
	Criar suas credenciais AWS (mesmo localmente elas precisam existir).
	Rode o comando: `aws configure` e dê nomes aos campos:

	EXEMPLO:
	```
		AWS Access Key ID: test 
		AWS Secret Access Key: test
		Default region name: us-east-1
		Default output format: json
	```

- Terceiro Passo
	Criar a tabela com comandos do AWS CLI. Como estamos usando o localstack, usaremos o `awslocal`
	na linha de comando, ele ja nos direciona para o endpoint do localstack invés da aws;

	Exemplo caso nossa tabela chamasse Dicas
	```
	awslocal dynamodb create-table \
	--table-name Dicas \
	--attribute-definitions \
	AttributeName=Id,AttributeType=N \
	--key-schema \
	AttributeName=Id,KeyType=HASH \
	--provisioned-throughput \
	ReadCapacityUnits=5,WriteCapacityUnits=5
	```

- Quarto Passo
	Checar se a tabela foi criada com o comando: `awslocal dynamodb list-tables`

- Quinto Passo
	Adicionar um item com o comando:

	```
	awslocal dynamodb put-item \
	--table-name Dicas  \
	--item \
	'{"Id": {"N": "1"}, "Projeto": {"S": "Minishell"}, "Dica": {"S": "Cuidado com o Waitpid! Sempre teste <cat | cat | ls> e compare com o Bash original :D"}}'
	```

- Sexto Passo
	Checar estado da tabela. Com o comando `scan`, conseguimos ver toda a tabela:
	`awslocal dynamodb scan --table-name Dicas`
