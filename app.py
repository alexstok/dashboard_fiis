import dash
from dash import html, dcc, callback, Input, Output, State, Dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import json
import numpy as np
import plotly.express as px
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Importar componentes personalizados
from data_handler import FIIDataHandler
from components.tables import create_main_table, create_portfolio_table, create_dividend_calendar_table, create_advanced_indicators_table
from components.charts import (create_sector_distribution_chart, create_top_dividend_chart, 
                              create_top_discounted_chart, create_opportunity_chart, 
                              create_portfolio_distribution_chart, create_cap_rate_vacancia_chart,
                              create_yield_curve_chart)
from components.filters import create_filter_panel, create_portfolio_input_form, create_advanced_filter_tabs
from components.modals import (create_fii_details_modal, create_fii_overview_content, 
                              create_fii_dividend_content, create_fii_analysis_content,
                              create_fii_advanced_content, create_fii_recommendation_content)

# Inicializar o app Dash com suppress_callback_exceptions=True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Dashboard de FIIs - Análise de Dividendos e Rentabilidade"

# Inicializar o manipulador de dados
data_handler = FIIDataHandler()

# Layout principal do app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard Avançado de FIIs", className="text-center my-4"),
            html.H5("Análise de Dividendos, Rentabilidade e Indicadores Avançados", className="text-center mb-4"),
        ], width=12)
    ]),
    
    dbc.Tabs([
        # Aba principal com tabelas e gráficos
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Div(id="filter-container", className="mt-3"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("FIIs abaixo de R$ 25,00", className="mt-4"),
                    html.Div(id="top-fiis-table-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Todos os FIIs", className="mt-4"),
                    html.Div(id="all-fiis-table-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Análise de Mercado", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="sector-distribution-chart-container"),
                                ], width=6),
                                
                                dbc.Col([
                                    html.Div(id="top-dividend-chart-container"),
                                ], width=6),
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="top-discounted-chart-container"),
                                ], width=6),
                                
                                dbc.Col([
                                    html.Div(id="opportunity-chart-container"),
                                ], width=6),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Indicadores Avançados", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="cap-rate-vacancia-chart-container"),
                                ], width=6),
                                
                                dbc.Col([
                                    html.Div(id="yield-curve-chart-container"),
                                ], width=6),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Alertas de Oportunidades", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Melhores Oportunidades"),
                                        dbc.CardBody(id="best-opportunities-container"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Alto Dividend Yield"),
                                        dbc.CardBody(id="high-dy-container"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Baixo P/VP"),
                                        dbc.CardBody(id="low-pvp-container"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Abaixo do Preço Justo"),
                                        dbc.CardBody(id="below-fair-price-container"),
                                    ]),
                                ], width=3),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Exportar Dados para CSV",
                        id="export-data-button",
                        color="primary",
                        className="mt-4"
                    ),
                    dcc.Download(id="download-dataframe-csv"),
                ], width=12, className="d-flex justify-content-end")
            ]),
        ], label="Dashboard Principal"),
        
        # Aba de análise avançada
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("Filtros Avançados", className="mt-4"),
                    html.Div(id="advanced-filter-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Análise Multidimensional", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="advanced-analysis-container"),
                                ], width=12),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Comparação de Indicadores", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="indicators-comparison-container"),
                                ], width=12),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
        ], label="Análise Avançada"),
        
        # Aba de portfólio
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Div(id="portfolio-input-container", className="mt-3"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Meu Portfólio", className="mt-4"),
                    html.Div(id="portfolio-table-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Resumo do Portfólio", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Valor Total"),
                                        dbc.CardBody(id="portfolio-total-value"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Rentabilidade"),
                                        dbc.CardBody(id="portfolio-returns"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Dividendos Mensais"),
                                        dbc.CardBody(id="portfolio-monthly-dividends"),
                                    ]),
                                ], width=3),
                                
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Dividendos Anuais"),
                                        dbc.CardBody(id="portfolio-annual-dividends"),
                                    ]),
                                ], width=3),
                            ]),
                        ])
                    ]),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Distribuição do Portfólio", className="mt-4"),
                    html.Div(id="portfolio-distribution-chart-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Análise de Risco do Portfólio", className="mt-4"),
                    html.Div(id="portfolio-risk-analysis-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Exportar Portfólio para CSV",
                        id="export-portfolio-button",
                        color="primary",
                        className="mt-4"
                    ),
                    dcc.Download(id="download-portfolio-csv"),
                ], width=12, className="d-flex justify-content-end")
            ]),
        ], label="Meu Portfólio"),
        
        # Aba de calendário
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("Calendário de Dividendos", className="mt-4"),
                    html.Div(id="dividend-calendar-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Próximos Eventos", className="mt-4"),
                    html.Div(id="upcoming-events-container"),
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Como Funcionam os Dividendos de FIIs", className="mt-4"),
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Data de Corte (Data Com)"),
                            html.P("A data de corte, também conhecida como 'data com', é o último dia em que você pode comprar um FII e ainda ter direito ao próximo dividendo. Se você comprar o FII no dia seguinte à data de corte, não receberá o próximo dividendo."),
                            
                            html.H4("Data Ex"),
                            html.P("A data ex é o primeiro dia em que o FII é negociado sem o direito ao próximo dividendo. Geralmente é o dia seguinte à data de corte."),
                            
                            html.H4("Data de Pagamento"),
                            html.P("A data de pagamento é quando o dividendo é efetivamente depositado na sua conta. Geralmente ocorre alguns dias após a data de corte."),
                            
                            html.H4("Isenção de Imposto de Renda"),
                            html.P("Uma das principais vantagens dos FIIs é que os dividendos distribuídos são isentos de Imposto de Renda para pessoas físicas."),
                        ])
                    ]),
                ], width=12)
            ]),
        ], label="Calendário de Dividendos"),
    ]),
    
    # Modal de detalhes do FII
    create_fii_details_modal(),
    
    # Armazenamento de dados
    dcc.Store(id='all-fiis-data-store'),
    dcc.Store(id='filtered-fiis-data-store'),
    dcc.Store(id='portfolio-data-store', data=[]),
    dcc.Store(id='selected-fii-data-store'),
    dcc.Store(id='historical-data-store'),
    
    # Elemento dummy para inicialização
    html.Div(id="_", style={"display": "none"}),
    
    # Componentes ocultos para evitar erros de callback
    dbc.Button(id="modal-add-to-portfolio", style={"display": "none"}),
    dbc.Input(id="modal-quantity-input", type="number", style={"display": "none"}),
    dbc.Input(id="modal-price-input", type="number", style={"display": "none"}),
    dbc.Input(id="simulation-value-input", type="number", style={"display": "none"}),
    html.Div(id="simulation-results", style={"display": "none"}),
    html.Div(id="annual-projection-results", style={"display": "none"}),
    dcc.Graph(id="projection-chart", style={"display": "none"}),
    
    # Informações de atualização
    dbc.Row([
        dbc.Col([
            html.Div(id="last-update-info", className="text-muted text-right mt-4"),
        ], width=12)
    ]),
    
], fluid=True)

