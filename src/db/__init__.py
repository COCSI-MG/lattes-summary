#!/usr/bin/env python
# encoding: utf-8

"""
Módulo de gerenciamento de banco de dados SQLite3 para o sistema Lattes.
"""

from .connect import connect, get_db_path

__all__ = ['connect', 'get_db_path']

