import flet as ft 
#import dados 


def main(page: ft.Page):


    #somatransacao = dados.quant_total

    barras = ft.BarChart(
        max_y=80,
        min_y=0,
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=50,
                        width=20,
                        color=ft.colors.CYAN,
                        border_radius=0,
                    ),
                ]
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=30,
                        width=20,
                        color=ft.colors.CYAN,
                        border_radius=0,
                    ),
                ]
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=10,
                        width=20,
                        color=ft.colors.CYAN,
                        border_radius=0,
                    ),
                ]
            )
        ],
        horizontal_grid_lines=ft.ChartGridLines(interval=5, color=ft.colors.WHITE, width=0.5, dash_pattern=[3,3]),
        left_axis=ft.ChartAxis(
            title=ft.Text(value=f"Valor total", color=ft.colors.WHITE),
            title_size=20,
            show_labels=False,
        ),
        bottom_axis=ft.ChartAxis(
            title=ft.Text(value=f"dia das transações", color=ft.colors.WHITE),
            title_size=20,
            show_labels=True,
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text(value="01/09", color=ft.colors.WHITE),
                ),
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text(value="10/09", color=ft.colors.WHITE),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text(value="23/09", color=ft.colors.WHITE),
                ),
            ],
            labels_interval=2,
        )
    )

    layout = ft.Container(
        border_radius=10,
        padding=10,
        expand=True,
        bgcolor=ft.colors.BLACK,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(value="Visão Geral", color=ft.colors.WHITE, size=18),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Text(value="Entradas", color=ft.colors.WHITE, size=18),
                        ft.Text(value=f"{0.00} Transações",color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Saídas", color=ft.colors.WHITE, size=18),
                        ft.Text(value=f"{0.00} Transações",color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Text(value="Saldo Total", color=ft.colors.WHITE, size=18),
                        ft.Text(value=f"{0.00} Transações",color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=2, color=ft.colors.WHITE),

                ft.Row(
                    [
                        ft.Container(
                            border_radius=10,
                            bgcolor=ft.colors.CYAN_100,
                            height=50,
                            width=100,
                            content=ft.Row(
                                [
                                    ft.Text(value="ENTRADAS", color=ft.colors.BLACK, size=12, weight=ft.FontWeight.BOLD)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )  
                        ),
                        ft.Container(
                            border_radius=10,
                            bgcolor=ft.colors.RED_100,
                            height=50,
                            width=100,
                            content=ft.Row(
                                [
                                    ft.Text(value="SAÍDAS", color=ft.colors.BLACK, size=12,  weight=ft.FontWeight.BOLD)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )  
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                barras,
            ]
        )
    )


    page.add(layout)





ft.app(target=main)