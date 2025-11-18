#!/usr/bin/env python
# encoding: utf-8
import os
import sys
from create import create_database, create_tables
from connect import get_db_path


def delete_database(db_path: str) -> bool:
    """
    Deleta o arquivo do banco de dados se existir.
    
    Args:
        db_path: Caminho para o arquivo do banco de dados
        
    Returns:
        True se o banco foi deletado, False se não existia
    """
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✓ Banco de dados deletado: {db_path}")
            return True
        else:
            print(f"⚠ Banco de dados não existe: {db_path}")
            return False
    except OSError as e:
        print(f"✗ Erro ao deletar banco de dados: {e}")
        raise


def main():
    print("=" * 60)
    print("Recriando banco de dados Lattes")
    print("=" * 60)
    
    db_path = get_db_path()
    
    print(f"\nCaminho do banco: {db_path}\n")
    
    print("⚠️  ATENÇÃO: Esta ação irá DELETAR o banco de dados existente!")
    print("⚠️  Todos os dados serão perdidos e o banco será recriado do zero.\n")
    
    resposta = input("Deseja continuar? (s/N): ").strip().lower()
    
    if resposta not in ('s', 'sim', 'y', 'yes'):
        print("\n✗ Operação cancelada pelo usuário")
        sys.exit(0)
    
    print()
    
    conn = None
    try:
        delete_database(db_path)
        conn = create_database(db_path)
        create_tables(conn)
        
        print("\n" + "=" * 60)
        print("✓ Banco de dados recriado com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Erro durante a recriação: {e}")
        print("=" * 60)
        sys.exit(1)
        
    finally:
        if conn:
            conn.close()
            print("\n✓ Conexão com o banco de dados fechada")


if __name__ == "__main__":
    main()

