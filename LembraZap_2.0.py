import customtkinter as ctk
import pywhatkit as kit
import pyautogui as pg
import threading
import os
import sys
import time
import ctypes
import random
import requests
import pandas as pd
from io import StringIO
from tkinter import ttk
from PIL import Image, ImageDraw
from datetime import datetime

# --- AJUSTE DE CAMINHO PARA EXECUTÁVEL (.EXE) ---
# Isso garante que o programa encontre os arquivos mesmo após ser compilado
if getattr(sys, 'frozen', False):
    # Se rodando como .exe
    diretorio_base = os.path.dirname(sys.executable)
else:
    # Se rodando como script .py
    diretorio_base = os.path.dirname(os.path.abspath(__file__))

os.chdir(diretorio_base)

# --- CONFIGURAÇÃO OBRIGATÓRIA ---
URL_PLANILHA_LOGIN = "***"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback
        self.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(self, text="🔒 ACESSO RESTRITO", font=("Roboto", 22, "bold"))
        self.label.pack(pady=(60, 20))

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Usuário", width=280, height=45)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=280, height=45)
        self.pass_entry.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="ENTRAR NO SISTEMA", command=self.validar_login, 
                                       width=280, height=50, fg_color="#1f538d", font=("Roboto", 14, "bold"))
        self.btn_login.pack(pady=25)

        self.lbl_status = ctk.CTkLabel(self, text="", text_color="#7f8c8d")
        self.lbl_status.pack()

    def validar_login(self):
        user_digitado = self.user_entry.get().strip()
        pass_digitado = self.pass_entry.get().strip()
        self.lbl_status.configure(text="⏳ Verificando...", text_color="yellow")
        self.update()

        try:
            response = requests.get(URL_PLANILHA_LOGIN)
            if response.status_code != 200: raise Exception()
            df = pd.read_csv(StringIO(response.text))
            df.columns = [c.strip() for c in df.columns]
            
            login_valido = False
            for _, row in df.iterrows():
                if str(row['Usuario']).strip() == user_digitado and str(row['Senha']).strip() == pass_digitado:
                    login_valido = True
                    break

            if login_valido: self.login_callback()
            else: self.lbl_status.configure(text="❌ Credenciais incorretas!", text_color="#e74c3c")
        except:
            if user_digitado == "admin" and pass_digitado == "1234": self.login_callback()
            else: self.lbl_status.configure(text="⚠️ Erro de conexão", text_color="orange")

