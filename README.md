# API restaurante

Fase 1: exploración del dominio de pedidos de un restaurante. La API devuelve
datos de ejemplo en memoria; todavía no consulta ni modifica la base de datos
MySQL.

## Requisitos e instalación

Se recomienda Python 3.10 o superior.

```powershell
cd "C:\VSCode\API restaurante"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

La carpeta `.venv` y el archivo `.env` son locales y están excluidos de Git.
Para preparar la futura configuración de MySQL, copia `.env.example` a `.env`
y completa allí los valores proporcionados para el entorno local. No guardes
credenciales en el código ni las compartas.

## Ejecución

Desde la carpeta raíz del proyecto (`C:\VSCode\API restaurante`), con el
entorno virtual activado:

```powershell
python -m uvicorn app.main:app --reload
```

No ejecutes `app\main.py` directamente: la aplicación forma parte del paquete
`app` y necesita iniciarse desde la raíz del proyecto como módulo.

La API estará disponible en `http://127.0.0.1:8000`. La documentación
interactiva se encuentra en `http://127.0.0.1:8000/docs`.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/health` | Confirma que la API está activa. |
| GET | `/categories` | Devuelve las categorías de ejemplo. |
| GET | `/tables` | Devuelve las mesas de ejemplo. |
| GET | `/categories/{category_id}/products` | Devuelve los productos de una categoría. |

Los identificadores de categoría deben ser enteros positivos. Un identificador
con formato incorrecto devuelve HTTP 422; una categoría inexistente devuelve
HTTP 404. Los errores de validación incluyen un mensaje en español.

## Datos de prueba

- Categorías: Entrantes (1), Principales (2), Postres (3).
- Mesa disponible para esta fase: Mesa 2 (id 2).
- Productos por categoría: Entrantes incluye Ensaladilla y Croquetas;
  Principales incluye Paella; Postres incluye Flan.

## Estructura

```text
app/
  dao/              Acceso a los datos de ejemplo en memoria
  models/           Modelos de las entidades del dominio
  utils/            Configuración de entorno y conexión MySQL
  main.py           Aplicación FastAPI y rutas
.env.example        Nombres de variables, sin credenciales
.gitignore
requirements.txt
```

`DatabaseConnection` prepara la apertura y el cierre de una conexión MySQL
usando variables de entorno. En esta fase no se invoca desde las rutas: los
endpoints utilizan los DAO con datos de ejemplo.
