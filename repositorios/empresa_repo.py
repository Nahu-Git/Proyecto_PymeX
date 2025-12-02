from modelos.empresa import Empresa
from repositorios.base import BaseRepositorio
from db.connection import db


class EmpresaRepositorio(BaseRepositorio[Empresa]):
    def crear(self, empresa: Empresa) -> Empresa:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO empresas (nombre, rut, email_contacto)
                VALUES (?, ?, ?)
                """,
                (empresa.nombre, empresa.rut, empresa.email_contacto),
            )
            empresa.id = cur.lastrowid
        return empresa

    def obtener_por_id(self, empresa_id: int) -> Empresa | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, rut, email_contacto
                FROM empresas
                WHERE id = ?
                """,
                (empresa_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[Empresa]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, rut, email_contacto
                FROM empresas
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, empresa: Empresa) -> Empresa:
        if empresa.id is None:
            raise ValueError("No se puede actualizar una empresa sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE empresas
                SET nombre = ?, rut = ?, email_contacto = ?
                WHERE id = ?
                """,
                (empresa.nombre, empresa.rut, empresa.email_contacto, empresa.id),
            )
        return empresa

    def eliminar(self, empresa_id: int) -> None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM empresas
                WHERE id = ?
                """,
                (empresa_id,),
            )

    # ---------- Helper interno ----------

    def _row_to_entity(self, row) -> Empresa:
        return Empresa(
            id=row[0],
            nombre=row[1],
            rut=row[2],
            email_contacto=row[3],
        )