# Callbacks

# Carregar dados iniciais
@app.callback(
    [Output('all-fiis-data-store', 'data'),
     Output('last-update-info', 'children')],
    [Input('_', 'children')],
    prevent_initial_call=False
)
def load_initial_data(_):
    df = data_handler.fetch_data()
    last_update = data_handler.last_update.strftime("%d/%m/%Y %H:%M:%S") if data_handler.last_update else "N/A"
    return df.to_dict('records'), f"Última atualização: {last_update}"

# Inicializar componentes
@app.callback(
    [Output('filter-container', 'children'),
     Output('advanced-filter-container', 'children'),
     Output('top-fiis-table-container', 'children'),
     Output('all-fiis-table-container', 'children'),
     Output('sector-distribution-chart-container', 'children'),
     Output('top-dividend-chart-container', 'children'),
     Output('top-discounted-chart-container', 'children'),
     Output('opportunity-chart-container', 'children'),
     Output('cap-rate-vacancia-chart-container', 'children'),
     Output('yield-curve-chart-container', 'children'),
     Output('portfolio-input-container', 'children'),
     Output('dividend-calendar-container', 'children')],
    [Input('all-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def initialize_components(all_fiis_data):
    if not all_fiis_data:
        return [html.Div("Carregando dados...") for _ in range(12)]
    
    df = pd.DataFrame(all_fiis_data)
    
    # Obter lista de segmentos únicos para o filtro
    segments = sorted(df['Segmento'].unique())
    
    # Criar componentes
    filter_panel = create_filter_panel(segments)
    advanced_filter_tabs = create_advanced_filter_tabs()
    
    top_fiis = data_handler.get_top_fiis_by_price(max_price=25, limit=30)
    top_fiis_table = create_main_table(top_fiis, id_prefix='top')
    
    all_fiis = data_handler.get_all_fiis(limit=150)
    all_fiis_table = create_main_table(all_fiis, id_prefix='all')
    
    sector_chart = create_sector_distribution_chart(df)
    top_dividend_chart = create_top_dividend_chart(df)
    top_discounted_chart = create_top_discounted_chart(df)
    opportunity_chart = create_opportunity_chart(df)
    cap_rate_vacancia_chart = create_cap_rate_vacancia_chart(df)
    yield_curve_chart = create_yield_curve_chart(df)
    
    portfolio_form = create_portfolio_input_form()
    
    calendar_data = data_handler.get_dividend_calendar()
    calendar_table = create_dividend_calendar_table(calendar_data)
    
    return [
        filter_panel,
        advanced_filter_tabs,
        top_fiis_table,
        all_fiis_table,
        sector_chart,
        top_dividend_chart,
        top_discounted_chart,
        opportunity_chart,
        cap_rate_vacancia_chart,
        yield_curve_chart,
        portfolio_form,
        calendar_table
    ]

# Aplicar filtros
@app.callback(
    Output('filtered-fiis-data-store', 'data'),
    [Input('apply-filters-button', 'n_clicks')],
    [State('all-fiis-data-store', 'data'),
     State('segment-filter', 'value'),
     State('min-dy-filter', 'value'),
     State('max-price-filter', 'value'),
     State('max-pvp-filter', 'value'),
     State('ticker-search', 'value'),
     State('min-liquidez-filter', 'value')],
    prevent_initial_call=True
)
def apply_filters(n_clicks, all_fiis_data, segment, min_dy, max_price, max_pvp, ticker, min_liquidez):
    if not n_clicks or not all_fiis_data:
        raise PreventUpdate
    
    df = pd.DataFrame(all_fiis_data)
    filtered_df = data_handler.filter_data(df, segment, min_dy, max_price, ticker, max_pvp, min_liquidez)
    
    return filtered_df.to_dict('records')

# Limpar filtros
@app.callback(
    [Output('segment-filter', 'value'),
     Output('min-dy-filter', 'value'),
     Output('max-price-filter', 'value'),
     Output('max-pvp-filter', 'value'),
     Output('ticker-search', 'value'),
     Output('min-liquidez-filter', 'value')],
    [Input('clear-filters-button', 'n_clicks')],
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return 'Todos', 0, 500, 2, '', 0

# Atualizar tabelas com dados filtrados
@app.callback(
    [Output('top-table', 'data'),
     Output('all-table', 'data')],
    [Input('filtered-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def update_tables(filtered_data):
    if not filtered_data:
        raise PreventUpdate
    
    df = pd.DataFrame(filtered_data)
    
    # Filtrar para tabela de top FIIs (abaixo de R$25)
    top_fiis = df[df['Preço'] <= 25].copy()
    top_fiis = top_fiis.sort_values('DY Anual', ascending=False).head(30)
    
    # Tabela com todos os FIIs
    all_fiis = df.head(150)
    
    return top_fiis.to_dict('records'), all_fiis.to_dict('records')

# Atualizar alertas de oportunidades
@app.callback(
    [Output('best-opportunities-container', 'children'),
     Output('high-dy-container', 'children'),
     Output('low-pvp-container', 'children'),
     Output('below-fair-price-container', 'children')],
    [Input('all-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def update_opportunity_alerts(all_fiis_data):
    if not all_fiis_data:
        return [html.Div("Carregando...") for _ in range(4)]
    
    df = pd.DataFrame(all_fiis_data)
    
    # Melhores oportunidades (alto DY + baixo P/VP + alto Sharpe)
    df_copy = df.copy()
    df_copy.loc[:, 'Opportunity_Score'] = df_copy['DY Anual'] - (df_copy['P/VP'] * 2) + df_copy.get('Sharpe Ratio', 0) * 2
    best_opportunities = df_copy.sort_values('Opportunity_Score', ascending=False).head(5)
    best_opps_list = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Div(f"{row['Ticker']} - {row['Segmento']}"),
            html.Small(f"DY: {row['DY Anual']:.2f}% | P/VP: {row['P/VP']:.2f} | Preço: R$ {row['Preço']:.2f}")
        ])
        for _, row in best_opportunities.iterrows()
    ], flush=True)
    
    # Alto dividend yield
    high_dy = df.sort_values('DY Anual', ascending=False).head(5)
    high_dy_list = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Div(f"{row['Ticker']} - {row['Segmento']}"),
            html.Small(f"DY: {row['DY Anual']:.2f}% | Preço: R$ {row['Preço']:.2f}")
        ])
        for _, row in high_dy.iterrows()
    ], flush=True)
    
    # Baixo P/VP
    low_pvp = df.sort_values('P/VP').head(5)
    low_pvp_list = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Div(f"{row['Ticker']} - {row['Segmento']}"),
            html.Small(f"P/VP: {row['P/VP']:.2f} | Preço: R$ {row['Preço']:.2f}")
        ])
        for _, row in low_pvp.iterrows()
    ], flush=True)
    
    # Abaixo do preço justo
    df_copy2 = df.copy()
    df_copy2.loc[:, 'Price_Discount'] = (df_copy2['Preço Justo'] / df_copy2['Preço']) - 1
    below_fair = df_copy2[df_copy2['Price_Discount'] > 0].sort_values('Price_Discount', ascending=False).head(5)
    below_fair_list = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Div(f"{row['Ticker']} - {row['Segmento']}"),
            html.Small(f"{row['Price_Discount']*100:.2f}% abaixo | Preço: R$ {row['Preço']:.2f} | Justo: R$ {row['Preço Justo']:.2f}")
        ])
        for _, row in below_fair.iterrows()
    ], flush=True)
    
    return best_opps_list, high_dy_list, low_pvp_list, below_fair_list

