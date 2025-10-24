import csv
from datetime import date
import calendar
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .db import connect
from .utils import iso, br, working_days_without_mon_wed, fmt_currency

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 8))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle Uber — Ganhos & Combustível")
        self.geometry("950x650")
        self.configure(bg='#f0f0f0')  # Fundo cinza claro
        self.conn = connect()

        # Tema moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Tema mais moderno

        # Estilos personalizados
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelFrame', background='#ffffff', borderwidth=2, relief='solid')
        self.style.configure('TLabelFrame.Label', background='#ffffff', font=('Segoe UI', 11, 'bold'), foreground='#333333')
        self.style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10), foreground='#333333')
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6, relief='flat', background='#4CAF50', foreground='white')
        self.style.map('TButton', background=[('active', '#45a049')])
        self.style.configure('TEntry', font=('Segoe UI', 10), padding=4)
        self.style.configure('TCombobox', font=('Segoe UI', 10), padding=4)
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#e0e0e0')

        nb = ttk.Notebook(self)
        self.tab_lanca = ttk.Frame(nb)
        self.tab_resumo = ttk.Frame(nb)
        nb.add(self.tab_lanca, text="📝 Lançamentos")
        nb.add(self.tab_resumo, text="📊 Resumo")
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_lancamentos()
        self.build_resumo()
        self.refresh_tables()
        self.update_resumo()

    # ----------------- LANÇAMENTOS -----------------
    def build_lancamentos(self):
        frm = ttk.Frame(self.tab_lanca, padding=15)
        frm.pack(fill="both", expand=True)

        # Corridas
        box1 = ttk.LabelFrame(frm, text="🚗 Corrida (receita)", padding=10)
        box1.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        ttk.Label(box1, text="Data (dd/mm/aaaa):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(box1, text="Valor R$:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(box1, text="KM:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.e_c_data = ttk.Entry(box1, width=16)
        self.e_c_valor = ttk.Entry(box1, width=14)
        self.e_c_km = ttk.Entry(box1, width=12)
        self.e_c_data.grid(row=1, column=0, padx=5, pady=5)
        self.e_c_valor.grid(row=1, column=1, padx=5, pady=5)
        self.e_c_km.grid(row=1, column=2, padx=5, pady=5)
        btn_add_corrida = ttk.Button(box1, text="➕ Adicionar", command=self.add_corrida)
        btn_add_corrida.grid(row=1, column=3, padx=10, pady=5)
        Tooltip(btn_add_corrida, "Adicionar nova corrida com data, valor e quilômetros")

        # Abastecimentos
        box2 = ttk.LabelFrame(frm, text="⛽ Abastecimento (despesa)", padding=10)
        box2.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        ttk.Label(box2, text="Data (dd/mm/aaaa):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(box2, text="Litros:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(box2, text="Preço/L (R$):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.e_a_data = ttk.Entry(box2, width=16)
        self.e_a_litros = ttk.Entry(box2, width=12)
        self.e_a_preco = ttk.Entry(box2, width=12)
        self.e_a_data.grid(row=1, column=0, padx=5, pady=5)
        self.e_a_litros.grid(row=1, column=1, padx=5, pady=5)
        self.e_a_preco.grid(row=1, column=2, padx=5, pady=5)
        btn_add_abast = ttk.Button(box2, text="➕ Adicionar", command=self.add_abastecimento)
        btn_add_abast.grid(row=1, column=3, padx=10, pady=5)
        Tooltip(btn_add_abast, "Adicionar novo abastecimento com data, litros e preço por litro")

        # Tabelas
        tblfrm = ttk.Frame(frm)
        tblfrm.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=8, pady=8)
        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=1)

        self.tbl_corridas = ttk.Treeview(tblfrm, columns=("data","valor","km","id"), show="headings", height=12)
        headings_corridas = [("Data", 130), ("Valor (R$)", 130), ("KM", 90), ("id", 0)]
        for i, (h, w) in enumerate(headings_corridas):
            self.tbl_corridas.heading(i, text=h)
            self.tbl_corridas.column(i, width=w, anchor="center")
        self.tbl_corridas.column(3, width=0, stretch=False)

        self.tbl_abasts = ttk.Treeview(tblfrm, columns=("data","litros","preco","total","id"), show="headings", height=12)
        headings_abasts = [("Data", 130), ("Litros", 110), ("Preço/L", 110), ("Total (R$)", 130), ("id", 0)]
        for i, (h, w) in enumerate(headings_abasts):
            self.tbl_abasts.heading(i, text=h)
            self.tbl_abasts.column(i, width=w, anchor="center")
        self.tbl_abasts.column(4, width=0, stretch=False)

        ttk.Label(tblfrm, text="🚗 Corridas", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,5))
        self.tbl_corridas.pack(fill="x", pady=5)
        btns1 = ttk.Frame(tblfrm)
        btns1.pack(anchor="e", pady=5)
        btn_del_corrida = ttk.Button(btns1, text="🗑️ Excluir", command=self.del_corrida)
        btn_del_corrida.pack(side="right", padx=5)
        Tooltip(btn_del_corrida, "Excluir corrida selecionada")

        ttk.Label(tblfrm, text="⛽ Abastecimentos", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(15,5))
        self.tbl_abasts.pack(fill="x", pady=5)
        btns2 = ttk.Frame(tblfrm)
        btns2.pack(anchor="e", pady=5)
        btn_del_abast = ttk.Button(btns2, text="🗑️ Excluir", command=self.del_abastecimento)
        btn_del_abast.pack(side="right", padx=5)
        Tooltip(btn_del_abast, "Excluir abastecimento selecionado")

    def add_corrida(self):
        try:
            d = iso(self.e_c_data.get() or date.today().strftime("%d/%m/%Y"))
            v = float(self.e_c_valor.get().replace(",", "."))
            km = float(self.e_c_km.get().replace(",", "."))
            cur = self.conn.cursor()
            cur.execute("INSERT INTO corridas(data,valor,km) VALUES(?,?,?)", (d,v,km))
            self.conn.commit()
            self.e_c_valor.delete(0, tk.END); self.e_c_km.delete(0, tk.END)
            self.refresh_tables(); self.update_resumo()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar corrida.\n{e}")

    def add_abastecimento(self):
        try:
            d = iso(self.e_a_data.get() or date.today().strftime("%d/%m/%Y"))
            l = float(self.e_a_litros.get().replace(",", "."))
            p = float(self.e_a_preco.get().replace(",", "."))
            cur = self.conn.cursor()
            cur.execute("INSERT INTO abastecimentos(data,litros,preco_l) VALUES(?,?,?)", (d,l,p))
            self.conn.commit()
            self.e_a_litros.delete(0, tk.END); self.e_a_preco.delete(0, tk.END)
            self.refresh_tables(); self.update_resumo()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar abastecimento.\n{e}")

    def del_corrida(self):
        sel = self.tbl_corridas.selection()
        if not sel: return
        iid = sel[0]
        rid = self.tbl_corridas.set(iid, "id")
        if messagebox.askyesno("Confirmar", "Excluir corrida selecionada?"):
            cur = self.conn.cursor(); cur.execute("DELETE FROM corridas WHERE id=?", (rid,))
            self.conn.commit(); self.refresh_tables(); self.update_resumo()

    def del_abastecimento(self):
        sel = self.tbl_abasts.selection()
        if not sel: return
        iid = sel[0]
        rid = self.tbl_abasts.set(iid, "id")
        if messagebox.askyesno("Confirmar", "Excluir abastecimento selecionado?"):
            cur = self.conn.cursor(); cur.execute("DELETE FROM abastecimentos WHERE id=?", (rid,))
            self.conn.commit(); self.refresh_tables(); self.update_resumo()

    def refresh_tables(self):
        for t in (self.tbl_corridas, self.tbl_abasts):
            for i in t.get_children(): t.delete(i)
        cur = self.conn.cursor()
        for row in cur.execute("SELECT id,data,valor,km FROM corridas ORDER BY data DESC, id DESC"):
            self.tbl_corridas.insert("", "end", values=(br(row[1]), f"{row[2]:.2f}", f"{row[3]:.2f}", row[0]))
        for row in cur.execute("SELECT id,data,litros,preco_l FROM abastecimentos ORDER BY data DESC, id DESC"):
            total = row[2]*row[3]
            self.tbl_abasts.insert("", "end", values=(br(row[1]), f"{row[2]:.2f}", f"{row[3]:.2f}", f"{total:.2f}", row[0]))

    # ----------------- RESUMO -----------------
    def build_resumo(self):
        frm = ttk.Frame(self.tab_resumo, padding=15)
        frm.pack(fill="both", expand=True)

        top = ttk.Frame(frm, padding=10)
        top.pack(fill="x", pady=10)
        ttk.Label(top, text="📅 Mês:", font=("Segoe UI", 11)).pack(side="left")
        self.cb_mes = ttk.Combobox(top, values=[f"{i:02d} - {calendar.month_name[i]}" for i in range(1,13)], width=20, state="readonly")
        self.cb_mes.current(date.today().month-1)
        self.cb_mes.pack(side="left", padx=8)

        ttk.Label(top, text="Ano:", font=("Segoe UI", 11)).pack(side="left", padx=(15,0))
        years = [str(y) for y in range(date.today().year-3, date.today().year+2)]
        self.cb_ano = ttk.Combobox(top, values=years, width=8, state="readonly")
        self.cb_ano.set(str(date.today().year))
        self.cb_ano.pack(side="left", padx=8)

        btn_atualizar = ttk.Button(top, text="🔄 Atualizar", command=self.update_resumo)
        btn_atualizar.pack(side="left", padx=10)
        Tooltip(btn_atualizar, "Atualizar resumo com dados do mês selecionado")

        btn_export = ttk.Button(top, text="📄 Exportar CSV", command=self.export_csv_mes)
        btn_export.pack(side="right")
        Tooltip(btn_export, "Exportar dados mensais para arquivo CSV")

        self.lbls = {}
        grid = ttk.Frame(frm, padding=10)
        grid.pack(fill="x", pady=15)
        fields = [
            ("💰 Receita (corridas)", "receita"),
            ("⛽ Gasto com combustível", "comb"),
            ("📈 Lucro líquido", "lucro"),
            ("🚗 KM percorridos", "km"),
            ("⛽ Litros abastecidos", "litros"),
            ("💵 Preço médio/L", "pm_l"),
            ("📅 Dias trabalhados (sem seg/qua)", "dias"),
            ("🎯 Meta líquida por dia", "meta_dia"),
            ("📊 Líquido por km", "liq_km"),
        ]
        for i,(label,key) in enumerate(fields):
            ttk.Label(grid, text=label + ":", font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", padx=8, pady=6)
            v = ttk.Label(grid, text="—", font=("Segoe UI", 12, "bold"), foreground="#2E8B57")
            v.grid(row=i, column=1, sticky="w", padx=8, pady=6)
            self.lbls[key] = v

    def month_bounds(self, y, m):
        last = calendar.monthrange(y, m)[1]
        ini = date(y, m, 1).strftime("%Y-%m-%d")
        fim = date(y, m, last).strftime("%Y-%m-%d")
        return ini, fim

    def update_resumo(self):
        try:
            m = int(self.cb_mes.get().split(" - ")[0])
            y = int(self.cb_ano.get())
        except Exception:
            messagebox.showerror("Erro", "Selecione mês e ano válidos.")
            return
        di, df = self.month_bounds(y, m)

        cur = self.conn.cursor()
        receita, km = 0.0, 0.0
        for v, k in cur.execute("SELECT valor, km FROM corridas WHERE data BETWEEN ? AND ?", (di, df)):
            receita += v; km += k
        litros, gasto_comb, preco_medio = 0.0, 0.0, 0.0
        precos = []
        for l, p in cur.execute("SELECT litros, preco_l FROM abastecimentos WHERE data BETWEEN ? AND ?", (di, df)):
            litros += l; gasto_comb += l*p; precos.append(p)
        if precos:
            preco_medio = sum(precos)/len(precos)
        lucro = receita - gasto_comb
        dias_trab = working_days_without_mon_wed(y, m)
        meta_dia = (lucro/dias_trab) if dias_trab else 0.0
        liq_km = (lucro/km) if km>0 else 0.0

        self.lbls["receita"].config(text=fmt_currency(receita))
        self.lbls["comb"].config(text=fmt_currency(gasto_comb))
        self.lbls["lucro"].config(text=fmt_currency(lucro))
        self.lbls["km"].config(text=f"{km:.1f} km")
        self.lbls["litros"].config(text=f"{litros:.2f} L")
        self.lbls["pm_l"].config(text=(fmt_currency(preco_medio) + "/L") if preco_medio else "—")
        self.lbls["dias"].config(text=str(dias_trab))
        self.lbls["meta_dia"].config(text=fmt_currency(meta_dia))
        self.lbls["liq_km"].config(text=fmt_currency(liq_km) if km>0 else "—")

    def export_csv_mes(self):
        try:
            m = int(self.cb_mes.get().split(" - ")[0])
            y = int(self.cb_ano.get())
        except Exception:
            messagebox.showerror("Erro", "Selecione mês e ano válidos.")
            return
        di, df = self.month_bounds(y, m)
        fn = filedialog.asksaveasfilename(defaultextension=".csv",
                                          initialfile=f"controle_uber_{y}-{m:02d}.csv",
                                          filetypes=[("CSV","*.csv")])
        if not fn: return
        cur = self.conn.cursor()
        with open(fn, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["TIPO","DATA","VALOR","KM/LITROS","PRECO_L"])
            for d, v, k in cur.execute("SELECT data,valor,km FROM corridas WHERE data BETWEEN ? AND ? ORDER BY data", (di, df)):
                w.writerow(["CORRIDA", br(d), f"{v:.2f}", f"{k:.2f}", ""])
            for d, l, p in cur.execute("SELECT data,litros,preco_l FROM abastecimentos WHERE data BETWEEN ? AND ? ORDER BY data", (di, df)):
                w.writerow(["ABAST", br(d), f"{l*p:.2f}", f"{l:.2f}", f"{p:.2f}"])
        messagebox.showinfo("Exportado", f"Arquivo salvo em:\n{fn}")