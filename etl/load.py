import mysql.connector
import simplejson as json
import sys
import re

unique_companies = sys.argv[1]

config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "dbWebRH-Dev"
}

try:
    # Conectar ao MySQL
    conn = mysql.connector.connect(**config)

    # Check if connection is successful
    if conn.is_connected():
        print("Connected to MySQL successfully!")

    cursor = conn.cursor()

    # Crie a tabela se ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            status BOOLEAN DEFAULT FALSE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
   
    companies_list = re.findall(r"'(.*?)'", unique_companies)

    # Convert to JSON
    companies_json = json.dumps(companies_list, ensure_ascii=False, indent=2)
    companies_list = json.loads(companies_json)

    # print(companies_json)

    # for company in companies_list:
    #     print(company)

    # Inserir empresas
    for company in companies_list:
        try:
            cursor.execute("INSERT IGNORE INTO companies (name) VALUES (%s)", (company,))
            print(company)
        except Exception as e:
            print(f"Erro ao inserir '{company}': {e}")

    # Salvar alterações
    conn.commit()
    print("Empresas inseridas com sucesso!")

except mysql.connector.Error as err:
    print(f"Erro de conexão ou execução: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