# Adicionar FII ao portfólio
@app.callback(
    Output('portfolio-data-store', 'data'),
    [Input('add-to-portfolio-button', 'n_clicks'),
     Input('modal-add-to-portfolio', 'n_clicks')],
    [State('portfolio-data-store', 'data'),
     State('all-fiis-data-store', 'data'),
     State('portfolio-ticker-input', 'value'),
     State('portfolio-quantity-input', 'value'),
     State('portfolio-price-input', 'value'),
     State('selected-fii-data-store', 'data'),
     State('modal-quantity-input', 'value'),
     State('modal-price-input', 'value')],
    prevent_initial_call=True
)
def add_to_portfolio(n_clicks1, n_clicks2, portfolio_data, all_fiis_data, ticker, quantity, price, selected_fii, modal_quantity, modal_price):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Verificar se o trigger é válido
    if trigger_id not in ['add-to-portfolio-button', 'modal-add-to-portfolio']:
        raise PreventUpdate
    
    if trigger_id == 'add-to-portfolio-button':
        if not ticker or not quantity or not price:
            return portfolio_data
        
        # Verificar se o ticker existe
        df = pd.DataFrame(all_fiis_data)
        if ticker not in df['Ticker'].values:
            return portfolio_data
        
        fii_data = df[df['Ticker'] == ticker].iloc[0].to_dict()
        
    elif trigger_id == 'modal-add-to-portfolio':
        if not selected_fii or not modal_quantity or not modal_price:
            return portfolio_data
        
        ticker = selected_fii['Ticker']
        quantity = modal_quantity
        price = modal_price
        fii_data = selected_fii
    
    else:
        return portfolio_data
    
    # Adicionar ao portfólio
    new_item = {
        'Ticker': ticker,
        'Quantidade': quantity,
        'Preço Médio': price,
        'Preço Atual': fii_data['Preço'],
        'Segmento': fii_data['Segmento'],
        'DY Anual': fii_data['DY Anual'],
        'DY Mensal': fii_data['DY Mensal'],
    }
    
    # Verificar se o FII já existe no portfólio
    for i, item in enumerate(portfolio_data):
        if item['Ticker'] == ticker:
            # Atualizar quantidade e preço médio
            total_value = (item['Quantidade'] * item['Preço Médio']) + (quantity * price)
            total_quantity = item['Quantidade'] + quantity
            new_avg_price = total_value / total_quantity
            
            portfolio_data[i]['Quantidade'] = total_quantity
            portfolio_data[i]['Preço Médio'] = new_avg_price
            return portfolio_data
    
    # Adicionar novo item
    portfolio_data.append(new_item)
    return portfolio_data

