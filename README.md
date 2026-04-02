# 🚀 LembraZap PRO v2.0
> Automação Inteligente para Mensagens e Fidelização de Clientes.

O **LembraZap PRO** é uma ferramenta desktop desenvolvida em Python para otimizar o fluxo de comunicação de pequenos negócios e empreendedores. O projeto foca em escalabilidade, segurança e facilidade de uso.


<img width="462" height="600" alt="Untitled design (2)" src="https://github.com/user-attachments/assets/02fcb197-13ed-46dc-bf99-3a4cef08d4c0" />

<img width="462" height="600" alt="Untitled design (1)" src="https://github.com/user-attachments/assets/c7540511-9e36-4458-a8ce-63d3aa6b00d1" />

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Interface Gráfica:** `CustomTkinter` (Modern UI/UX)
* **Automação:** `PyWhatKit` e `PyAutoGUI`
* **Dados:** `Pandas` para processamento de listas e `Requests` para integração com API.
* **Segurança:** Sistema de Login persistente via **Google Sheets** (CSV dinâmico).

## ✨ Funcionalidades Principais
* **Gestão de Clientes:** Cadastro e exclusão de contatos com histórico de último envio.
* **Autenticação na Nuvem:** Acesso restrito controlado via planilha remota (permite revogar acesso em tempo real).
* **Disparos Inteligentes:**
    * Variáveis personalizadas (ex: "Olá {nome}").
    * Intervalos aleatórios entre mensagens para evitar bloqueios.
    * Filtro anti-duplicidade (não envia para quem já recebeu no dia).
* **Multi-threading:** Processamento em segundo plano para manter a interface responsiva durante os envios.

## 📦 Como gerar o Executável (.exe)
Para compilar o projeto com todas as dependências visuais, utilize o comando:
```bash
pyinstaller --noconsole --onefile --clean --collect-all customtkinter --icon=logo.ico --name "LembraZap_PRO" LembraZap_2.0.py
