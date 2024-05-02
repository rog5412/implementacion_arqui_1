##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: dashboard.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define los elementos visuales de la pantalla
#   del tablero
#
#-------------------------------------------------------------------------
from src.controller.dashboard_controller import DashboardController
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Output, Input
from datetime import datetime


class Dashboard:

    def __init__(self, app):
        self.app = app
        self.date_from = datetime(2024, 1, 1).date()
        self.date_to = datetime(2024, 12, 31).date()
        self.app.callback(
            [Output("sales-per-date", "figure")], #Output("most-selled-products","children")],
            [Input("date_from", "date"), Input("date_to", "date")]
        )(self.update_dates)

    def update_dates(self, date_from, date_to):
        date_from = date_from.split("T")[0]
        date_to = date_to.split("T")[0]
        date_from =  datetime.strptime(date_from,"%Y-%m-%d")
        date_to = datetime.strptime(date_to,"%Y-%m-%d")
        print("formato de las fechas")
        print(date_from)
        print(date_to)
        data = DashboardController.load_sales_per_date_range(date_from, date_to)
        #most_selled = DashboardController.load_most_selled_products(date_from, date_to)
        print("Contenido de data")
        print(data)
        return (
            px.bar(data, x="dates", y="sales"),
            #[
            #    html.Div(
            #        [
            #            dbc.Row(
            #                [
            #                    html.H5(f"- {product['product']} [{product['times']} time(s) sold]" if int(product['times']) > 0 else "- ", style={"font-weight":"bold"}),
            #                ]
            #            ),
            #        ]
            #    )
            #    for product in most_selled
            #]
        )

    def document(self):
        return dbc.Container(
            fluid = True,
            children = [
                self._navbar_dates_picker("Pick the dates"),
                html.Br(),
                self._header_title("Sales Report"),
                html.Div(html.Hr()),
                self._header_subtitle("Sales summary financial report"),
                html.Br(),
                self._highlights_cards(),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_providers_by_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_sales_per_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.H3("Ventas por fecha", className="card-title"),
                                                    dcc.Graph(
                                                        id='sales-per-date',
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_orders_per_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._panel_best_sellers(),
                                    width=6
                                ),
                                dbc.Col(
                                    self._panel_worst_sales(),
                                    width=6
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._panel_most_selled_products(),
                                    width=12
                                ),
                            ]
                        )
                        
                    ]
                ),
            ]
        )

    def _header_title(self, title):
        return dbc.Row(
            [
                dbc.Col(html.H2(title, className="display-4"))
            ]
        )

    def _header_subtitle(self, subtitle):
        return html.Div(
            [
                html.P(
                    subtitle,
                    className="lead",
                ),
            ],
            id="blurb",
            style={"margin-top": "100px"}
        )

    def _card_value(self, label, value):
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H2(value, className="card-title"),
                    ]
                ),
                dbc.CardFooter(label),
            ]
        )

    def _highlights_cards(self):
        products = DashboardController.load_products()
        orders = DashboardController.load_orders()
        providers = DashboardController.load_providers()
        locations = DashboardController.load_locations()
        sales = DashboardController.load_sales()
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self._card_value("Products", products["products"])
                        ),
                        dbc.Col(
                            self._card_value("Orders", orders["orders"])
                        ),
                        dbc.Col(
                            self._card_value("Providers", providers["providers"])
                        ),
                        dbc.Col(
                            self._card_value("Locations", locations["locations"])
                        ),
                        dbc.Col(
                            self._card_value("Sales", "$ {:,.2f}".format(float(sales['sales'])))
                        ),
                    ]
                ),
            ]
        )

    # Se agregó esta función
    def _navbar_dates_picker(self, title: str):
        return dbc.Navbar(
            dbc.Container(
                [
                    self._header_title(title),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.DatePickerSingle(id="date_from", date = datetime(2024, 1, 1).date())
                            ),
                            dbc.Col(
                                dcc.DatePickerSingle(id="date_to", date = datetime(2024, 12, 31).date())
                            )
                        ]
                    ),
                ]
            ),
            class_name="mb-5",
            dark=True,
            fixed="top",
        )
    #
    
    def _bar_chart_providers_by_location(self):
        data = DashboardController.load_providers_per_location()
        bar_char_fig = px.bar(data, x="location", y="providers")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Providers per location", className="card-title"),
                        dcc.Graph(
                            id='providers-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_sales_per_location(self):
        data = DashboardController.load_sales_per_location()
        bar_char_fig = px.bar(data, x="location", y="sales")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Sales per location", className="card-title"),
                        dcc.Graph(
                            id='sales-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_orders_per_location(self):
        data = DashboardController.load_orders_per_location()
        bar_char_fig = px.bar(data, x="location", y="orders")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Orders per location", className="card-title"),
                        dcc.Graph(
                            id='orders-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _panel_best_sellers(self):
        best_sellers = DashboardController.load_best_sellers()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Best sellers", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in best_sellers
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_worst_sales(self):
        worst_sales = DashboardController.load_worst_sales()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Worst sales", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in worst_sales
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_most_selled_products(self):
        most_selled = DashboardController.load_most_selled_products(self.date_from, self.date_to)
        return html.Div(
            id='most-selled-products',
            children=[
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("Most selled", className="card-title"),
                            html.Br(),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                [
                                                    html.H5(f"- {product['product']} [{product['times']} time(s) sold]", style={"font-weight":"bold"}),
                                                ]
                                            ),
                                        ]
                                    )

                                    for product in most_selled
                                ]
                            )
                        ]
                    )
                )
            ]
        )
