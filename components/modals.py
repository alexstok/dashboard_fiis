from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def create_fii_details_modal():
    """Cria o modal de detalhes do FII"""
    modal = dbc.Modal(
        [
            dbc.ModalHeader(html.H3(id="fii-details-header")),
            dbc.ModalBody([
                dbc.Tabs([
                    dbc.Tab([
                        html.Div(id="fii-overview-content", className="mt-3"),
                    ], label="Visão Geral"),
                    
                    dbc.Tab([
                        html.Div(id="fii-dividend-content", className="mt-3"),
                    ], label="Dividendos"),
                    
                    dbc.Tab([
                        html.Div(id="fii-analysis-content", className="mt-3"),
                    ], label="Análise"),
                    
                    dbc.Tab([
                        html.Div(id="fii-advanced-content", className="mt-3"),
                    ], label="Indicadores Avançados"),
                    
                    dbc.Tab([
                        html.Div(id="fii-recommendation-content", className="mt-3"),
                    ], label="Recomendação"),
                ]),
            ]),
            dbc.ModalFooter(
                dbc.Button("Fechar", id="close-fii-details-modal", className="ml-auto")
            ),
        ],
        id="fii-details-modal",
        size="xl",
    )
    
    return modal

def create_fii_overview_content(fii_data):
    """Cria o conteúdo da aba de visão geral do FII"""
    if fii_data is None:
        return html.Div("Dados não disponíveis")
    
    overview = dbc.Row([
        dbc.Col([
            html.H4("Informações Básicas"),
            dbc.Table([
                html.Tbody([
                    html.Tr([html.Td("Ticker"), html.Td(fii_data.get('Ticker', 'N/A'))]),
                    html.Tr([html.Td("Segmento"), html.Td(fii_data.get('Segmento', 'N/A'))]),
                    html.Tr([html.Td("Preço Atual"), html.Td(f"R$ {fii_data.get('Preço', 0):.2f}")]),
                    html.Tr([html.Td("P/VP"), html.Td(f"{fii_data.get('P/VP', 0):.2f}")]),
                    html.Tr([html.Td("Preço Justo"), html.Td(f"R$ {fii_data.get('Preço Justo', 0):.2f}")]),
                    html.Tr([html.Td("Vacância"), html.Td(f"{fii_data.get('Vacância', 0):.2f}%")]),
                ])
            ]),
        ], width=6),
        
        dbc.Col([
            html.H4("Indicadores de Rendimento"),
            dbc.Table([
                html.Tbody([
                    html.Tr([html.Td("DY Anual"), html.Td(f"{fii_data.get('DY Anual', 0):.2f}%")]),
                    html.Tr([html.Td("DY Mensal"), html.Td(f"{fii_data.get('DY Mensal', 0):.2f}%")]),
                    html.Tr([html.Td("Último Dividendo"), html.Td(f"R$ {fii_data.get('Último Dividendo', 0):.4f}")]),
                    html.Tr([html.Td("Cap Rate"), html.Td(f"{fii_data.get('Cap Rate', 0):.2f}%")]),
                    html.Tr([html.Td("TIR Estimada"), html.Td(f"{fii_data.get('TIR Estimada', 0):.2f}%")]),
                    html.Tr([html.Td("Sharpe Ratio"), html.Td(f"{fii_data.get('Sharpe Ratio', 0):.2f}")]),
                ])
            ]),
        ], width=6),
        
        dbc.Col([
            html.H4("Adicionar ao Portfólio"),
            dbc.InputGroup([
                dbc.InputGroupText("Quantidade"),
                dbc.Input(id="modal-quantity-input", type="number", min=1, step=1),
            ], className="mb-2"),
            dbc.InputGroup([
                dbc.InputGroupText("Preço Médio"),
                dbc.Input(id="modal-price-input", type="number", min=0, step=0.01, 
                          value=fii_data.get('Preço', 0)),
            ], className="mb-2"),
            dbc.Button("Adicionar ao Portfólio", id="modal-add-to-portfolio", color="success", className="mt-2"),
        ], width=12, className="mt-4"),
    ])
    
    return overview

