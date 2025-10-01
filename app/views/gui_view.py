"""Interface gráfica Tkinter pura (sem CustomTkinter)."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from app.bd.connection import init_db
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.departamento_controller import DepartamentoController
from app.bd.manutencaoBD import zerarBD as cli_zerarBD

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:  # Fallback sem imagem
    PIL_OK = False

COLORS = {
    'bg': '#1a1a1a',
    'panel': '#262626',
    'accent': '#8b1e1e',
    'accent_hover': '#6b1616',
    'gold': '#d4af37',
    'fg': '#e5e5e5',
    'muted': '#999999'
}

FONT_TITLE = ('Segoe UI', 16, 'bold')

class MiniRHApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mini RH - Tkinter')
        self.geometry('1000x600')
        self.minsize(900, 520)
        self.configure(bg=COLORS['bg'])

        self._func_sel_id = None
        self._dep_sel_id = None
        self._current_section = 'func'

        # Monta layout base e configura estilos ANTES de criar treeviews
        self._build_layout()
        self._configure_treeview_style()
        self._load_background()
        self._build_func_section()
        self._status('Pronto')

    # ---------- Estilo Treeview ----------
    def _configure_treeview_style(self):
        style = ttk.Style(self)
        try:
            # 'clam' permite customização de cores de scrollbars melhor que 'default' em muitos sistemas.
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Treeview',
                        background=COLORS['panel'],
                        fieldbackground=COLORS['panel'],
                        foreground=COLORS['fg'],
                        rowheight=24,
                        bordercolor=COLORS['bg'],
                        borderwidth=0)
        style.configure('Treeview.Heading',
                        background=COLORS['bg'],
                        foreground=COLORS['gold'],
                        relief='flat')
        style.map('Treeview',
                  background=[('selected', COLORS['accent'])],
                  foreground=[('selected', 'white')])


    # ---------- Layout Base ----------
    def _build_layout(self):
        self.sidebar = tk.Frame(self, width=180, bg='#101010', highlightthickness=0, bd=0)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text='MINI RH', fg=COLORS['gold'], bg='#101010', font=('Segoe UI', 18, 'bold')).pack(pady=(18,2))
        tk.Label(self.sidebar, text='Tkinter', fg=COLORS['muted'], bg='#101010', font=('Segoe UI', 11)).pack(pady=(0,18))
        tk.Button(self.sidebar, text='Funcionários', command=self._build_func_section, bg=COLORS['accent'], fg='white').pack(fill='x', padx=10, pady=4)
        tk.Button(self.sidebar, text='Departamentos', command=self._build_dep_section, bg=COLORS['accent'], fg='white').pack(fill='x', padx=10, pady=4)
        tk.Button(self.sidebar, text='Recarregar', command=self._reload_current, bg='#444444', fg='white').pack(fill='x', padx=10, pady=(24,4))
        tk.Button(self.sidebar, text='Zerar Banco', command=self._confirm_zerar_banco, bg='#663300', fg='white').pack(fill='x', padx=10, pady=(4,4))
        tk.Button(self.sidebar, text='Sair', command=self.destroy, bg='#552222', fg='white').pack(side='bottom', fill='x', padx=10, pady=18)

        # Frame principal ocupa todo o restante sem criar faixa entre sidebar e conteúdo
        self.main = tk.Frame(self, bg=COLORS['panel'], highlightthickness=0, bd=0)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.status_var = tk.StringVar()
        self.status = tk.Label(self, textvariable=self.status_var, anchor='w', bg='#111111', fg=COLORS['muted'])
        self.status.pack(side=tk.BOTTOM, fill='x')

    def _status(self, msg: str):
        self.status_var.set(msg)

    # ---------- Background ----------
    def _load_background(self):
        if not PIL_OK:
            return
        path = Path(__file__).parent.parent / 'assets' / 'logo_pmmg.png'
        if not path.exists():
            return
        try:
            img = Image.open(path).convert('RGBA').resize((230,230), Image.Resampling.LANCZOS)
            try:
                alpha = img.split()[-1]
                alpha = alpha.point(lambda p: int(p*0.55))  # marca d'água 55%
                img.putalpha(alpha)
            except Exception:
                pass
            self._bg_img = ImageTk.PhotoImage(img)
        except Exception as e:
            print('Falha ao carregar imagem:', e)

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()
        self._load_background()

    def _toolbar(self, parent, novo, editar, remover, atualizar):
        bar = tk.Frame(parent, bg=COLORS['bg'])
        bar.pack(fill='x', pady=(0,8))
        tk.Button(bar, text='Novo', command=novo, bg=COLORS['accent'], fg='white', width=10).pack(side='left', padx=3)
        tk.Button(bar, text='Editar', command=editar, bg=COLORS['accent'], fg='white', width=10).pack(side='left', padx=3)
        tk.Button(bar, text='Remover', command=remover, bg='#77222a', fg='white', width=10).pack(side='left', padx=3)
        tk.Button(bar, text='Atualizar', command=atualizar, bg='#444444', fg='white', width=10).pack(side='left', padx=3)
        return bar

    # ---------- Funcionários ----------
    def _build_func_section(self):
        self._current_section = 'func'
        self._clear_main()
        tk.Label(self.main, text='Funcionários', font=FONT_TITLE, fg=COLORS['gold'], bg=COLORS['panel']).pack(anchor='w', padx=0, pady=(8,8))
        # Barra de ferramentas + filtro
        bar = tk.Frame(self.main, bg=COLORS['panel'])
        bar.pack(fill='x', padx=0)
        self._toolbar(bar, self._novo_func, self._editar_func, self._remover_func, self._carregar_funcionarios)
        # Filtro por nome/cargo
        filt_frame = tk.Frame(bar, bg=COLORS['panel'])
        filt_frame.pack(side='right', padx=4)
        tk.Label(filt_frame, text='Filtro:', bg=COLORS['panel'], fg=COLORS['muted']).pack(side='left')
        self._func_filter_var = tk.StringVar()
        ent = tk.Entry(filt_frame, textvariable=self._func_filter_var, width=18)
        ent.pack(side='left', padx=4)
        ent.bind('<KeyRelease>', lambda _e: self._carregar_funcionarios())
        cols = ('id','nome','cargo','salario','departamento','ativo')
        container = tk.Frame(self.main, bg=COLORS['panel'])
        container.pack(fill='both', expand=True, padx=0, pady=4)
        # Frame da tabela ocupa ~80% da largura para liberar espaço da imagem de fundo
        frame_table = tk.Frame(container, bg=COLORS['panel'])
        frame_table.pack(side='left', fill='both', expand=True)
        self.tree_func = ttk.Treeview(frame_table, columns=cols, show='headings')
        vsb = ttk.Scrollbar(frame_table, orient='vertical', command=self.tree_func.yview, style='Dark.Vertical.TScrollbar')
        hsb = ttk.Scrollbar(frame_table, orient='horizontal', command=self.tree_func.xview, style='Dark.Horizontal.TScrollbar')
        self._func_scrollbars = (vsb, hsb, frame_table)
        self.tree_func.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree_func.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, columnspan=2, sticky='ew')
        frame_table.rowconfigure(0, weight=1)
        frame_table.columnconfigure(0, weight=1)
        # Espaço reservado (spacer) para a imagem no canto direito
        spacer = tk.Frame(container, width=250, bg=COLORS['panel'])
        spacer.pack(side='right', fill='y')
        if hasattr(self, '_bg_img'):
            lbl_logo = tk.Label(spacer, image=self._bg_img, bg=COLORS['panel'], borderwidth=0)
            lbl_logo.pack(side='bottom', anchor='se', padx=4, pady=4)
            self._bg_label = lbl_logo
        headers = {'id':'ID','nome':'Nome','cargo':'Cargo','salario':'Salário','departamento':'Depto','ativo':'Ativo'}
        for c in cols:
            self.tree_func.heading(c, text=headers[c])
            base_w = 90
            if c == 'nome':
                base_w = 160
            elif c == 'cargo':
                base_w = 120
            elif c == 'salario':
                base_w = 110
            elif c == 'departamento':
                base_w = 120
            self.tree_func.column(c, width=base_w, minwidth=60, anchor='center', stretch=True)
        
        self.tree_func.configure(selectmode='browse')
        self.tree_func.bind('<<TreeviewSelect>>', self._on_select_func)
        self.tree_func.bind('<Double-1>', lambda e: self._editar_func())
        self.tree_func.bind('<Button-3>', self._menu_contexto_func)
        self.tree_func.bind('<Configure>', lambda e: self.after_idle(self._refresh_func_scrollbars))
        self._carregar_funcionarios()

    def _carregar_funcionarios(self):
        for i in self.tree_func.get_children():
            self.tree_func.delete(i)
        try:
            filtro = ''
            if hasattr(self, '_func_filter_var'):
                filtro = (self._func_filter_var.get() or '').strip().lower()
            for idx, f in enumerate(FuncionarioController.listar()):
                if filtro and (filtro not in f.nome.lower() and filtro not in f.cargo.lower()):
                    continue
                salario_fmt = f"{f.salario:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')  # formata pt-BR simples
                dep_nome = f.departamento_nome or '(sem)'
                values = (f.id, f.nome, f.cargo, salario_fmt, dep_nome, 'Sim' if f.ativo else 'Não')
                tag = 'odd' if idx % 2 else 'even'
                self.tree_func.insert('', 'end', values=values, tags=(tag,))
            
            self.tree_func.tag_configure('even', background=COLORS['panel'])
            self.tree_func.tag_configure('odd', background='#303030')
            self._status(f"{len(self.tree_func.get_children())} funcionário(s) carregado(s)")
            self.after_idle(self._refresh_func_scrollbars)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def _menu_contexto_func(self, event):
        if not self.tree_func.identify_row(event.y):
            return
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Editar', command=self._editar_func)
        menu.add_command(label='Remover', command=self._remover_func)
        menu.add_separator()
        menu.add_command(label='Atualizar', command=self._carregar_funcionarios)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _on_select_func(self, _):
        sel = self.tree_func.selection()
        if not sel:
            self._func_sel_id = None
            return
        self._func_sel_id = self.tree_func.item(sel[0])['values'][0]
        self._status(f"Funcionário selecionado ID {self._func_sel_id}")

    def _novo_func(self):
        self._form_funcionario()

    def _editar_func(self):
        if not self._func_sel_id:
            messagebox.showinfo('Selecione', 'Selecione um funcionário primeiro.')
            return
        func = FuncionarioController.obter(self._func_sel_id)
        if not func:
            messagebox.showerror('Erro', 'Funcionário não encontrado.')
            return
        self._form_funcionario(func)

    def _form_funcionario(self, func=None):
        win = tk.Toplevel(self)
        win.title('Editar Funcionário' if func else 'Novo Funcionário')
        win.configure(bg=COLORS['panel'])
        win.geometry('430x480')
        frm = tk.Frame(win, bg=COLORS['panel'])
        frm.pack(fill='both', expand=True, padx=12, pady=12)
        def row(lbl, r):
            tk.Label(frm, text=lbl, bg=COLORS['panel'], fg=COLORS['gold']).grid(row=r,column=0,sticky='w', pady=4)
        nome_var = tk.StringVar(value=getattr(func,'nome',''))
        cargo_var = tk.StringVar(value=getattr(func,'cargo',''))
        sal_var = tk.StringVar(value=str(getattr(func,'salario','')))
        data_var = tk.StringVar(value=getattr(func,'data_admissao',''))
        ativo_var = tk.IntVar(value=getattr(func,'ativo',1))
        row('Nome:',0); tk.Entry(frm,textvariable=nome_var).grid(row=0,column=1,sticky='ew')
        row('Cargo:',1); tk.Entry(frm,textvariable=cargo_var).grid(row=1,column=1,sticky='ew')
        row('Salário:',2); tk.Entry(frm,textvariable=sal_var).grid(row=2,column=1,sticky='ew')
        row('Data (YYYY-MM-DD):',3); tk.Entry(frm,textvariable=data_var).grid(row=3,column=1,sticky='ew')
        deps = DepartamentoController.listar(); dep_opcoes = ['(sem)'] + [f"{d.id} - {d.nome}" for d in deps]
        dep_var = tk.StringVar(value='(sem)')
        if func and func.departamento_id:
            for d in deps:
                if d.id == func.departamento_id:
                    dep_var.set(f"{d.id} - {d.nome}"); break
        row('Departamento:',4); tk.OptionMenu(frm, dep_var, *dep_opcoes).grid(row=4,column=1,sticky='ew')
        row('Ativo (1/0):',5); tk.Entry(frm,textvariable=ativo_var).grid(row=5,column=1,sticky='ew')
        frm.columnconfigure(1, weight=1)
        def salvar():
            try:
                nome = nome_var.get().strip(); cargo = cargo_var.get().strip(); salario = float(sal_var.get()); data_adm = data_var.get().strip(); ativo = int(ativo_var.get())
                dep_escolha = dep_var.get(); departamento_id = None
                if dep_escolha != '(sem)': departamento_id = int(dep_escolha.split(' - ')[0])
                if func:
                    if not FuncionarioController.atualizar(func.id, nome, cargo, salario, departamento_id, data_adm, ativo):
                        messagebox.showerror('Erro','Falha ao atualizar.'); return
                    messagebox.showinfo('Sucesso','Funcionário atualizado.')
                else:
                    novo_id = FuncionarioController.criar(nome, cargo, salario, departamento_id, data_adm)
                    messagebox.showinfo('Sucesso', f'Funcionário criado ID {novo_id}.')
                self._carregar_funcionarios(); win.destroy()
            except ValueError as e: messagebox.showerror('Erro', str(e))
            except Exception as e: messagebox.showerror('Erro', str(e))
        tk.Button(frm, text='Salvar', command=salvar, bg=COLORS['accent'], fg='white').grid(row=99,column=0,columnspan=2,pady=18)

    def _remover_func(self):
        if not self._func_sel_id:
            messagebox.showinfo('Selecione', 'Selecione um funcionário primeiro.'); return
        if not messagebox.askyesno('Confirmar', f'Remover funcionário ID {self._func_sel_id}?'): return
        try:
            if FuncionarioController.remover(self._func_sel_id): messagebox.showinfo('Sucesso','Removido.'); self._carregar_funcionarios()
            else: messagebox.showerror('Erro','Não encontrado.')
        except Exception as e: messagebox.showerror('Erro', str(e))

    # ---------- Departamentos ----------
    def _build_dep_section(self):
        self._current_section = 'dep'
        self._clear_main()
        tk.Label(self.main, text='Departamentos', font=FONT_TITLE, fg=COLORS['gold'], bg=COLORS['panel']).pack(anchor='w', padx=0, pady=(8,8))
        bar = tk.Frame(self.main, bg=COLORS['panel'])
        bar.pack(fill='x', padx=0)
        self._toolbar(bar, self._novo_dep, self._editar_dep, self._remover_dep, self._carregar_departamentos)
        filt_frame = tk.Frame(bar, bg=COLORS['panel'])
        filt_frame.pack(side='right', padx=4)
        tk.Label(filt_frame, text='Filtro:', bg=COLORS['panel'], fg=COLORS['muted']).pack(side='left')
        self._dep_filter_var = tk.StringVar()
        ent = tk.Entry(filt_frame, textvariable=self._dep_filter_var, width=18)
        ent.pack(side='left', padx=4)
        ent.bind('<KeyRelease>', lambda _e: self._carregar_departamentos())
        cols = ('id','nome','descricao')
        container = tk.Frame(self.main, bg=COLORS['panel'])
        container.pack(fill='both', expand=True, padx=0, pady=4)
        frame_table = tk.Frame(container, bg=COLORS['panel'])
        frame_table.pack(side='left', fill='both', expand=True)
        self.tree_dep = ttk.Treeview(frame_table, columns=cols, show='headings')
        vsb = ttk.Scrollbar(frame_table, orient='vertical', command=self.tree_dep.yview, style='Dark.Vertical.TScrollbar')
        hsb = ttk.Scrollbar(frame_table, orient='horizontal', command=self.tree_dep.xview, style='Dark.Horizontal.TScrollbar')
        self._dep_scrollbars = (vsb, hsb, frame_table)
        self.tree_dep.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree_dep.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, columnspan=2, sticky='ew')
        frame_table.rowconfigure(0, weight=1)
        frame_table.columnconfigure(0, weight=1)
        spacer = tk.Frame(container, width=250, bg=COLORS['panel'])
        spacer.pack(side='right', fill='y')
        if hasattr(self, '_bg_img'):
            lbl_logo = tk.Label(spacer, image=self._bg_img, bg=COLORS['panel'], borderwidth=0)
            lbl_logo.pack(side='bottom', anchor='se', padx=4, pady=4)
            self._bg_label = lbl_logo
        headers = {'id':'ID','nome':'Nome','descricao':'Descrição'}
        for c in cols:
            self.tree_dep.heading(c, text=headers[c])
            base_w = 120 if c != 'descricao' else 340
            self.tree_dep.column(c, width=base_w, minwidth=60, anchor='center', stretch=True)
        self.tree_dep.configure(selectmode='browse')
        self.tree_dep.bind('<<TreeviewSelect>>', self._on_select_dep)
        self.tree_dep.bind('<Double-1>', lambda e: self._editar_dep())
        self.tree_dep.bind('<Button-3>', self._menu_contexto_dep)
        self.tree_dep.bind('<Configure>', lambda e: self.after_idle(self._refresh_dep_scrollbars))
        self._carregar_departamentos()

    def _carregar_departamentos(self):
        for i in self.tree_dep.get_children():
            self.tree_dep.delete(i)
        try:
            filtro = ''
            if hasattr(self, '_dep_filter_var'):
                filtro = (self._dep_filter_var.get() or '').strip().lower()
            lista = DepartamentoController.listar()
            inserted = 0
            for idx, d in enumerate(lista):
                if filtro and filtro not in d.nome.lower():
                    continue
                desc = (d.descricao or '')
                values = (d.id, d.nome, desc)
                tag = 'odd' if inserted % 2 else 'even'
                self.tree_dep.insert('', 'end', values=values, tags=(tag,))
                inserted += 1
            if inserted == 0:
                # Placeholder visual para indicar ausência de dados/resultado de filtro
                self.tree_dep.insert('', 'end', values=('—', 'Nenhum departamento', 'Use "Novo" para cadastrar'), tags=('even',))
                print('[DEBUG] Nenhum departamento listado (filtro="%s"). Total bruto na base: %d' % (filtro, len(lista)))
            self.tree_dep.tag_configure('even', background=COLORS['panel'])
            self.tree_dep.tag_configure('odd', background='#303030')
            efetivos = inserted
            self._status(f"{efetivos} departamento(s) carregado(s)")
            self.after_idle(self._refresh_dep_scrollbars)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    # ---------- Auto ocultação de Scrollbars ----------
    def _refresh_func_scrollbars(self):
        if not hasattr(self, '_func_scrollbars'): return
        vsb, hsb, frame = self._func_scrollbars
        # Vertical
        first, last = self.tree_func.yview()
        if first == 0.0 and last == 1.0:
            vsb.grid_remove()
        else:
            vsb.grid()
        # Horizontal
        xfirst, xlast = self.tree_func.xview()
        if xfirst == 0.0 and xlast == 1.0:
            hsb.grid_remove()
        else:
            hsb.grid()

    def _refresh_dep_scrollbars(self):
        if not hasattr(self, '_dep_scrollbars'): return
        vsb, hsb, frame = self._dep_scrollbars
        first, last = self.tree_dep.yview()
        if first == 0.0 and last == 1.0:
            vsb.grid_remove()
        else:
            vsb.grid()
        xfirst, xlast = self.tree_dep.xview()
        if xfirst == 0.0 and xlast == 1.0:
            hsb.grid_remove()
        else:
            hsb.grid()

    # ---------- Zerar Banco (Opção B) ----------
    def _confirm_zerar_banco(self):
        win = tk.Toplevel(self)
        win.title('Confirmar Zerar Banco')
        win.configure(bg=COLORS['panel'])
        win.geometry('460x220')
        tk.Label(win, text='Esta ação apaga TODOS os dados de Funcionários e Departamentos.',
                 bg=COLORS['panel'], fg=COLORS['gold'], wraplength=430, justify='left').pack(padx=14, pady=(14,8), anchor='w')
        tk.Label(win, text='Digite a palavra exata ZERAR para confirmar:',
                 bg=COLORS['panel'], fg=COLORS['muted']).pack(padx=14, anchor='w')
        entrada = tk.Entry(win)
        entrada.pack(padx=14, fill='x')
        info_var = tk.StringVar(value='')
        lbl_info = tk.Label(win, textvariable=info_var, bg=COLORS['panel'], fg='#cc8844')
        lbl_info.pack(padx=14, pady=(4,8), anchor='w')
        btn_frame = tk.Frame(win, bg=COLORS['panel'])
        btn_frame.pack(fill='x', pady=(4,10))
        def executar():
            if entrada.get().strip().upper() != 'ZERAR':
                info_var.set('Texto incorreto. Digite exatamente ZERAR.')
                return
            # Executa lógica de zerar sem input CLI
            try:
                from app.bd.connection import get_connection
                with get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM funcionario;')
                    cur.execute('DELETE FROM departamento;')
                    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('funcionario','departamento');")
                    conn.commit()
                messagebox.showinfo('Sucesso', 'Banco zerado com sucesso.')
                win.destroy()
                # Recarrega a seção atual
                self._reload_current()
            except Exception as e:
                messagebox.showerror('Erro', f'Falha ao zerar: {e}')
        tk.Button(btn_frame, text='Confirmar', command=executar, bg='#883333', fg='white', width=12).pack(side='left', padx=10)
        tk.Button(btn_frame, text='Cancelar', command=win.destroy, bg='#444444', fg='white', width=12).pack(side='left')
        entrada.focus_set()

    def _menu_contexto_dep(self, event):
        if not self.tree_dep.identify_row(event.y):
            return
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Editar', command=self._editar_dep)
        menu.add_command(label='Remover', command=self._remover_dep)
        menu.add_separator()
        menu.add_command(label='Atualizar', command=self._carregar_departamentos)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _on_select_dep(self, _):
        sel = self.tree_dep.selection()
        if not sel: self._dep_sel_id = None; return
        self._dep_sel_id = self.tree_dep.item(sel[0])['values'][0]
        self._status(f"Departamento selecionado ID {self._dep_sel_id}")

    def _form_departamento(self, dep=None):
        win = tk.Toplevel(self); win.title('Editar Departamento' if dep else 'Novo Departamento'); win.configure(bg=COLORS['panel']); win.geometry('430x260')
        frm = tk.Frame(win, bg=COLORS['panel']); frm.pack(fill='both', expand=True, padx=12, pady=12)
        tk.Label(frm, text='Nome:', bg=COLORS['panel'], fg=COLORS['gold']).grid(row=0,column=0,sticky='w', pady=4)
        nome_var = tk.StringVar(value=getattr(dep,'nome','')); tk.Entry(frm, textvariable=nome_var).grid(row=0,column=1,sticky='ew')
        tk.Label(frm, text='Descrição:', bg=COLORS['panel'], fg=COLORS['gold']).grid(row=1,column=0,sticky='w', pady=4)
        desc_var = tk.StringVar(value=getattr(dep,'descricao','')); tk.Entry(frm, textvariable=desc_var).grid(row=1,column=1,sticky='ew')
        frm.columnconfigure(1, weight=1)
        def salvar():
            try:
                nome = nome_var.get().strip(); descricao = desc_var.get().strip() or None
                if dep:
                    if not DepartamentoController.atualizar(dep.id, nome, descricao): messagebox.showerror('Erro','Falha ao atualizar.'); return
                    messagebox.showinfo('Sucesso','Departamento atualizado.')
                else:
                    novo_id = DepartamentoController.criar(nome, descricao); messagebox.showinfo('Sucesso', f'Departamento criado ID {novo_id}.')
                self._carregar_departamentos(); win.destroy()
            except ValueError as e: messagebox.showerror('Erro', str(e))
            except Exception as e: messagebox.showerror('Erro', str(e))
        tk.Button(frm, text='Salvar', command=salvar, bg=COLORS['accent'], fg='white').grid(row=99,column=0,columnspan=2, pady=15)

    # wrappers semelhantes aos de funcionários
    def _novo_dep(self):
        self._form_departamento()

    def _editar_dep(self):
        if not self._dep_sel_id:
            messagebox.showinfo('Selecione', 'Selecione um departamento primeiro.')
            return
        dep = DepartamentoController.obter(self._dep_sel_id)
        if not dep:
            messagebox.showerror('Erro', 'Departamento não encontrado.')
            return
        self._form_departamento(dep)

    def _remover_dep(self):
        if not self._dep_sel_id: messagebox.showinfo('Selecione','Selecione um departamento primeiro.'); return
        # evita tentativa de remover linha placeholder "Nenhum departamento"
        if not isinstance(self._dep_sel_id, int):
            messagebox.showinfo('Aviso', 'Linha informativa selecionada, nada para remover.')
            return
        if not messagebox.askyesno('Confirmar', f'Remover departamento ID {self._dep_sel_id}?'): return
        try:
            if DepartamentoController.remover(self._dep_sel_id): messagebox.showinfo('Sucesso','Removido.'); self._carregar_departamentos()
            else: messagebox.showerror('Erro','Não encontrado (ou possui funcionários).')
        except Exception as e: messagebox.showerror('Erro', str(e))

    def _reload_current(self):
        if self._current_section == 'func': self._build_func_section()
        else: self._build_dep_section()

def run_gui():
    init_db(); app = MiniRHApp(); app.mainloop()

if __name__ == '__main__':
    run_gui()
