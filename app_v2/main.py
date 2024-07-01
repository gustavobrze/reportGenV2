import streamlit as st
from base import client_list
from generate_pdf import genPDF

st.title("Gerador de Relatórios")

sheet = st.file_uploader('Selecione a planilha:')

if sheet:
    
    clients = client_list(sheet)

    client = st.selectbox("Selecione um cliente:", clients)

    #st.download_button(label="Gerar PDF", data=genPDF(sheet, client), file_name=f'{client.strip()}.pdf', mime='application/octet-stream')
    if st.button("Gerar PDF"):
    # Gerar PDF com base no nome selecionado e dados da planilha
        genPDF(sheet, client)

        with open("temp.pdf", "rb") as pdf_file:
            pdf = pdf_file.read()
        
        st.download_button('Baixar relatório', pdf, f'{client.strip()}.pdf', mime="application/octet-stream")
        pdf_file.close()
        st.success("Relatório gerado.")
