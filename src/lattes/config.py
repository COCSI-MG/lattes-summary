#!/usr/bin/env python
# encoding: utf-8

import os

class LattesConfig:
    """
    Classe para gerenciar as configurações do scriptLattes.
    Define valores padrão e permite personalização dos parâmetros.
    """
    
    def __init__(self, **kwargs):
        """
        Inicializa as configurações com valores padrão.
        Valores podem ser sobrescritos através de kwargs.
        
        Args:
            **kwargs: Parâmetros de configuração personalizados
        """
        # Configurações globais
        self.nome_grupo = kwargs.get('nome_grupo', 'cefet')
        self.arquivo_entrada = kwargs.get('arquivo_entrada', '')  # Será preenchido dinamicamente
        self.diretorio_saida = kwargs.get('diretorio_saida', '')  # Será preenchido dinamicamente
        self.email_admin = kwargs.get('email_admin', 'admin@email.com')
        self.idioma = kwargs.get('idioma', 'PT')
        self.ano_inicial = kwargs.get('ano_inicial', 1900)
        self.ano_final = kwargs.get('ano_final', 2025)
        self.itens_por_pagina = kwargs.get('itens_por_pagina', 5000)
        self.diretorio_cache = kwargs.get('diretorio_cache', '')  # Será preenchido dinamicamente
        
        # Relatórios de produção bibliográfica
        self.rel_artigo_periodico = kwargs.get('rel_artigo_periodico', True)
        self.rel_livro = kwargs.get('rel_livro', True)
        self.rel_capitulo_livro = kwargs.get('rel_capitulo_livro', True)
        self.rel_jornal = kwargs.get('rel_jornal', True)
        self.rel_trabalho_completo = kwargs.get('rel_trabalho_completo', True)
        self.rel_resumo_expandido = kwargs.get('rel_resumo_expandido', True)
        self.rel_resumo = kwargs.get('rel_resumo', True)
        self.rel_artigo_aceito = kwargs.get('rel_artigo_aceito', True)
        self.rel_apresentacao = kwargs.get('rel_apresentacao', True)
        self.rel_outro_biblio = kwargs.get('rel_outro_biblio', True)
        
        # Produções técnicas
        self.rel_soft_registro = kwargs.get('rel_soft_registro', True)
        self.rel_soft_sem_registro = kwargs.get('rel_soft_sem_registro', True)
        self.rel_produto_tec = kwargs.get('rel_produto_tec', True)
        self.rel_processo = kwargs.get('rel_processo', True)
        self.rel_trabalho_tec = kwargs.get('rel_trabalho_tec', True)
        self.rel_outro_tec = kwargs.get('rel_outro_tec', True)
        self.rel_entrevista = kwargs.get('rel_entrevista', True)
        
        # Produções artísticas
        self.rel_prod_artistica = kwargs.get('rel_prod_artistica', True)
        
        # Orientações em andamento
        self.orient_and_pos_doc = kwargs.get('orient_and_pos_doc', True)
        self.orient_and_doc = kwargs.get('orient_and_doc', True)
        self.orient_and_mest = kwargs.get('orient_and_mest', True)
        self.orient_and_esp = kwargs.get('orient_and_esp', True)
        self.orient_and_tcc = kwargs.get('orient_and_tcc', True)
        self.orient_and_ic = kwargs.get('orient_and_ic', True)
        self.orient_and_outro = kwargs.get('orient_and_outro', True)
        
        # Orientações concluídas
        self.orient_conc_pos_doc = kwargs.get('orient_conc_pos_doc', True)
        self.orient_conc_doc = kwargs.get('orient_conc_doc', True)
        self.orient_conc_mest = kwargs.get('orient_conc_mest', True)
        self.orient_conc_esp = kwargs.get('orient_conc_esp', True)
        self.orient_conc_tcc = kwargs.get('orient_conc_tcc', True)
        self.orient_conc_ic = kwargs.get('orient_conc_ic', True)
        self.orient_conc_outro = kwargs.get('orient_conc_outro', True)
        
        # Relatórios adicionais
        self.rel_projeto = kwargs.get('rel_projeto', True)
        self.rel_premio = kwargs.get('rel_premio', True)
        self.rel_part_evento = kwargs.get('rel_part_evento', True)
        self.rel_org_evento = kwargs.get('rel_org_evento', True)
        
        # Grafo de colaborações
        self.grafo_mostrar = kwargs.get('grafo_mostrar', True)
        self.grafo_todos_nos = kwargs.get('grafo_todos_nos', True)
        self.grafo_rotulos = kwargs.get('grafo_rotulos', False)
        
        # Itens incluídos no grafo
        self.grafo_artigo = kwargs.get('grafo_artigo', True)
        self.grafo_livro = kwargs.get('grafo_livro', True)
        self.grafo_capitulo = kwargs.get('grafo_capitulo', True)
        self.grafo_jornal = kwargs.get('grafo_jornal', True)
        self.grafo_trab_comp = kwargs.get('grafo_trab_comp', True)
        self.grafo_res_exp = kwargs.get('grafo_res_exp', True)
        self.grafo_resumo = kwargs.get('grafo_resumo', True)
        self.grafo_art_aceito = kwargs.get('grafo_art_aceito', True)
        self.grafo_apres = kwargs.get('grafo_apres', True)
        self.grafo_outro_bib = kwargs.get('grafo_outro_bib', True)
        self.grafo_soft_reg = kwargs.get('grafo_soft_reg', True)
        self.grafo_soft_sem = kwargs.get('grafo_soft_sem', True)
        self.grafo_prod_tec = kwargs.get('grafo_prod_tec', True)
        self.grafo_proc = kwargs.get('grafo_proc', True)
        self.grafo_trab_tec = kwargs.get('grafo_trab_tec', True)
        self.grafo_outro_tec = kwargs.get('grafo_outro_tec', True)
        self.grafo_entrev = kwargs.get('grafo_entrev', True)
        self.grafo_art_prod = kwargs.get('grafo_art_prod', True)
        
        # Métricas
        self.rel_metricas = kwargs.get('rel_metricas', True)
    
    def _bool_to_config(self, valor):
        """
        Converte valor booleano para formato de configuração (sim/nao).
        
        Args:
            valor (bool): Valor booleano
            
        Returns:
            str: "sim" ou "nao"
        """
        return "sim" if valor else "nao"
    
    def gerar_config_text(self, arquivo_entrada, diretorio_saida):
        """
        Gera o texto do arquivo de configuração baseado nos atributos da classe.
        
        Args:
            arquivo_entrada (str): Caminho para o arquivo de lista de currículos
            diretorio_saida (str): Caminho para o diretório de saída
            
        Returns:
            str: Texto completo da configuração
        """
        cache_dir = os.path.join(os.path.abspath(diretorio_saida), 'cache')
        
        config_text = f"""# Configuração para download de currículos Lattes
global-nome_do_grupo = {self.nome_grupo}
global-arquivo_de_entrada = {os.path.abspath(arquivo_entrada)}
global-diretorio_de_saida = {os.path.abspath(diretorio_saida)}
global-email_do_admin = {self.email_admin}
global-idioma = {self.idioma}
global-itens_desde_o_ano = {self.ano_inicial}
global-itens_ate_o_ano = {self.ano_final}
global-itens_por_pagina = {self.itens_por_pagina}
global-diretorio_de_armazenamento_de_cvs = {cache_dir}

# Relatórios de produção
relatorio-incluir_artigo_em_periodico = {self._bool_to_config(self.rel_artigo_periodico)}
relatorio-incluir_livro_publicado = {self._bool_to_config(self.rel_livro)}
relatorio-incluir_capitulo_de_livro_publicado = {self._bool_to_config(self.rel_capitulo_livro)}
relatorio-incluir_texto_em_jornal_de_noticia = {self._bool_to_config(self.rel_jornal)}
relatorio-incluir_trabalho_completo_em_congresso = {self._bool_to_config(self.rel_trabalho_completo)}
relatorio-incluir_resumo_expandido_em_congresso = {self._bool_to_config(self.rel_resumo_expandido)}
relatorio-incluir_resumo_em_congresso = {self._bool_to_config(self.rel_resumo)}
relatorio-incluir_artigo_aceito_para_publicacao = {self._bool_to_config(self.rel_artigo_aceito)}
relatorio-incluir_apresentacao_de_trabalho = {self._bool_to_config(self.rel_apresentacao)}
relatorio-incluir_outro_tipo_de_producao_bibliografica = {self._bool_to_config(self.rel_outro_biblio)}

relatorio-incluir_software_com_registro = {self._bool_to_config(self.rel_soft_registro)}
relatorio-incluir_software_sem_registro = {self._bool_to_config(self.rel_soft_sem_registro)}
relatorio-incluir_produto_tecnologico = {self._bool_to_config(self.rel_produto_tec)}
relatorio-incluir_processo_ou_tecnica = {self._bool_to_config(self.rel_processo)}
relatorio-incluir_trabalho_tecnico = {self._bool_to_config(self.rel_trabalho_tec)}
relatorio-incluir_outro_tipo_de_producao_tecnica = {self._bool_to_config(self.rel_outro_tec)}
relatorio-incluir_entrevista_mesas_e_comentarios = {self._bool_to_config(self.rel_entrevista)}

relatorio-incluir_producao_artistica = {self._bool_to_config(self.rel_prod_artistica)}

# Relatórios de orientações
relatorio-mostrar_orientacoes = sim
relatorio-incluir_orientacao_em_andamento_pos_doutorado = {self._bool_to_config(self.orient_and_pos_doc)}
relatorio-incluir_orientacao_em_andamento_doutorado = {self._bool_to_config(self.orient_and_doc)}
relatorio-incluir_orientacao_em_andamento_mestrado = {self._bool_to_config(self.orient_and_mest)}
relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao = {self._bool_to_config(self.orient_and_esp)}
relatorio-incluir_orientacao_em_andamento_tcc = {self._bool_to_config(self.orient_and_tcc)}
relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica = {self._bool_to_config(self.orient_and_ic)}
relatorio-incluir_orientacao_em_andamento_outro_tipo = {self._bool_to_config(self.orient_and_outro)}

relatorio-incluir_orientacao_concluida_pos_doutorado = {self._bool_to_config(self.orient_conc_pos_doc)}
relatorio-incluir_orientacao_concluida_doutorado = {self._bool_to_config(self.orient_conc_doc)}
relatorio-incluir_orientacao_concluida_mestrado = {self._bool_to_config(self.orient_conc_mest)}
relatorio-incluir_orientacao_concluida_monografia_de_especializacao = {self._bool_to_config(self.orient_conc_esp)}
relatorio-incluir_orientacao_concluida_tcc = {self._bool_to_config(self.orient_conc_tcc)}
relatorio-incluir_orientacao_concluida_iniciacao_cientifica = {self._bool_to_config(self.orient_conc_ic)}
relatorio-incluir_orientacao_concluida_outro_tipo = {self._bool_to_config(self.orient_conc_outro)}

# Relatórios adicionais
relatorio-incluir_projeto = {self._bool_to_config(self.rel_projeto)}
relatorio-incluir_premio = {self._bool_to_config(self.rel_premio)}
relatorio-incluir_participacao_em_evento = {self._bool_to_config(self.rel_part_evento)}
relatorio-incluir_organizacao_de_evento = {self._bool_to_config(self.rel_org_evento)}

# Grafo de colaborações
grafo-mostrar_grafo_de_colaboracoes = {self._bool_to_config(self.grafo_mostrar)}
grafo-mostrar_todos_os_nos_do_grafo = {self._bool_to_config(self.grafo_todos_nos)}
grafo-considerar_rotulos_dos_membros_do_grupo = {self._bool_to_config(self.grafo_rotulos)}

grafo-incluir_artigo_em_periodico = {self._bool_to_config(self.grafo_artigo)}
grafo-incluir_livro_publicado = {self._bool_to_config(self.grafo_livro)}
grafo-incluir_capitulo_de_livro_publicado = {self._bool_to_config(self.grafo_capitulo)}
grafo-incluir_texto_em_jornal_de_noticia = {self._bool_to_config(self.grafo_jornal)}
grafo-incluir_trabalho_completo_em_congresso = {self._bool_to_config(self.grafo_trab_comp)}
grafo-incluir_resumo_expandido_em_congresso = {self._bool_to_config(self.grafo_res_exp)}
grafo-incluir_resumo_em_congresso = {self._bool_to_config(self.grafo_resumo)}
grafo-incluir_artigo_aceito_para_publicacao = {self._bool_to_config(self.grafo_art_aceito)}
grafo-incluir_apresentacao_de_trabalho = {self._bool_to_config(self.grafo_apres)}
grafo-incluir_outro_tipo_de_producao_bibliografica = {self._bool_to_config(self.grafo_outro_bib)}

grafo-incluir_software_com_registro = {self._bool_to_config(self.grafo_soft_reg)}
grafo-incluir_software_sem_registro = {self._bool_to_config(self.grafo_soft_sem)}
grafo-incluir_produto_tecnologico = {self._bool_to_config(self.grafo_prod_tec)}
grafo-incluir_processo_ou_tecnica = {self._bool_to_config(self.grafo_proc)}
grafo-incluir_trabalho_tecnico = {self._bool_to_config(self.grafo_trab_tec)}
grafo-incluir_outro_tipo_de_producao_tecnica = {self._bool_to_config(self.grafo_outro_tec)}
grafo-incluir_entrevista_mesas_e_comentarios = {self._bool_to_config(self.grafo_entrev)}

grafo-incluir_producao_artistica = {self._bool_to_config(self.grafo_art_prod)}

# Métricas
relatorio-incluir_metricas = {self._bool_to_config(self.rel_metricas)}
"""
        return config_text

