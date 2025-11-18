#!/usr/bin/env python
# encoding: utf-8

import sqlite3
import os


def get_db_path() -> str:
    """
    Retorna o caminho padrão do banco de dados.
    
    Returns:
        Caminho absoluto para o arquivo do banco de dados
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "lattes_db.sqlite3"
    )


def connect(db_path: str = None) -> sqlite3.Connection:
    """
    Cria uma conexão com o banco de dados SQLite3.
    
    Args:
        db_path: Caminho para o arquivo do banco de dados.
                 Se None, usa o caminho padrão.
        
    Returns:
        Conexão com o banco de dados
        
    Raises:
        sqlite3.Error: Se houver erro ao conectar
    """
    if db_path is None:
        db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Erro ao conectar ao banco de dados: {e}")