def create_fii_dividend_content(ticker, history_data=None):
    """Cria o conteúdo da aba de dividendos do FII"""
    from components.charts import create_dividend_history_chart
    
    content = html.Div([
        html.H4("Histórico de Dividendos"),
        create_dividend_history_chart(ticker, history_data),
        
        html.H4("Projeção de Rendimentos", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Simulação de Investimento"),
                    dbc.CardBody([
                        dbc.InputGroup([
                            dbc.InputGroupText("Valor a Investir (R$)"),
                            dbc.Input(id="simulation-value-input", type="number", min=1000, step=100, value=10000),
                        ], className="mb-2"),
                        html.Div(id="simulation-results", className="mt-3"),
                    ]),
                ]),
            ], width=12),
        ]),
        
        html.H4("Projeção Anual", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Rendimentos Projetados"),
                    dbc.CardBody([
                        html.Div(id="annual-projection-results"),
                        dcc.Graph(id="projection-chart"),
                    ]),
                ]),
            ], width=12),
        ]),
        
        html.H4("Datas Importantes", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Próximas Datas"),
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Evento"),
                                    html.Th("Data"),
                                    html.Th("Valor Estimado")
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td("Data de Corte"),
                                    html.Td(id="next-cut-date"),
                                    html.Td(id="next-dividend-value")
                                ]),
                                html.Tr([
                                    html.Td("Data Ex"),
                                    html.Td(id="next-ex-date"),
                                    html.Td("-")
                                ]),
                                html.Tr([
                                    html.Td("Data de Pagamento"),
                                    html.Td(id="next-payment-date"),
                                    html.Td("-")
                                ])
                            ])
                        ]),
                        html.P("As datas acima são estimativas baseadas no histórico de pagamentos.", className="text-muted mt-3"),
                    ]),
                ]),
            ], width=12),
        ]),
    ])
    
    return content