# Atualizar tabela do portfólio
@app.callback(
    Output('portfolio-table-container', 'children'),
    Input('portfolio-data-store', 'data'),
    prevent_initial_call=True
)
def update_portfolio_table(portfolio_data):
    if not portfolio_data:
        return html.Div("Adicione FIIs ao seu portfólio para visualizar a tabela.")
    return create_portfolio_table(portfolio_data)

# Atualizar resumo do portfólio
@app.callback(
    [Output('portfolio-total-value', 'children'),
     Output('portfolio-returns', 'children'),
     Output('portfolio-monthly-dividends', 'children'),
     Output('portfolio-annual-dividends', 'children'),
     Output('portfolio-distribution-chart-container', 'children'),
     Output('portfolio-risk-analysis-container', 'children')],
    [Input('portfolio-data-store', 'data'),
     Input('all-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def update_portfolio_summary(portfolio_data, all_fiis_data):
    if not portfolio_data:
        return [
            "R$ 0,00",
            "0,00%",
            "R$ 0,00",
            "R$ 0,00",
            html.Div("Adicione FIIs ao seu portfólio para visualizar a distribuição."),
            html.Div("Adicione FIIs ao seu portfólio para visualizar a análise de risco.")
        ]
    
    df = pd.DataFrame(portfolio_data)
    
    # Calcular valores
    df.loc[:, 'Valor Investido'] = df['Quantidade'] * df['Preço Médio']
    df.loc[:, 'Valor Atual'] = df['Quantidade'] * df['Preço Atual']
    df.loc[:, 'Rentabilidade'] = ((df['Valor Atual'] / df['Valor Investido']) - 1) * 100
    df.loc[:, 'Dividendos Mensais'] = df['Valor Atual'] * (df['DY Mensal'] / 100)
    df.loc[:, 'Dividendos Anuais'] = df['Valor Atual'] * (df['DY Anual'] / 100)
    df.loc[:, 'Yield on Cost'] = (df['Dividendos Anuais'] / df['Valor Investido']) * 100
    
    total_invested = df['Valor Investido'].sum()
    total_current = df['Valor Atual'].sum()
    total_return = ((total_current / total_invested) - 1) * 100 if total_invested > 0 else 0
    total_monthly_dividends = df['Dividendos Mensais'].sum()
    total_annual_dividends = df['Dividendos Anuais'].sum()
    
    # Formatar valores
    total_value = html.Div([
        html.H3(f"R$ {total_current:.2f}"),
        html.P(f"Investido: R$ {total_invested:.2f}", className="text-muted")
    ])
    
    returns_color = "text-success" if total_return >= 0 else "text-danger"
    returns = html.Div([
        html.H3([f"{'+' if total_return >= 0 else ''}{total_return:.2f}%"], className=returns_color),
        html.P(f"R$ {total_current - total_invested:.2f}", className="text-muted")
    ])
    
    monthly_dividends = html.Div([
        html.H3(f"R$ {total_monthly_dividends:.2f}"),
        html.P(f"{(total_monthly_dividends / total_current) * 100:.2f}% a.m." if total_current > 0 else "0.00% a.m.", className="text-muted")
    ])
    
    annual_dividends = html.Div([
        html.H3(f"R$ {total_annual_dividends:.2f}"),
        html.P(f"{(total_annual_dividends / total_current) * 100:.2f}% a.a." if total_current > 0 else "0.00% a.a.", className="text-muted")
    ])
    
    # Gráfico de distribuição
    distribution_chart = create_portfolio_distribution_chart(portfolio_data)
    
    # Análise de risco do portfólio
    all_fiis_df = pd.DataFrame(all_fiis_data)
    
    # Calcular métricas de risco
    portfolio_dy = (total_annual_dividends / total_current) * 100 if total_current > 0 else 0
    market_dy = all_fiis_df['DY Anual'].mean()
    
    portfolio_pvp = df['P/VP'].mean() if 'P/VP' in df.columns else 1.0
    market_pvp = all_fiis_df['P/VP'].mean()
    
    # Diversificação por segmento
    segment_count = df['Segmento'].nunique()
    total_segments = all_fiis_df['Segmento'].nunique()
    diversification = (segment_count / total_segments) * 100
    
    risk_analysis = dbc.Card([
        dbc.CardHeader("Análise de Risco e Qualidade do Portfólio"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Rendimento vs Mercado"),
                        dbc.CardBody([
                            html.P(f"DY do Portfólio: {portfolio_dy:.2f}%"),
                            html.P(f"DY Médio do Mercado: {market_dy:.2f}%"),
                            html.P(f"Diferença: {portfolio_dy - market_dy:+.2f}%", 
                                  className="text-success" if portfolio_dy >= market_dy else "text-danger")
                        ]),
                    ]),
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Valorização vs Mercado"),
                        dbc.CardBody([
                            html.P(f"P/VP Médio do Portfólio: {portfolio_pvp:.2f}"),
                            html.P(f"P/VP Médio do Mercado: {market_pvp:.2f}"),
                            html.P(f"Diferença: {portfolio_pvp - market_pvp:+.2f}", 
                                  className="text-danger" if portfolio_pvp >= market_pvp else "text-success")
                        ]),
                    ]),
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Diversificação"),
                        dbc.CardBody([
                            html.P(f"Segmentos no Portfólio: {segment_count} de {total_segments}"),
                            html.P(f"Nível de Diversificação: {diversification:.1f}%"),
                            html.P(f"Avaliação: {'Boa' if diversification > 50 else 'Média' if diversification > 30 else 'Baixa'}", 
                                  className=f"{'text-success' if diversification > 50 else 'text-warning' if diversification > 30 else 'text-danger'}")
                        ]),
                    ]),
                ], width=4),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H5("Recomendações para o Portfólio", className="mt-4"),
                    html.Ul([
                        html.Li("Aumentar diversificação por segmentos") if diversification < 50 else None,
                        html.Li("Considerar FIIs com maior dividend yield") if portfolio_dy < market_dy else None,
                        html.Li("Buscar FIIs com menor P/VP") if portfolio_pvp > market_pvp else None,
                        html.Li("Portfólio bem posicionado em termos de rendimento") if portfolio_dy > market_dy else None,
                        html.Li("Portfólio com boa valorização (P/VP abaixo da média)") if portfolio_pvp < market_pvp else None,
                    ]),
                ], width=12),
            ]),
        ]),
    ])
    
    return total_value, returns, monthly_dividends, annual_dividends, distribution_chart, risk_analysis

