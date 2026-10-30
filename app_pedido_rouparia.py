import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Rouparia Hospitalar", layout="wide")
st.title("🧺 Sistema Avançado e Consolidado de Rouparia")

NOME_PLANILHA = "app de rouparia.xlsx"

# 📋 1. REGRAS DOS KITS PRINCIPAIS
KITS_CIRURGIAS = {
    "Cirurgia Ortopédica": {"Campos Cirúrgicos": 8, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 2, "Traçados": 3},
    "Cirurgia Geral": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Ginecologia": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Pediatria": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Bucomaxilo": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Urologia": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Vascular": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Otorrino": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Parto Vaginal": {"Campos Cirúrgicos": 4, "Aventais": 3, "Lençóis": 3, "Cobertores": 1, "Campos de Mesa": 1},
    "Pequena Cirurgia": {"Campos Fenestrados": 1, "Campos 70x70": 1},
    "Oftalmologia (Kit Padrão)": {"Campos Cirúrgicos": 4, "Avental": 1, "Lençóis": 1, "Campos 100x100": 1}
}

KITS_ADICIONAIS = {
    "Nenhum": {},
    "Raquianestesia": {"Campos 70x70": 2},
    "SVD (Sondagem Vesical de Demora)": {"Campos Fenestrados": 1},
    "Cateterismo Venoso Central (CVC)": {"Campos Fenestrados": 1, "Campos 70x70": 1}
}

LISTA_OUTROS_SETORES = [
    "Maternidade", "UTI 1", "UTI 2", "Clínica médica 1", "Clínica médica 2",
    "Clínica cirúrgica 1", "Clínica cirúrgica 2", "Emergência", "Estabilização",
    "Ambulatório", "Pediatria"
]

colunas = ["Data/Hora", "Setor/Categoria", "Item/Procedimento Base", "Tamanho", "Qtd Solicitada", "Status"]

if os.path.exists(NOME_PLANILHA):
    try:
        df = pd.read_excel(NOME_PLANILHA)
        for col in colunas:
            if col not in df.columns:
                df[col] = None
    except Exception:
        df = pd.DataFrame(columns=colunas)
else:
    df = pd.DataFrame(columns=colunas)

# 🎨 Configuração de colunas para exibição limpa
config_colunas = {
    "Status": st.column_config.TextColumn("Situação", help="Status de entrega"),
    "Qtd Solicitada": st.column_config.NumberColumn("Qtd")
}

