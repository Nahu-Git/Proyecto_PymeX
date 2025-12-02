from modelos.plan import Plan
from repositorios.base import BaseRepositorio
from db.connection import db


class PlanRepositorio(BaseRepositorio[Plan]):
    def crear(self, plan: Plan) -> Plan:
        """
        Inserta un nuevo plan en la tabla 'planes'.
        """
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO planes (empresa_id, nombre, bajada_mbps, subida_mbps,
                                    contencion, precio_clp, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    plan.empresa_id,
                    plan.nombre,
                    plan.bajada_mbps,
                    plan.subida_mbps,
                    plan.contencion,
                    plan.precio_clp,
                    plan.descripcion,
                ),
            )
            plan.id = cur.lastrowid
        return plan

    def obtener_por_id(self, plan_id: int) -> Plan | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, empresa_id, nombre, bajada_mbps, subida_mbps,
                       contencion, precio_clp, descripcion
                FROM planes
                WHERE id = ?
                """,
                (plan_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[Plan]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, empresa_id, nombre, bajada_mbps, subida_mbps,
                       contencion, precio_clp, descripcion
                FROM planes
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def listar_por_empresa(self, empresa_id: int) -> list[Plan]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, empresa_id, nombre, bajada_mbps, subida_mbps,
                       contencion, precio_clp, descripcion
                FROM planes
                WHERE empresa_id = ?
                """,
                (empresa_id,),
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, plan: Plan) -> Plan:
        if plan.id is None:
            raise ValueError("No se puede actualizar un plan sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE planes
                SET empresa_id = ?, nombre = ?, bajada_mbps = ?, subida_mbps = ?,
                    contencion = ?, precio_clp = ?, descripcion = ?
                WHERE id = ?
                """,
                (
                    plan.empresa_id,
                    plan.nombre,
                    plan.bajada_mbps,
                    plan.subida_mbps,
                    plan.contencion,
                    plan.precio_clp,
                    plan.descripcion,
                    plan.id,
                ),
            )
        return plan

    def eliminar(self, plan_id: int) -> None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM planes
                WHERE id = ?
                """,
                (plan_id,),
            )

    def _row_to_entity(self, row) -> Plan:
        return Plan(
            id=row[0],
            empresa_id=row[1],
            nombre=row[2],
            bajada_mbps=row[3],
            subida_mbps=row[4],
            contencion=row[5],
            precio_clp=row[6],
            descripcion=row[7] or "",
        )
