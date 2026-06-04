📋 Task Tracker Clean API - Producto Académico N° 1

Este repositorio contiene la aplicación funcional desarrollada para la asignatura de Construcción de Software en la Universidad Continental. Se trata de una API REST robusta diseñada para la gestión ágil de tareas diarias, construida bajo el enfoque híbrido de desarrollo acelerado con Inteligencia Artificial y supervisión de ingeniería humana.

👤 Autor

Hanter Paucar Matos (Desarrollador Individual)

Curso: Construcción de Software

Institución: Universidad Continental (UC)

🛠️ Tecnologías Utilizadas

Python 3.10+

FastAPI (Framework moderno de alto rendimiento)

Pydantic v2 (Validación estricta de esquemas de datos)

Uvicorn (Servidor ASGI de alto rendimiento)

🚀 Instrucciones de Instalación y Ejecución

Sigue estos sencillos pasos para levantar y probar la API de forma local en tu computadora:

1. Clonar el Repositorio

git clone https://github.com/HanterPaucar/PA1_Desarrollo_IA.git
cd PA1_Desarrollo_IA


2. Configurar el Entorno Virtual (Opcional pero recomendado)

python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate


3. Instalar Dependencias

pip install -r requirements.txt


4. Iniciar el Servidor de Desarrollo

uvicorn app:app --reload


Una vez levantado, la consola indicará que la aplicación se encuentra corriendo en:

👉 http://127.0.0.1:8000

📖 Documentación Interactiva (Swagger)

FastAPI genera automáticamente documentación detallada sobre los endpoints de la API. Con el servidor corriendo, puedes acceder directamente a:

Swagger UI: http://127.0.0.1:8000/docs (Para probar interactivamente las peticiones)

ReDoc: http://127.0.0.1:8000/redoc (Esquemas técnicos detallados)

📂 Estructura de Endpoints Disponibles

Método

Ruta

Descripción

HTTP Status

POST

/tasks

Registra una tarea con validación estricta de negocio.

201 Created

GET

/tasks

Obtiene el listado de tareas almacenadas en memoria.

200 OK

GET

/tasks/{task_id}

Obtiene una tarea en base a su UUID único.

200 OK / 404 Not Found

PUT

/tasks/{task_id}

Actualiza el estado o atributos de una tarea.

200 OK / 404 Not Found

DELETE

/tasks/{task_id}

Elimina físicamente una tarea del diccionario.

204 No Content / 404 Not Found

🛡️ Robustez y Control de Errores Implementado

La aplicación implementa un sistema defensivo avanzado para interceptar excepciones críticas del negocio sin interrumpir la operatividad del servidor:

Ocultación de Trazas (Tracebacks): Evita la filtración de código interno en caso de errores inesperados enviando respuestas estructuradas limpias.

Manejo Global Interceptor: Un decorador centralizado captura las excepciones customizadas de negocio (TaskAppException) y responde con formatos de API estandarizados y los respectivos códigos de estado HTTP correctos.

Validación de Frontera: El esquema de Pydantic bloquea textos inválidos o payloads masivos no admitidos por el dominio del software.
