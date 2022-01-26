import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

from urllib.error import URLError

# https://towardsdatascience.com/deploying-your-ml-model-using-streamlit-and-ngrok-c2eea3fd9763
#
# df.isnull().sum() #checking for null values in our data
# df.describe() #checking various values such as mean, median of different columnss and so on
#


@st.cache
def get_BB_dados():
    df = pd.read_excel(
        "imoveisBB_4a.xlsx"
    )  # "C:\Users\earau\PYTHON2022\imoveisBB_4a.xlsx"

    df = df[df["Vlr_venda_imovel"].str.contains(r"R$ ", na=True) == True]
    df.drop(df[df["Vlr_venda_imovel"] == "Sob consulta"].index, inplace=True)
    # pd.set_option("display.float_format", "{:.2f}".format)
    df["Vlr_venda_imovel"] = df["Vlr_venda_imovel"].astype(float)
    return df
    # return df.set_index("Estado_imovel")  # nro_imovel


try:

    default_Colunas = [
        "nro_imovel",
        # "link_imovel",
        # "desc_imovel",
        "desc_imovel_detalhe",
        "Vlr_venda_imovel",
        "Desc%",
        # "Cidade_imovel",
        # "Estado_imovel",
        # "end_imovel",
        # "status_imovel",
        # "Desc_imovel_numeros",
        # "GRUPO",
        # "GRUPO_DESC",
        # "Area1",
        # "GRUPO_AREA",
        # "Situacao",
        # "TipoVenda",
    ]

    df = get_BB_dados()
    lista_Estados = list(df["Estado_imovel"].drop_duplicates())

    lista_Situacao = list(df["Situacao"].drop_duplicates())
    lista_TipoVenda = list(df["TipoVenda"].drop_duplicates())

    lista_Desconto = list(df["GRUPO_DESC"].drop_duplicates())
    lista_Area = list(df["GRUPO_AREA"].drop_duplicates())

    add_selectbox = st.sidebar.selectbox(
        "Versão Planilha", ("Básica", "A Implementar", "A implementar")
    )

    colunas = st.sidebar.multiselect(
        "Escolha as Colunas que deseja ver:",
        df.columns.tolist(),
        default=default_Colunas,
    )

    escolha_Situacao = st.sidebar.multiselect(
        "Estados:", lista_Situacao, default=lista_Situacao
    )

    escolha_TipoVenda = st.sidebar.multiselect(
        "Cidades:", lista_TipoVenda, default=lista_TipoVenda
    )

    range_precos = st.sidebar.slider(
        "Preço Máximo:", min_value=0.0, max_value=1000000.0, step=10000.0, value=50000.0
    )
    escolha_Estado = st.sidebar.multiselect(
        "Estados:", lista_Estados, default=lista_Estados
    )

    escolha_Desconto = st.sidebar.multiselect(
        "Desconto:", lista_Desconto, default=lista_Desconto
    )

    escolha_Area = st.sidebar.multiselect("Área:", lista_Area, default=lista_Area)

    if not colunas:
        st.error("Favor selecionar ao menos uma coluna.")
    else:
        # https://pythonforundergradengineers.com/streamlit-app-with-bokeh.html 
        # st.title("Simple Streamlit App")
        # st.text("Type a number in the box below")
        # n = st.number_input("Number", step=1)
        # st.write(f"{n} + 1 = {n+1}")
        # s = st.text_input("Type a name in the box below")
        # st.write(f"Hello {s}")

        st.markdown(
            "<h1 style='text-align: center; color: White;background-color:#e84343'>Exposição do Dataframe</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: Black;'>Imóveis BB</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h4 style='text-align: center; color: Black;'>Janeiro/2022</h4>",
            unsafe_allow_html=True,
        )
        st.sidebar.header("Será que ajuda na análise dos dados?")
        st.sidebar.text(
            "Creio que sim, pois permite fazer filtros e ver o resultado na hora."
        )
        st.sidebar.header("Vai ser atualizado?")
        st.sidebar.text("Sim, mensalmente!")

        df = df[df["Situacao"].isin(escolha_Situacao)]
        df = df[df["TipoVenda"].isin(escolha_TipoVenda)]
        df = df[df["Estado_imovel"].isin(escolha_Estado)]
        df = df[df["GRUPO_DESC"].isin(escolha_Desconto)]
        df = df[df["GRUPO_AREA"].isin(escolha_Area)]
        df = df[df["Vlr_venda_imovel"] < range_precos]

        st.dataframe(
            df[colunas].style.format({"Vlr_venda_imovel": "{:.2f}"}), 1200, 700
        )


except URLError as e:
    st.error(
        """
        **Este demo necessita de acesso a internet**

        Erro de Conexão: %s
    """
        % e.reason
    )


# from pyngrok import ngrok
# !ngrok authtoken [Enter your authtoken here]

# só LINUX ??? !nohup streamlit run app.py &
# só pra assinantes do ngrok  ... url = ngrok.connect(port = 8501)
# só pra assinantes do ngrok  ... url #generates our URL

# !streamlit run --server.port 80 app.py >/dev/null #used for starting our server
