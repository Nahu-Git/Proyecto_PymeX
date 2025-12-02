from datetime import date
from modelos.contrato import ContratoPlan
from repositorios.base import BaseRepositorio
from db.connection import db


class ContratoRepositorio(BaseRepositorio[ContratoPlan]):
    def crear(self, contrato: ContratoPlan) -> ContratoPlan:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO contratos (cliente_id, plan_id, fecha_inicio,
                                       fecha_fin, estado)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    contrato.cliente_id,
                    contrato.plan_id,
                    contrato.fecha_inicio.isoformat(),
                    contrato.fecha_fin.isoformat() if contrato.fecha_fin else None,
                    contrato.estado,
                ),
            )
            contrato.id = cur.lastrowid
        return contrato

    def obtener_por_id(self, contrato_id: int) -> ContratoPlan | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, cliente_id, plan_id, fecha_inicio, fecha_fin, estado
                FROM contratos
                WHERE id = ?
                """,
                (contrato_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[ContratoPlan]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, cliente_id, plan_id, fecha_inicio, fecha_fin, estado
                FROM contratos
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def listar_por_cliente(self, cliente_id: int) -> list[ContratoPlan]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, cliente_id, plan_id, fecha_inicio, fecha_fin, estado
                FROM contratos
                WHERE cliente_id = ?
                """,
                (cliente_id,),
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, contrato: ContratoPlan) -> ContratoPlan:
        if contrato.id is None:
            raise ValueError("No se puede actualizar un contrato sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE contratos
                SET cliente_id = ?, plan_id = ?, fecha_inicio = ?,
                    fecha_fin = ?, estado = ?
                WHERE id = ?
                """,
                (
                    contrato.cliente_id,
                    contrato.plan_id,
                    contrato.fecha_inicio.isoformat(),
                    contrato.fecha_fin.isoformat() if contrato.fecha_fin else None,
                    contrato.estado,
                    contrato.id,
                ),
            )
        return contrato

    def eliminar(self, contrato_id: int) -> None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM contratos
                WHERE id = ?
                """,
                (contrato_id,),
            )

    def _row_to_entity(self, row) -> ContratoPlan:
        return ContratoPlan(
            id=row[0],
            cliente_id=row[1],
            plan_id=row[2],
            fecha_inicio=date.fromisoformat(row[3]),
            fecha_fin=date.fromisoformat(row[4]) if row[4] else None,
            estado=row[5],
        )
