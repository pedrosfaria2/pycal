import sqlalchemy

# Substitua pelo URL do seu banco de dados
DATABASE_URL = "mysql://user@localhost/dbname"

# Crie um engine para conectar ao banco de dados
engine = sqlalchemy.create_engine(DATABASE_URL)

# Teste a conexão
try:
    with engine.connect() as connection:
        print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