# Exportar dados para CSV
@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('export-data-button', 'n_clicks'),
    State('all-fiis-data-store', 'data'),
    prevent_initial_call=True
)
def export_data_to_csv(n_clicks, all_fiis_data):
    if not n_clicks or not all_fiis_data:
        raise PreventUpdate
    
    df = pd.DataFrame(all_fiis_data)
    return dcc.send_data_frame(df.to_csv, "fiis_data.csv", index=False)

# Exportar portfólio para CSV
@app.callback(
    Output('download-portfolio-csv', 'data'),
    Input('export-portfolio-button', 'n_clicks'),
    State('portfolio-data-store', 'data'),
    prevent_initial_call=True
)
def export_portfolio_to_csv(n_clicks, portfolio_data):
    if not n_clicks or not portfolio_data:
        raise PreventUpdate
    
    df = pd.DataFrame(portfolio_data)
    return dcc.send_data_frame(df.to_csv, "meu_portfolio_fiis.csv", index=False)

# Carregar dados históricos para um FII específico
@app.callback(
    Output('historical-data-store', 'data'),
    Input('selected-fii-data-store', 'data'),
    prevent_initial_call=True
)
def load_historical_data(selected_fii):
    if not selected_fii:
        raise PreventUpdate
    
    ticker = selected_fii['Ticker']
    history_data = data_handler.get_advanced_indicators(ticker)
    
    if history_data is None:
        return []
    
    return history_data.to_dict('records')

