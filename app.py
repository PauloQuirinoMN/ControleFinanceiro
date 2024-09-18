import flet as ft
import openpyxl # Manipular Excel
import os # Acessa documentos através do sistema operacinal
from datetime import datetime # Capturar informações de data e hora

def main(page: ft.Page):

    total_entrada = ft.Container(
        border_radius=5,
        height=60,
        width=120,
        bgcolor=ft.colors.BLACK12,
        content=ft.Column(
            [
                ft.Text(value=0, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value='Entradas', size=15, weight=ft.FontWeight.W_700),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    total_saida = ft.Container(
        border_radius=5,
        height=60,
        width=120,
        bgcolor=ft.colors.BLACK12,
        content=ft.Column(
            [
                ft.Text(value=0, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value='Saídas', size=15, weight=ft.FontWeight.W_700),
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
                ft.Text(value='Saldo Total', size=15, weight=ft.FontWeight.W_700),
                ft.Text(value=0, size=30, weight=ft.FontWeight.BOLD),
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

    btn_baixar_dados = ft.IconButton(icon=ft.icons.DOWNLOAD, icon_size=20, disabled=True,  on_click=lambda _:print('aqui baixar e limpa dos dados'))

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
        ],
    )

    anom = ft.TextField(label='Ano', height=30, width=80)
    mesm = ft.TextField(label='Mês', height=30, width=80)
    diam = ft.TextField(label='Dia', height=30, width=80)
   
    data_manual = ft.Container(
        content=ft.Column(
            [
                ft.Divider(),
                ft.Text(value='Caso não preenchas data, será salvo a data de agora', size=10),
                anom,
                mesm,
                diam,
                ft.Divider(),
            ]
        )
    )

    def ok_fecha_alerta_erro(e):
        page.dialog.open=False
        page.update()

    def formulario(e):
        alerta.open = True
        page.update()

    def salvar_dados(e):

        def mostrar_alerta_erro(mensagem):
            alerte_erro = ft.AlertDialog(
                title=ft.Text("Presta Atenção Abestado!"),
                content=ft.Text(mensagem),
                actions=[
                    ft.TextButton('Ok', on_click=ok_fecha_alerta_erro),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                open=True
            )
            page.dialog = alerte_erro
            page.update()
        
        if not descricao.value.strip():
            mostrar_alerta_erro("Descrição é obrigatória!")
            return
        try:
            valor_float = float(valor.value)
            if valor_float <= 0:
                raise ValueError("Valor deve ser maior que '0'!")
        except ValueError:
            mostrar_alerta_erro("Valor inválido!")
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

        alerta.open = False
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
                trasacao = ft.Container(
                    margin=2,
                    padding=10,
                    bgcolor=ft.colors.GREEN_50,
                    border_radius=5,
                    content=ft.Row(
                        [
                            ft.Text(row[1], width=70, size=12, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{row[7]}/{row[6]}/{row[5]}", width=70, size=12, color=ft.colors.BLACK, weight=ft.FontWeight.W_600),
                            ft.Text(f"R$ {row[3]}", width=70, size=12, color=ft.colors.BLACK, weight=ft.FontWeight.W_600),
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


    historico = ft.Container(
        expand=True,
        border_radius = 10,
        padding = 10,
        margin = 10,
        content = ft.Column(
            [],
            scroll=ft.ScrollMode.AUTO
        )
    )
    
    
    alerta = ft.AlertDialog(
        title=ft.Text(value='Nova transação'),
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
    page.overlay.append(alerta)
    page.update()


    layout = ft.Container(
        expand=True,
        bgcolor=ft.colors.BLACK26,
        border_radius=5,
        padding=5,
        content=ft.Column(
            [
                ft.Row([ft.Text(value='Saldos', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)], alignment=ft.MainAxisAlignment.START),
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
                        ft.Text(value='Transações', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        btn_baixar_dados,
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

ft.app(target=main)