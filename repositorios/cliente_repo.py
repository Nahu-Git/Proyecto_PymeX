from modelos.cliente import Cliente
from repositorios.base import BaseRepositorio
from db.connection import db


class ClienteRepositorio(BaseRepositorio[Cliente]):
    def crear(self, cliente: Cliente) -> Cliente:
        """
        Inserta un nuevo cliente.
        """
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO clientes (nombre, rut, email, telefono)
                VALUES (?, ?, ?, ?)
                """,
                (cliente.nombre, cliente.rut, cliente.email, cliente.telefono),
            )
            cliente.id = cur.lastrowid
        return cliente

    def obtener_por_id(self, cliente_id: int) -> Cliente | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, rut, email, telefono
                FROM clientes
                WHERE id = ?
                """,
                (cliente_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[Cliente]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, rut, email, telefono
                FROM clientes
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, cliente: Cliente) -> Cliente:
        if cliente.id is None:
            raise ValueError("No se puede actualizar un cliente sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE clientes
                SET nombre = ?, rut = ?, email = ?, telefono = ?
                WHERE id = ?
                """,
                (cliente.nombre, cliente.rut, cliente.email, cliente.telefono, cliente.id),
            )
        return cliente

    def eliminar(self, cliente_id: int) -> None:

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM clientes
                WHERE id = ?
                """,
                (cliente_id,),
            )

    def _row_to_entity(self, row) -> Cliente:
        return Cliente(
            id=row[0],
            nombre=row[1],
            rut=row[2],
            email=row[3],
            telefono=row[4],
        )