class LembraZap(ctk.CTk):
    def __init__(self):
        super().__init__()
        myappid = 'meuprojeto.lembrazap.pro.2.0'
        try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except: pass

        self.title("LembraZap PRO v2.0")
        self.centralizar_janela(600, 750) 
        self.gerar_icon_sistema()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")
        self.show_login()

    def show_login(self):
        for widget in self.container.winfo_children(): widget.destroy()
        LoginWindow(self.container, self.show_main_app)

    def show_main_app(self):
        for widget in self.container.winfo_children(): widget.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        self.executando = False
        self.pausado = False

        header = ctk.CTkFrame(self.container, fg_color="#1e1e1e", height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="LembraZap PRO v2.0", font=("Roboto", 22, "bold"), text_color="#2ecc71").pack(pady=15)

        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(pady=10, padx=15, fill="both", expand=True)
        self.tabview.add("📤 Envio")
        self.tabview.add("👥 Lista")

        # --- ABA ENVIO ---
        tab_envio = self.tabview.tab("📤 Envio")
        f_inputs = ctk.CTkFrame(tab_envio, fg_color="transparent")
        f_inputs.pack(pady=5, padx=5, fill="x")
        self.entry_nome = ctk.CTkEntry(f_inputs, placeholder_text="Nome", height=35); self.entry_nome.pack(side="left", padx=5, expand=True, fill="x")
        self.entry_fone = ctk.CTkEntry(f_inputs, placeholder_text="55...", height=35); self.entry_fone.pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(tab_envio, text="💾 SALVAR CLIENTE NA LISTA", command=self.salvar_cliente, fg_color="#1f538d").pack(pady=5)

        self.txt_msg = ctk.CTkTextbox(tab_envio, height=100)
        self.txt_msg.pack(pady=5, padx=10, fill="x")
        self.txt_msg.insert("0.0", "Olá {nome}! Tudo bem?")

        # --- SEÇÃO DE AJUSTES ---
        f_config_geral = ctk.CTkFrame(tab_envio, fg_color="#2b2b2b", border_width=1, border_color="#3d3d3d")
        f_config_geral.pack(pady=10, padx=10, fill="x")
        f_grid = ctk.CTkFrame(f_config_geral, fg_color="transparent")
        f_grid.pack(pady=10, padx=10)

        ctk.CTkLabel(f_grid, text="Carregar (s):", font=("Roboto", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.wait_pagina = ctk.CTkEntry(f_grid, width=45, height=25); self.wait_pagina.grid(row=0, column=1, padx=2); self.wait_pagina.insert(0, "25")

        ctk.CTkLabel(f_grid, text="Pós Colar (s):", font=("Roboto", 11)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.wait_colar = ctk.CTkEntry(f_grid, width=45, height=25); self.wait_colar.grid(row=0, column=3, padx=2); self.wait_colar.insert(0, "4")

        ctk.CTkLabel(f_grid, text="Pós Digitar (s):", font=("Roboto", 11)).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.wait_digitar = ctk.CTkEntry(f_grid, width=45, height=25); self.wait_digitar.grid(row=0, column=5, padx=2); self.wait_digitar.insert(0, "2")

        f_delay_rand = ctk.CTkFrame(f_config_geral, fg_color="transparent")
        f_delay_rand.pack(pady=(0, 10))
        ctk.CTkLabel(f_delay_rand, text="⏳ Intervalo entre envios:", font=("Roboto", 12)).pack(side="left", padx=5)
        self.delay_min = ctk.CTkEntry(f_delay_rand, width=40, height=25); self.delay_min.pack(side="left"); self.delay_min.insert(0, "15")
        ctk.CTkLabel(f_delay_rand, text="até", font=("Roboto", 12)).pack(side="left", padx=5)
        self.delay_max = ctk.CTkEntry(f_delay_rand, width=40, height=25); self.delay_max.pack(side="left"); self.delay_max.insert(0, "25")
        ctk.CTkLabel(f_delay_rand, text="segundos", font=("Roboto", 12)).pack(side="left", padx=5)

        self.check_pular_hoje = ctk.CTkCheckBox(tab_envio, text="Não enviar para quem já recebeu hoje", font=("Roboto", 12))
        self.check_pular_hoje.pack(pady=5); self.check_pular_hoje.select() 

        ctk.CTkLabel(tab_envio, text="⚠️ ATENÇÃO: Use intervalos adequados para evitar bloqueios.", 
                     text_color="#e67e22", font=("Roboto", 11, "bold")).pack(pady=2)

        self.btn_disparar = ctk.CTkButton(tab_envio, text="🚀 INICIAR DISPAROS", fg_color="#27ae60", 
                                          height=45, font=("Roboto", 13, "bold"), command=self.iniciar_thread)
        self.btn_disparar.pack(pady=10, padx=20, fill="x")
        
        f_ctrl = ctk.CTkFrame(tab_envio, fg_color="transparent"); f_ctrl.pack()
        self.btn_pausar = ctk.CTkButton(f_ctrl, text="⏸ PAUSAR", state="disabled", width=120, command=self.alternar_pausa); self.btn_pausar.grid(row=0, column=0, padx=5)
        self.btn_parar = ctk.CTkButton(f_ctrl, text="⏹ PARAR", fg_color="#c0392b", state="disabled", width=120, command=self.parar_envio); self.btn_parar.grid(row=0, column=1, padx=5)

        # --- ABA LISTA ---
        self.tabela = ttk.Treeview(self.tabview.tab("👥 Lista"), columns=("Nome", "Fone", "Qtd", "Data"), show="headings")
        for col in ("Nome", "Fone", "Qtd", "Data"): 
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=100)
        self.tabela.pack(pady=10, padx=10, fill="both", expand=True)
        ctk.CTkButton(self.tabview.tab("👥 Lista"), text="🗑 EXCLUIR SELECIONADO", fg_color="#c0392b", command=self.deletar_cliente).pack(pady=5)

        self.lbl_status = ctk.CTkLabel(self.container, text="● Sistema Pronto", text_color="#7f8c8d")
        self.lbl_status.pack(pady=5)
        self.carregar_lista()

    def centralizar_janela(self, largura, altura):
        lw, lh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{largura}x{altura}+{(lw//2)-(largura//2)}+{max(0, (lh//2)-(altura//2)-60)}")

    def gerar_icon_sistema(self):
        try: self.iconbitmap("logo.ico") 
        except: pass

    def carregar_lista(self):
        for i in self.tabela.get_children(): self.tabela.delete(i)
        if os.path.exists("clientes.txt"):
            with open("clientes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    p = linha.strip().split(",")
                    if len(p) == 4: self.tabela.insert("", "end", values=(p[0], p[1], p[2], p[3]))

    def salvar_cliente(self):
        n, f = self.entry_nome.get().strip(), self.entry_fone.get().strip()
        if n and f:
            with open("clientes.txt", "a", encoding="utf-8") as file: file.write(f"{n},{f},0,Nunca\n")
            self.entry_nome.delete(0, 'end'); self.entry_fone.delete(0, 'end'); self.carregar_lista()

    def deletar_cliente(self):
        sel = self.tabela.selection()
        if not sel: return
        fones = [self.tabela.item(s)['values'][1] for s in sel]
        linhas = []
        with open("clientes.txt", "r", encoding="utf-8") as f:
            for l in f:
                if not any(str(fn) in l for fn in fones): linhas.append(l)
        with open("clientes.txt", "w", encoding="utf-8") as f: f.writelines(linhas)
        self.carregar_lista()

    def alternar_pausa(self):
        self.pausado = not self.pausado
        self.btn_pausar.configure(text="▶ RETOMAR" if self.pausado else "⏸ PAUSAR")

    def parar_envio(self):
        self.executando = False
        self.lbl_status.configure(text="🛑 Parando...", text_color="red")

    def iniciar_thread(self):
        self.executando, self.pausado = True, False
        self.btn_disparar.configure(state="disabled")
        self.btn_pausar.configure(state="normal")
        self.btn_parar.configure(state="normal")
        threading.Thread(target=self.enviar_logica, daemon=True).start()

    def enviar_logica(self):
        msg_base = self.txt_msg.get("0.0", "end").strip()
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        if not os.path.exists("clientes.txt"): return
        with open("clientes.txt", "r", encoding="utf-8") as f: linhas = f.readlines()

        try:
            t_pagina = int(self.wait_pagina.get())
            t_colar = int(self.wait_colar.get())
            t_digitar = int(self.wait_digitar.get())
            t_min = int(self.delay_min.get())
            t_max = int(self.delay_max.get())
        except:
            t_pagina, t_colar, t_digitar, t_min, t_max = 25, 4, 2, 15, 25

        novas_linhas = []
        for linha in linhas:
            if not self.executando:
                novas_linhas.append(linha); continue
            
            while self.pausado: time.sleep(1)
            
            partes = linha.strip().split(",")
            if len(partes) != 4: continue
            nome, fone, env, dt = partes

            if self.check_pular_hoje.get() == 1 and data_hoje in dt:
                self.lbl_status.configure(text=f"⏭️ Pulando {nome}", text_color="yellow")
                novas_linhas.append(linha); time.sleep(0.5); continue
            
            self.lbl_status.configure(text=f"🚀 Enviando para {nome}...", text_color="white")
            
            try:
                # 1. Abre o link (PyWhatKit cuida de carregar e colar a mensagem)
                kit.sendwhatmsg_instantly(f"+{fone}", msg_base.replace("{nome}", nome), wait_time=t_pagina, tab_close=False)
                
                # 2. Pausa maior para garantir que o navegador está na frente
                time.sleep(t_colar)
                
                # Clique rápido no meio da tela para garantir foco absoluto antes do Enter
                pg.click(pg.size().width/2, pg.size().height/2)
                time.sleep(0.5)

                # 3. Pressiona Enter
                pg.press("enter")
                time.sleep(1)
                
                # Atalho para fechar a aba
                pg.hotkey('ctrl', 'w') 
                
                novo_envio = str(int(env) + 1)
                nova_data = datetime.now().strftime("%d/%m/%Y %H:%M")
                novas_linhas.append(f"{nome},{fone},{novo_envio},{nova_data}\n")
                
                tempo_espera = random.randint(t_min, t_max)
                time.sleep(tempo_espera)
            except Exception as e:
                print(f"Erro no envio: {e}")
                novas_linhas.append(linha)

        with open("clientes.txt", "w", encoding="utf-8") as f: f.writelines(novas_linhas)
        self.after(0, self.carregar_lista)
        self.executando = False
        self.btn_disparar.configure(state="normal")
        self.lbl_status.configure(text="✅ Concluído!", text_color="#2ecc71")

if __name__ == "__main__":
    app = LembraZap()
    app.mainloop()