def create_fii_analysis_content(fii_data, all_fiis_df):
    """Cria o conteúdo da aba de análise do FII"""
    if fii_data is None or all_fiis_df is None or all_fiis_df.empty:
        return html.Div("Dados não disponíveis para análise")
    
    from components.charts import create_advanced_analysis_chart
    
    # Criar gráfico de análise avançada
    analysis_chart = create_advanced_analysis_chart(all_fiis_df, fii_data['Ticker'])
    
    # Encontrar FIIs do mesmo segmento para comparação
    segment = fii_data.get('Segmento', '')
    segment_fiis = all_fiis_df[all_fiis_df['Segmento'] == segment]
    
    # Calcular médias do segmento
    segment_avg_dy = segment_fiis['DY Anual'].mean()
    segment_avg_pvp = segment_fiis['P/VP'].mean()
    segment_avg_cap_rate = segment_fiis['Cap Rate'].mean() if 'Cap Rate' in segment_fiis.columns else 0
    segment_avg_vacancia = segment_fiis['Vacância'].mean() if 'Vacância' in segment_fiis.columns else 0
    
    # Criar gráfico de comparação
    comparison_data = {
        'Métrica': ['DY Anual (%)', 'P/VP', 'Cap Rate (%)', 'Vacância (%)'],
        f'{fii_data["Ticker"]}': [
            fii_data['DY Anual'], 
            fii_data['P/VP'], 
            fii_data.get('Cap Rate', 0), 
            fii_data.get('Vacância', 0)
        ],
        f'Média {segment}': [
            segment_avg_dy, 
            segment_avg_pvp, 
            segment_avg_cap_rate, 
            segment_avg_vacancia
        ]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        df_comparison, 
        x='Métrica', 
        y=[f'{fii_data["Ticker"]}', f'Média {segment}'],
        barmode='group',
        title=f'Comparação com a Média do Segmento {segment}'
    )
    
    content = html.Div([
        html.H4("Análise Multidimensional"),
        analysis_chart,
        
        html.H4("Comparação com o Segmento", className="mt-4"),
        dcc.Graph(figure=fig),
        
        html.H4("Posição no Ranking", className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H5("Dividend Yield"),
                html.P(f"Posição: {all_fiis_df['DY Anual'].rank(ascending=False)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0]:.0f}º de {len(all_fiis_df)} FIIs"),
                html.P(f"Percentil: {100 - (all_fiis_df['DY Anual'].rank(ascending=False, pct=True)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0] * 100):.1f}%"),
            ], width=6),
            
            dbc.Col([
                html.H5("P/VP"),
                html.P(f"Posição: {all_fiis_df['P/VP'].rank()[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0]:.0f}º de {len(all_fiis_df)} FIIs"),
                html.P(f"Percentil: {(all_fiis_df['P/VP'].rank(pct=True)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0] * 100):.1f}%"),
            ], width=6),
        ]),
        
                dbc.Row([
            dbc.Col([
                html.H5("Cap Rate"),
                html.P(f"Posição: {all_fiis_df['Cap Rate'].rank(ascending=False)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0]:.0f}º de {len(all_fiis_df)} FIIs"),
                html.P(f"Percentil: {100 - (all_fiis_df['Cap Rate'].rank(ascending=False, pct=True)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0] * 100):.1f}%"),
            ], width=6),
            
            dbc.Col([
                html.H5("Vacância"),
                html.P(f"Posição: {all_fiis_df['Vacância'].rank()[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0]:.0f}º de {len(all_fiis_df)} FIIs"),
                html.P(f"Percentil: {(all_fiis_df['Vacância'].rank(pct=True)[all_fiis_df['Ticker'] == fii_data['Ticker']].values[0] * 100):.1f}%"),
            ], width=6),
        ]),
        
        html.H4("Análise de Risco", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Volatilidade"),
                    dbc.CardBody([
                        html.P(f"Volatilidade (12m): {fii_data.get('Volatilidade', 15.3):.1f}%"),
                        html.P(f"Beta: {fii_data.get('Beta', 0.85):.2f}"),
                        html.P(f"Sharpe Ratio: {fii_data.get('Sharpe Ratio', 0.92):.2f}"),
                    ]),
                ]),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Liquidez"),
                    dbc.CardBody([
                        html.P(f"Volume Médio Diário: R$ {fii_data.get('Liquidez', 2500000)/1000000:.2f}M"),
                        html.P(f"Negócios Diários: {int(fii_data.get('Liquidez', 2500000)/3000)}"),
                        html.P(f"Liquidez: {'Alta' if fii_data.get('Liquidez', 0) > 1000000 else 'Média' if fii_data.get('Liquidez', 0) > 500000 else 'Baixa'}"),
                    ]),
                ]),
            ], width=6),
        ]),
    ])
    
    return content

