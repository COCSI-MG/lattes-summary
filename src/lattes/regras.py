#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import pandas as pd
from typing import List, Optional, Any
from scriptLattes.parserLattes import ParserLattes


class Regras:
    """
    Classe responsável por definir e aplicar regras de classificação
    de trabalhos acadêmicos em atividades específicas.
    
    Cada método de regra recebe um objeto Trabalho e retorna Optional[str]
    indicando a atividade determinada pela regra, ou None se a regra não se aplicar.
    """
    
    def __init__(self, cache_dir: str = None):
        """
        Args:
            cache_dir: Diretório onde estão os arquivos de cache do Lattes.
                      Necessário para regras que dependem de informações do cache.
        """
        self.cache_dir = cache_dir
        self._nomes_citacao_cache = {}
        self._qualis_issn_df = None
        self._carregar_issns_qualis()
    
    def _carregar_issns_qualis(self):
        """
        Carrega o arquivo Excel com os ISSNs da base Qualis em um DataFrame pandas.
        O DataFrame fica armazenado em self._qualis_issn_df para uso nas regras.
        """
        try:
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'template',
                'lista_issn_qualis.xlsx'
            )
            
            if os.path.exists(template_path):
                self._qualis_issn_df = pd.read_excel(template_path)
            else:
                print(f"Aviso: Arquivo de ISSNs Qualis não encontrado em {template_path}")
        except Exception as e:
            print(f"Erro ao carregar arquivo de ISSNs Qualis: {e}")
    
    def _get_field_value_from_outros(self, trabalho, keys: List[str], default=None) -> Any:
        """
        Busca o valor de um campo no dicionário 'outros' do trabalho usando múltiplas chaves.
        
        Args:
            trabalho: Objeto Trabalho
            keys: Lista de possíveis nomes de chaves a serem buscadas no dicionário 'outros'
            default: Valor padrão caso nenhuma chave seja encontrada
            
        Returns:
            Valor encontrado ou default
        """
        if not trabalho.outros:
            return default
            
        for key in keys:
            if key in trabalho.outros and trabalho.outros[key] not in (None, ''):
                return trabalho.outros[key]
        return default
    
    def _tem_doi(self, trabalho) -> bool:
        """
        Verifica se o trabalho possui DOI.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            True se o trabalho possui DOI, False caso contrário
        """
        return trabalho.doi is not None and str(trabalho.doi).strip() != ''
    
    def _tem_issn(self, trabalho) -> bool:
        """
        Verifica se o trabalho possui ISSN.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            True se o trabalho possui ISSN, False caso contrário
        """
        return trabalho.issn is not None and str(trabalho.issn).strip() != ''
    
    def _tem_isbn(self, trabalho) -> bool:
        """
        Verifica se o trabalho possui ISBN.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            True se o trabalho possui ISBN, False caso contrário
        """
        return trabalho.isbn is not None and str(trabalho.isbn).strip() != ''
    
    def _extrair_nomes_citacao_do_cache(self, id_lattes: str) -> List[str]:
        """
        Extrai os nomes em citações bibliográficas do arquivo de cache do Lattes.
        
        Este método utiliza o parser do scriptLattes para extrair os nomes
        em citações bibliográficas do currículo Lattes em HTML.
        
        Args:
            id_lattes: ID do Lattes do pesquisador (16 dígitos)
            
        Returns:
            Lista de nomes em citações bibliográficas, ou lista vazia se não encontrar
        """
        if id_lattes in self._nomes_citacao_cache:
            return self._nomes_citacao_cache[id_lattes]
        
        if not self.cache_dir:
            return []
        
        arquivo_cache = os.path.join(self.cache_dir, id_lattes)
        
        if not os.path.exists(arquivo_cache):
            self._nomes_citacao_cache[id_lattes] = []
            return []
        
        try:
            script_lattes_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'scriptLattes'
            )
            if script_lattes_path not in sys.path:
                sys.path.append(script_lattes_path)
            
            with open(arquivo_cache, 'r', encoding='utf-8') as f:
                html_content = f.read()
            parser = ParserLattes(id_lattes, html_content)
            nomes_citacao = parser.nomeEmCitacoesBibliograficas
            
            if nomes_citacao:
                nomes_lista = [nome.strip() for nome in nomes_citacao.split(';')]
                self._nomes_citacao_cache[id_lattes] = nomes_lista
                return nomes_lista
            
        except Exception as e:
            print(f"Erro ao extrair nomes de citação do cache {id_lattes}: {e}")
        
        self._nomes_citacao_cache[id_lattes] = []
        return []
    
    def _eh_primeiro_autor(self, trabalho, nomes_citacao: List[str]) -> bool:
        """
        Verifica se algum dos nomes em citações bibliográficas aparece como primeiro autor.
        
        Args:
            trabalho: Objeto Trabalho
            nomes_citacao: Lista de nomes em citações bibliográficas do pesquisador
            
        Returns:
            True se o pesquisador é o primeiro autor, False caso contrário
        """
        if not trabalho.autores or not nomes_citacao:
            return False
        
        autores_lista = trabalho.autores.split(';')
        if not autores_lista:
            return False
        
        primeiro_autor = autores_lista[0].strip()
        
        for nome in nomes_citacao:
            if nome in primeiro_autor or primeiro_autor in nome:
                return True
        
        return False
    
    # ==================== REGRAS DE CLASSIFICAÇÃO ====================
    
    def regra_artigos_aceitos_com_doi(self, trabalho) -> Optional[str]:
        """
        Regra: Artigos aceitos com DOI devem ser classificados como Periódicos Indexados.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Nome da atividade se a regra se aplicar, None caso contrário
        """
        if trabalho.categoria == 'Artigos aceitos' and self._tem_doi(trabalho):
            return 'Periódicos Indexados'
        
        return None
    
    def regra_artigos_completos_com_issn(self, trabalho) -> Optional[str]:
        """
        Regra: Artigos completos em periódicos com ISSN.
        - Se o ISSN está na base Qualis: retorna "Periódicos não indexados constantes na base Qualis"
        - Caso contrário: retorna "Periódicos Indexados"
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Nome da atividade se a regra se aplicar, None caso contrário
        """
        if trabalho.categoria == 'Artigos completos em periódicos' and self._tem_issn(trabalho):
            # Verifica se o ISSN está na lista da base Qualis
            if self._qualis_issn_df is not None:
                issn_trabalho = str(trabalho.issn).strip()
                # Verifica na primeira coluna (ISSN)
                if issn_trabalho in self._qualis_issn_df.iloc[:, 0].values:
                    return 'Periódicos não indexados constantes na base Qualis'
            
            # Se não está na base Qualis ou não conseguiu carregar o arquivo
            return 'Periódicos Indexados'
        
        return None
    
    def regra_livros_com_isbn(self, trabalho) -> Optional[str]:
        """
        Regra: Livros publicados com ISBN são classificados como Livros - Completo.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Nome da atividade se a regra se aplicar, None caso contrário
        """
        if trabalho.categoria == 'Livros publicados' and self._tem_isbn(trabalho):
            return 'Livros - Completo'
        
        return None
    
    def regra_capitulos_com_isbn(self, trabalho) -> Optional[str]:
        """
        Regra: Capítulos de livros com ISBN são classificados como Livros - Capítulo.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Nome da atividade se a regra se aplicar, None caso contrário
        """
        if trabalho.categoria == 'Capítulos de livros' and self._tem_isbn(trabalho):
            return 'Livros - Capítulo'
        
        return None
    
    def regra_projetos_pesquisa_coordenador(self, trabalho) -> Optional[str]:
        """
        Regra: Projetos de pesquisa onde o autor é o primeiro autor são classificados
        como "Projeto de Pesquisa - Coordenador", caso contrário como 
        "Projeto de Pesquisa - Participação".
        
        Esta regra depende dos arquivos de cache do Lattes para extrair os nomes
        em citações bibliográficas e verificar a autoria.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Nome da atividade se a regra se aplicar, None caso contrário
        """
        if trabalho.categoria != 'Projetos de pesquisa':
            return None
        
        if not self.cache_dir:
            return None
        
        if not os.path.exists(self.cache_dir):
            return None
        
        try:
            cache_files = os.listdir(self.cache_dir)
            
            for id_lattes in cache_files:
                if not id_lattes.isdigit() or len(id_lattes) != 16:
                    continue
                
                nomes_citacao = self._extrair_nomes_citacao_do_cache(id_lattes)
                if not nomes_citacao:
                    continue
                
                if self._eh_primeiro_autor(trabalho, nomes_citacao):
                    return 'Projeto de Pesquisa - Coordenador'
            
            return 'Projeto de Pesquisa - Participação'
            
        except Exception as e:
            print(f"Erro ao processar regra de projetos de pesquisa: {e}")
            return None
    
    def obter_todas_regras(self) -> List:
        """
        Retorna uma lista com todas as regras disponíveis em ordem de prioridade.
        
        Returns:
            Lista de métodos de regras
        """
        return [
            self.regra_projetos_pesquisa_coordenador,
            self.regra_artigos_aceitos_com_doi,
            self.regra_artigos_completos_com_issn,
            self.regra_livros_com_isbn,
            self.regra_capitulos_com_isbn,
        ]

