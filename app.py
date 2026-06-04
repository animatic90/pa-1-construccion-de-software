"""
Task Tracker Clean API
Asignatura: Construcción de Software (Universidad Continental)
Desarrollador: Hanter Paucar Matos (Trabajo Autónomo)
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid

# =====================================================================
# 1. ARQUITECTURA DE EXCEPCIONES PERSONALIZADAS (Manejo de Errores)
# =====================================================================

class TaskAppException(Exception):
    """Clase base abstracta para capturar errores de negocio en la aplicación."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TaskNotFoundError(TaskAppException):
    """Excepción de dominio: Se gatilla si el ID solicitado no existe."""
    def __init__(self, task_id: str):
        super().__init__(
            message=f"Operación Inválida. La tarea con ID '{task_id}' no existe en el sistema.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class InvalidTaskDataError(TaskAppException):
    """Excepción de dominio: Se gatilla por violaciones de reglas de negocio en los datos."""
    def __init__(self, details: str):
        super().__init__(
            message=f"Inconsistencia en la información de entrada: {details}",
            status_code=status.HTTP_400_BAD_REQUEST
        )


# =====================================================================
# 2. MODELOS DE DOMINIO Y ESQUEMAS DE VALIDACIÓN (Pydantic / Clean Code)
# =====================================================================

class TaskSchema(BaseModel):
    """Esquema de datos autovalidante. Sigue el principio de robustez en las fronteras."""
    id: Optional[str] = Field(default=None, description="UUID único autogenerado por el backend")
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Título de la tarea. Debe tener entre 3 y 100 caracteres."
    )
    description: str = Field(
        ..., 
        max_length=500, 
        description="Descripción detallada de la meta u objetivo."
    )
    completed: bool = Field(
        default=False, 
        description="Estado lógico de realización."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Aprender Clean Code",
                "description": "Leer el capítulo 3 del libro de Robert C. Martin.",
                "completed": False
            }
        }


# =====================================================================
# 3. CONFIGURACIÓN DEL ENGINE / FastAPI
# =====================================================================

app = FastAPI(
    title="Task Tracker Clean API (Hanter Paucar)",
    description="Backend de alta robustez desarrollado con FastAPI, aplicando guías PEP 8 y SOLID.",
    version="1.1.0"
)

# Base de datos simulada en memoria (Diccionario Key-Value para búsquedas O(1))
DATABASE_TASKS: Dict[str, TaskSchema] = {}


# =====================================================================
# 4. CAPA DE INTERCEPTACIÓN GLOBAL (Manejador de Excepciones)
# =====================================================================

@app.exception_handler(TaskAppException)
async def custom_exception_handler(request: Request, exc: TaskAppException):
    """
    Handler Global: Intercepta excepciones controladas de la lógica de negocio
    y evita la exposición de trazas internas del servidor, devolviendo una respuesta limpia.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_type": exc.__class__.__name__,
            "message": exc.message,
            "status": "failure"
        }
    )


# =====================================================================
# 5. CONTROLADORES / ENDPOINTS (CRUD API)
# =====================================================================

@app.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskSchema):
    """Registra una nueva tarea validando restricciones de negocio."""
    # Validación explícita de negocio: Palabras reservadas prohibidas
    if "error" in task.title.lower() or "bug" in task.title.lower():
        raise InvalidTaskDataError("El título no puede contener términos de falla técnica directa.")
    
    task.id = str(uuid.uuid4())
    DATABASE_TASKS[task.id] = task
    return task


@app.get("/tasks", response_model=List[TaskSchema])
async def get_all_tasks():
    """Obtiene el listado completo de tareas registradas."""
    return list(DATABASE_TASKS.values())


@app.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task_by_id(task_id: str):
    """Busca una tarea específica por su identificador UUID."""
    if task_id not in DATABASE_TASKS:
        raise TaskNotFoundError(task_id)
    return DATABASE_TASKS[task_id]


@app.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, updated_task: TaskSchema):
    """Actualiza de forma segura todos los atributos de una tarea."""
    if task_id not in DATABASE_TASKS:
        raise TaskNotFoundError(task_id)
    
    updated_task.id = task_id
    DATABASE_TASKS[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """Elimina permanentemente una tarea del listado."""
    if task_id not in DATABASE_TASKS:
        raise TaskNotFoundError(task_id)
    del DATABASE_TASKS[task_id]
    return None
