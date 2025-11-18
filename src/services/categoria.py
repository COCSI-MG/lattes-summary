#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.connect import connect


class CategoriaService:
    def __init__(self, db_path: str = None):
        """
        Inicializa o serviço de categorias.
        
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
    
    def get_all_categorias(self) -> List[Dict[str, any]]:
        """
        Busca todas as categorias cadastradas no banco de dados.
        
        Returns:
            Lista de dicionários contendo id e categoria de cada registro
            
        Example:
            [
                {'id': 1, 'categoria': 'Artigos completos em periódicos'},
                {'id': 2, 'categoria': 'Livros publicados'},
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
                SELECT id, categoria
                FROM categoria_lattes
                ORDER BY categoria
            """)
            
            rows = cursor.fetchall()
            categorias = []
            for row in rows:
                categorias.append({
                    'id': row['id'],
                    'categoria': row['categoria']
                })
            
            return categorias
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar categorias: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_categoria(self, categoria_id: int, novo_nome: str) -> bool:
        """
        Atualiza o nome de uma categoria específica.
        
        Args:
            categoria_id: ID da categoria a ser atualizada
            novo_nome: Novo nome para a categoria
            
        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
            
        Raises:
            sqlite3.Error: Se houver erro na atualização
            ValueError: Se o categoria_id não existir, novo_nome for vazio ou já existir
        """
        if not novo_nome or novo_nome.strip() == "":
            raise ValueError("O nome da categoria não pode ser vazio")
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM categoria_lattes WHERE id = ?
            """, (categoria_id,))
            
            if cursor.fetchone() is None:
                raise ValueError(f"Categoria com ID {categoria_id} não encontrada")
            
            cursor.execute("""
                SELECT id FROM categoria_lattes WHERE categoria = ? AND id != ?
            """, (novo_nome, categoria_id))
            
            if cursor.fetchone() is not None:
                raise ValueError(f"Já existe uma categoria com o nome '{novo_nome}'")
            
            cursor.execute("""
                UPDATE categoria_lattes
                SET categoria = ?
                WHERE id = ?
            """, (novo_nome, categoria_id))
            
            conn.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"Erro ao atualizar categoria: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_categoria_by_id(self, categoria_id: int) -> Optional[Dict[str, any]]:
        """
        Busca uma categoria específica pelo ID.
        
        Args:
            categoria_id: ID da categoria
            
        Returns:
            Dicionário com os dados da categoria ou None se não encontrada
            
        Raises:
            sqlite3.Error: Se houver erro na consulta
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, categoria
                FROM categoria_lattes
                WHERE id = ?
            """, (categoria_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'categoria': row['categoria']
                }
            
            return None
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Erro ao buscar categoria: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_categoria(self, nome_categoria: str) -> int:
        """
        Cria uma nova categoria no banco de dados.
        
        Args:
            nome_categoria: Nome da nova categoria
            
        Returns:
            ID da categoria criada
            
        Raises:
            sqlite3.Error: Se houver erro na inserção
            ValueError: Se o nome for vazio ou já existir
        """
        if not nome_categoria or nome_categoria.strip() == "":
            raise ValueError("O nome da categoria não pode ser vazio")
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM categoria_lattes WHERE categoria = ?
            """, (nome_categoria,))
            
            if cursor.fetchone() is not None:
                raise ValueError(f"Já existe uma categoria com o nome '{nome_categoria}'")
            
            cursor.execute("""
                INSERT INTO categoria_lattes (categoria)
                VALUES (?)
            """, (nome_categoria,))
            
            conn.commit()
            
            return cursor.lastrowid
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"Erro ao criar categoria: {e}")
        finally:
            if conn:
                conn.close()
    
    def delete_categoria(self, categoria_id: int) -> bool:
        """
        Remove uma categoria do banco de dados.
        
        Args:
            categoria_id: ID da categoria a ser removida
            
        Returns:
            True se a remoção foi bem-sucedida, False caso contrário
            
        Raises:
            sqlite3.Error: Se houver erro na remoção
            ValueError: Se o categoria_id não existir
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
            
            cursor.execute("""
                DELETE FROM categoria_lattes
                WHERE id = ?
            """, (categoria_id,))
            
            conn.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"Erro ao deletar categoria: {e}")
        finally:
            if conn:
                conn.close()

