# Banking System

Sistema bancario desarrollado con Django para la gestión de cuentas, clientes, movimientos bancarios y operaciones financieras.

## Características

- **Gestión de Clientes**: Registro y administración de clientes (personas naturales y jurídicas)
- **Gestión de Cuentas**: Manejo de cuentas de ahorro, corrientes y a plazo fijo
- **Operaciones Bancarias**: Depósitos, retiros, transferencias
- **Cuentas a Plazo**: Cancelación y renovación de cuentas a plazo
- **Portal de Clientes**: Interfaz dedicada para que los clientes gestionen sus cuentas
- **Portal de Administración**: Panel de control para empleados y administradores
- **Movimientos Bancarios**: Historial detallado de todas las transacciones
- **Tipos de Cambio**: Gestión de tasas de cambio
- **Embargos Judiciales**: Registro y control de retenciones judiciales

## Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/MateoTVara/banking-sys.git
cd bankingsys
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

#### Crear el esquema en MySQL

```sql
CREATE SCHEMA bankingdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Crear archivo `.env`

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

#### Crear archivo `my.ini`

Crear un archivo `my.ini` en la raíz del proyecto con la siguiente estructura:

```ini
[client]
database = bankingdb
user = tu_usuario_mysql
password = tu_contraseña_mysql
host = localhost
port = 3306
default-character-set = utf8mb4
```

**Nota**: Completar los campos `user` y `password` con tus credenciales de MySQL.

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Cargar datos de prueba

Ejecutar el script SQL `placeholderDataBankingsys.sql` en tu base de datos MySQL para cargar datos de prueba.

```bash
mysql -u tu_usuario -p bankingdb < placeholderDataBankingsys.sql
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

El sistema estará disponible en: `http://127.0.0.1:8000`

## Credenciales de Acceso

### Administradores
- **Usuario**: `admin` | **Contraseña**: `admin`

### Empleados
- **Usuario**: `empleado` | **Contraseña**: `empleado`

### Clientes
- **Usuario**: `cliente` | **Contraseña**: `client`
- **Usuario**: `juanp` | **Contraseña**: `juanp`
- **Usuario**: `inversionessac` | **Contraseña**: `inversionessac`
- **Usuario**: `marial` | **Contraseña**: `marial`
- **Usuario**: `serviciosglobales` | **Contraseña**: `serviciosglobales`
- **Usuario**: `carlosg` | **Contraseña**: `carlosg`
- **Usuario**: `constructoranorte` | **Contraseña**: `constructoranorte`

## Estructura del Proyecto

```
bankingsys/
├── bankingsys/          # Aplicación principal
│   ├── models/          # Modelos de datos
│   ├── views/           # Vistas y controladores
│   ├── templates/       # Plantillas HTML
│   └── migrations/      # Migraciones de base de datos
├── core/                # Configuración del proyecto
├── static/              # Archivos estáticos (CSS, JS)
├── docs/                # Documentación
└── manage.py            # Script de gestión de Django
```

## Uso

### Portal de Administración
Acceder a `http://localhost:8000/management/` para el panel de administración y gestión de empleados.

### Portal de Clientes
Acceder a `http://localhost:8000/portal/` para el portal de clientes donde pueden:
- Ver sus cuentas y saldos
- Realizar depósitos y retiros
- Hacer transferencias
- Abrir y cerrar cuentas
- Ver historial de movimientos
- Gestionar cuentas a plazo

## Tecnologías Utilizadas

- **Backend**: Django 4.x
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js

## Contribuidores

- MateoTVara
- JEFFRYHERRERA25
- Geancrack13

## Licencia

Este proyecto es de uso académico.
