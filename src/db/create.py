#!/usr/bin/env python
# encoding: utf-8
import sqlite3
import os
from connect import connect, get_db_path


def create_database(db_path: str = "lattes_db.sqlite3") -> sqlite3.Connection:
    """
    Cria ou conecta ao banco de dados SQLite3.
    
    Args:
        db_path: Caminho para o arquivo do banco de dados
        
    Returns:
        Conexão com o banco de dados
    """
    try:
        db_exists = os.path.exists(db_path)
        conn = connect(db_path)
        
        if db_exists:
            print(f"✓ Conectado ao banco de dados existente: {db_path}")
        else:
            print(f"✓ Banco de dados criado com sucesso: {db_path}")
        
        return conn
    except sqlite3.Error as e:
        print(f"✗ Erro ao criar/conectar ao banco de dados: {e}")
        raise


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Cria as tabelas necessárias no banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividade_ponto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atividade TEXT NOT NULL UNIQUE,
                pontos INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_atividade 
            ON atividade_ponto(atividade)
        """)
        
        conn.commit()
        print("✓ Tabela 'atividade_ponto' criada/verificada com sucesso")
        
        cursor.execute("SELECT COUNT(*) FROM atividade_ponto")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("⚠ Tabela vazia. Inserindo dados padrão...")
            insert_default_data(conn)
        else:
            print(f"✓ Tabela já contém {count} registro(s)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria_lattes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categoria 
            ON categoria_lattes(categoria)
        """)
        
        conn.commit()
        print("✓ Tabela 'categoria_lattes' criada/verificada com sucesso")
        
        cursor.execute("SELECT COUNT(*) FROM categoria_lattes")
        count_cat = cursor.fetchone()[0]
        
        if count_cat == 0:
            print("⚠ Tabela vazia. Inserindo categorias padrão...")
            insert_default_categoria_lattes(conn)
        else:
            print(f"✓ Tabela já contém {count_cat} categoria(s)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria_atividade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_id INTEGER NOT NULL,
                atividade_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categoria_lattes(id),
                FOREIGN KEY (atividade_id) REFERENCES atividade_ponto(id),
                UNIQUE(categoria_id, atividade_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categoria_id 
            ON categoria_atividade(categoria_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_atividade_id 
            ON categoria_atividade(atividade_id)
        """)
        
        conn.commit()
        print("✓ Tabela 'categoria_atividade' criada/verificada com sucesso")
        
        cursor.execute("SELECT COUNT(*) FROM categoria_atividade")
        count_rel = cursor.fetchone()[0]
        
        if count_rel == 0:
            print("⚠ Tabela vazia. Inserindo relações padrão...")
            insert_default_categoria_atividade(conn)
        else:
            print(f"✓ Tabela já contém {count_rel} relação(ões)")
            
    except sqlite3.Error as e:
        print(f"✗ Erro ao criar tabelas: {e}")
        raise


def insert_default_data(conn: sqlite3.Connection) -> None:
    """
    Insere dados padrão na tabela atividade_ponto.
    
    Args:
        conn: Conexão com o banco de dados
    """
    try:
        cursor = conn.cursor()
        default_data = [
            ('Periódicos Indexados', 10),
            ('Periódicos não indexados constantes na base Qualis', 4),
            ('Anais de Congressos', 2),
            ('Livros - Completo', 8),
            ('Livros - Organizado', 2),
            ('Livros - Capítulo', 2),
            ('Livros - Tradução', 2),
            ('Projeto de Pesquisa - Coordenador', 2),
            ('Projeto de Pesquisa - Participação', 1),
            ('Bolsa de Produtividade PQ ou DT', 2),
            ('Carta Patente', 8),
        ]
        
        cursor.executemany("""
            INSERT INTO atividade_ponto (atividade, pontos)
            VALUES (?, ?)
        """, default_data)
        
        conn.commit()
        print(f"✓ {len(default_data)} registros padrão inseridos com sucesso")
        
    except sqlite3.Error as e:
        print(f"✗ Erro ao inserir dados padrão: {e}")
        raise


def insert_default_categoria_lattes(conn: sqlite3.Connection) -> None:
    """
    Insere categorias padrão na tabela categoria_lattes.
    
    Args:
        conn: Conexão com o banco de dados
    """
    try:
        cursor = conn.cursor()
        categorias = [
            ('Artigos completos em periódicos',),
            ('Livros publicados',),
            ('Capítulos de livros',),
            ('Textos em jornais',),
            ('Trabalhos completos em congressos',),
            ('Resumos expandidos',),
            ('Resumos em congressos',),
            ('Artigos aceitos',),
            ('Apresentações de trabalho',),
            ('Outros tipos',),
            ('Software com registro',),
            ('Software sem registro',),
            ('Produtos tecnológicos',),
            ('Processos ou técnicas',),
            ('Trabalhos técnicos',),
            ('Outros tipos (técnicas)',),
            ('Entrevistas e comentários',),
            ('Total de produções artísticas',),
            ('Pós-doutorado (andamento)',),
            ('Doutorado (andamento)',),
            ('Mestrado (andamento)',),
            ('Especialização (andamento)',),
            ('TCC (andamento)',),
            ('Iniciação científica (andamento)',),
            ('Outros tipos (andamento)',),
            ('Pós-doutorado (concluída)',),
            ('Doutorado (concluída)',),
            ('Mestrado (concluída)',),
            ('Especialização (concluída)',),
            ('TCC (concluída)',),
            ('Iniciação científica (concluída)',),
            ('Outros tipos (concluída)',),
            ('Projetos de pesquisa',),
            ('Prêmios e títulos',),
            ('Participação em eventos',),
            ('Organização de eventos',),
        ]
        
        cursor.executemany("""
            INSERT INTO categoria_lattes (categoria)
            VALUES (?)
        """, categorias)
        
        conn.commit()
        print(f"✓ {len(categorias)} categorias inseridas com sucesso")
        
    except sqlite3.Error as e:
        print(f"✗ Erro ao inserir categorias padrão: {e}")
        raise


def insert_default_categoria_atividade(conn: sqlite3.Connection) -> None:
    """
    Insere relações padrão entre categorias e atividades.
    Ignora categorias que não têm atividade associada (None).
    
    Args:
        conn: Conexão com o banco de dados
    """
    try:
        cursor = conn.cursor()
        
        categoria_para_atividade = {
            'Artigos completos em periódicos': 'Periódicos Indexados',
            'Livros publicados': 'Livros - Completo',
            'Capítulos de livros': 'Livros - Capítulo',
            'Textos em jornais': 'Periódicos Indexados',
            'Trabalhos completos em congressos': 'Anais de Congressos',
            'Resumos expandidos': 'Anais de Congressos',
            'Resumos em congressos': 'Anais de Congressos',
            'Software com registro': 'Carta Patente',
            'Projetos de pesquisa': 'Projeto de Pesquisa - Participação',
        }
        
        relacoes_inseridas = 0
        for categoria_nome, atividade_nome in categoria_para_atividade.items():
            cursor.execute("""
                SELECT c.id as categoria_id, a.id as atividade_id
                FROM categoria_lattes c, atividade_ponto a
                WHERE c.categoria = ? AND a.atividade = ?
            """, (categoria_nome, atividade_nome))
            
            resultado = cursor.fetchone()
            if resultado:
                categoria_id = resultado[0]
                atividade_id = resultado[1]
                
                cursor.execute("""
                    INSERT INTO categoria_atividade (categoria_id, atividade_id)
                    VALUES (?, ?)
                """, (categoria_id, atividade_id))
                
                relacoes_inseridas += 1
        
        conn.commit()
        print(f"✓ {relacoes_inseridas} relações inseridas com sucesso")
        
    except sqlite3.Error as e:
        print(f"✗ Erro ao inserir relações padrão: {e}")
        raise


def main():
    print("Inicializando banco de dados Lattes")
    print("=" * 60)
    
    db_path = get_db_path()
    
    print(f"\nCaminho do banco: {db_path}\n")
    
    conn = None
    try:
        conn = create_database(db_path)
        create_tables(conn)
        
        print("✓ Banco de dados configurado com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Erro durante a configuração: {e}")
        print("=" * 60)
        
    finally:
        if conn:
            conn.close()
            print("\n✓ Conexão com o banco de dados fechada")


if __name__ == "__main__":
    main()

