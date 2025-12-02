from datetime import date, datetime
from modelos.indicadores import IndicadorEconomico, ConsultaIndicador
from repositorios.base import BaseRepositorio
from db.connection import db


class IndicadoresRepositorio(BaseRepositorio[IndicadorEconomico]):
    # ---------- CRUD básico sobre IndicadorEconomico ----------

    def crear(self, indicador: IndicadorEconomico) -> IndicadorEconomico:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO indicadores (nombre, fecha_valor, valor)
                VALUES (?, ?, ?)
                """,
                (
                    indicador.nombre,
                    indicador.fecha_valor.isoformat(),
                    indicador.valor,
                ),
            )
            indicador.id = cur.lastrowid
        return indicador

    def obtener_por_id(self, indicador_id: int) -> IndicadorEconomico | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, fecha_valor, valor
                FROM indicadores
                WHERE id = ?
                """,
                (indicador_id,),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    def listar(self) -> list[IndicadorEconomico]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, fecha_valor, valor
                FROM indicadores
                """
            )
            rows = cur.fetchall()

        return [self._row_to_entity(r) for r in rows]

    def actualizar(self, indicador: IndicadorEconomico) -> IndicadorEconomico:
        if indicador.id is None:
            raise ValueError("No se puede actualizar un indicador sin id")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE indicadores
                SET nombre = ?, fecha_valor = ?, valor = ?
                WHERE id = ?
                """,
                (
                    indicador.nombre,
                    indicador.fecha_valor.isoformat(),
                    indicador.valor,
                    indicador.id,
                ),
            )
        return indicador

    def eliminar(self, indicador_id: int) -> None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM indicadores
                WHERE id = ?
                """,
                (indicador_id,),
            )

    # ---------- Métodos específicos de indicadores ----------

    def obtener_por_nombre_y_fecha(
        self, nombre: str, fecha: date
    ) -> IndicadorEconomico | None:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nombre, fecha_valor, valor
                FROM indicadores
                WHERE nombre = ? AND fecha_valor = ?
                """,
                (nombre.upper(), fecha.isoformat()),
            )
            row = cur.fetchone()

        return self._row_to_entity(row) if row else None

    # ---------- Manejo de consultas de indicadores ----------

    def registrar_consulta(self, consulta: ConsultaIndicador) -> ConsultaIndicador:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO consultas_indicadores
                (indicador_id, usuario_id, fecha_consulta, fuente)
                VALUES (?, ?, ?, ?)
                """,
                (
                    consulta.indicador_id,
                    consulta.usuario_id,
                    consulta.fecha_consulta.isoformat(),
                    consulta.fuente,
                ),
            )
            consulta.id = cur.lastrowid
        return consulta

    def listar_consultas_por_usuario(self, usuario_id: int) -> list[ConsultaIndicador]:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, indicador_id, usuario_id, fecha_consulta, fuente
                FROM consultas_indicadores
                WHERE usuario_id = ?
                """,
                (usuario_id,),
            )
            rows = cur.fetchall()

        return [self._row_to_consulta(r) for r in rows]

    # ---------- Helpers internos ----------

    def _row_to_entity(self, row) -> IndicadorEconomico:
        return IndicadorEconomico(
            id=row[0],
            nombre=row[1],
            fecha_valor=date.fromisoformat(row[2]),
            valor=row[3],
        )

    def _row_to_consulta(self, row) -> ConsultaIndicador:
        return ConsultaIndicador(
            id=row[0],
            indicador_id=row[1],
            usuario_id=row[2],
            fecha_consulta=datetime.fromisoformat(row[3]),
            fuente=row[4],
        )
