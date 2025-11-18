#!/usr/bin/env python
# encoding: utf-8

from dataclasses import dataclass
import sys
import os
from typing import Dict, List, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.atividade import AtividadeService
from services.categoria import CategoriaService
from .regras import Regras

@dataclass
class Trabalho:
    autores: str
    titulo: str
    categoria: str # categoria definida pelo lattes para o trabalho
    atividade: str # atividade definida pelo usuário ou pelas regras para o trabalho
    pontos: Optional[int] # pontuação calculada
    ano: str
    doi: str
    issn: str
    isbn: str
    outros: dict
    texto_completo: str
    nome_arquivo: str # nome do arquivo html que o trabalho foi extraido

class IndiceR:
    """
    Classe responsável por calcular o Índice R de trabalhos acadêmicos.
    
    O Índice R é calculado como a soma dos pontos de todas as atividades
    associadas aos trabalhos, aplicando regras de negócio específicas que
    têm prioridade sobre as relações padrão do banco de dados.
    """
    
    def __init__(self, db_path: str = None, cache_dir: str = None):
        """
        Args:
            db_path: Caminho para o banco de dados. Se None, usa o caminho padrão.
            cache_dir: Diretório onde estão os arquivos de cache do Lattes.
                      Se None, usa o caminho padrão 'tmp/cache' relativo ao projeto.
        """
        self.atividade_service = AtividadeService(db_path)
        self.categoria_service = CategoriaService(db_path)
        
        if cache_dir is None:
            projeto_raiz = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            cache_dir = os.path.join(projeto_raiz, 'tmp', 'cache')
        
        self.regras = Regras(cache_dir)
        self.lista_regras = self.regras.obter_todas_regras()
        
        self._carregar_dados_banco()
    
    def _carregar_dados_banco(self):
        """
        Carrega os dados de atividades e suas pontuações do banco de dados.
        """
        atividades = self.atividade_service.get_all_atividades()
        self.atividade_pontos = {
            ativ['atividade']: ativ['pontos'] 
            for ativ in atividades
        }
        
        relacoes = self.atividade_service.get_all_categoria_atividade()
        self.categoria_para_atividade = {
            rel['categoria']: rel['atividade']
            for rel in relacoes
        }
    
    def aplicar_regras(self, trabalho: Trabalho) -> Optional[str]:
        """
        Aplica todas as regras ao trabalho e retorna a atividade determinada.
        
        As regras são aplicadas em ordem de prioridade. A primeira regra que
        se aplicar determina a atividade final.
        
        Args:
            trabalho: Objeto Trabalho contendo os dados do trabalho
                
        Returns:
            Nome da atividade determinada pelas regras ou None se nenhuma regra se aplicar
        """
        for regra in self.lista_regras:
            atividade = regra(trabalho)
            if atividade is not None:
                return atividade
        
        return None
    
    def determinar_atividade(self, trabalho: Trabalho) -> Optional[str]:
        """
        Determina a atividade de um trabalho, aplicando regras com prioridade
        sobre o mapeamento padrão do banco de dados.
        
        Ordem de prioridade:
        1. Regras customizadas (definidas nos métodos _regra_*)
        2. Atividade já definida no trabalho
        3. Mapeamento categoria -> atividade do banco de dados
        
        Args:
            trabalho: Objeto Trabalho contendo os dados do trabalho
            
        Returns:
            Nome da atividade determinada ou None se não for possível determinar
        """
        # Prioridade 1: Aplica regras customizadas
        atividade_regra = self.aplicar_regras(trabalho)
        if atividade_regra is not None:
            return atividade_regra
        
        # Prioridade 2: Usa atividade já definida no trabalho
        if trabalho.atividade is not None and trabalho.atividade != '':
            return trabalho.atividade
        
        # Prioridade 3: Busca no mapeamento categoria -> atividade
        if trabalho.categoria in self.categoria_para_atividade:
            return self.categoria_para_atividade[trabalho.categoria]
        
        return None
    
    def calcular_pontos_trabalho(self, trabalho: Trabalho) -> int:
        """
        Calcula os pontos de um trabalho específico.
        
        Args:
            trabalho: Objeto Trabalho
            
        Returns:
            Pontos do trabalho (0 se não puder determinar a atividade)
        """
        if trabalho.pontos is not None and trabalho.pontos != '':
            try:
                return int(trabalho.pontos)
            except (ValueError, TypeError):
                pass
        
        atividade = self.determinar_atividade(trabalho)
        if atividade is None:
            return 0
        
        return self.atividade_pontos.get(atividade, 0)
    
    def calcular_indice_r(self, trabalhos: List[Trabalho]) -> Dict[str, Any]:
        """
        Calcula o Índice R para uma lista de trabalhos.
        
        Args:
            trabalhos: Lista de objetos Trabalho
            
        Returns:
            Dicionário contendo:
            - indice_r: Valor total do Índice R
            - total_trabalhos: Número total de trabalhos processados
            - trabalhos_processados: Lista de trabalhos com atividades e pontos atualizados
            - trabalhos_sem_atividade: Lista de trabalhos que não puderam ser classificados
        """
        trabalhos_processados = []
        trabalhos_sem_atividade = []
        pontos_total = 0
        
        for trabalho in trabalhos:
            atividade = self.determinar_atividade(trabalho)
            
            pontos = self.calcular_pontos_trabalho(trabalho)
            
            trabalho.atividade = atividade if atividade else trabalho.atividade
            trabalho.pontos = pontos
            
            if atividade is None:
                trabalhos_sem_atividade.append(trabalho)
            else:
                trabalhos_processados.append(trabalho)
                pontos_total += pontos
        
        return {
            'indice_r': pontos_total,
            'total_trabalhos': len(trabalhos),
            'trabalhos_processados': trabalhos_processados,
            'trabalhos_sem_atividade': trabalhos_sem_atividade
        }
    
    def processar_trabalhos(self, trabalhos: List[Trabalho]) -> List[Trabalho]:
        """
        Processa uma lista de trabalhos, determinando atividades e pontos.
        
        Este método é útil quando você só quer atualizar os trabalhos sem
        calcular o índice R total.
        
        Args:
            trabalhos: Lista de objetos Trabalho
            
        Returns:
            Lista de trabalhos com atividades e pontos atualizados
        """
        trabalhos_processados = []
        
        for trabalho in trabalhos:
            atividade = self.determinar_atividade(trabalho)
            trabalho.atividade = atividade if atividade else trabalho.atividade
            
            pontos = self.calcular_pontos_trabalho(trabalho)
            trabalho.pontos = pontos
            
            trabalhos_processados.append(trabalho)
        
        return trabalhos_processados
    
    def adicionar_regra_customizada(self, nome_regra: str, funcao_regra):
        """
        Permite adicionar regras customizadas dinamicamente.
        
        Args:
            nome_regra: Nome identificador da regra
            funcao_regra: Função que implementa a regra.
                         Deve receber um trabalho (Trabalho) e retornar Optional[str]
        
        Example:
            def minha_regra(trabalho: Trabalho) -> Optional[str]:
                if trabalho.categoria == 'Minha Categoria':
                    return 'Minha Atividade'
                return None
            
            indice_r = IndiceR()
            indice_r.adicionar_regra_customizada('minha_regra', minha_regra)
        """
        setattr(self, f'_regra_{nome_regra}', funcao_regra)
    
    def obter_atividades_disponiveis(self) -> Dict[str, int]:
        """
        Retorna todas as atividades disponíveis e seus pontos.
        
        Returns:
            Dicionário com atividade -> pontos
        """
        return self.atividade_pontos.copy()
    
    def obter_categorias_disponiveis(self) -> List[str]:
        """
        Retorna todas as categorias disponíveis.
        
        Returns:
            Lista de nomes de categorias
        """
        return list(self.categoria_para_atividade.keys())

