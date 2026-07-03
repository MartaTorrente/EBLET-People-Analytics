import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# CONFIGURACIÓN DE LA CONEXIÓN
# ==========================================
# Cambia 'root' y 'tu_password' por tu usuario y contraseña de MySQL
usuario = 'root'
password = 'Chopan'
host = 'localhost'
database = 'eblet_db'

# Creamos el motor de conexión
engine = create_engine(f'mysql+pymysql://{usuario}:{password}@{host}/{database}?charset=utf8mb4')

print("🔌 Conectado a MySQL. Iniciando carga de datos...")

# ==========================================
# CARGA DE DATOS
# ==========================================
try:
    # 1. Cargar Empresas
    df_empresas = pd.read_csv('empresas.csv')
    df_empresas.to_sql('empresas', con=engine, if_exists='append', index=False)
    print(f"✅ Empresas cargadas: {len(df_empresas)} registros.")

    # 2. Cargar Empleados
    df_empleados = pd.read_csv('empleados.csv')
    df_empleados.to_sql('empleados', con=engine, if_exists='append', index=False)
    print(f"✅ Empleados cargados: {len(df_empleados)} registros.")

    # 3. Cargar Encuestas (Q1 a Q48)
    df_encuestas = pd.read_csv('encuestas.csv')
    df_encuestas.to_sql('encuestas', con=engine, if_exists='append', index=False)
    print(f"✅ Encuestas cargadas: {len(df_encuestas)} registros.")

    # 4. Cargar Scores
    df_scores = pd.read_csv('scores.csv')
    df_scores.to_sql('scores', con=engine, if_exists='append', index=False)
    print(f"✅ Scores cargados: {len(df_scores)} registros.")

    print("\n🎉 ¡Carga completada con éxito! Ya puedes consultar tus datos en MySQL.")

except Exception as e:
    print(f"❌ Error durante la carga: {e}")