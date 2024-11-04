import flet as ft
import openpyxl # Manipular Excel
import os # Acessa documentos através do sistema operacinal
from datetime import datetime # Capturar informações de data e hora
import pandas as pd



def main(page: ft.Page):

    preto = '#3D3D3D'
    azul = "#4895EF"
    verde = "#75975e"
    grafite = '#747169'
    vermelho = '#ee6b6e'

    desc_porc_real = ft.Container(
        expand=True,
        padding=10,
        margin=5,
        border_radius=10,
        content=ft.Column([]),
    )

    total_entrada = ft.Container(
        border_radius=5,
        height=60,
        width=120,
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.NORTH, color=verde),
                ft.Text(value=0, size=15, weight=ft.FontWeight.BOLD, color=verde),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    total_saida = ft.Container(
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=5,
        height=60,
        width=120,
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.SOUTH, color=vermelho),
                ft.Text(value=0, size=15, weight=ft.FontWeight.BOLD, color=verde),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    saldo_total = ft.Container(
        margin=10,
        expand=True,
        border_radius=5,
        content=ft.Row(
            [
                ft.Text(value=0, size=25, weight=ft.FontWeight.BOLD, color=verde)
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
                            ft.Text(row[1], width=70, size=12, color=ft.colors.WHITE, weight=ft.FontWeight.W_600),
                            ft.Text(f"{row[7]}/{row[6]}/{row[5]}", width=70, size=12, color=ft.colors.WHITE, weight=ft.FontWeight.W_600),
                            ft.Text(f"R$ {row[3]}", width=70, size=12, color=ft.colors.WHITE, weight=ft.FontWeight.W_600),
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

        total_entrada.content.controls[1].value = f"R$ {en:.2f}"
        total_saida.content.controls[1].value = f"R$ {sa:.2f}"
        saldo_total.content.controls[0].value =  f"R$ {to:.2f}"

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
    
    def abrir_pg_analise(e):
        page.clean()
        page.add(pg_analise)
        page.update()
        
    def fecha_pg(e):
        page.clean()
        page.add(
        layout,
        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=formulario)
    )
        page.update()

    
    
    data_inicial = ft.Text(value=0, size=15, color=ft.colors.WHITE)
    data_final = ft.Text(value=0, size=15, color=ft.colors.WHITE)

    def calcular_totais(df_filtrado):
        # Filtra todas as transações do tipo "Entrada"
        entradas = df_filtrado[df_filtrado['Tipo'] == 'Entrada']
        soma_entradas = entradas['Valor'].sum()
        qtd_entradas = len(entradas)

        # Filtra todas as transações do tipo "Saída"
        saidas = df_filtrado[df_filtrado['Tipo'] == 'Saída']
        soma_saidas = saidas['Valor'].sum()
        qtd_saidas = len(saidas)

    # Total geral de transações
        total_transacoes = soma_entradas + soma_saidas
        qtd_transacoes = qtd_entradas + qtd_saidas

    # Retornar os resultados
        return {
            'total_entradas': soma_entradas,
            'qtd_entradas': qtd_entradas,
            'total_saidas': soma_saidas,
            'qtd_saidas': qtd_saidas,
            'total_transacoes': total_transacoes,
            'qtd_transacoes': qtd_transacoes
        }
    

    # Inicializando as variáveis globais com None
    data_inicial_datetime = None
    data_final_datetime = None

    def on_date_selected(e):

        global data_inicial_datetime, data_final_datetime

        selected_date = e.control.value

        data_formatada = selected_date.strftime("%d/%m/%y")
        if e.control.data == "from_date":
            data_inicial.value = f"De: {data_formatada}"
            data_inicial_datetime = selected_date
            data_inicial.update()
        elif e.control.data == "to_date":
            data_final.value = f"Até: {data_formatada}"
            data_final_datetime = selected_date
            data_final.update()

        # Chamar a função de filtragem apenas quando ambas as datas forem selecionadas
        # Checar se ambas as datas foram selecionadas (ou se data final foi preenchida automaticamente)
            while data_inicial_datetime is not None and data_final_datetime is not None:
                
                df_filtrados = filtrar_dados_por_periodo(data_inicial_datetime, data_final_datetime)
                resultados = calcular_totais(df_filtrados)

                # Usando os resultados nas variáveis
                quantidade_entrada.value = f"{resultados['qtd_entradas']}. Entradas"
                valor_entrada.value = f"R$      {resultados['total_entradas']:.2f}"
                quantidade_saida.value = f"{resultados['qtd_saidas']}. Saídas"
                valor_saida.value = f"R$      {resultados['total_saidas']:.2f}"
                quantidade_transacoes.value = f"{resultados['qtd_transacoes']}. Transações"
                valor_transacoes.value = f"R$      {resultados['total_transacoes']:.2f}"
                page.update()
                return resultados
            else:
                return
    

    #Aqui começa o tratamento para exibir informações sobre das transações e seus valores
    # dentro do período selecionado e filtrado por entrada ou saída
    def filtrando_tipo(e):
        global data_inicial_datetime, data_final_datetime
        tipo = e.control.data 
        # Checar se ambas as datas foram selecionadas (ou se data final foi preenchida automaticamente
        if data_inicial_datetime is not None and data_final_datetime is not None:
            df = filtrar_dados_por_periodo(data_inicial_datetime, data_final_datetime)
            if tipo == 'E':
                df_entradas = df[df['Tipo'] == 'Entrada']
                df_entradas_processado = processa_dados(df_entradas)
                return df_entradas_processado
            elif tipo == 'S':
                df_saidas = df[df['Tipo'] == 'Saída']
                df_saidas_processado = processa_dados(df_saidas)
                return df_saidas_processado
        else:
            return

    lista_trasacoes = []
    
    def processa_dados(df):

        # 1º calcular o valor total
        total_valor = df['Valor'].sum()
        # 2. Agrupe o DataFrame por 'Descrição' para calcular a quantidade e o valor total de cada grupo
        agrupamento = df.groupby('Descrição').agg(
            quantidade=('Valor', 'size'),        # Conta quantas vezes a descrição aparece
            valor_total=('Valor', 'sum')         # Soma os valores para cada descrição
        ).reset_index()  # Convertemos para um DataFrame padrão após o agrupamento    
        # 3. Calcule a porcentagem de cada descrição em relação ao total do período selecionado
        agrupamento['percentual'] = (agrupamento['valor_total'] / total_valor * 100).round(2)

        def listas_dados_processado(df):
            global lista_trasacoes 

            lista_processada = df.values.tolist()
            lista_trasacoes = lista_processada
            return lista_processada

        listas_processadas = listas_dados_processado(agrupamento)

        desc_porc_real.content.controls.clear()

        for i in listas_processadas:
            trasa_text = f"{i[1]} x {i[0]}  R${i[2]:.2f}  total de {i[3]} %"
            u = ft.Row([ft.Text(trasa_text, style=ft.TextStyle(size=13, color=ft.colors.WHITE))])
            # Adiciona a linha ao container desc_porc_real
            desc_porc_real.content.controls.append(u)
        # Atualiza o container para exibir as novas linhas
        desc_porc_real.update()
        


    # Função que usa os objetos datetime
    def filtrar_dados_por_periodo(data_inicial_datetime, data_final_datetime):
    # Carrega o arquivo Excel
        df = pd.read_excel("transacoes.xlsx")

    # Criar a coluna de data no formato datetime
        df['Data'] = pd.to_datetime(df[['Ano', 'Mês', 'Dia']].rename(columns={'Ano': 'year', 'Mês': 'month', 'Dia': 'day'}))

    # Filtrar o dataframe pelo período selecionado
        df_filtrado = df[(df['Data'] >= data_inicial_datetime) & (df['Data'] <= data_final_datetime)]

        return df_filtrado

    datepicker_de = ft.DatePicker(
        open=False,
        data="from_date",
        on_change=on_date_selected 
    )

    datepicker_ate = ft.DatePicker(
        open=False,
        data="to_date",
        on_change=on_date_selected 
    )

    def abrir_date_de(e):
        e.page.overlay.append(datepicker_de)
        datepicker_de.open = True
        e.page.update()

    def abrir_date_ate(e):
        e.page.overlay.append(datepicker_ate)
        datepicker_ate.open = True
        e.page.update()

    quantidade_entrada = ft.Text(value="0. Entrada", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)
    valor_entrada = ft.Text(value="0.00 R$", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)
    quantidade_saida = ft.Text(value="0. Saída", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)
    valor_saida = ft.Text(value="0.00 R$", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)
    quantidade_transacoes = ft.Text(value="0. Transações", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)
    valor_transacoes = ft.Text(value="0.00 R$", weight=ft.FontWeight.W_500,  italic=True, size=15, color=ft.colors.WHITE)


    infor_geral = ft.Container(
        margin=5,
        padding=5,
        content=ft.Column(
            [
                ft.Row(
                    [
                        quantidade_entrada,                      
                        valor_entrada,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        quantidade_saida,
                        valor_saida,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        quantidade_transacoes,
                        valor_transacoes,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]
        )
    )



    filtro_tipo = ft.Container(
        border_radius=10,
        bgcolor=ft.colors.WHITE10,
        content=ft.Row(
            [
                ft.Container(
                    data='E',
                    on_click=filtrando_tipo,
                    height=35,
                    width=35,
                    bgcolor=ft.colors.BLUE,
                    shape=ft.BoxShape.CIRCLE,
                    content=ft.Text(value="E", weight=ft.FontWeight.BOLD, size=20, color=ft.colors.BLUE_50, text_align=ft.TextAlign.CENTER),
                ),
                ft.Container(
                    data='S',
                    on_click=filtrando_tipo,
                    height=35,
                    width=35,
                    bgcolor=ft.colors.RED,
                    shape=ft.BoxShape.CIRCLE,
                    content=ft.Text(value="S", weight=ft.FontWeight.BOLD, size=20, color=ft.colors.RED_50, text_align=ft.TextAlign.CENTER),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    )

    barras_forma = ft.Container(
        expand=True,
        height=150,
        content=ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=20,
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=30,
                            width=20,
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=20,
                            width=20,
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=10,
                            width=20,
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=2,
                            width=20,
                        ),
                    ],
                    bars_space=15,
                )
            ]
        )
    )

    lista=['Pix', 'Dinheiro', 'Outros', 'Fiado', 'Cartão']
    porcentagem_forma = ['40', '30', '20', '10', '2']

    pizza_forma = ft.Container(
        expand=True,
        height=120,
        width=100,
        #bgcolor=ft.colors.AMBER_100,
        content=ft.PieChart(
            center_space_radius=15,
            sections=[
                ft.PieChartSection(
                    value=40,
                    title=f"{lista[0]} {porcentagem_forma[0]} %",
                    radius=50,
                    title_position=0.5,
                ),
            ],
        )
    )
    real_forma = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(value="Pix...", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300),
                        ft.Text(value="2580,20", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Dinheiro...", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300),
                        ft.Text(value="1200.00", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Outros...", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300),
                        ft.Text(value="600.00", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Fiado...", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300),
                        ft.Text(value="200.00", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Cartão...", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300),
                        ft.Text(value="0.00", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.W_300)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )
        

    painel = ft.Container(

        content=ft.Column(
            [ 
                ft.Text(value='Formas de Transações', color=ft.colors.WHITE, size=18, italic=True),
                ft.Row(
                    [
                        pizza_forma,
                        real_forma
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                ft.Text(value='Categorias das Transações', color=ft.colors.WHITE, size=18, italic=True),
                barras_forma,
                ft.Text(value='Sobre as Transações', color=ft.colors.WHITE, size=18, italic=True),
                desc_porc_real

            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
    )



    pg_analise = ft.Container(
        expand=True,
        bgcolor=preto,
        padding=10,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.CLOSE, icon_color=ft.colors.WHITE, icon_size=20, on_click=fecha_pg),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Text(value="Período", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                ft.Column(
                    [
                        ft.Row([
                            data_inicial,
                            ft.IconButton(icon=ft.icons.CALENDAR_TODAY, icon_color=ft.colors.WHITE, on_click=abrir_date_de),
                            data_final,
                            ft.IconButton(icon=ft.icons.CALENDAR_TODAY, icon_color=ft.colors.WHITE, on_click=abrir_date_ate)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ],
                ),
                infor_geral,
                filtro_tipo,
                painel,
            ]
        )
    )


    analise = ft.IconButton(icon=ft.icons.ANALYTICS, icon_color=verde, icon_size=25, on_click=abrir_pg_analise)
    btn_limpardados = ft.IconButton(icon=ft.icons.DELETE_FOREVER, icon_color=vermelho, icon_size=25, on_click=mostrar_alerta_confirmacao)

    
    b = '#00FF7F' 
    c = '#ADFF2F'
    d = '#FFC300' 

    

    layout = ft.Container(
        expand=True,
        bgcolor=preto,
        border_radius=5,
        padding=5,
        content=ft.Column(
            [
                ft.Row([analise], alignment=ft.MainAxisAlignment.END),
                ft.Container(
                    margin=15,
                    border=ft.border.all(width=0.5, color=ft.colors.WHITE),
                    gradient=ft.LinearGradient(
                        colors=[
                        b, c, d
                        ]
                    ),
                    border_radius=10,
                    content=ft.Column(
                        [
                            ft.Row([saldo_total], alignment=ft.MainAxisAlignment.END),
                            ft.Row([total_entrada, total_saida], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                        ]
                    )
                ),
                ft.Row(
                    [
                        ft.Text(value='TRANSAÇÕES', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
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
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)