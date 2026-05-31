import streamlit as st
from hotel import check_in, check_out, listar_ocupacao, listar_historico, listar_funcionarios

# st.title("Hotel do Ary")
# st.subheader("Sistema de gerenciamento hoteleiro")
# st.text("Menu")
# st.button("Check-in")
# st.button("Check-out")
# st.button("Histórico")
# st.button("Listar Ocupação")
# st.button("Listar Funcionários")

# if st.button("Check-in"):
#     st.text_input("Matrícula:")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Check-in', on_click=click_button)

if st.session_state.clicked:
    st_matricula = st.text_input("Matrícula:")  
    st.button("Executar", on_click=check_in, args=(st_matricula,))