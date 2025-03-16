from dash import dcc, html
import dash_bootstrap_components as dbc

def create_filter_panel(segments):
    """Cria o painel de filtros para a tabela de FIIs"""
    segment_options = [{'label': 'Todos', 'value': 'Todos'}]
    segment_options.extend([{'label': seg, 'value': seg} for seg in segments])
    
    filter_panel = dbc.Card([
        dbc.CardHeader("Filtros Avançados"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Segmento:"),
                    dcc.Dropdown(
                        id='segment-filter',
                        options=segment_options,
                        value='Todos',
                        clearable=False
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Dividend Yield Mínimo (%):"),
                    dcc.Slider(
                        id='min-dy-filter',
                        min=0,
                        max=15,
                        step=0.5,
                        value=0,
                        marks={i: str(i) for i in range(0, 16, 3)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Preço Máximo (R$):"),
                    dcc.Slider(
                        id='max-price-filter',
                        min=0,
                        max=500,
                        step=10,
                        value=500,
                        marks={i: str(i) for i in range(0, 501, 100)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("P/VP Máximo:"),
                    dcc.Slider(
                        id='max-pvp-filter',
                        min=0,
                        max=2,
                        step=0.1,
                        value=2,
                        marks={i/10: str(i/10) for i in range(0, 21, 5)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Buscar Ticker:"),
                    dbc.Input(
                        id='ticker-search',
                        type="text",
                        placeholder="Ex: KNRI11",
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Liquidez Mínima (R$):"),
                    dcc.Slider(
                        id='min-liquidez-filter',
                        min=0,
                        max=5000000,
                        step=100000,
                        value=0,
                        marks={i: f"{i/1000000:.1f}M" for i in range(0, 5000001, 1000000)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Vacância Máxima (%):"),
                    dcc.Slider(
                        id='max-vacancia-filter',
                        min=0,
                        max=30,
                        step=1,
                        value=30,
                        marks={i: str(i) for i in range(0, 31, 5)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Cap Rate Mínimo (%):"),
                    dcc.Slider(
                        id='min-cap-rate-filter',
                        min=0,
                        max=15,
                        step=0.5,
                        value=0,
                        marks={i: str(i) for i in range(0, 16, 3)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], width=3),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Aplicar Filtros",
                        id="apply-filters-button",
                        color="primary",
                        className="mt-3"
                    ),
                    dbc.Button(
                        "Limpar Filtros",
                        id="clear-filters-button",
                        color="secondary",
                        className="mt-3 ml-2"
                    ),
                ], width=12, className="d-flex justify-content-end")
            ]),
        ]),
    ])
    
    return filter_panel

def create_portfolio_input_form():
    """Cria o formulário para adicionar FIIs ao portfólio"""
    form = dbc.Card([
        dbc.CardHeader("Adicionar FII ao Portfólio"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Ticker:"),
                    dbc.Input(id="portfolio-ticker-input", placeholder="Ex: KNRI11", type="text"),
                ], width=3),
                
                                dbc.Col([
                    html.Label("Quantidade de Cotas:"),
                    dbc.Input(id="portfolio-quantity-input", placeholder="Ex: 100", type="number", min=1),
                ], width=3),
                
                dbc.Col([
                    html.Label("Preço Médio (R$):"),
                    dbc.Input(id="portfolio-price-input", placeholder="Ex: 115.50", type="number", min=0, step=0.01),
                ], width=3),
                
                dbc.Col([
                    html.Br(),
                    dbc.Button("Adicionar ao Portfólio", id="add-to-portfolio-button", color="success", className="mt-2"),
                ], width=3),
            ]),
        ]),
    ])
    
    return form

def create_advanced_filter_tabs():
    """Cria tabs com diferentes tipos de filtros avançados"""
    tabs = dbc.Tabs([
        dbc.Tab([
            html.Div([
                html.H5("Filtros por Rentabilidade", className="mt-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("DY Anual Mínimo (%):"),
                        dcc.Slider(
                            id='min-dy-annual-filter',
                            min=0,
                            max=15,
                            step=0.5,
                            value=0,
                            marks={i: str(i) for i in range(0, 16, 3)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("TIR Estimada Mínima (%):"),
                        dcc.Slider(
                            id='min-tir-filter',
                            min=0,
                            max=20,
                            step=0.5,
                            value=0,
                            marks={i: str(i) for i in range(0, 21, 4)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                ]),
            ], className="p-3"),
        ], label="Rentabilidade"),
        
        dbc.Tab([
            html.Div([
                html.H5("Filtros por Valorização", className="mt-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("P/VP Máximo:"),
                        dcc.Slider(
                            id='max-pvp-adv-filter',
                            min=0,
                            max=2,
                            step=0.1,
                            value=2,
                            marks={i/10: str(i/10) for i in range(0, 21, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("Spread P/VP Máximo (%):"),
                        dcc.Slider(
                            id='max-spread-pvp-filter',
                            min=-30,
                            max=30,
                            step=5,
                            value=30,
                            marks={i: str(i) for i in range(-30, 31, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                ]),
            ], className="p-3"),
        ], label="Valorização"),
        
        dbc.Tab([
            html.Div([
                html.H5("Filtros por Qualidade", className="mt-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("Vacância Máxima (%):"),
                        dcc.Slider(
                            id='max-vacancia-adv-filter',
                            min=0,
                            max=30,
                            step=1,
                            value=30,
                            marks={i: str(i) for i in range(0, 31, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("Cap Rate Mínimo (%):"),
                        dcc.Slider(
                            id='min-cap-rate-adv-filter',
                            min=0,
                            max=15,
                            step=0.5,
                            value=0,
                            marks={i: str(i) for i in range(0, 16, 3)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                ]),
            ], className="p-3"),
        ], label="Qualidade"),
        
        dbc.Tab([
            html.Div([
                html.H5("Filtros por Risco", className="mt-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("Sharpe Ratio Mínimo:"),
                        dcc.Slider(
                            id='min-sharpe-filter',
                            min=-1,
                            max=2,
                            step=0.1,
                            value=-1,
                            marks={i/10: str(i/10) for i in range(-10, 21, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("Liquidez Mínima (R$):"),
                        dcc.Slider(
                            id='min-liquidez-adv-filter',
                            min=0,
                            max=5000000,
                            step=100000,
                            value=0,
                            marks={i: f"{i/1000000:.1f}M" for i in range(0, 5000001, 1000000)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ], width=6),
                ]),
            ], className="p-3"),
        ], label="Risco"),
    ])
    
    return tabs

