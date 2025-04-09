
import streamlit as st
from datetime import datetime
from googletrans import Translator
import pandas as pd
from pathlib import Path

# Inicializa o tradutor
translator = Translator()

# Configurações da página
st.set_page_config(page_title="Pendências ArcelorMittal", layout="wide")
st.markdown("## 📋 Pendências ArcelorMittal")

# Caminho do arquivo Excel para salvar os dados
arquivo_excel = Path("pendencias_arcelormittal.xlsx")

with st.form("form_pendencia", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        planta = "BWWTP"
        st.text_input("Planta", value=planta, disabled=True)
        fase = st.radio("Fase", ["Construção", "Comissionamento"])
        impedimento = st.radio("Impedimento?", ["Sim", "Não"])
        prioridade = st.radio("Prioridade", ["0", "1", "2"])

    with col2:
        data = datetime.now().strftime("%Y/%m/%d %H:%M")
        st.text_input("Data", value=data, disabled=True)
        tag = st.text_input("TAG")
        sistema_teste = st.text_input("Sistema de teste")
        disciplina = st.selectbox("Disciplina", ["Electric", "Instrumentation", "Mechanic", "Piping", "Process"])

    with col3:
        descricao_en = st.text_area("Descrição en-us")
        descricao_pt = st.text_area("Descrição pt-br")
        companhia = st.text_input("Executado por / Responsabilidade")
        responsavel = st.text_input("Responsável pela abertura")

    # Tradução automática
    if descricao_pt and not descricao_en:
        try:
            descricao_en = translator.translate(descricao_pt, src='pt', dest='en').text
        except:
            st.warning("Erro ao traduzir do português para o inglês.")
    elif descricao_en and not descricao_pt:
        try:
            descricao_pt = translator.translate(descricao_en, src='en', dest='pt').text
        except:
            st.warning("Erro ao traduzir do inglês para o português.")

    st.text_area("Descrição en-us traduzida", value=descricao_en, height=100, disabled=True)
    st.text_area("Descrição pt-br traduzida", value=descricao_pt, height=100, disabled=True)

    campos_obrigatorios = all([tag, sistema_teste, disciplina, descricao_pt, descricao_en, companhia, responsavel])

    submit = st.form_submit_button("Salvar Pendência")
    if submit:
        if campos_obrigatorios:
            nova_linha = pd.DataFrame([{
                "Data": data,
                "TAG": tag,
                "Sistema de Teste": sistema_teste,
                "Disciplina": disciplina,
                "Fase": fase,
                "Planta": planta,
                "Impedimento": impedimento,
                "Prioridade": prioridade,
                "Descrição pt-br": descricao_pt,
                "Descrição en-us": descricao_en,
                "Executado por / Responsabilidade": companhia,
                "Responsável pela abertura": responsavel
            }])

            if arquivo_excel.exists():
                df_existente = pd.read_excel(arquivo_excel)
                df_completo = pd.concat([df_existente, nova_linha], ignore_index=True)
            else:
                df_completo = nova_linha

            df_completo.to_excel(arquivo_excel, index=False)
            st.success("✅ Pendência salva com sucesso!")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos antes de salvar.")
