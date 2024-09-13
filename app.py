import flet as ft
import openpyxl # Manipular Excel
import os # Acessa documentos através do sistema operacinal
from datetime import datetime # Capturar informações de data e hora

def main(page: ft.Page):

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


    def formulario(e):
        alerta.open = True
        page.update()

    def salvar_dados(e):
        arquivo = "transacoes.xlsx"

        agora = datetime.now()
        ano = agora.year
        mes = agora.month
        dia = agora.day
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
        

        alerta.open = False
        page.update()


    saldo_total = ft.Container(
        border_radius=20,
        height=60,
        width=100,
        bgcolor=ft.colors.BLACK12,
        content=ft.Column(
            [
                ft.Text(value='1.590,00', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value='Saldo Total', size=15, weight=ft.FontWeight.W_700),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    total_entrada = ft.Container(
        border_radius=20,
        height=60,
        width=100,
        bgcolor=ft.colors.BLUE_200,
        content=ft.Column(
            [
                ft.Text(value='2.460,00', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value='Entradas', size=15, weight=ft.FontWeight.W_700),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    total_saida = ft.Container(
        border_radius=20,
        height=60,
        width=100,
        bgcolor=ft.colors.RED_200,
        content=ft.Column(
            [
                ft.Text(value='1.025,00', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value='Saídas', size=15, weight=ft.FontWeight.W_700),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    historico = ft.DataTable(
        border_radius=10,
        bgcolor=ft.colors.CYAN_100,
        vertical_lines=ft.BorderSide(width=2, color=ft.colors.BLACK12),
        horizontal_lines=ft.BorderSide(width=2, color=ft.colors.BLACK),
        column_spacing=20,
        columns=[
            ft.DataColumn(label=ft.Text('Descrição')),
            ft.DataColumn(label=ft.Text('Data')),
            ft.DataColumn(label=ft.Text('Valor')),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(value='Uber')),
                    ft.DataCell(content=ft.Text(value='11/09/2024')),
                    ft.DataCell(content=ft.Text(value='5.58')),
                ]
            )
        ]
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
        margin=0,
        expand=True,
        bgcolor=ft.colors.BLUE_100,
        border_radius=20,
        padding=10,
        content=ft.Column(
            [
                ft.Row([ft.Text(value='FINANCEIRO', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_900)], alignment=ft.MainAxisAlignment.START),
                ft.Row(
                    [
                        saldo_total,
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    total_entrada,
                    total_saida
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Divider(),
                ft.Text(value='Transações', size=20, color=ft.colors.LIGHT_BLUE_500 ,weight=ft.FontWeight.BOLD),
                historico, 
            ],
            spacing=10,
        )
    )

    page.add(
        layout,
        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=formulario)
    )

ft.app(target=main)