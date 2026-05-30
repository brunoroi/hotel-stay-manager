import streamlit as st
import pandas as pd
from datetime import datetime

def menu():
   while True:
        print("""
        === HOTEL ===
        
        1 - Check-in
        2 - Check-out
        3 - Ocupação
        4 - Histórico
        5 - Listar funcionários
              
        0 - Sair
            
    """)

        opcao = input("Escolha uma opção acima: ")
        print("\n")
        
        match opcao:
            case "1":
              listar_funcionarios()
              matricula = input("Matrícula: ")
              check_in(matricula)

            case "2":
              matricula = input("Matrícula: ")
              check_out(matricula)
            
            case "3":
              listar_ocupacao()

            case "4":
              listar_historico()
            
            case "5":
              listar_funcionarios()     

            case "0":
              break
           
            case _:
              print("Opção inválida.")


funcionarios = [
    {"matricula": "101", "nome": "Bruno", "sobrenome": "Andrade Ribeiro", "empresa": "RUMO"},
    {"matricula": "102", "nome": "Beatriz", "sobrenome": "Weber da Silva", "empresa": "RUMO"},
    {"matricula": "103", "nome": "Gerson", "sobrenome": "Ribeiro Sobrinho", "empresa": "RUMO"}
]

quartos = [
    {"numero": 1, "tipo": "normal"},
    {"numero": 2, "tipo": "normal"},
    {"numero": 3, "tipo": "normal"},
    {"numero": 4, "tipo": "normal"},
    {"numero": 5, "tipo": "normal"},
    {"numero": 6, "tipo": "extra"},
    {"numero": 7, "tipo": "extra"},
    {"numero": 8, "tipo": "extra"},
    {"numero": 9, "tipo": "extra"},
    {"numero": 10, "tipo": "extra"}
]

try:
    estadias = pd.read_csv("estadias.csv").to_dict("records")
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "id_estadia",
      "matricula",
      "numero_quarto",
      "data_checkin",
      "data_checkout",
      "status"
    ])

    df.to_csv("estadias.csv", index=False)

    estadias = []

def listar_funcionarios():
   print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
   for funcionario in funcionarios:
      print(f"Matrícula: {funcionario['matricula']} | Nome: {funcionario['nome']} {funcionario['sobrenome']} | Empresa: {funcionario['empresa']}\n")

def buscar_funcionario(matricula: str) -> dict | None:
  for funcionario in funcionarios:
    if funcionario["matricula"] == matricula:
      return funcionario
  return None

def buscar_quarto(numero: int) -> dict | None:
  for quarto in quartos:
    if quarto["numero"] == numero:
      return quarto
  return None

def buscar_estadia_ativa(matricula: str) -> dict | None:
  for estadia in estadias:
    if estadia["matricula"] == matricula and estadia["status"] == "ativa":
      return estadia
  return None

def quarto_esta_ocupado(numero_quarto: int) -> bool:
  for estadia in estadias:
    if estadia["numero_quarto"] == numero_quarto and estadia["status"] == "ativa":
      return True
  return False

def proximo_quarto_disponivel(tipo: str) -> dict | None:
  for quarto in quartos:
    if quarto["tipo"] == tipo and not quarto_esta_ocupado(quarto["numero"]):
      return quarto
  return None

def gerar_id_estadia() -> int:
  return len(estadias) + 1

def _salvar_estadias() -> None:
  df_estadias_temp = pd.DataFrame(estadias)
  df_estadias_temp.to_csv("estadias.csv", index=False)

def check_in(matricula: str) -> None:
  funcionario = buscar_funcionario(matricula)
  if not funcionario:
    print(f"[ERRO] Matrícula '{matricula}' não encontrada no cadastro.")
    return

  if buscar_estadia_ativa(matricula):
    print(f"[ERRO] O funcionário {funcionario['nome']} {funcionario['sobrenome']} já está hospedado.")
    return

  quarto = proximo_quarto_disponivel("normal") or proximo_quarto_disponivel("extra")
  if not quarto:
    print(f"[ERRO] Não há quartos disponíveis no momento.")
    return
  
  now = datetime.now()

  nova_estadia = {
      "id_estadia":    gerar_id_estadia(),
      "matricula":     matricula,
      "numero_quarto": quarto["numero"],
      "data_checkin":  now.strftime("%d/%m/%Y %H:%M:%S"),
      "data_checkout": None,
      "status":        "ativa",
  }
  estadias.append(nova_estadia)

  _salvar_estadias()

  tipo_label = "EXTRA (cota normal esgotada)" if quarto["tipo"] == "extra" else "normal"
  print(
      f"[CHECK-IN] {funcionario['nome']} {funcionario['sobrenome']} "
      f"→ Quarto {quarto['numero']} ({tipo_label}) | "
      f"Entrada: {nova_estadia['data_checkin']}"
    )

def check_out(matricula: str) -> None:
    funcionario = buscar_funcionario(matricula)
    if not funcionario:
        print(f"[ERRO] Matrícula '{matricula}' não encontrada no cadastro.")
        return
    estadia = buscar_estadia_ativa(matricula)
    if not estadia:
        print(f"[ERRO] O funcionário {funcionario['nome']} {funcionario['sobrenome']} não possui estadia ativa.")
        return

    now = datetime.now()

    estadia["data_checkout"] = now.strftime("%d/%m/%Y %H:%M:%S")
    estadia["status"] = "encerrada"

    _salvar_estadias()

    print(
      f"[CHECK-OUT] {funcionario['nome']} {funcionario['sobrenome']} "
      f"← Quarto {estadia['numero_quarto']} liberado | "
      f"Saída: {estadia['data_checkout']}"
    )  

def listar_ocupacao() -> None:
    """Exibe o status atual de todos os quartos."""
    print("\n--- STATUS DOS QUARTOS ---")
    for q in quartos:
        ocupado = quarto_esta_ocupado(q["numero"])
        hospede = ""
        if ocupado:
            for e in estadias:
                if e["numero_quarto"] == q["numero"] and e["status"] == "ativa":
                    f = buscar_funcionario(e["matricula"])
                    hospede = f" → {f['nome']} {f['sobrenome']}" if f else ""
        status = "OCUPADO" if ocupado else "LIVRE"
        print(f"  Quarto {q['numero']:>2} ({q['tipo']:>6}): {status}{hospede}")
    print()

def listar_historico() -> None:
    """Exibe o histórico completo de estadias."""
    print("\n--- HISTÓRICO DE ESTADIAS ---")
    if not estadias:
        print("  Nenhuma estadia registrada.")
        return
    for e in estadias:
        f = buscar_funcionario(e["matricula"])
        nome = f"{f['nome']} {f['sobrenome']}" if f else e["matricula"]
        saida = e["data_checkout"] or "em curso"
        print(
            f"  #{e['id_estadia']} | {nome} | "
            f"Quarto {e['numero_quarto']} | "
            f"Entrada: {e['data_checkin']} | Saída: {saida} | [{e['status'].upper()}]"
        )
    print()

if __name__ == "__main__":
    menu()
    
