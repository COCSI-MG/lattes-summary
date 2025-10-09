#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import tempfile
import warnings
import shutil
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning, module="scriptLattes")
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scriptLattes'))

from scriptLattes.grupo import Grupo
from scriptLattes.util import *
from .config import LattesConfig

class LattesDownloader:
    """
    Classe para baixar informações de currículos Lattes usando a biblioteca scriptLattes.
    """
    
    def __init__(self, output_dir="tmp", config_options=None):
        """
        Inicializa o downloader de currículos Lattes.
        
        Args:
            output_dir (str): Diretório onde serão salvos os HTMLs (padrão: "tmp")
            config_options (dict): Opções de configuração personalizadas (opcional)
        """
        print(f"Inicializando downloader de currículos Lattes")
        self.output_dir = output_dir
        self.temp_config = None
        self.temp_list = None
        self.config_options = config_options or {}
        
        if not os.path.exists(self.output_dir):
            print(f"Criando diretório de saída: {self.output_dir}")
            os.makedirs(self.output_dir)
    
    def _create_temp_files(self, ids_lattes):
        """
        Cria arquivos temporários de configuração e lista para o scriptLattes.
        
        Args:
            ids_lattes (list): Lista de IDs de currículos Lattes
        """
        print(f"\n[DEBUG] Criando arquivos temporários para o scriptLattes...")
        print(f"[DEBUG] Recebidos {len(ids_lattes)} ID(s): {ids_lattes}")
        
        ids_unicos = list(dict.fromkeys(ids_lattes))
        if len(ids_lattes) != len(ids_unicos):
            print(f"[AVISO] Detectadas {len(ids_lattes) - len(ids_unicos)} duplicata(s) de ID(s)!")
            print(f"[DEBUG] IDs únicos: {ids_unicos}")
            ids_lattes = ids_unicos
        
        temp_list_path = os.path.join(self.output_dir, 'curriculos.list')
        self.temp_list = open(temp_list_path, 'w')
        print(f"[DEBUG] Arquivo de lista temporário criado: {self.temp_list.name}")
        
        for i, id_lattes in enumerate(ids_lattes):
            linha = f"{id_lattes} , Pesquisador {i+1}\n"
            self.temp_list.write(linha)
            print(f"[DEBUG] Escrito: {linha.strip()}")
        
        self.temp_list.close()
        config = LattesConfig(**self.config_options)
        config_content = config.gerar_config_text(
            arquivo_entrada=self.temp_list.name,
            diretorio_saida=self.output_dir
        )
        temp_config_path = os.path.join(self.output_dir, 'config.config')
        self.temp_config = open(temp_config_path, 'w')
        self.temp_config.write(config_content)
        self.temp_config.close()
    
    def _cleanup_temp_files(self):
        """
        Remove apenas arquivos temporários de configuração (.config e .list).
        """
        if self.temp_config:
            config_path = self.temp_config.name if hasattr(self.temp_config, 'name') else self.temp_config
            if os.path.exists(config_path):
                os.unlink(config_path)
        if self.temp_list:
            list_path = self.temp_list.name if hasattr(self.temp_list, 'name') else self.temp_list
            if os.path.exists(list_path):
                os.unlink(list_path)
    
    def limpar_tudo(self):
        """
        Limpa TODO o conteúdo do diretório de saída, incluindo cache.
        Útil para começar do zero.
        
        Returns:
            dict: Resultado da operação de limpeza
        """
        print(f"\n[LIMPEZA COMPLETA] Removendo todo o conteúdo de: {self.output_dir}")
        
        if not os.path.exists(self.output_dir):
            return {
                'sucesso': True,
                'mensagem': 'Diretório não existe, nada para limpar.'
            }
        
        arquivos_removidos = 0
        diretorios_removidos = 0
        erros = []
        
        try:
            for item in os.listdir(self.output_dir):
                item_path = os.path.join(self.output_dir, item)
                
                if os.path.isfile(item_path):
                    try:
                        os.remove(item_path)
                        arquivos_removidos += 1
                        print(f"  ✓ Removido arquivo: {item}")
                    except Exception as e:
                        erros.append(f"Erro ao remover {item}: {str(e)}")
                        print(f"  ✗ Erro ao remover {item}: {str(e)}")
                
                elif os.path.isdir(item_path):
                    try:
                        shutil.rmtree(item_path)
                        diretorios_removidos += 1
                        print(f"  ✓ Removido diretório: {item}")
                    except Exception as e:
                        erros.append(f"Erro ao remover diretório {item}: {str(e)}")
                        print(f"  ✗ Erro ao remover diretório {item}: {str(e)}")
            
            mensagem = f"Limpeza concluída! Removidos {arquivos_removidos} arquivo(s) e {diretorios_removidos} diretório(s)."
            print(f"\n[LIMPEZA CONCLUÍDA] {mensagem}")
            
            return {
                'sucesso': True,
                'mensagem': mensagem,
                'arquivos_removidos': arquivos_removidos,
                'diretorios_removidos': diretorios_removidos,
                'erros': erros if erros else None
            }
            
        except Exception as e:
            erro_msg = f"Erro durante a limpeza: {str(e)}"
            print(f"\n[ERRO NA LIMPEZA] {erro_msg}")
            return {
                'sucesso': False,
                'mensagem': erro_msg,
                'erro': str(e)
            }
    
    def baixar_curriculos(self, ids_lattes):
        """
        Baixa informações de currículos Lattes e salva os HTMLs na pasta especificada.
        
        Args:
            ids_lattes (list): Lista de IDs de currículos Lattes para baixar
            
        Returns:
            dict: Informações sobre o processo de download
        """
        print(f"Baixando {len(ids_lattes)} currículos Lattes...")
        if not ids_lattes:
            raise ValueError("Lista de IDs de currículos Lattes não pode estar vazia")
        
        print(f"[LATTES DOWNLOADER INICIADO]")
        print(f"Baixando {len(ids_lattes)} currículos Lattes...")
        print(f"Diretório de saída: {os.path.abspath(self.output_dir)}")
        
        tempo_inicial = datetime.now()
        
        self._cleanup_temp_files()
        try:
            self._create_temp_files(ids_lattes)
            
            print("\n[EXECUTANDO SCRIPTLATTES]")
            grupo = Grupo(self.temp_config.name)
            print(f"Grupo criado com sucesso!")
            if criarDiretorio(grupo.obterParametro('global-diretorio_de_saida')):
                print("\n[1/4] Carregando dados dos CVs Lattes...")
                grupo.carregarDadosCVLattes()  # obrigatório
                
                print("\n[2/4] Compilando listas de itens...")
                grupo.compilarListasDeItems()  # obrigatório
                
                print("\n[3/4] Gerando grafos de colaborações...")
                grupo.gerarGrafosDeColaboracoes()  # obrigatório
                
                print("\n[4/4] Gerando páginas web...")
                grupo.gerarPaginasWeb()  # obrigatório
                
                print("\n[FINALIZANDO] Gerando arquivos temporários...")
                grupo.gerarArquivosTemporarios()  # obrigatório
                
                copiarArquivos(grupo.obterParametro('global-diretorio_de_saida'))
                
                print("\n[DOWNLOAD CONCLUÍDO]")
                print(f"Arquivos HTML salvos em: {os.path.abspath(self.output_dir)}")
                
                resultado = {
                    'sucesso': True,
                    'curriculos_processados': len(ids_lattes),
                    'diretorio_saida': os.path.abspath(self.output_dir),
                    'tempo_execucao': None,
                    'erro': None
                }
                
            else:
                raise Exception("Não foi possível criar o diretório de saída")
                
        except Exception as e:
            print(f"\n[ERRO] Falha no download: {str(e)}")
            resultado = {
                'sucesso': False,
                'curriculos_processados': 0,
                'diretorio_saida': None,
                'tempo_execucao': None,
                'erro': str(e)
            }
            
        finally:
            pass
        
        tempo_final = datetime.now()
        tempo_decorrido = tempo_final - tempo_inicial
        resultado['tempo_execucao'] = self._formatar_tempo_decorrido(tempo_decorrido)
        
        print(f"\nProcesso executado em: {resultado['tempo_execucao']}")
        
        return resultado
    
    def _formatar_tempo_decorrido(self, tempo_decorrido):
        """
        Formata o tempo decorrido em formato legível.
        
        Args:
            tempo_decorrido (datetime.timedelta): Tempo decorrido
            
        Returns:
            str: Tempo formatado
        """
        segundos = int(tempo_decorrido.total_seconds())
        
        if segundos < 60:
            return f"{segundos} segundos"
        elif segundos < 3600:
            minutos, segundos = divmod(segundos, 60)
            return f"{minutos} minutos e {segundos} segundos"
        else:
            horas, segundos = divmod(segundos, 3600)
            minutos, segundos = divmod(segundos, 60)
            return f"{horas} horas, {minutos} minutos e {segundos} segundos"