import dash_bootstrap_components as dbc
from dash import dash_table, html
import pandas as pd

def create_main_table(df, id_prefix='main'):
    """Cria a tabela principal de FIIs"""
    if df is None or df.empty:
        return html.Div("Nenhum dado disponível")
    
    # Formatar colunas numéricas
    df_display = df.copy()
    df_display['Preço'] = df_display['Preço'].map('R$ {:.2f}'.format)
    df_display['DY Anual'] = df_display['DY Anual'].map('{:.2f}%'.format)
    df_display['DY Mensal'] = df_display['DY Mensal'].map('{:.2f}%'.format)
    df_display['P/VP'] = df_display['P/VP'].map('{:.2f}'.format)
    df_display['Preço Justo'] = df_display['Preço Justo'].map('R$ {:.2f}'.format)
    
    # Adicionar colunas de indicadores avançados se existirem
    if 'Cap Rate' in df_display.columns:
        df_display['Cap Rate'] = df_display['Cap Rate'].map('{:.2f}%'.format)
    if 'Vacância' in df_display.columns:
        df_display['Vacância'] = df_display['Vacância'].map('{:.2f}%'.format)
    if 'Sharpe Ratio' in df_display.columns:
        df_display['Sharpe Ratio'] = df_display['Sharpe Ratio'].map('{:.2f}'.format)
    if 'TIR Estimada' in df_display.columns:
        df_display['TIR Estimada'] = df_display['TIR Estimada'].map('{:.2f}%'.format)
    
    # Definir colunas a exibir
    columns = [
        {"name": "Ticker", "id": "Ticker", "type": "text"},
        {"name": "Segmento", "id": "Segmento", "type": "text"},
        {"name": "Preço", "id": "Preço", "type": "text"},
        {"name": "DY Anual", "id": "DY Anual", "type": "text"},
        {"name": "P/VP", "id": "P/VP", "type": "text"},
        {"name": "Preço Justo", "id": "Preço Justo", "type": "text"},
    ]
    
    # Adicionar colunas avançadas se disponíveis
    if 'Vacância' in df_display.columns:
        columns.append({"name": "Vacância", "id": "Vacância", "type": "text"})
    if 'Cap Rate' in df_display.columns:
        columns.append({"name": "Cap Rate", "id": "Cap Rate", "type": "text"})
    if 'Sharpe Ratio' in df_display.columns:
        columns.append({"name": "Sharpe", "id": "Sharpe Ratio", "type": "text"})
    
    columns.append({"name": "Oportunidade", "id": "Oportunidade", "type": "text"})
    
    table = dash_table.DataTable(
        id=f'{id_prefix}-table',
        columns=columns,
        data=df_display.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'minWidth': '100px',
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'fontWeight': 'bold',
            'textAlign': 'center',
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'Oportunidade', 'filter_query': '{Oportunidade} eq "Sim"'},
                'backgroundColor': '#d4edda',
                'color': '#155724'
            },
                        {
                'if': {'column_id': 'P/VP', 'filter_query': '{P/VP} contains "0."'},
                'backgroundColor': '#d4edda',
                'color': '#155724'
            },
            {
                'if': {'column_id': 'DY Anual', 'filter_query': '{DY Anual} contains "1"'},
                'backgroundColor': '#d4edda',
                'color': '#155724'
            },
            {
                'if': {'column_id': 'Sharpe Ratio', 'filter_query': '{Sharpe Ratio} contains "1."'},
                'backgroundColor': '#d4edda',
                'color': '#155724'
            },
        ],
        sort_action="native",
        filter_action="native",
        page_size=15,
        row_selectable="single",
        selected_rows=[],
    )
    
    return table

