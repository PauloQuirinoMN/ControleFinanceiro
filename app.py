import flet as ft
import openpyxl # Manipular Excel
import os # Acessa documentos através do sistema operacinal
from datetime import datetime # Capturar informações de data e hora

def main(page: ft.Page):

  
    branco = "#F4F5F0"
    azul = "#4895EF"
    verde = "#75975e"
    grafite = '#747169'
    vermelho = '#ee6b6e'

    total_entrada = ft.Container(
        border_radius=5,
        height=60,
        width=120,
        content=ft.Column(
            [
                ft.Text(value=0, size=20, weight=ft.FontWeight.BOLD, color=grafite),
                ft.Text(value='Entradas', size=15, weight=ft.FontWeight.W_700, color=azul),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    total_saida = ft.Container(
        border_radius=5,
        height=60,
        width=120,
        content=ft.Column(
            [
                ft.Text(value=0, size=20, weight=ft.FontWeight.BOLD, color=grafite),
                ft.Text(value='Saídas', size=15, weight=ft.FontWeight.W_700, color=vermelho),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    saldo_total = ft.Container(
        margin=10,
        expand=True,
        border_radius=5,
        content=ft.Row(
            [
                ft.Text(value='Saldo Total', size=15, weight=ft.FontWeight.W_700, color=grafite),
                ft.Text(value=0, size=30, weight=ft.FontWeight.BOLD, color=verde),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    tipo = ft.Dropdown(
        label='Tipo de Transação',
        options=
        [
            ft.dropdown.Option('Entrada'),
            ft.dropdown.Option('Saída'),                    
        ],
    )

    descricao = ft.TextField(label='Descrição')

    categoria = ft.Dropdown(
        label='Categoria',
        options=[
            ft.dropdown.Option('Alimento'),
            ft.dropdown.Option('Transporte'), 
            ft.dropdown.Option('Salário'),
            ft.dropdown.Option('Lazer'),
            ft.dropdown.Option('Moradia'),
            ft.dropdown.Option('Vestiuário'),
            ft.dropdown.Option('Esposte'),
            ft.dropdown.Option('Empréstimos'),  
            ft.dropdown.Option('Outros'),                 
        ]
    )

    valor =  ft.TextField(label='Valor')

    forma = ft.Dropdown(
        label='Forma de Transação',
        options=[
            ft.dropdown.Option('Dinheiro'),
            ft.dropdown.Option('Cartão'), 
            ft.dropdown.Option('Pix'),
            ft.dropdown.Option('Fiado'), 
            ft.dropdown.Option('Outro'),                   
        ],
    )

    anom = ft.TextField(label='Ano', keyboard_type = ft.KeyboardType.NUMBER, height=30, width=80)
    mesm = ft.TextField(label='Mês', keyboard_type = ft.KeyboardType.NUMBER, height=30, width=80)
    diam = ft.TextField(label='Dia', keyboard_type = ft.KeyboardType.NUMBER, height=30, width=80)
   
    data_manual = ft.Container(
        content=ft.Column(
            [
                ft.Divider(),
                ft.Text(value='Ano, Mês e Dia para períodos passados', size=15, italic=True, color=vermelho),
                anom,
                mesm,
                diam,
                ft.Divider(),
            ]
        )
    )

    historico = ft.Container(
        expand=True,
        padding = 10,
        margin = 5,
        content = ft.Column(
            [],
            scroll=ft.ScrollMode.AUTO
        )
    )

    # adicionar o alerta ao overlay
    def adicionar_alerta(alerta):
        if alerta not in page.overlay:
            page.overlay.append(alerta)
        alerta.open = True
        page.update()

    # remover o alerta ao overlay
    def remover_alerta(alerta):
        alerta.open = False
        page.update()
    
    def mostrar_alerta_erro_descricao():
            alerte_erro = ft.AlertDialog(
                title=ft.Text("Presta Atenção Abestado!", color=grafite),
                content=ft.Text('Descrição é obrigatório', color=vermelho),
                actions=[
                    ft.TextButton('Ok', on_click=lambda e: remover_alerta(alerte_erro)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                open=True
            )
            adicionar_alerta(alerte_erro)

    def mostrar_alerta_erro_valor():
            alerte_erro = ft.AlertDialog(
                title=ft.Text("Presta Atenção Abestado!", color=grafite),
                content=ft.Text('Valor é obrigatório', color=vermelho),
                actions=[
                    ft.TextButton('Ok', on_click=lambda e: remover_alerta(alerte_erro)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                open=True
            )
            adicionar_alerta(alerte_erro)
    
    def mostrar_alerta_erro_tipo():
            alerte_tipo = ft.AlertDialog(
            title=ft.Text("Presta Atenção Abestado!", color=grafite),
                content=ft.Text('Tipo é obrigatório', color=vermelho),
                actions=[
                    ft.TextButton('Ok', on_click=lambda e: remover_alerta(alerte_tipo)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                open=True
            )
            adicionar_alerta(alerte_tipo)


    def salvar_dados(e): 


        if tipo.value is None or tipo.value == "":
            mostrar_alerta_erro_tipo()
            return

    
        if not descricao.value.strip():
            mostrar_alerta_erro_descricao()
            return
        try:
            valor_float = float(valor.value)
            if valor_float <= 0:
                raise ValueError("Valor deve ser maior que '0'!")
        except ValueError:
            mostrar_alerta_erro_valor()
            return 
   

        arquivo = "transacoes.xlsx"

        agora = datetime.now()

        if anom.value == "" and mesm.value == "" and diam.value == "":
            ano = agora.year
            mes = agora.month
            dia = agora.day
            hora = agora.strftime("%H:%M:%S")
        else:
            ano = anom.value if anom.value else agora.year
            mes = mesm.value if mesm.value else agora.month
            dia = diam.value if diam.value else agora.day
            hora = agora.strftime("%H:%M:%S") 
            
        # Verificando se o arquivo já existe
        if not os.path.exists(arquivo):
            # Cria um novo arquivo Excel e defino os cabeçalhos
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Transações"
            sheet.append(["Tipo", "Descrição", "Categoria", "Valor", "Forma de Transação", "Ano", "Mês", "Dia", "Hora"])
            workbook.save(arquivo)

        # Abrir o arquivo Excel para adicionar novos dados
        workbook = openpyxl.load_workbook(arquivo)
        sheet = workbook.active
        # Adicinar os dados do formulário ao Excel

        sheet.append([
            tipo.value,
            descricao.value,
            categoria.value,
            valor.value,
            forma.value,
            ano,
            mes,
            dia,
            hora
        ])
        # Salvar o arquivo
        workbook.save(arquivo)

        # Limpando os campos do formulário
        tipo.value = None
        descricao.value = " "
        categoria.value = None
        valor.value = " "
        forma.value = None

        anom.value = ""
        mesm.value = ""
        diam.value = ""
        
        # Atualiza o histórico assim que os dados forem salvos
        atualizar_historico()

        alerta_Form.open = False
        page.update()

    def atualizar_historico():
        # Limpando o histórico anterior

        historico.content.controls.clear()

        if os.path.exists("transacoes.xlsx"):
            workbook = openpyxl.load_workbook("transacoes.xlsx")
            sheet = workbook.active

            # iterar sobre as linhas do excel, começando da segunda linha
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Cria um novo container para cada transação

                # definir a cor da borda com base no tipo de transição
                tipo = row[0]
                if tipo == "Entrada":
                    cor = azul
                elif tipo == "Saída":
                    cor = vermelho
                else:
                    cor = grafite
                # Criando container para cada transação   
                trasacao = ft.Container(
                    border=ft.Border(left=ft.BorderSide(width=4, color=cor)),
                    margin=2,
                    padding=10,
                    border_radius=0,
                    content=ft.Row(
                        [
                            ft.Text(row[1], width=70, size=12, color=grafite, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{row[7]}/{row[6]}/{row[5]}", width=70, size=12, color=grafite, weight=ft.FontWeight.W_600),
                            ft.Text(f"R$ {row[3]}", width=70, size=12, color=grafite, weight=ft.FontWeight.W_600),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        spacing=10,
                    )
                )
                # adiconar o novo container ao container de histórico
                historico.content.controls.append(trasacao)    
        atualizar_saldos()

    def atualizar_saldos():

        # Verificando se o arquivo já existe
        if not os.path.exists("transacoes.xlsx"):
            # Cria um novo arquivo Excel e defino os cabeçalhos
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Transações"
            sheet.append(["Tipo", "Descrição", "Categoria", "Valor", "Forma de Transação", "Ano", "Mês", "Dia", "Hora"])
            workbook.save("transacoes.xlsx")
        

        workbook = openpyxl.load_workbook("transacoes.xlsx")
        sheet = workbook.active
        en = 0
        sa = 0
            
        for row in sheet.iter_rows(min_row=2, values_only=True):
            valor = float(row[3])
            if row[0] == 'Entrada':
                en += valor
            elif row[0] == 'Saída':
                sa += valor
        to = en - sa

        total_entrada.content.controls[0].value = f"R$ {en:.2f}"
        total_saida.content.controls[0].value = f"R$ {sa:.2f}"
        saldo_total.content.controls[1].value =  f"R$ {to:.2f}"

        page.update()

    alerta_Form = ft.AlertDialog(
        title=ft.Text(value='Nova transação', color=grafite),
        content=ft.Column(
            [
                tipo, 
                descricao,
                categoria,
                valor,
                forma,
                data_manual,
            ]
        ),
        actions=[
            ft.ElevatedButton('Salvar', on_click=salvar_dados)
        ],
        open=False
    )


    # Associando o alerta a page
    page.overlay.append(alerta_Form)
    page.update()

    # Abrir alerta do formulário
    def formulario(e):
        alerta_Form.open = True
        page.update()
    
    def limpardados(e):
        historico.content.controls.clear() # Limpa o histórico da interface
        arquivo = "transacoes.xlsx" # Limpa o conteúdo do xlsx
        if os.path.exists(arquivo):
            workbook = openpyxl.load_workbook(arquivo)
            sheet = workbook.active

            # Manter o cabeçalho e apagar as outras linhas
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                for cell in row:
                    cell.value = None
            workbook.save(arquivo)

        total_entrada.content.controls[0].value = "R$ 0.00"
        total_saida.content.controls[0].value = "R$ 0.00"
        saldo_total.content.controls[1].value = "R$ 0.00"

        page.update()
    
    def mostrar_alerta_confirmacao(e):
        # Criar um Alerta
        alerta_confirmacao_limpeza = ft.AlertDialog(
            title=ft.Text("Confirmar Limpeza de dados"),
            content=ft.Text("Você tem certeza que deseja apagar todos os dados? esta ação é irreversível", color=vermelho, size=15, weight=ft.FontWeight.BOLD, italic=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: remover_alerta(alerta_confirmacao_limpeza)),
                ft.ElevatedButton("Confirmar",on_click=lambda e: [remover_alerta(alerta_confirmacao_limpeza),
                                                                   limpardados(e)
                ]
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            open=True
        )
        adicionar_alerta(alerta_confirmacao_limpeza)
        atualizar_saldos()

    def adicionar_alerta(alerta):
        if alerta not in page.overlay:
            page.overlay.append(alerta)
        alerta.open = True
        page.update()  

    def remover_alerta(alerta):
        alerta.open = False
        page.update()


    analise = ft.IconButton(icon=ft.icons.ANALYTICS, icon_color=verde, icon_size=25, disabled=True)
    btn_limpardados = ft.IconButton(icon=ft.icons.DELETE_FOREVER, icon_color=vermelho, icon_size=25, on_click=mostrar_alerta_confirmacao)

    layout = ft.Container(
        expand=True,
        bgcolor=branco,
        border_radius=5,
        padding=5,
        content=ft.Column(
            [
                ft.Row([ft.Text(value='Saldos', size=20, weight=ft.FontWeight.BOLD, color=azul)], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    total_entrada,
                    total_saida
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Row(
                    [
                        saldo_total,
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Row(
                    [
                        ft.Text(value='Transações', size=20, weight=ft.FontWeight.BOLD, color=azul),
                        analise,
                        btn_limpardados,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                historico 
            ],
            spacing=10,
        )
    )

    # Inicia o app buscando o histórico atualizado
    atualizar_historico()

    page.add(
        layout,
        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=formulario)
    )
if __name__ == "__,main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)