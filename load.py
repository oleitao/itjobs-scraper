import mysql.connector
import simplejson as json
import sys

unique_companies = sys.argv[1]
print("test")
print(unique_companies)



# try:
#     # Conectar ao MySQL
#     conn = mysql.connector.connect(**config)
#     cursor = conn.cursor()

#     # Crie a tabela se ainda não existir
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS companies (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) UNIQUE
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """)

#     # Inserir empresas
#     for company in unique_companies:
#         try:
#             cursor.execute("INSERT IGNORE INTO companies (name) VALUES (%s)", (company,))
#         except Exception as e:
#             print(f"Erro ao inserir '{company}': {e}")

#     # Salvar alterações
#     conn.commit()
#     print("Empresas inseridas com sucesso!")

# except mysql.connector.Error as err:
#     print(f"Erro de conexão ou execução: {err}")
# finally:
#     if 'cursor' in locals():
#         cursor.close()
#     if 'conn' in locals():
#         conn.close()