def create_portfolio_table(portfolio_data):
    """Cria a tabela do portfólio do usuário"""
    if portfolio_data is None or len(portfolio_data) == 0:
        return html.Div("Nenhum FII adicionado ao portfólio")
    
    df = pd.DataFrame(portfolio_data)
    
    # Calcular valores adicionais
    df['Valor Investido'] = df['Quantidade'] * df['Preço Médio']
    df['Valor Atual'] = df['Quantidade'] * df['Preço Atual']
    df['Rentabilidade'] = ((df['Valor Atual'] / df['Valor Investido']) - 1) * 100
    df['Dividendos Mensais'] = df['Valor Atual'] * (df['DY Mensal'] / 100)
    df['Yield on Cost'] = (df['Dividendos Mensais'] * 12 / df['Valor Investido']) * 100
    
    # Formatar para exibição
    df_display = df.copy()
    df_display['Preço Médio'] = df_display['Preço Médio'].map('R$ {:.2f}'.format)
    df_display['Preço Atual'] = df_display['Preço Atual'].map('R$ {:.2f}'.format)
    df_display['Valor Investido'] = df_display['Valor Investido'].map('R$ {:.2f}'.format)
    df_display['Valor Atual'] = df_display['Valor Atual'].map('R$ {:.2f}'.format)
    df_display['Rentabilidade'] = df_display['Rentabilidade'].map('{:+.2f}%'.format)
    df_display['Dividendos Mensais'] = df_display['Dividendos Mensais'].map('R$ {:.2f}'.format)
    df_display['Yield on Cost'] = df_display['Yield on Cost'].map('{:.2f}%'.format)
    
    table = dash_table.DataTable(
        id='portfolio-table',
        columns=[
            {"name": "Ticker", "id": "Ticker"},
            {"name": "Quantidade", "id": "Quantidade"},
            {"name": "Preço Médio", "id": "Preço Médio"},
            {"name": "Preço Atual", "id": "Preço Atual"},
            {"name": "Valor Investido", "id": "Valor Investido"},
            {"name": "Valor Atual", "id": "Valor Atual"},
            {"name": "Rentabilidade", "id": "Rentabilidade"},
            {"name": "Dividendos Mensais", "id": "Dividendos Mensais"},
            {"name": "Yield on Cost", "id": "Yield on Cost"},
        ],
        data=df_display.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'fontWeight': 'bold',
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'Rentabilidade', 'filter_query': '{Rentabilidade} contains "+"'},
                'color': 'green'
            },
            {
                'if': {'column_id': 'Rentabilidade', 'filter_query': '{Rentabilidade} contains "-"'},
                'color': 'red'
            },
        ],
        row_deletable=True,
    )
    
    return table

def create_dividend_calendar_table(calendar_data):
    """Cria a tabela de calendário de dividendos"""
    if calendar_data is None or calendar_data.empty:
        return html.Div("Nenhum evento de dividendo disponível")
    
    table = dash_table.DataTable(
        id='calendar-table',
        columns=[
            {"name": "Ticker", "id": "Ticker"},
            {"name": "Data de Corte", "id": "Data de Corte"},
            {"name": "Data de Pagamento", "id": "Data de Pagamento"},
            {"name": "Valor Previsto", "id": "Valor Previsto", "type": "numeric", "format": {"specifier": "$.2f"}},
        ],
        data=calendar_data.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'fontWeight': 'bold',
        },
        sort_action="native",
        page_size=10,
    )
    
    return table

