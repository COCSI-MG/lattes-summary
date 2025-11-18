#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.connect import connect


class AtividadeService:
    def __init__(self, db_path: str = None):
        """
        Inicializa o serviço de atividades.
        
        Args:
            db_path: Caminho para o banco de dados. Se None, usa o caminho padrão.
        """
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtém uma conexão com o banco de dados.
        
        Returns:
            Conexão com o banco de dados SQLite3
            
        Raises:
            sqlite3.Error: Se houver erro ao conectar
        """
        return connect(self.db_path)
    
    def get_all_atividades(self) -> List[Dict[str, any]]:
        """
        Busca todas as atividades cadastradas no banco de dados.
        
        Returns:
            Lista de dicionários contendo id, atividade e pontos de cada atividade
            
        Example:
            [
                {'id': 1, 'atividade': 'Periódicos Indexados', 'pontos': 10},
                {'id': 2, 'atividade': 'Anais de Congressos', 'pontos': 2},
                ...
            ]
            
        Raises:
            sqlite3.Error: Se houver erro na consulta
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, atividade, pontos
                FROM atividade_ponto
                ORDER BY atividade
            """)
            
            rows = cursor.fetchall()
            atividades = []
            for row in rows:
                atividades.append({
                    'id': row['id'],
                    'atividade': row['atividade'],
                    'pontos': row['pontos']
                })
            
            return atividades
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar atividades: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_atividade(self, atividade_id: int, novos_pontos: int) -> bool:
        """
        Atualiza os pontos de uma atividade específica.
        
        Args:
            atividade_id: ID da atividade a ser atualizada
            novos_pontos: Novo valor de pontos para a atividade
            
        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
            
        Raises:
            sqlite3.Error: Se houver erro na atualização
            ValueError: Se o atividade_id não existir ou novos_pontos for negativo
        """
        if novos_pontos < 0:
            raise ValueError("Os pontos não podem ser negativos")
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM atividade_ponto WHERE id = ?
            """, (atividade_id,))
            
            if cursor.fetchone() is None:
                raise ValueError(f"Atividade com ID {atividade_id} não encontrada")
            
            cursor.execute("""
                UPDATE atividade_ponto
                SET pontos = ?
                WHERE id = ?
            """, (novos_pontos, atividade_id))
            
            conn.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"Erro ao atualizar atividade: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_atividade_by_id(self, atividade_id: int) -> Optional[Dict[str, any]]:
        """
        Busca uma atividade específica pelo ID.
        
        Args:
            atividade_id: ID da atividade
            
        Returns:
            Dicionário com os dados da atividade ou None se não encontrada
            
        Raises:
            sqlite3.Error: Se houver erro na consulta
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, atividade, pontos
                FROM atividade_ponto
                WHERE id = ?
            """, (atividade_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'atividade': row['atividade'],
                    'pontos': row['pontos']
                }
            
            return None
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar atividade: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_all_categoria_atividade(self) -> List[Dict[str, any]]:
        """
        Busca todas as relações entre categorias e atividades.
        
        Returns:
            Lista de dicionários contendo os dados da relação:
            [
                {
                    'id': 1,
                    'categoria_id': 1,
                    'categoria': 'Artigos completos em periódicos',
                    'atividade_id': 1,
                    'atividade': 'Periódicos Indexados',
                    'pontos': 10
                },
                ...
            ]
            
        Raises:
            sqlite3.Error: Se houver erro na consulta
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    ca.id,
                    ca.categoria_id,
                    c.categoria,
                    ca.atividade_id,
                    a.atividade,
                    a.pontos
                FROM categoria_atividade ca
                INNER JOIN categoria_lattes c ON ca.categoria_id = c.id
                INNER JOIN atividade_ponto a ON ca.atividade_id = a.id
                ORDER BY c.categoria
            """)
            
            rows = cursor.fetchall()
            relacoes = []
            for row in rows:
                relacoes.append({
                    'id': row['id'],
                    'categoria_id': row['categoria_id'],
                    'categoria': row['categoria'],
                    'atividade_id': row['atividade_id'],
                    'atividade': row['atividade'],
                    'pontos': row['pontos']
                })
            
            return relacoes
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar relações categoria-atividade: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_categoria_atividade(self, categoria_id: int, atividade_id: Optional[int]) -> bool:
        """
        Atualiza a relação entre uma categoria e uma atividade.
        Se atividade_id for None, remove a relação existente.
        Se já existir uma relação para a categoria, atualiza para a nova atividade.
        Caso contrário, cria uma nova relação.
        
        Args:
            categoria_id: ID da categoria
            atividade_id: ID da atividade (ou None para remover a relação)
            
        Returns:
            True se a operação foi bem-sucedida
            
        Raises:
            sqlite3.Error: Se houver erro na operação
            ValueError: Se categoria_id não existir ou atividade_id não existir (quando não None)
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM categoria_lattes WHERE id = ?
            """, (categoria_id,))
            
            if cursor.fetchone() is None:
                raise ValueError(f"Categoria com ID {categoria_id} não encontrada")
            
            if atividade_id is not None:
                cursor.execute("""
                    SELECT id FROM atividade_ponto WHERE id = ?
                """, (atividade_id,))
                
                if cursor.fetchone() is None:
                    raise ValueError(f"Atividade com ID {atividade_id} não encontrada")
            
            cursor.execute("""
                SELECT id FROM categoria_atividade WHERE categoria_id = ?
            """, (categoria_id,))
            
            relacao_existente = cursor.fetchone()
            
            if atividade_id is None:
                if relacao_existente:
                    cursor.execute("""
                        DELETE FROM categoria_atividade WHERE categoria_id = ?
                    """, (categoria_id,))
                    conn.commit()
                    return True
                else:
                    return True
            else:
                if relacao_existente:
                    cursor.execute("""
                        UPDATE categoria_atividade
                        SET atividade_id = ?
                        WHERE categoria_id = ?
                    """, (atividade_id, categoria_id))
                else:
                    cursor.execute("""
                        INSERT INTO categoria_atividade (categoria_id, atividade_id)
                        VALUES (?, ?)
                    """, (categoria_id, atividade_id))
                
                conn.commit()
                return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"Erro ao atualizar relação categoria-atividade: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_categoria_atividade_by_categoria_id(self, categoria_id: int) -> Optional[Dict[str, any]]:
        """
        Busca a relação de uma categoria específica com sua atividade.
        
        Args:
            categoria_id: ID da categoria
            
        Returns:
            Dicionário com os dados da relação ou None se não houver relação
            {
                'id': 1,
                'categoria_id': 1,
                'categoria': 'Artigos completos em periódicos',
                'atividade_id': 1,
                'atividade': 'Periódicos Indexados',
                'pontos': 10
            }
            
        Raises:
            sqlite3.Error: Se houver erro na consulta
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    ca.id,
                    ca.categoria_id,
                    c.categoria,
                    ca.atividade_id,
                    a.atividade,
                    a.pontos
                FROM categoria_atividade ca
                INNER JOIN categoria_lattes c ON ca.categoria_id = c.id
                INNER JOIN atividade_ponto a ON ca.atividade_id = a.id
                WHERE ca.categoria_id = ?
            """, (categoria_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'categoria_id': row['categoria_id'],
                    'categoria': row['categoria'],
                    'atividade_id': row['atividade_id'],
                    'atividade': row['atividade'],
                    'pontos': row['pontos']
                }
            
            return None
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar relação categoria-atividade: {e}")
        finally:
            if conn:
                conn.close()