# Funções auxiliares para gerar relatórios de texto formatados para impressão
def converter_para_relatorio_texto(dataframe, titulo):
    linhas_texto = [f"=== {titulo.upper()} ===", f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n", dataframe.to_string(index=False)]
    return "\n".join(linhas_texto)

# 🗓️ Abas Principais
aba_pedidos, aba_consolidado = st.tabs(["📝 Lançar Novos Pedidos", "📊 Painel da Rouparia (Consolidado e Filtros)"])

data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
linhas_para_salvar = []

# ==================== ABA 1: LANÇAMENTO DE PEDIDOS ====================
with aba_pedidos:
    aba_cc, aba_cme, aba_oftalmo, aba_outros = st.tabs([
        "🏥 Centro Cirúrgico", "🧪 CME", "👁️ Oftalmologia (Avulsos)", "🏢 Outros Setores"
    ])

    with aba_cc:
        st.subheader("Registrar Demanda do Centro Cirúrgico")
        with st.form("form_cc", clear_on_submit=True):
            procedimento_principal = st.selectbox("Selecione a Cirurgia", list(KITS_CIRURGIAS.keys()))
            qtd_principal = st.number_input("Número de Cirurgias", min_value=1, value=1, step=1)
            adicional_selecionado = st.selectbox("Procedimento adicional / Anestesia?", list(KITS_ADICIONAIS.keys()))
            qtd_adicional = st.number_input("Número de adicionais", min_value=0, value=0, step=1)
            btn_cc = st.form_submit_button("Gerar Pedido Centro Cirúrgico")
            if btn_cc:
                for item, qtd_un in KITS_CIRURGIAS[procedimento_principal].items():
                    linhas_para_salvar.append({"Data/Hora": data_atual, "Setor/Categoria": "Centro Cirúrgico", "Item/Procedimento Base": f"{procedimento_principal} - {item}", "Tamanho": "N/A", "Qtd Solicitada": qtd_un * qtd_principal, "Status": "🔴 Pendente"})
                if adicional_selecionado != "Nenhum" and qtd_adicional > 0:
                    for item, qtd_un in KITS_ADICIONAIS[adicional_selecionado].items():
                        linhas_para_salvar.append({"Data/Hora": data_atual, "Setor/Categoria": "Centro Cirúrgico", "Item/Procedimento Base": f"{adicional_selecionado} - {item}", "Tamanho": "N/A", "Qtd Solicitada": qtd_un * qtd_adicional, "Status": "🔴 Pendente"})

    with aba_cme:
        st.subheader("Registrar Pedido para CME")
        with st.form("form_cme", clear_on_submit=True):
            item_cme = st.selectbox("Selecione o Item", ["Unissex", "Campos Simples", "Campos 100x100", "Campos Velhos de Expurgo", "Capa de Arco"])
            tamanho_cme = st.selectbox("Tamanho (Se aplicável)", ["N/A", "P", "M", "G", "GG", "EXGG"])
            qtd_cme = st.number_input("Quantidade", min_value=1, value=1, step=1, key="q_cme")
            btn_cme = st.form_submit_button("Gravar Pedido CME")
            if btn_cme:
                linhas_para_salvar.append({"Data/Hora": data_atual, "Setor/Categoria": "CME", "Item/Procedimento Base": item_cme, "Tamanho": tamanho_cme, "Qtd Solicitada": qtd_cme, "Status": "🔴 Pendente"})

    with aba_oftalmo:
        st.subheader("Itens Específicos - Oftalmologia")
        with st.form("form_oftalmo", clear_on_submit=True):
            item_oft = st.selectbox("Selecione o Item Avulso", ["Pijama Paciente", "Unissex (Equipe)", "Campos Cirúrgicos", "Avental", "Lençóis", "Campo 100x100"])
            tamanho_oft = st.selectbox("Tamanho (Se aplicável)", ["N/A", "P", "M", "G", "GG", "EXGG"], key="t_oft")
            qtd_oft = st.number_input("Quantidade", min_value=1, value=1, step=1, key="q_oft")
            btn_oft = st.form_submit_button("Gravar Pedido Oftalmologia")
            if btn_oft:
                linhas_para_salvar.append({"Data/Hora": data_atual, "Setor/Categoria": "Oftalmologia", "Item/Procedimento Base": item_oft, "Tamanho": tamanho_oft, "Qtd Solicitada": qtd_oft, "Status": "🔴 Pendente"})

    with aba_outros:
        st.subheader("Pedidos para Setores de Internação e Unidades")
        with st.form("form_outros", clear_on_submit=True):
            setor_especifico = st.selectbox("Selecione o Setor Solicitante", LISTA_OUTROS_SETORES)
            item_outros = st.selectbox("Selecione o Item", ["Lençóis", "Fronhas", "Cobertores", "Unissex", "Traçados", "Toalhas", "Pijamas"])
            tamanho_outros = st.selectbox("Tamanho (Se aplicável)", ["N/A", "P", "M", "G", "GG", "EXGG"], key="t_outros")
            qtd_outros = st.number_input("Quantidade", min_value=1, value=1, step=1, key="q_outros")
            btn_outros = st.form_submit_button("Gravar Pedido Outros Setores")
            if btn_outros:
                linhas_para_salvar.append({"Data/Hora": data_atual, "Setor/Categoria": setor_especifico, "Item/Procedimento Base": item_outros, "Tamanho": tamanho_outros, "Qtd Solicitada": qtd_outros, "Status": "🔴 Pendente"})

# PROCESSAMENTO DE SALVAMENTO
if linhas_para_salvar:
    df_novos = pd.DataFrame(linhas_para_salvar)
    df = pd.concat([df, df_novos], ignore_index=True)
    df.to_excel(NOME_PLANILHA, index=False)
    st.success("✅ Pedido(s) registrado(s) com sucesso!")
    st.rerun()

# ==================== ABA 2: PAINEL DA ROUPARIA / GERENCIAL ====================
with aba_consolidado:
    if not df.empty:
        # --- SEÇÃO 1: CONSOLIDADO GERAL DE ROUPAS ---
        col_tit, col_btn = st.columns(2)
        with col_tit:
            st.subheader("📊 Totais Consolidados (Para Separação no Estoque)")
            st.markdown("Soma de itens com status **Pendente** para agilizar a distribuição física:")
        
        # Agrupamento inteligente por Item + Tamanho (filtrando pelo emoji de pendente)
        df_pendentes = df[df["Status"].str.contains("Pendente", na=False)]
        
        if not df_pendentes.empty:
            df_agrupado = df_pendentes.groupby(["Item/Procedimento Base", "Tamanho"])["Qtd Solicitada"].sum().reset_index()
            df_agrupado.columns = ["Item / Roupa Descrição", "Tamanho", "Total Geral a Separar"]
            st.dataframe(df_agrupado, use_container_width=True)
            with col_btn:
                txt_print_agrupado = converter_para_relatorio_texto(df_agrupado, "Lista de Separacao da Rouparia - Consolidado")
                st.download_button(
                    label="📄 Exportar Lista de Separação (.txt)",
                    data=txt_print_agrupado,
                    file_name=f"separacao_rouparia_{datetime.now().strftime('%d_%m_%H%M')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("Nenhum item pendente para consolidação no momento.")

        st.markdown("---")

        # --- SEÇÃO 2: FILTROS E HISTÓRICO DETALHADO ---
        st.subheader("🔍 Filtros de Busca e Controle de Status")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            todos_setores = ["Todos"] + sorted(list(df["Setor/Categoria"].dropna().unique()))
            setor_filtrado = st.selectbox("Filtrar por Setor/Origem", todos_setores)
        with c2:
            todos_status = ["Todos", "Pendente", "Entregue"]
            status_filtrado = st.selectbox("Filtrar por Status", todos_status)
        with c3:
            marcar_entregue = st.checkbox("Habilitar Painel de Baixas/Entregas")

        # Aplicação dos filtros no DataFrame exibido
        df_filtrado = df.copy()
        if setor_filtrado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Setor/Categoria"] == setor_filtrado]
