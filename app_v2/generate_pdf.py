import fpdf
from base import generateReport
from datetime import datetime as dt
import streamlit as st
import os

@st.cache_data
def genPDF(sheet, client):

    report = generateReport(sheet, client)
    name = report[0]
    i = report[2]
    vi = report[4]
    vacc = report[5]
    df = report[3]

    # Crie um objeto FPDF
    pdf = fpdf.FPDF()

    # Defina o formato da página
    pdf.add_page()
    pdf.image('logo.png', x=90, y=00, w=30, h=30)
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0,10, 'Demonstrativo mensal', align='C')
    # Adicione o logo da empresa

    # Nome, CPF e data de hoje centralizados
    pdf.ln(20)
    pdf.set_x(10)  # Posicione o cursor no centro da página
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, f'Cliente: {name}')
    pdf.set_x(90)
    pdf.set_x(160)
    pdf.cell(0, 10, f'Data: {dt.today().strftime("%d/%m/%Y")}')

    pdf.ln(20)

    pdf.set_x(10)
    pdf.cell(0, 10, f'Rentabilidade Contratada: {i}')
    pdf.set_x(80)
    pdf.cell(0, 10, f'Valor Aportado: {vi}')
    pdf.set_x(150)
    pdf.cell(0, 10, f'Valor Atual: {vacc}')

    pdf.ln(30)

    pdf.set_x(25)
    # Print DataFrame header with borders and centered alignment
    pdf.set_fill_color(0, 52, 135)  # Light gray background for header
    pdf.set_text_color(255, 255, 255)  # Black text color
    for col_index, col_name in enumerate(df.columns):
        pdf.cell(40, 5, col_name, border=1, align='C', fill=True)
    pdf.ln(5)  # Line break after header


    # Print DataFrame data with borders
    pdf.set_fill_color(255, 255, 255)  # White background for data cells
    pdf.set_text_color(0, 0, 0)  # Black text color
    for index, row in df.iterrows():
        pdf.set_x(25)
        for col_index, value in enumerate(row):
            pdf.cell(40, 5, str(value), border=1, align='C', fill=True)
        pdf.ln(5)  # Line break after each row

    # Combinar nome do arquivo e diretório de salvamento

    # Salvar o PDF
    return pdf.output('temp.pdf')