def create_fii_advanced_content(fii_data, all_fiis_df, history_data=None):
    """Cria o conteúdo da aba de indicadores avançados do FII"""
    if fii_data is None:
        return html.Div("Dados não disponíveis para análise avançada")
    
    from components.tables import create_advanced_indicators_table
    from components.charts import create_historical_performance_chart
    
    # Criar tabela de indicadores avançados
    indicators_table = create_advanced_indicators_table(history_data)
    
    # Criar gráfico de desempenho histórico
    performance_chart = create_historical_performance_chart(fii_data['Ticker'], history_data)
    
    content = html.Div([
        html.H4("Indicadores Avançados"),
        indicators_table,
        
        html.H4("Desempenho Histórico", className="mt-4"),
        performance_chart,
        
        html.H4("Análise de Valor", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Modelo de Gordon"),
                    dbc.CardBody([
                        html.P("O Modelo de Gordon calcula o valor justo com base no último dividendo, taxa de crescimento esperada e taxa de desconto."),
                        html.Div([
                            html.P(f"Último Dividendo Mensal: R$ {fii_data.get('Último Dividendo', 0):.4f}"),
                            html.P(f"Dividendo Anual: R$ {fii_data.get('Último Dividendo', 0) * 12:.2f}"),
                            html.P(f"Taxa de Crescimento Estimada: {fii_data.get('Taxa de Crescimento', 3):.1f}%"),
                            html.P(f"Taxa de Desconto: {fii_data.get('Taxa de Desconto', 10):.1f}%"),
                            html.Hr(),
                            html.P(f"Preço Justo (Gordon): R$ {(fii_data.get('Último Dividendo', 0) * 12) / ((fii_data.get('Taxa de Desconto', 10) - fii_data.get('Taxa de Crescimento', 3)) / 100):.2f}"),
                        ]),
                    ]),
                ]),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Yield on Cost"),
                    dbc.CardBody([
                        html.P("Yield on Cost (YoC) mede o rendimento atual com base no preço original de aquisição."),
                        html.Div([
                            html.P(f"Preço Atual: R$ {fii_data.get('Preço', 0):.2f}"),
                            html.P(f"DY Atual: {fii_data.get('DY Anual', 0):.2f}%"),
                            html.Hr(),
                            html.P("Simulação de YoC para diferentes preços de aquisição:"),
                            dbc.Table([
                                html.Thead([
                                    html.Tr([
                                        html.Th("Preço de Aquisição"),
                                        html.Th("Yield on Cost")
                                    ])
                                ]),
                                html.Tbody([
                                    html.Tr([
                                        html.Td(f"R$ {fii_data.get('Preço', 100) * 0.8:.2f}"),
                                        html.Td(f"{fii_data.get('DY Anual', 7) * (fii_data.get('Preço', 100) / (fii_data.get('Preço', 100) * 0.8)):.2f}%")
                                    ]),
                                    html.Tr([
                                        html.Td(f"R$ {fii_data.get('Preço', 100) * 0.9:.2f}"),
                                        html.Td(f"{fii_data.get('DY Anual', 7) * (fii_data.get('Preço', 100) / (fii_data.get('Preço', 100) * 0.9)):.2f}%")
                                    ]),
                                    html.Tr([
                                        html.Td(f"R$ {fii_data.get('Preço', 100):.2f}"),
                                        html.Td(f"{fii_data.get('DY Anual', 7):.2f}%")
                                    ]),
                                    html.Tr([
                                        html.Td(f"R$ {fii_data.get('Preço', 100) * 1.1:.2f}"),
                                        html.Td(f"{fii_data.get('DY Anual', 7) * (fii_data.get('Preço', 100) / (fii_data.get('Preço', 100) * 1.1)):.2f}%")
                                    ]),
                                ])
                            ]),
                        ]),
                    ]),
                ]),
            ], width=6),
        ]),
        
        html.H4("Indicadores de Qualidade", className="mt-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Qualidade dos Ativos"),
                    dbc.CardBody([
                        html.P(f"Cap Rate: {fii_data.get('Cap Rate', 0):.2f}%"),
                        html.P(f"Vacância: {fii_data.get('Vacância', 0):.2f}%"),
                        html.P(f"Taxa de Ocupação: {100 - fii_data.get('Vacância', 0):.2f}%"),
                        html.P(f"Inadimplência: {fii_data.get('Inadimplência', 3):.2f}%"),
                    ]),
                ]),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Gestão"),
                    dbc.CardBody([
                        html.P(f"Taxa de Administração: {fii_data.get('Taxa de Administração', 1):.2f}%"),
                        html.P(f"Taxa de Performance: {fii_data.get('Taxa de Performance', 20):.0f}% do que exceder {fii_data.get('Benchmark', 'IFIX')}"),
                        html.P(f"Gestora: {fii_data.get('Gestora', 'N/A')}"),
                        html.P(f"Patrimônio Líquido: R$ {fii_data.get('Patrimônio Líquido', 500000000)/1000000:.2f}M"),
                    ]),
                ]),
            ], width=6),
        ]),
    ])
    
    return content

