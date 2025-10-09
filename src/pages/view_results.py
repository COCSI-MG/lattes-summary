#!/usr/bin/env python
# encoding: utf-8

import streamlit as st
import os
import json
import re
import pandas as pd

def extract_json_from_html(html_content):
    """
    Extrai o JSON embutido no HTML (array DATA).
    """
    try:
        match = re.search(r'const DATA = (\[.*?\]);', html_content, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            return data
        return []
    except Exception as e:
        st.error(f"Erro ao extrair dados: {str(e)}")
        return []

def extract_title_from_html(html_content):
    """
    Extrai o título da página HTML.
    """
    try:
        match = re.search(r'<h3>(.*?)</h3>', html_content)
        if match:
            return match.group(1)
        return "Sem título"
    except:
        return "Sem título"

def main():
    """
    Página de visualização de resultados do download.
    """
    st.title("📊 Visualização de Resultados Lattes")
    st.markdown("---")
    
    if 'download_resultado' not in st.session_state:
        st.warning("⚠️ Nenhum resultado de download encontrado. Por favor, execute o download primeiro.")
        if st.button("← Voltar para Filtro Lattes"):
            st.switch_page("pages/filter_lattes.py")
        return
    
    resultado = st.session_state['download_resultado']
    output_dir = st.session_state['output_dir']
    config_options = st.session_state['config_options']
    
    st.success(f"✅ Resultados carregados de: `{output_dir}`")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Currículos Processados", resultado['curriculos_processados'])
    with col2:
        st.metric("Tempo de Execução", resultado['tempo_execucao'])
    
    st.markdown("---")
    
    if st.button("← Voltar para Filtro Lattes"):
        st.switch_page("pages/filter_lattes.py")
    
    st.markdown("---")
    
    categorias = {
        '📚 Produções Bibliográficas': [
            ('PB-0.html', 'Total de produções bibliográficas', True),
            ('PB0-0.html', 'Artigos completos em periódicos', config_options.get('rel_artigo_periodico')),
            ('PB1-0.html', 'Livros publicados', config_options.get('rel_livro')),
            ('PB2-0.html', 'Capítulos de livros', config_options.get('rel_capitulo_livro')),
            ('PB3-0.html', 'Textos em jornais', config_options.get('rel_jornal')),
            ('PB4-0.html', 'Trabalhos completos em congressos', config_options.get('rel_trabalho_completo')),
            ('PB5-0.html', 'Resumos expandidos', config_options.get('rel_resumo_expandido')),
            ('PB6-0.html', 'Resumos em congressos', config_options.get('rel_resumo')),
            ('PB7-0.html', 'Artigos aceitos', config_options.get('rel_artigo_aceito')),
            ('PB8-0.html', 'Apresentações de trabalho', config_options.get('rel_apresentacao')),
            ('PB9-0.html', 'Outros tipos', config_options.get('rel_outro_biblio')),
        ],
        '🔧 Produções Técnicas': [
            ('PT-0.html', 'Total de produções técnicas', True),
            ('PT0-0.html', 'Software com registro', config_options.get('rel_soft_registro')),
            ('PT1-0.html', 'Software sem registro', config_options.get('rel_soft_sem_registro')),
            ('PT2-0.html', 'Produtos tecnológicos', config_options.get('rel_produto_tec')),
            ('PT3-0.html', 'Processos ou técnicas', config_options.get('rel_processo')),
            ('PT4-0.html', 'Trabalhos técnicos', config_options.get('rel_trabalho_tec')),
            ('PT5-0.html', 'Outros tipos', config_options.get('rel_outro_tec')),
            ('PT6-0.html', 'Entrevistas e comentários', config_options.get('rel_entrevista')),
        ],
        '🎨 Produções Artísticas': [
            ('PA-0.html', 'Total de produções artísticas', config_options.get('rel_prod_artistica')),
        ],
        '📝 Orientações em Andamento': [
            ('OA-0.html', 'Total de orientações em andamento', True),
            ('OA0-0.html', 'Pós-doutorado', config_options.get('orient_and_pos_doc')),
            ('OA1-0.html', 'Doutorado', config_options.get('orient_and_doc')),
            ('OA2-0.html', 'Mestrado', config_options.get('orient_and_mest')),
            ('OA3-0.html', 'Especialização', config_options.get('orient_and_esp')),
            ('OA4-0.html', 'TCC', config_options.get('orient_and_tcc')),
            ('OA5-0.html', 'Iniciação científica', config_options.get('orient_and_ic')),
            ('OA6-0.html', 'Outros tipos', config_options.get('orient_and_outro')),
        ],
        '✅ Orientações Concluídas': [
            ('OC-0.html', 'Total de orientações concluídas', True),
            ('OC0-0.html', 'Pós-doutorado', config_options.get('orient_conc_pos_doc')),
            ('OC1-0.html', 'Doutorado', config_options.get('orient_conc_doc')),
            ('OC2-0.html', 'Mestrado', config_options.get('orient_conc_mest')),
            ('OC3-0.html', 'Especialização', config_options.get('orient_conc_esp')),
            ('OC4-0.html', 'TCC', config_options.get('orient_conc_tcc')),
            ('OC5-0.html', 'Iniciação científica', config_options.get('orient_conc_ic')),
            ('OC6-0.html', 'Outros tipos', config_options.get('orient_conc_outro')),
        ],
        '➕ Outros': [
            ('Pj-0.html', 'Projetos de pesquisa', config_options.get('rel_projeto')),
            ('Pm-0.html', 'Prêmios e títulos', config_options.get('rel_premio')),
            ('Ep-0.html', 'Participação em eventos', config_options.get('rel_part_evento')),
            ('Eo-0.html', 'Organização de eventos', config_options.get('rel_org_evento')),
        ],
    }
    
    for categoria, arquivos in categorias.items():
        st.markdown(f"## {categoria}")
        
        categoria_tem_dados = False
        
        for arquivo, descricao, habilitado in arquivos:
            if not habilitado:
                continue
            
            file_path = os.path.join(output_dir, arquivo)
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    data = extract_json_from_html(html_content)
                    
                    if data:
                        categoria_tem_dados = True
                        df = pd.DataFrame(data)
                        df_sem_duplicatas = df.drop_duplicates()
                        num_duplicatas = len(df) - len(df_sem_duplicatas)
                        
                        with st.expander(f"### {descricao} ({len(df_sem_duplicatas)} itens)", expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Total de Itens", len(df_sem_duplicatas))
                            with col2:
                                if 'ano' in df_sem_duplicatas.columns:
                                    anos_unicos = df_sem_duplicatas['ano'].nunique()
                                    st.metric("Anos Diferentes", anos_unicos)
                            
                            if num_duplicatas > 0:
                                st.info(f"ℹ️ {num_duplicatas} duplicata(s) removida(s) automaticamente.")
                            
                            st.markdown("---")
                            
                            st.dataframe(
                                df_sem_duplicatas,
                                use_container_width=True,
                                height=400
                            )
                            
                            csv = df_sem_duplicatas.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Baixar CSV",
                                data=csv,
                                file_name=f"{arquivo.replace('.html', '')}.csv",
                                mime="text/csv",
                            )
                except Exception as e:
                    st.error(f"Erro ao carregar {arquivo}: {str(e)}")
        
        if not categoria_tem_dados:
            st.info(f"Nenhum dado encontrado para esta categoria.")
        
        st.markdown("---")
    
    if st.button("← Voltar para Filtro Lattes", key="voltar_fim"):
        st.switch_page("pages/filter_lattes.py")

if __name__ == "__main__":
    main()
