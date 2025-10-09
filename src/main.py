#!/usr/bin/env python
# encoding: utf-8

import streamlit as st

st.set_page_config(
    page_title="CEFET Lattes - Sistema de Busca",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """
    Aplicação principal do sistema CEFET Lattes
    """
    st.title("📚 CEFET Lattes - Sistema de Busca e Análise")
    st.markdown("---")
    
    st.markdown("""
    ### Bem-vindo ao Sistema de Busca e Análise de Currículos Lattes
    
    Este sistema permite:
    - 🔍 Buscar e baixar currículos Lattes
    - 📊 Gerar relatórios de produção acadêmica
    - 🔗 Visualizar grafos de colaborações
    - 📈 Analisar métricas de produção
    
    **Para começar, clique no botão abaixo:**
    """)
    
    if st.button("🚀 Ir para Filtro Lattes", type="primary", use_container_width=True):
        st.switch_page("pages/filter_lattes.py")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**📋 Relatórios**\n\nGere relatórios detalhados de produções bibliográficas, técnicas e artísticas")
    
    with col2:
        st.success("**🎓 Orientações**\n\nAcompanhe orientações em andamento e concluídas")
    
    with col3:
        st.warning("**🔗 Colaborações**\n\nVisualize redes de colaboração entre pesquisadores")
    
    st.markdown("---")
    st.caption("Sistema desenvolvido utilizando https://github.com/jpmenachalco/scriptLattes e Streamlit")

if __name__ == "__main__":
    main()