def create_fii_recommendation_content(fii_data):
    """Cria o conteúdo da aba de recomendação do FII"""
    if fii_data is None:
        return html.Div("Dados não disponíveis para recomendação")
    
    # Lógica avançada de recomendação
    dy_score = 0
    if fii_data['DY Anual'] > 10:
        dy_score = 3
    elif fii_data['DY Anual'] > 8:
        dy_score = 2
    elif fii_data['DY Anual'] > 6:
        dy_score = 1
    
    pvp_score = 0
    if fii_data['P/VP'] < 0.8:
        pvp_score = 3
    elif fii_data['P/VP'] < 1:
        pvp_score = 2
    elif fii_data['P/VP'] < 1.2:
        pvp_score = 1
    
    price_score = 0
    if fii_data['Preço'] < fii_data['Preço Justo'] * 0.9:
        price_score = 3
    elif fii_data['Preço'] < fii_data['Preço Justo']:
        price_score = 2
    elif fii_data['Preço'] < fii_data['Preço Justo'] * 1.1:
        price_score = 1
    
    # Pontuações adicionais para indicadores avançados
    cap_rate_score = 0
    if 'Cap Rate' in fii_data:
        if fii_data['Cap Rate'] > 10:
            cap_rate_score = 3
        elif fii_data['Cap Rate'] > 8:
            cap_rate_score = 2
        elif fii_data['Cap Rate'] > 6:
            cap_rate_score = 1
    
    vacancia_score = 0
    if 'Vacância' in fii_data:
        if fii_data['Vacância'] < 5:
            vacancia_score = 3
        elif fii_data['Vacância'] < 10:
            vacancia_score = 2
        elif fii_data['Vacância'] < 15:
            vacancia_score = 1
    
    sharpe_score = 0
    if 'Sharpe Ratio' in fii_data:
        if fii_data['Sharpe Ratio'] > 1:
            sharpe_score = 3
        elif fii_data['Sharpe Ratio'] > 0.5:
            sharpe_score = 2
        elif fii_data['Sharpe Ratio'] > 0:
            sharpe_score = 1
    
    # Calcular pontuação total
    total_score = dy_score + pvp_score + price_score + cap_rate_score + vacancia_score + sharpe_score
    max_score = 18  # Pontuação máxima possível
    
    # Determinar recomendação com base na pontuação
    if total_score >= 14:
        recommendation = "Compra Forte"
        recommendation_color = "success"
    elif total_score >= 10:
        recommendation = "Compra"
        recommendation_color = "success"
    elif total_score >= 7:
        recommendation = "Neutro"
        recommendation_color = "warning"
    elif total_score >= 4:
        recommendation = "Venda"
        recommendation_color = "danger"
    else:
        recommendation = "Venda Forte"
        recommendation_color = "danger"
    
    content = html.Div([
        html.H4("Recomendação"),
        dbc.Alert(recommendation, color=recommendation_color, className="text-center"),
        
        html.H4("Pontuação Detalhada", className="mt-4"),
        dbc.Progress(
            [
                dbc.Progress(value=total_score/max_score*100, color=recommendation_color, bar=True),
            ],
            className="mb-3",
        ),
        html.P(f"Pontuação: {total_score} de {max_score} pontos"),
        
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Indicador"),
                    html.Th("Valor"),
                    html.Th("Pontuação")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("Dividend Yield"),
                    html.Td(f"{fii_data['DY Anual']:.2f}%"),
                    html.Td(f"{dy_score} de 3")
                ]),
                html.Tr([
                    html.Td("P/VP"),
                    html.Td(f"{fii_data['P/VP']:.2f}"),
                    html.Td(f"{pvp_score} de 3")
                ]),
                html.Tr([
                    html.Td("Preço vs Preço Justo"),
                    html.Td(f"R$ {fii_data['Preço']:.2f} vs R$ {fii_data['Preço Justo']:.2f}"),
                    html.Td(f"{price_score} de 3")
                ]),
                html.Tr([
                    html.Td("Cap Rate"),
                    html.Td(f"{fii_data.get('Cap Rate', 0):.2f}%"),
                    html.Td(f"{cap_rate_score} de 3")
                ]),
                html.Tr([
                    html.Td("Vacância"),
                    html.Td(f"{fii_data.get('Vacância', 0):.2f}%"),
                    html.Td(f"{vacancia_score} de 3")
                ]),
                html.Tr([
                    html.Td("Sharpe Ratio"),
                    html.Td(f"{fii_data.get('Sharpe Ratio', 0):.2f}"),
                    html.Td(f"{sharpe_score} de 3")
                ]),
            ])
        ]),
        
        html.H4("Pontos Fortes", className="mt-4"),
        dbc.ListGroup([
            dbc.ListGroupItem("Dividend Yield acima da média do mercado", color="success") if dy_score >= 2 else None,
            dbc.ListGroupItem("P/VP abaixo de 1, indicando desconto", color="success") if pvp_score >= 2 else None,
            dbc.ListGroupItem("Preço atual abaixo do preço justo", color="success") if price_score >= 2 else None,
            dbc.ListGroupItem("Cap Rate elevado, indicando boa rentabilidade dos ativos", color="success") if cap_rate_score >= 2 else None,
            dbc.ListGroupItem("Baixa vacância, indicando boa ocupação dos imóveis", color="success") if vacancia_score >= 2 else None,
            dbc.ListGroupItem("Bom Sharpe Ratio, indicando boa relação risco-retorno", color="success") if sharpe_score >= 2 else None,
        ], flush=True),
        
        html.H4("Pontos de Atenção", className="mt-4"),
        dbc.ListGroup([
            dbc.ListGroupItem("Dividend Yield abaixo da média do mercado", color="danger") if dy_score <= 1 else None,
            dbc.ListGroupItem("P/VP acima de 1, indicando possível sobrevalorização", color="danger") if pvp_score <= 1 else None,
            dbc.ListGroupItem("Preço atual acima do preço justo", color="danger") if price_score <= 1 else None,
            dbc.ListGroupItem("Cap Rate baixo, indicando rentabilidade insuficiente dos ativos", color="danger") if cap_rate_score <= 1 else None,
            dbc.ListGroupItem("Alta vacância, indicando problemas de ocupação", color="danger") if vacancia_score <= 1 else None,
            dbc.ListGroupItem("Sharpe Ratio baixo, indicando relação risco-retorno desfavorável", color="danger") if sharpe_score <= 1 else None,
        ], flush=True),
        
        html.H4("Projeção", className="mt-4"),
        dbc.Card([
            dbc.CardHeader("Projeção para 12 meses"),
            dbc.CardBody([
                html.P(f"Preço Alvo: R$ {fii_data['Preço Justo'] * 1.1:.2f}"),
                html.P(f"Potencial de Valorização: {((fii_data['Preço Justo'] * 1.1 / fii_data['Preço']) - 1) * 100:.2f}%"),
                html.P(f"Retorno Total Esperado (Valorização + Dividendos): {((fii_data['Preço Justo'] * 1.1 / fii_data['Preço']) - 1) * 100 + fii_data['DY Anual']:.2f}%"),
                html.P(f"TIR Estimada: {fii_data.get('TIR Estimada', ((fii_data['Preço Justo'] * 1.1 / fii_data['Preço']) - 1) * 100 + fii_data['DY Anual']):.2f}%"),
            ]),
        ]),
    ])
    
    return content


