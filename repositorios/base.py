from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class RepositorioBase(ABC, Generic[T]):
    @abstractmethod
    def agregar(self, entidad: T) -> None:
        """Agrega una nueva entidad al repositorio."""
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, id: int) -> T:
        """Obtiene una entidad por su ID."""
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, entidad: T) -> None:
        """Actualiza una entidad existente en el repositorio."""
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, id: int) -> None:
        """Elimina una entidad del repositorio por su ID."""
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> list[T]:
        """Lista todas las entidades en el repositorio."""
        raise NotImplementedError