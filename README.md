# API restaurante

Fase 2: recorrido de solo lectura de la carta del restaurante usando la base de
datos MySQL existente. La única mesa visible para la aplicación es **Mesa 02**
(ID `1093`). Esta fase no crea, corrige ni elimina datos.

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
| GET | `/tables` | Devuelve únicamente Mesa 02. |
| GET | `/categories` | Devuelve las categorías de la carta. |
| GET | `/categories/{category_id}/products` | Devuelve los productos de una categoría. |
| GET | `/products/{product_id}/presentations` | Devuelve solo las presentaciones activas del producto. |
| GET | `/products/{product_id}` | Devuelve los datos del producto. |

Los identificadores deben ser enteros positivos. Un identificador con formato
incorrecto devuelve HTTP 422; una categoría o producto inexistente devuelve
HTTP 404. Si MySQL no está disponible, la API devuelve HTTP 503. Los errores
de validación incluyen un mensaje en español.

## Recorrido de carta y esquema MySQL

La carta se obtiene de las tablas existentes `categorias`, `carta` y
`presentaciones`. Las columnas `unidad`, `tapa`, `media` y `racion` de `carta`
determinan qué presentaciones se ofrecen para cada producto. Las consultas
excluyen cualquier mesa distinta de `Mesa 02`. Los nombres de las columnas y
tablas se adaptan al esquema real de MySQL.

Para probar el recorrido, abre `/docs`, consulta las categorías, elige un
`category_id`, después un `product_id` y consulta sus presentaciones activas.

## Estructura

```text
app/
  dao/              Consultas de lectura a MySQL
  models/           Modelos de las entidades del dominio
  utils/            Configuración de entorno y conexión MySQL
  main.py           Aplicación FastAPI y rutas
.env.example        Nombres de variables, sin credenciales
.gitignore
requirements.txt
```

`DatabaseConnection` prepara la apertura y el cierre de una conexión MySQL
usando variables de entorno. Los DAO ejecutan consultas de lectura y los
modelos Pydantic validan las respuestas de la API.
