import streamlit as st
from hotel import check_in, check_out, listar_ocupacao, listar_historico, listar_funcionarios, estadias, quartos, funcionarios, buscar_funcionario, quarto_esta_ocupado
import pandas as pd

# ── Estado inicial ──────────────────────────────────────────────
if "tela" not in st.session_state:
    st.session_state.tela = "menu"

# ── Cabeçalho ───────────────────────────────────────────────────
st.title("🏨 Hotel do Ary")
st.subheader("Sistema de gerenciamento hoteleiro")
st.divider()

# ── MENU ────────────────────────────────────────────────────────
if st.session_state.tela == "menu":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Check-in", use_container_width=True):
            st.session_state.tela = "checkin"
            st.rerun()
        if st.button("📋 Ocupação", use_container_width=True):
            st.session_state.tela = "ocupacao"
            st.rerun()
        if st.button("👥 Funcionários", use_container_width=True):
            st.session_state.tela = "funcionarios"
            st.rerun()
    with col2:
        if st.button("🚪 Check-out", use_container_width=True):
            st.session_state.tela = "checkout"
            st.rerun()
        if st.button("📜 Histórico", use_container_width=True):
            st.session_state.tela = "historico"
            st.rerun()

# ── CHECK-IN ────────────────────────────────────────────────────
elif st.session_state.tela == "checkin":
    st.subheader("✅ Check-in")
    matricula = st.text_input("Matrícula do funcionário:")
    if st.button("Executar"):
        if matricula:
            sucesso, mensagem = check_in(matricula)
            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)
        else:
            st.warning("Digite uma matrícula.")
    if st.button("← Voltar"):
        st.session_state.tela = "menu"
        st.rerun()


# ── CHECK-OUT ───────────────────────────────────────────────────
elif st.session_state.tela == "checkout":
    st.subheader("🚪 Check-out")
    matricula = st.text_input("Matrícula do funcionário:")
    if st.button("Executar"):
        if matricula:
            sucesso, mensagem = check_out(matricula)
            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)
        else:
            st.warning("Digite uma matrícula.")
    if st.button("← Voltar"):
        st.session_state.tela = "menu"
        st.rerun()

# ── OCUPAÇÃO ────────────────────────────────────────────────────
elif st.session_state.tela == "ocupacao":
    st.subheader("📋 Ocupação atual")
    estadias_atuais = pd.read_csv("estadias.csv").to_dict("records")
    dados = []
    for q in quartos:
        ocupado = any(e["numero_quarto"] == q["numero"] and e["status"] == "ativa" for e in estadias_atuais)
        hospede = ""
        if ocupado:
            for e in estadias_atuais:
                if e["numero_quarto"] == q["numero"] and e["status"] == "ativa":
                    f = buscar_funcionario(e["matricula"])
                    hospede = f"{f['nome']} {f['sobrenome']}" if f else e["matricula"]
        dados.append({
            "Quarto": q["numero"],
            "Tipo": q["tipo"].capitalize(),
            "Status": "🔴 Ocupado" if ocupado else "🟢 Livre",
            "Hóspede": hospede
        })
    st.dataframe(dados, use_container_width=True)
    if st.button("← Voltar"):
        st.session_state.tela = "menu"
        st.rerun()

# ── HISTÓRICO ───────────────────────────────────────────────────
elif st.session_state.tela == "historico":
    st.subheader("📜 Histórico de estadias")
    estadias_atuais = pd.read_csv("estadias.csv").to_dict("records")
    if not estadias_atuais:
        st.info("Nenhuma estadia registrada.")
    else:
        dados = []
        for e in estadias_atuais:
            f = buscar_funcionario(str(e["matricula"]))
            nome = f"{f['nome']} {f['sobrenome']}" if f else e["matricula"]
            dados.append({
                "#": e["id_estadia"],
                "Funcionário": nome,
                "Quarto": e["numero_quarto"],
                "Entrada": e["data_checkin"],
                "Saída": e["data_checkout"] if e["data_checkout"] else "Em curso",
                "Status": e["status"].capitalize()
            })
        st.dataframe(dados, use_container_width=True)
    if st.button("← Voltar"):
        st.session_state.tela = "menu"
        st.rerun()

# ── FUNCIONÁRIOS ────────────────────────────────────────────────
elif st.session_state.tela == "funcionarios":
    st.subheader("👥 Funcionários cadastrados")
    st.dataframe(funcionarios, use_container_width=True)
    if st.button("← Voltar"):
        st.session_state.tela = "menu"
        st.rerun()