# Abrir modal de detalhes ao clicar em um FII
@app.callback(
    [Output('fii-details-modal', 'is_open'),
     Output('selected-fii-data-store', 'data'),
     Output('fii-details-header', 'children')],
    [Input('top-table', 'selected_rows'),
     Input('all-table', 'selected_rows'),
     Input('close-fii-details-modal', 'n_clicks')],
    [State('top-table', 'data'),
     State('all-table', 'data'),
     State('fii-details-modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_fii_details_modal(top_selected, all_selected, close_clicks, top_data, all_data, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'close-fii-details-modal':
        return False, None, ""
    
    if trigger_id == 'top-table' and top_selected:
        selected_fii = top_data[top_selected[0]]
        return True, selected_fii, f"{selected_fii['Ticker']} - {selected_fii['Segmento']}"
    
    if trigger_id == 'all-table' and all_selected:
        selected_fii = all_data[all_selected[0]]
        return True, selected_fii, f"{selected_fii['Ticker']} - {selected_fii['Segmento']}"
    
    return is_open, None, ""

# Atualizar conteúdo do modal de detalhes
@app.callback(
    [Output('fii-overview-content', 'children'),
     Output('fii-dividend-content', 'children'),
     Output('fii-analysis-content', 'children'),
     Output('fii-advanced-content', 'children'),
     Output('fii-recommendation-content', 'children')],
    [Input('selected-fii-data-store', 'data'),
     Input('historical-data-store', 'data')],
    [State('all-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def update_fii_details_content(selected_fii, history_data, all_fiis_data):
    if not selected_fii:
        raise PreventUpdate
    
    all_fiis_df = pd.DataFrame(all_fiis_data)
    history_df = pd.DataFrame(history_data) if history_data else None
    
    overview_content = create_fii_overview_content(selected_fii)
    dividend_content = create_fii_dividend_content(selected_fii['Ticker'], history_df)
    analysis_content = create_fii_analysis_content(selected_fii, all_fiis_df)
    advanced_content = create_fii_advanced_content(selected_fii, all_fiis_df, history_df)
    recommendation_content = create_fii_recommendation_content(selected_fii)
    
    return overview_content, dividend_content, analysis_content, advanced_content, recommendation_content

# Atualizar resultados da simulação de investimento
@app.callback(
    Output('simulation-results', 'children'),
    [Input('simulation-value-input', 'value')],
    [State('selected-fii-data-store', 'data')],
    prevent_initial_call=True
)
def update_simulation_results(investment_value, selected_fii):
    if not investment_value or not selected_fii:
        raise PreventUpdate
    
    price = selected_fii['Preço']
    dy_annual = selected_fii['DY Anual']
    dy_monthly = selected_fii['DY Mensal']
    
    # Calcular resultados
    num_shares = investment_value / price
    monthly_income = (investment_value * dy_monthly) / 100
    annual_income = (investment_value * dy_annual) / 100
    
    results = html.Div([
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Métrica"),
                    html.Th("Valor")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("Quantidade de Cotas"),
                    html.Td(f"{num_shares:.2f}")
                ]),
                html.Tr([
                    html.Td("Rendimento Mensal"),
                    html.Td(f"R$ {monthly_income:.2f}")
                ]),
                html.Tr([
                    html.Td("Rendimento Anual"),
                    html.Td(f"R$ {annual_income:.2f}")
                ]),
                html.Tr([
                    html.Td("Yield Mensal"),
                    html.Td(f"{dy_monthly:.2f}%")
                ]),
                html.Tr([
                    html.Td("Yield Anual"),
                    html.Td(f"{dy_annual:.2f}%")
                ])
            ])
        ]),
        
        html.H5("Projeção de Rendimentos", className="mt-3"),
        html.P(f"Com um investimento de R$ {investment_value:.2f} em {selected_fii['Ticker']}, você receberá aproximadamente R$ {monthly_income:.2f} por mês em dividendos, totalizando R$ {annual_income:.2f} por ano.")
    ])
    
    return results

