import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("puntuaciones.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS puntuaciones (nombre TEXT, puntuacion INTEGER)''')

# Cerrar la conexión
conn.close()
