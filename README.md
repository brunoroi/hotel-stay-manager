# 🏨 Hotel Stay Manager

Sistema de gerenciamento de fluxo de hóspedes para hotéis de pequeno porte, com suporte a contratos com empresas terceiras. Desenvolvido em Python com persistência em CSV via Pandas.

## 💡 Contexto

O sistema foi criado para substituir o controle manual feito em planilhas por uma empresa parceira. A lógica principal é a alocação automática de quartos: funcionários da empresa parceira ocupam primeiro os quartos da cota normal e, caso esteja lotada, são alocados automaticamente em quartos extras.

## ✅ Funcionalidades

- Check-in com alocação automática de quarto (normal → extra)
- Check-out com registro de horário de saída
- Listagem de ocupação em tempo real
- Histórico completo de estadias
- Listagem de funcionários cadastrados

## 🛠️ Tecnologias

- Python 3.10+
- Pandas — persistência de dados em CSV
- Streamlit — interface visual (em desenvolvimento)

## 📁 Estrutura

```
hotel-stay-manager/
│
├── hotel.py          # lógica principal do sistema
├── estadias.csv      # gerado automaticamente na primeira execução
└── README.md
```

## ▶️ Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/hotel-stay-manager.git
cd hotel-stay-manager
```

**2. Instale as dependências**
```bash
pip install pandas streamlit
```

**3. Execute o sistema via terminal**
```bash
python hotel.py
```

**4. Ou via interface Streamlit (em breve)**
```bash
python -m streamlit run app.py
```

## 📌 Status do projeto

🚧 Em desenvolvimento — interface Streamlit sendo implementada.