# Atualizar projeção anual
@app.callback(
    [Output('annual-projection-results', 'children'),
     Output('projection-chart', 'figure')],
    [Input('selected-fii-data-store', 'data')],
    prevent_initial_call=True
)
def update_annual_projection(selected_fii):
    if not selected_fii:
        raise PreventUpdate
    
    # Valores para projeção
    initial_investment = 10000  # R$ 10.000 como exemplo
    price = selected_fii['Preço']
    dy_annual = selected_fii['DY Anual'] / 100
    
    # Projeção para 10 anos
    years = list(range(1, 11))
    cumulative_dividends = []
    total_return = []
    
    current_dividends = 0
    for year in years:
        year_dividends = initial_investment * dy_annual
        current_dividends += year_dividends
        cumulative_dividends.append(current_dividends)
        total_return.append((current_dividends / initial_investment) * 100)
    
    # Criar tabela de resultados
    results_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Ano"),
                html.Th("Dividendos Acumulados"),
                html.Th("Retorno sobre Investimento")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(f"Ano {year}"),
                html.Td(f"R$ {cumulative_dividends[i-1]:.2f}"),
                html.Td(f"{total_return[i-1]:.2f}%")
            ]) for i, year in enumerate(years, 1)
        ])
    ])
    
    # Criar gráfico de projeção
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years,
        y=cumulative_dividends,
        name='Dividendos Acumulados (R$)',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=total_return,
        name='Retorno sobre Investimento (%)',
        mode='lines+markers',
        yaxis='y2',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=f'Projeção de Dividendos para 10 anos - {selected_fii["Ticker"]}',
        xaxis=dict(title='Ano'),
        yaxis=dict(
            title='Dividendos Acumulados (R$)',
            titlefont=dict(color='rgb(55, 83, 109)'),
            tickfont=dict(color='rgb(55, 83, 109)')
        ),
        yaxis2=dict(
            title='Retorno sobre Investimento (%)',
            titlefont=dict(color='rgb(26, 118, 255)'),
            tickfont=dict(color='rgb(26, 118, 255)'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    # Adicionar linha para o investimento inicial
    fig.add_hline(y=100, line_dash="dash", line_color="green", 
                 annotation_text="100% do Investimento Recuperado")
    
    return results_table, fig

# Atualizar próximas datas de dividendos
@app.callback(
    [Output('next-cut-date', 'children'),
     Output('next-ex-date', 'children'),
     Output('next-payment-date', 'children'),
     Output('next-dividend-value', 'children')],
    [Input('selected-fii-data-store', 'data')],
    prevent_initial_call=True
)
def update_dividend_dates(selected_fii):
    if not selected_fii:
        raise PreventUpdate
    
    # Em um cenário real, você buscaria essas datas de uma API ou banco de dados
    # Aqui, usaremos datas fictícias para demonstração
    from datetime import datetime, timedelta
    
    today = datetime.now()
    
    # Simular próximas datas
    next_cut = today + timedelta(days=10)
    next_ex = next_cut + timedelta(days=1)
    next_payment = next_cut + timedelta(days=15)
    
    # Estimar próximo dividendo com base no último
    last_dividend = selected_fii.get('Último Dividendo', 0)
    estimated_dividend = f"R$ {last_dividend:.4f} (estimado)"
    
    return [
        next_cut.strftime("%d/%m/%Y"),
        next_ex.strftime("%d/%m/%Y"),
        next_payment.strftime("%d/%m/%Y"),
        estimated_dividend
    ]

# Atualizar próximos eventos de dividendos
@app.callback(
    Output('upcoming-events-container', 'children'),
    [Input('all-fiis-data-store', 'data')],
    prevent_initial_call=True
)
def update_upcoming_events(all_fiis_data):
    if not all_fiis_data:
        raise PreventUpdate
    
    # Em um cenário real, você buscaria esses eventos de uma API ou banco de dados
    # Aqui, usaremos dados fictícios para demonstração
    from datetime import datetime, timedelta
    
    today = datetime.now()
    
    # Criar eventos fictícios para os próximos 30 dias
    events = []
    for i in range(15):
        event_date = today + timedelta(days=i)
        if i % 3 == 0:  # Apenas para criar alguns eventos de exemplo
            ticker = f"FII{i+1:02d}11"
            events.append({
                'Data': event_date.strftime("%d/%m/%Y"),
                'Ticker': ticker,
                'Tipo': 'Data de Corte' if i % 2 == 0 else 'Data de Pagamento',
                'Valor': f"R$ {0.5 + (i % 10) / 10:.2f}" if i % 2 != 0 else "N/A"
            })
    
    # Ordenar eventos por data
    events = sorted(events, key=lambda x: datetime.strptime(x['Data'], "%d/%m/%Y"))
    
    # Criar tabela de eventos
    events_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Data"),
                html.Th("Ticker"),
                html.Th("Tipo de Evento"),
                html.Th("Valor")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(event['Data']),
                html.Td(event['Ticker']),
                html.Td(event['Tipo']),
                html.Td(event['Valor'])
            ]) for event in events
        ])
    ])
    
    return events_table

# Executar o app
if __name__ == '__main__':
    app.run_server(debug=True)


