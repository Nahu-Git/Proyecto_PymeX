from typing import Optional
from modelos.usuario import Usuario, RolUsuario
from repositorios.base import BaseRepositorio
from db.connection import db


class UsuarioRepositorio(BaseRepositorio[Usuario]):
    def crear(self, usuario: Usuario) -> Usuario:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO usuarios (username, password_hash, rol)
                VALUES (?, ?, ?)
                """,
                (usuario.username, usuario.password_hash, usuario.rol.value),
            )
            usuario.id = cur.lastrowid
        return usuario

    def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, username, password_hash, rol
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def obtener_por_username(self, username: str) -> Usuario | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, username, password_hash, rol
                FROM usuarios
                WHERE username = ?
                """,
                (username,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[Usuario]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, username, password_hash, rol
                FROM usuarios
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, usuario: Usuario) -> Usuario:
        if usuario.id is None:
            raise ValueError("No se puede actualizar un usuario sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE usuarios
                SET username = ?, password_hash = ?, rol = ?
                WHERE id = ?
                """,
                (
                    usuario.username,
                    usuario.password_hash,
                    usuario.rol.value,
                    usuario.id,
                ),
            )
        return usuario

    def eliminar(self, usuario_id: int) -> None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )

    # ---------- Helpers internos ----------

    def _row_to_entity(self, row) -> Usuario:
        """
        row = (id, username, password_hash, rol)
        """
        return Usuario(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            rol=RolUsuario(row[3]),
        )
