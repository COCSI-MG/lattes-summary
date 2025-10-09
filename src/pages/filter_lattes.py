#!/usr/bin/env python
# encoding: utf-8

import streamlit as st
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lattes.lattes import LattesDownloader

def main():
    """
    Página de filtro e busca de currículos Lattes
    """
    st.title("🔍 Filtro Lattes - Busca de Currículos")
    st.markdown("---")
    
    st.sidebar.header("⚙️ Configurações de Busca")
    st.sidebar.subheader("📋 IDs dos Currículos Lattes")
    st.sidebar.caption("Insira os IDs dos currículos Lattes (um por linha)")
    
    ids_text = st.sidebar.text_area(
        "IDs Lattes",
        placeholder="1234567890123456\n9876543210987654",
        height=150,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("🌍 Configurações Globais")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        ano_inicial = st.number_input("Ano inicial", min_value=1900, max_value=2100, value=1900)
    with col2:
        ano_final = st.number_input("Ano final", min_value=1900, max_value=2100, value=2025)
    
    itens_por_pagina = st.sidebar.number_input(
        "Itens por página", 
        min_value=100, 
        max_value=10000, 
        value=5000,
        step=100
    )
    
    output_dir = st.sidebar.text_input("Diretório de saída", value="tmp")
    
    st.sidebar.markdown("---")
    
    # === Relatórios de Produção ===.
    with st.sidebar.expander("📚 Relatórios de Produção", expanded=False):
        rel_artigo_periodico = st.checkbox("Artigo em periódico", value=True, key="rel_artigo")
        rel_livro = st.checkbox("Livro publicado", value=True, key="rel_livro")
        rel_capitulo_livro = st.checkbox("Capítulo de livro", value=True, key="rel_cap")
        rel_jornal = st.checkbox("Texto em jornal", value=True, key="rel_jornal")
        rel_trabalho_completo = st.checkbox("Trabalho completo em congresso", value=True, key="rel_trab_comp")
        rel_resumo_expandido = st.checkbox("Resumo expandido em congresso", value=True, key="rel_res_exp")
        rel_resumo = st.checkbox("Resumo em congresso", value=True, key="rel_resumo")
        rel_artigo_aceito = st.checkbox("Artigo aceito para publicação", value=True, key="rel_art_aceito")
        rel_apresentacao = st.checkbox("Apresentação de trabalho", value=True, key="rel_apres")
        rel_outro_biblio = st.checkbox("Outro tipo de produção bibliográfica", value=True, key="rel_outro_bib")
    
    # === Relatórios de Produções Técnicas ===.
    with st.sidebar.expander("🔧 Produções Técnicas", expanded=False):
        rel_soft_registro = st.checkbox("Software com registro", value=True, key="rel_soft_reg")
        rel_soft_sem_registro = st.checkbox("Software sem registro", value=True, key="rel_soft_sem")
        rel_produto_tec = st.checkbox("Produto tecnológico", value=True, key="rel_prod_tec")
        rel_processo = st.checkbox("Processo ou técnica", value=True, key="rel_proc")
        rel_trabalho_tec = st.checkbox("Trabalho técnico", value=True, key="rel_trab_tec")
        rel_outro_tec = st.checkbox("Outro tipo de produção técnica", value=True, key="rel_outro_tec")
        rel_entrevista = st.checkbox("Entrevista, mesas e comentários", value=True, key="rel_entrev")
    
    # === Produções Artísticas ===.
    with st.sidebar.expander("🎨 Produções Artísticas", expanded=False):
        rel_prod_artistica = st.checkbox("Produção artística", value=True, key="rel_art")
    
    # === Orientações em Andamento ===.
    with st.sidebar.expander("📝 Orientações em Andamento", expanded=False):
        orient_and_pos_doc = st.checkbox("Pós-doutorado", value=True, key="and_pos")
        orient_and_doc = st.checkbox("Doutorado", value=True, key="and_doc")
        orient_and_mest = st.checkbox("Mestrado", value=True, key="and_mest")
        orient_and_esp = st.checkbox("Especialização", value=True, key="and_esp")
        orient_and_tcc = st.checkbox("TCC", value=True, key="and_tcc")
        orient_and_ic = st.checkbox("Iniciação científica", value=True, key="and_ic")
        orient_and_outro = st.checkbox("Outro tipo", value=True, key="and_outro")
    
    # === Orientações Concluídas ===.
    with st.sidebar.expander("✅ Orientações Concluídas", expanded=False):
        orient_conc_pos_doc = st.checkbox("Pós-doutorado", value=True, key="conc_pos")
        orient_conc_doc = st.checkbox("Doutorado", value=True, key="conc_doc")
        orient_conc_mest = st.checkbox("Mestrado", value=True, key="conc_mest")
        orient_conc_esp = st.checkbox("Especialização", value=True, key="conc_esp")
        orient_conc_tcc = st.checkbox("TCC", value=True, key="conc_tcc")
        orient_conc_ic = st.checkbox("Iniciação científica", value=True, key="conc_ic")
        orient_conc_outro = st.checkbox("Outro tipo", value=True, key="conc_outro")
    
    # === Relatórios Adicionais ===.
    with st.sidebar.expander("➕ Relatórios Adicionais", expanded=False):
        rel_projeto = st.checkbox("Projetos", value=True, key="rel_proj")
        rel_premio = st.checkbox("Prêmios", value=True, key="rel_premio")
        rel_part_evento = st.checkbox("Participação em eventos", value=True, key="rel_part_ev")
        rel_org_evento = st.checkbox("Organização de eventos", value=True, key="rel_org_ev")
    
    # === Grafo de Colaborações ===.
    with st.sidebar.expander("🔗 Grafo de Colaborações", expanded=False):
        grafo_mostrar = st.checkbox("Mostrar grafo de colaborações", value=True, key="grafo_most")
        grafo_todos_nos = st.checkbox("Mostrar todos os nós do grafo", value=True, key="grafo_nos")
        grafo_rotulos = st.checkbox("Considerar rótulos dos membros", value=False, key="grafo_rot")
        
        st.markdown("**Incluir no grafo:**")
        grafo_artigo = st.checkbox("Artigos em periódico", value=True, key="grafo_art")
        grafo_livro = st.checkbox("Livros", value=True, key="grafo_liv")
        grafo_capitulo = st.checkbox("Capítulos de livro", value=True, key="grafo_cap")
        grafo_jornal = st.checkbox("Textos em jornal", value=True, key="grafo_jorn")
        grafo_trab_comp = st.checkbox("Trabalhos completos", value=True, key="grafo_trab")
        grafo_res_exp = st.checkbox("Resumos expandidos", value=True, key="grafo_res_exp")
        grafo_resumo = st.checkbox("Resumos", value=True, key="grafo_res")
        grafo_art_aceito = st.checkbox("Artigos aceitos", value=True, key="grafo_art_ac")
        grafo_apres = st.checkbox("Apresentações", value=True, key="grafo_apres")
        grafo_outro_bib = st.checkbox("Outras produções bibliográficas", value=True, key="grafo_out_bib")
        grafo_soft_reg = st.checkbox("Software com registro", value=True, key="grafo_soft_reg")
        grafo_soft_sem = st.checkbox("Software sem registro", value=True, key="grafo_soft_sem")
        grafo_prod_tec = st.checkbox("Produtos tecnológicos", value=True, key="grafo_prod_tec")
        grafo_proc = st.checkbox("Processos ou técnicas", value=True, key="grafo_proc")
        grafo_trab_tec = st.checkbox("Trabalhos técnicos", value=True, key="grafo_trab_tec")
        grafo_outro_tec = st.checkbox("Outras produções técnicas", value=True, key="grafo_out_tec")
        grafo_entrev = st.checkbox("Entrevistas/mesas/comentários", value=True, key="grafo_entrev")
        grafo_art_prod = st.checkbox("Produções artísticas", value=True, key="grafo_art_prod")
    
    # === Métricas ===.
    with st.sidebar.expander("📊 Métricas", expanded=False):
        rel_metricas = st.checkbox("Incluir métricas", value=True, key="rel_metr")
    
    st.sidebar.markdown("---")
    buscar_button = st.sidebar.button("🚀 Buscar Currículos", type="primary", use_container_width=True)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("⚠️ Área de Limpeza")
    limpar_tudo_button = st.sidebar.button("🗑️ Limpar Tudo (incluindo cache)", 
                                            type="secondary", 
                                            use_container_width=True,
                                            help="Remove TODOS os arquivos do diretório de saída, incluindo o cache. Use para começar do zero.")
    
    if 'aguardando_confirmacao_limpeza' not in st.session_state:
        st.session_state['aguardando_confirmacao_limpeza'] = False
    
    if limpar_tudo_button:
        st.session_state['aguardando_confirmacao_limpeza'] = True
    
    if st.session_state['aguardando_confirmacao_limpeza']:
        st.warning("⚠️ **ATENÇÃO:** Você está prestes a remover TODOS os arquivos do diretório, incluindo o cache!")
        
        col1, col2 = st.columns(2)
        with col1:
            confirmar_limpeza = st.button("✅ Sim, limpar tudo!", type="primary", use_container_width=True)
        with col2:
            cancelar_limpeza = st.button("❌ Cancelar", type="secondary", use_container_width=True)
        
        if confirmar_limpeza:
            st.session_state['aguardando_confirmacao_limpeza'] = False
            
            with st.spinner("🗑️ Removendo todos os arquivos..."):
                try:
                    downloader = LattesDownloader(output_dir=output_dir)
                    resultado = downloader.limpar_tudo()
                    
                    if resultado['sucesso']:
                        st.success(f"✅ {resultado['mensagem']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Arquivos Removidos", resultado.get('arquivos_removidos', 0))
                        with col2:
                            st.metric("Diretórios Removidos", resultado.get('diretorios_removidos', 0))
                        
                        if resultado.get('erros'):
                            st.warning("⚠️ Alguns arquivos não puderam ser removidos:")
                            for erro in resultado['erros']:
                                st.write(f"- {erro}")
                        
                        if 'download_resultado' in st.session_state:
                            del st.session_state['download_resultado']
                        if 'output_dir' in st.session_state:
                            del st.session_state['output_dir']
                        if 'config_options' in st.session_state:
                            del st.session_state['config_options']
                    else:
                        st.error(f"❌ {resultado['mensagem']}")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao limpar: {str(e)}")
            
            st.stop()
        
        if cancelar_limpeza:
            st.session_state['aguardando_confirmacao_limpeza'] = False
            st.info("Limpeza cancelada.")
            st.rerun()
        
        st.stop()
    
    st.markdown("""
    ### Como usar:
    1. **Insira os IDs** dos currículos Lattes na barra lateral (um por linha)
    2. **Configure o período** de busca (ano inicial e final)
    3. **Selecione as opções** de relatórios que deseja incluir
    4. Clique em **"Buscar Currículos"** para iniciar o download
    5. Para começar do zero, use o botão **"Limpar Tudo"** na barra lateral
    
    ---
    """)
    
    if buscar_button:
        if not ids_text.strip():
            st.error("❌ Por favor, insira pelo menos um ID de currículo Lattes!")
            return
        
        ids_lattes = [id.strip() for id in ids_text.strip().split('\n') if id.strip()]
        ids_unicos = list(dict.fromkeys(ids_lattes))  # Preserva ordem e remove duplicatas
        
        if len(ids_lattes) != len(ids_unicos):
            st.warning(f"⚠️ Detectadas {len(ids_lattes) - len(ids_unicos)} duplicata(s) de ID(s). Processando apenas IDs únicos.")
            ids_lattes = ids_unicos
        
        st.info(f"📥 Processando {len(ids_lattes)} currículo(s) único(s)...")
        
        config_options = {
            'ano_inicial': ano_inicial,
            'ano_final': ano_final,
            'itens_por_pagina': itens_por_pagina,
            
            'rel_artigo_periodico': rel_artigo_periodico,
            'rel_livro': rel_livro,
            'rel_capitulo_livro': rel_capitulo_livro,
            'rel_jornal': rel_jornal,
            'rel_trabalho_completo': rel_trabalho_completo,
            'rel_resumo_expandido': rel_resumo_expandido,
            'rel_resumo': rel_resumo,
            'rel_artigo_aceito': rel_artigo_aceito,
            'rel_apresentacao': rel_apresentacao,
            'rel_outro_biblio': rel_outro_biblio,
            
            'rel_soft_registro': rel_soft_registro,
            'rel_soft_sem_registro': rel_soft_sem_registro,
            'rel_produto_tec': rel_produto_tec,
            'rel_processo': rel_processo,
            'rel_trabalho_tec': rel_trabalho_tec,
            'rel_outro_tec': rel_outro_tec,
            'rel_entrevista': rel_entrevista,
            
            'rel_prod_artistica': rel_prod_artistica,
            
            'orient_and_pos_doc': orient_and_pos_doc,
            'orient_and_doc': orient_and_doc,
            'orient_and_mest': orient_and_mest,
            'orient_and_esp': orient_and_esp,
            'orient_and_tcc': orient_and_tcc,
            'orient_and_ic': orient_and_ic,
            'orient_and_outro': orient_and_outro,
            
            'orient_conc_pos_doc': orient_conc_pos_doc,
            'orient_conc_doc': orient_conc_doc,
            'orient_conc_mest': orient_conc_mest,
            'orient_conc_esp': orient_conc_esp,
            'orient_conc_tcc': orient_conc_tcc,
            'orient_conc_ic': orient_conc_ic,
            'orient_conc_outro': orient_conc_outro,
            
            'rel_projeto': rel_projeto,
            'rel_premio': rel_premio,
            'rel_part_evento': rel_part_evento,
            'rel_org_evento': rel_org_evento,
            
            'grafo_mostrar': grafo_mostrar,
            'grafo_todos_nos': grafo_todos_nos,
            'grafo_rotulos': grafo_rotulos,
            'grafo_artigo': grafo_artigo,
            'grafo_livro': grafo_livro,
            'grafo_capitulo': grafo_capitulo,
            'grafo_jornal': grafo_jornal,
            'grafo_trab_comp': grafo_trab_comp,
            'grafo_res_exp': grafo_res_exp,
            'grafo_resumo': grafo_resumo,
            'grafo_art_aceito': grafo_art_aceito,
            'grafo_apres': grafo_apres,
            'grafo_outro_bib': grafo_outro_bib,
            'grafo_soft_reg': grafo_soft_reg,
            'grafo_soft_sem': grafo_soft_sem,
            'grafo_prod_tec': grafo_prod_tec,
            'grafo_proc': grafo_proc,
            'grafo_trab_tec': grafo_trab_tec,
            'grafo_outro_tec': grafo_outro_tec,
            'grafo_entrev': grafo_entrev,
            'grafo_art_prod': grafo_art_prod,
            
            'rel_metricas': rel_metricas,
        }
        
        with st.spinner("⏳ Baixando currículos... Isso pode levar alguns minutos."):
            try:
                downloader = LattesDownloader(output_dir=output_dir, config_options=config_options)
                
                resultado = downloader.baixar_curriculos(ids_lattes)
                
                if resultado['sucesso']:
                    st.success("✅ Download concluído com sucesso!")
                    
                    st.session_state['download_resultado'] = resultado
                    st.session_state['output_dir'] = output_dir
                    st.session_state['config_options'] = config_options
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Currículos Processados", resultado['curriculos_processados'])
                    with col2:
                        st.metric("Tempo de Execução", resultado['tempo_execucao'])
                    with col3:
                        st.info(f"📁 **Diretório:**\n\n`{resultado['diretorio_saida']}`")
                    
                    st.markdown("---")
                    st.markdown("### 📂 Arquivos Gerados")
                    st.markdown(f"""
                    Os arquivos HTML foram salvos em: `{resultado['diretorio_saida']}`
                    
                    Você pode abrir o arquivo `index.html` no navegador para visualizar os resultados.
                    """)
                    
                    st.markdown("---")
                    if st.button("📊 Visualizar Resultados na Aplicação", type="primary", use_container_width=True):
                        st.switch_page("pages/view_results.py")
                    
                else:
                    st.error(f"❌ Erro no download: {resultado['erro']}")
                    
            except Exception as e:
                st.error(f"❌ Erro ao processar: {str(e)}")
    
    else:
        st.markdown("### 📋 Configurações Atuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Período de busca:**")
            st.write(f"- Ano inicial: {ano_inicial}")
            st.write(f"- Ano final: {ano_final}")
            st.write(f"- Itens por página: {itens_por_pagina}")
        
        with col2:
            st.markdown("**Diretório de saída:**")
            st.code(output_dir)
        
        if ids_text.strip():
            ids_count = len([id for id in ids_text.strip().split('\n') if id.strip()])
            st.info(f"📝 {ids_count} ID(s) de currículo(s) inserido(s)")

if __name__ == "__main__":
    main()
