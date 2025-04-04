# Oracle Database Setup with Docker

Este repositorio contiene la configuración necesaria para crear y configurar una base de datos Oracle utilizando Docker, así como instrucciones para conectarse a ella usando Python.

## Requisitos previos

- Docker instalado y configurado
- Python 3.x instalado
- Permisos para ejecutar comandos Docker

## Configuración del entorno Python

Primero, crea y activa un entorno virtual de Python:

```bash
# Instalar máquina virtual
python -m venv nombre-de-maquina

# Activar el entorno virtual
# En Windows:
nombre-de-maquina\Scripts\activate
# En macOS/Linux:
source nombre-de-maquina/bin/activate
```

Instala las dependencias necesarias:

```bash
# Librería de Oracle para Python
python -m pip install oracledb --upgrade

# Para cargar variables de entorno desde archivo .env
pip install python-dotenv
```

## Configuración de Oracle Database en Docker

### Paso 1: Descargar y ejecutar imagen Oracle Database

```bash
docker container run -d --name oracle-docker -p 1521:1521 -e ORACLE_PWD=12345 container-registry.oracle.com/database/express:21.3.0-xe
```

Este comando:
- Descarga la imagen de Oracle Database Express Edition 21.3.0
- Crea un contenedor llamado "oracle-docker"
- Mapea el puerto 1521 del contenedor al puerto 1521 de tu máquina local
- Configura la contraseña del sistema como "12345"

### Paso 2: Ingresar al editor SQL del contenedor Oracle Database

```bash
docker exec -it oracle-docker sqlplus system/12345@localhost:1521/XEPDB1
```

## Configuración de la base de datos

### Paso 3: Crear la tabla SYSTEM.CUSTOMER dentro del editor SQL

```sql
CREATE TABLE SYSTEM.CUSTOMER(
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dni CHAR(8),
    firstname VARCHAR2(100),
    lastname VARCHAR2(100),
    state CHAR(1)
);
```

### Paso 4: Insertar un registro en la tabla SYSTEM.CUSTOMER

```sql
INSERT INTO SYSTEM.CUSTOMER (dni, firstname, lastname, state) 
VALUES ('12345678', 'Juan', 'Perez', 'A');
```

### Paso 5: Configurar formato para visualización de datos

```sql
SET LINESIZE 200;
SET PAGESIZE 50;
COLUMN dni FORMAT A10;
COLUMN firstname FORMAT A20;
COLUMN lastname FORMAT A20;
COLUMN state FORMAT A5;
```

### Paso 6: Listar los registros de la tabla SYSTEM.CUSTOMER

```sql
SELECT * FROM SYSTEM.CUSTOMER;
```

### Paso 7: Salir del editor SQL

```sql
exit
```

## Conexión desde Python

Para conectarse a la base de datos desde Python, puede utilizar el siguiente ejemplo:

```python
import oracledb
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la conexión
username = os.getenv("DB_USER", "system")
password = os.getenv("DB_PASSWORD", "12345")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "1521")
service = os.getenv("DB_SERVICE", "XEPDB1")

# Establecer conexión
connection = oracledb.connect(
    user=username,
    password=password,
    dsn=f"{host}:{port}/{service}"
)

# Crear cursor
cursor = connection.cursor()

# Ejemplo de consulta
cursor.execute("SELECT * FROM SYSTEM.CUSTOMER")
for row in cursor:
    print(row)

# Cerrar conexión
cursor.close()
connection.close()
```

## Archivo .env de ejemplo

Cree un archivo llamado `.env` en la raíz de su proyecto con el siguiente contenido:

```
DB_USER=system
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=XEPDB1
```

## Notas importantes

- Por seguridad, no utilice la contraseña "12345" en entornos de producción
- La configuración actual utiliza el esquema SYSTEM, lo cual no es recomendable para entornos de producción
- Considere crear un usuario dedicado para la aplicación con permisos limitados

## Comandos Docker útiles

```bash
# Ver contenedores en ejecución
docker ps

# Detener el contenedor Oracle
docker stop oracle-docker

# Iniciar el contenedor Oracle
docker start oracle-docker

# Eliminar el contenedor Oracle
docker rm oracle-docker
```