def create_advanced_indicators_table(indicators_data):
    """Cria uma tabela com indicadores avançados para um FII específico"""
    if indicators_data is None or indicators_data.empty:
        return html.Div("Dados de indicadores avançados não disponíveis")
    
    # Selecionar apenas os dados mais recentes
    latest_data = indicators_data.iloc[-1].to_dict()
    
    # Criar tabela de indicadores
    table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Indicador"),
                html.Th("Valor"),
                html.Th("Avaliação")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td("Dividend Yield Anual"),
                html.Td(f"{latest_data.get('DY Anual', 0):.2f}%"),
                html.Td(get_indicator_evaluation("DY Anual", latest_data.get('DY Anual', 0)))
            ]),
            html.Tr([
                html.Td("P/VP"),
                html.Td(f"{latest_data.get('P/VP', 0):.2f}"),
                html.Td(get_indicator_evaluation("P/VP", latest_data.get('P/VP', 0)))
            ]),
            html.Tr([
                html.Td("Cap Rate"),
                html.Td(f"{latest_data.get('Cap Rate', 0):.2f}%"),
                html.Td(get_indicator_evaluation("Cap Rate", latest_data.get('Cap Rate', 0)))
            ]),
            html.Tr([
                html.Td("Vacância"),
                html.Td(f"{latest_data.get('Vacância', 0):.2f}%"),
                html.Td(get_indicator_evaluation("Vacância", latest_data.get('Vacância', 0)))
            ]),
            html.Tr([
                html.Td("Sharpe Ratio"),
                html.Td(f"{latest_data.get('Sharpe Ratio', 0):.2f}"),
                html.Td(get_indicator_evaluation("Sharpe Ratio", latest_data.get('Sharpe Ratio', 0)))
            ]),
            html.Tr([
                html.Td("TIR Estimada"),
                html.Td(f"{latest_data.get('TIR Estimada', 0):.2f}%"),
                html.Td(get_indicator_evaluation("TIR Estimada", latest_data.get('TIR Estimada', 0)))
            ]),
            html.Tr([
                html.Td("Spread P/VP"),
                html.Td(f"{latest_data.get('Spread P/VP', 0):.2f}%"),
                html.Td(get_indicator_evaluation("Spread P/VP", latest_data.get('Spread P/VP', 0)))
            ]),
        ])
    ], bordered=True, hover=True)
    
    return table

def get_indicator_evaluation(indicator, value):
    """Retorna uma avaliação qualitativa para um indicador"""
    if indicator == "DY Anual":
        if value >= 10:
            return html.Span("Excelente", style={"color": "green"})
        elif value >= 7:
            return html.Span("Bom", style={"color": "lightgreen"})
        elif value >= 5:
            return html.Span("Regular", style={"color": "orange"})
        else:
            return html.Span("Baixo", style={"color": "red"})
    
    elif indicator == "P/VP":
        if value < 0.8:
            return html.Span("Barato", style={"color": "green"})
        elif value < 1:
            return html.Span("Justo", style={"color": "lightgreen"})
        elif value < 1.2:
            return html.Span("Caro", style={"color": "orange"})
        else:
            return html.Span("Muito caro", style={"color": "red"})
    
    elif indicator == "Cap Rate":
        if value >= 10:
            return html.Span("Excelente", style={"color": "green"})
        elif value >= 8:
            return html.Span("Bom", style={"color": "lightgreen"})
        elif value >= 6:
            return html.Span("Regular", style={"color": "orange"})
        else:
            return html.Span("Baixo", style={"color": "red"})
    
    elif indicator == "Vacância":
        if value < 5:
            return html.Span("Excelente", style={"color": "green"})
        elif value < 10:
            return html.Span("Boa", style={"color": "lightgreen"})
        elif value < 15:
            return html.Span("Regular", style={"color": "orange"})
        else:
            return html.Span("Alta", style={"color": "red"})
    
    elif indicator == "Sharpe Ratio":
        if value >= 1:
            return html.Span("Excelente", style={"color": "green"})
        elif value >= 0.5:
            return html.Span("Bom", style={"color": "lightgreen"})
        elif value >= 0:
            return html.Span("Regular", style={"color": "orange"})
        else:
            return html.Span("Ruim", style={"color": "red"})
    
    elif indicator == "TIR Estimada":
        if value >= 15:
            return html.Span("Excelente", style={"color": "green"})
        elif value >= 12:
            return html.Span("Boa", style={"color": "lightgreen"})
        elif value >= 9:
            return html.Span("Regular", style={"color": "orange"})
        else:
            return html.Span("Baixa", style={"color": "red"})
    
    elif indicator == "Spread P/VP":
        if value <= -15:
            return html.Span("Muito descontado", style={"color": "green"})
        elif value <= -5:
            return html.Span("Descontado", style={"color": "lightgreen"})
        elif value <= 5:
            return html.Span("Justo", style={"color": "orange"})
        else:
            return html.Span("Prêmio", style={"color": "red"})
    
    return "N/A"

