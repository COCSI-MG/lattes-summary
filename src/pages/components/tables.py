#!/usr/bin/env python
# encoding: utf-8

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.services.atividade import AtividadeService
from src.services.categoria import CategoriaService


def render_tabela_atividades_pontos(load_atividade_pontos_callback):
    """
    Renderiza o expander com a tabela de atividades e pontos editável.
    
    Args:
        load_atividade_pontos_callback: Função callback para recarregar os pontos do banco
    """
    with st.expander('Tabela de atividades e pontos', expanded=False):
        try:
            atividade_service = AtividadeService()
            atividades_db = atividade_service.get_all_atividades()
            tabela_pontos = pd.DataFrame(atividades_db)
            if not tabela_pontos.empty:
                tabela_pontos = tabela_pontos.sort_values('pontos', ascending=False)
        except Exception as e:
            st.error(f"Erro ao carregar atividades: {e}")
            tabela_pontos = pd.DataFrame(columns=['id', 'atividade', 'pontos'])
        
        edited_pontos = st.data_editor(
            tabela_pontos,
            hide_index=True,
            use_container_width=True,
            height=360,
            key='editor_pontos_atividades',
            column_config={
                'id': st.column_config.NumberColumn('ID', disabled=True, width='small'),
                'atividade': st.column_config.TextColumn('Atividade', disabled=True),
                'pontos': st.column_config.NumberColumn('Pontos', min_value=0, required=True),
            },
        )
        
        if st.button('💾 Salvar', key='btn_salvar_pontos', use_container_width=True):
            try:
                atividade_service = AtividadeService()
                alteracoes_realizadas = 0
                erros = []
                
                for idx, row in edited_pontos.iterrows():
                    atividade_id = row['id']
                    novos_pontos = int(row['pontos'])
                    
                    original_row = tabela_pontos[tabela_pontos['id'] == atividade_id]
                    if not original_row.empty:
                        pontos_originais = int(original_row.iloc[0]['pontos'])
                        if novos_pontos != pontos_originais:
                            try:
                                atividade_service.update_atividade(atividade_id, novos_pontos)
                                alteracoes_realizadas += 1
                            except Exception as e:
                                erros.append(f"Erro ao atualizar '{row['atividade']}': {e}")
                
                if alteracoes_realizadas > 0:
                    st.success(f'✅ {alteracoes_realizadas} atividade(s) atualizada(s) com sucesso!')
                    st.session_state['indice_r_atividade_pontos'] = load_atividade_pontos_callback()
                    st.rerun()
                elif not erros:
                    st.info('ℹ️ Nenhuma alteração foi detectada.')
                
                if erros:
                    for erro in erros:
                        st.error(erro)
                        
            except Exception as e:
                st.error(f"Erro ao salvar alterações: {e}")


def render_relacao_categoria_atividade(load_categoria_atividade_callback):
    """
    Renderiza o expander com a relação entre categorias e atividades editável.
    
    Args:
        load_categoria_atividade_callback: Função callback para recarregar as relações do banco
    """
    with st.expander('Relação entre Categoria e Atividade', expanded=False):
        st.caption('Configure qual atividade está associada a cada categoria Lattes')
        
        try:
            atividade_service = AtividadeService()
            categoria_service = CategoriaService()
            
            todas_categorias = categoria_service.get_all_categorias()
            todas_atividades = atividade_service.get_all_atividades()
            atividades_dict = {atv['id']: atv['atividade'] for atv in todas_atividades}
            
            relacoes = atividade_service.get_all_categoria_atividade()
            relacoes_dict = {rel['categoria_id']: rel['atividade_id'] for rel in relacoes}
            
            dados_tabela = []
            for cat in todas_categorias:
                atividade_id = relacoes_dict.get(cat['id'], None)
                atividade_nome = atividades_dict.get(atividade_id, None) if atividade_id else None
                
                dados_tabela.append({
                    'categoria_id': cat['id'],
                    'categoria': cat['categoria'],
                    'atividade_id': atividade_id,
                    'atividade': atividade_nome
                })
            
            tabela_relacao = pd.DataFrame(dados_tabela)
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            tabela_relacao = pd.DataFrame(columns=['categoria_id', 'categoria', 'atividade_id', 'atividade'])
        
        if not tabela_relacao.empty:
            atividade_opcoes = [None] + [atv['atividade'] for atv in todas_atividades]
            
            edited_relacao = st.data_editor(
                tabela_relacao,
                hide_index=True,
                use_container_width=True,
                height=400,
                key='editor_categoria_atividade',
                column_config={
                    'categoria_id': st.column_config.NumberColumn('ID Cat', disabled=True, width='small'),
                    'categoria': st.column_config.TextColumn('Categoria', disabled=True, width='medium'),
                    'atividade_id': None,
                    'atividade': st.column_config.SelectboxColumn(
                        'Atividade',
                        options=atividade_opcoes,
                        required=False,
                        help='Selecione a atividade associada ou deixe em branco'
                    ),
                },
            )
            
            if st.button('💾 Salvar relações', key='btn_salvar_relacoes', use_container_width=True):
                try:
                    atividade_service = AtividadeService()
                    alteracoes_realizadas = 0
                    erros = []
                    
                    atividade_nome_para_id = {atv['atividade']: atv['id'] for atv in todas_atividades}
                    
                    for idx, row in edited_relacao.iterrows():
                        categoria_id = int(row['categoria_id'])
                        nova_atividade_nome = row['atividade']
                        
                        if nova_atividade_nome is None or nova_atividade_nome == '' or pd.isna(nova_atividade_nome):
                            nova_atividade_id = None
                        else:
                            nova_atividade_id = atividade_nome_para_id.get(nova_atividade_nome)
                        
                        original_row = tabela_relacao[tabela_relacao['categoria_id'] == categoria_id]
                        if not original_row.empty:
                            atividade_id_original = original_row.iloc[0]['atividade_id']
                            if pd.isna(atividade_id_original):
                                atividade_id_original = None
                            else:
                                atividade_id_original = int(atividade_id_original)
                            
                            if nova_atividade_id != atividade_id_original:
                                try:
                                    atividade_service.update_categoria_atividade(categoria_id, nova_atividade_id)
                                    alteracoes_realizadas += 1
                                except Exception as e:
                                    erros.append(f"Erro ao atualizar '{row['categoria']}': {e}")
                    
                    if alteracoes_realizadas > 0:
                        st.success(f'✅ {alteracoes_realizadas} relação(ões) atualizada(s) com sucesso!')
                        st.session_state['indice_r_categoria_para_atividade'] = load_categoria_atividade_callback()
                        st.rerun()
                    elif not erros:
                        st.info('ℹ️ Nenhuma alteração foi detectada.')
                    
                    if erros:
                        for erro in erros:
                            st.error(erro)
                            
                except Exception as e:
                    st.error(f"Erro ao salvar alterações: {e}")

