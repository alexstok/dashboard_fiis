import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd
import numpy as np

def create_sector_distribution_chart(df):
    """Cria gráfico de distribuição por setor com dividend yield médio"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    sector_data = df.groupby('Segmento').agg({
        'Ticker': 'count',
        'DY Anual': 'mean'
    }).reset_index()
    
    sector_data.rename(columns={'Ticker': 'Quantidade'}, inplace=True)
    
    fig = px.bar(
        sector_data,
        x='Segmento',
        y='Quantidade',
        color='DY Anual',
        color_continuous_scale='Viridis',
        labels={
            'Segmento': 'Segmento',
            'Quantidade': 'Quantidade de FIIs',
            'DY Anual': 'DY Anual Médio (%)'
        },
        title='Distribuição por Segmento e DY Médio'
    )
    
    return dcc.Graph(figure=fig, id='sector-distribution-chart')

def create_top_dividend_chart(df, limit=15):
    """Cria gráfico dos FIIs com maiores dividendos"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    top_dy = df.sort_values('DY Anual', ascending=False).head(limit)
    
    fig = px.bar(
        top_dy,
        x='Ticker',
        y='DY Anual',
        color='Segmento',
        labels={
            'Ticker': 'FII',
            'DY Anual': 'Dividend Yield Anual (%)',
            'Segmento': 'Segmento'
        },
        title='Top 15 FIIs com Maiores Dividendos'
    )
    
    return dcc.Graph(figure=fig, id='top-dividend-chart')

def create_top_discounted_chart(df, limit=15):
    """Cria gráfico dos FIIs mais descontados (menor P/VP)"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    top_discounted = df.sort_values('P/VP').head(limit)
    
    fig = px.bar(
        top_discounted,
        x='Ticker',
        y='P/VP',
        color='Segmento',
        labels={
            'Ticker': 'FII',
            'P/VP': 'P/VP',
            'Segmento': 'Segmento'
        },
        title='Top 15 FIIs Mais Descontados (Menor P/VP)'
    )
    
    fig.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="P/VP = 1")
    
    return dcc.Graph(figure=fig, id='top-discounted-chart')

def create_opportunity_chart(df):
    """Cria gráfico de dispersão mostrando oportunidades (DY vs P/VP)"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    fig = px.scatter(
        df,
        x='P/VP',
        y='DY Anual',
        color='Segmento',
        size='Preço',
        hover_name='Ticker',
        labels={
            'P/VP': 'P/VP',
            'DY Anual': 'Dividend Yield Anual (%)',
            'Segmento': 'Segmento',
            'Preço': 'Preço (R$)'
        },
        title='Mapa de Oportunidades: DY vs P/VP'
    )
    
    # Adicionar linhas de referência
    fig.add_hline(y=df['DY Anual'].median(), line_dash="dash", line_color="green", 
                 annotation_text="DY Médio")
    fig.add_vline(x=1, line_dash="dash", line_color="red", 
                 annotation_text="P/VP = 1")
    
    # Adicionar áreas de quadrantes
    fig.add_shape(
        type="rect",
        x0=0, y0=df['DY Anual'].median(),
        x1=1, y1=df['DY Anual'].max() + 1,
        line=dict(color="rgba(0,0,0,0)"),
        fillcolor="rgba(0,255,0,0.1)",
    )
    
    return dcc.Graph(figure=fig, id='opportunity-chart')

def create_portfolio_distribution_chart(portfolio_data):
    """Cria gráfico de pizza da distribuição do portfólio por segmento"""
    if portfolio_data is None or len(portfolio_data) == 0:
        return dcc.Graph(figure=go.Figure())
    
    df = pd.DataFrame(portfolio_data)
    df['Valor Atual'] = df['Quantidade'] * df['Preço Atual']
    
    segment_data = df.groupby('Segmento')['Valor Atual'].sum().reset_index()
    
    fig = px.pie(
        segment_data,
        values='Valor Atual',
        names='Segmento',
        title='Distribuição do Portfólio por Segmento',
        hole=0.4,
    )
    
    return dcc.Graph(figure=fig, id='portfolio-distribution-chart')

def create_dividend_history_chart(ticker, history_data=None):
    """Cria gráfico de histórico de dividendos para um FII específico"""
    if history_data is None:
        # Dados fictícios para demonstração
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        history_data = {
            'Mês': months,
            'Valor': np.random.uniform(0.5, 1.2, 12),
            'DY Mensal': np.random.uniform(0.5, 1.0, 12),
        }
    
    df = pd.DataFrame(history_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Mês'],
        y=df['Valor'],
        name='Dividendo (R$)',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Mês'],
        y=df['DY Mensal'],
        name='DY Mensal (%)',
        mode='lines+markers',
        yaxis='y2',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=f'Histórico de Dividendos - {ticker}',
        xaxis=dict(title='Mês'),
        yaxis=dict(
            title='Dividendo (R$)',
            titlefont=dict(color='rgb(55, 83, 109)'),
            tickfont=dict(color='rgb(55, 83, 109)')
        ),
        yaxis2=dict(
            title='DY Mensal (%)',
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
    
    return dcc.Graph(figure=fig, id='dividend-history-chart')

def create_advanced_analysis_chart(df, ticker):
    """Cria gráfico de análise avançada para um FII específico"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Selecionar dados do FII específico
    fii_data = df[df['Ticker'] == ticker]
    
    if fii_data.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Criar gráfico de radar para análise multidimensional
    categories = ['DY Anual', 'P/VP', 'Cap Rate', 'Vacância', 'Sharpe Ratio', 'TIR Estimada']
    
    # Normalizar valores para escala de 0 a 10
    values = []
    for cat in categories:
        if cat in fii_data.columns:
            val = fii_data[cat].values[0]
            
            # Normalização específica para cada indicador
            if cat == 'DY Anual':
                norm_val = min(10, max(0, val / 15 * 10))  # 15% DY = 10 pontos
            elif cat == 'P/VP':
                norm_val = min(10, max(0, (2 - val) / 1.5 * 10))  # P/VP 0.5 = 10 pontos, P/VP 2.0 = 0 pontos
            elif cat == 'Cap Rate':
                norm_val = min(10, max(0, val / 12 * 10))  # 12% Cap Rate = 10 pontos
            elif cat == 'Vacância':
                norm_val = min(10, max(0, (20 - val) / 20 * 10))  # 0% Vacância = 10 pontos, 20% = 0 pontos
            elif cat == 'Sharpe Ratio':
                norm_val = min(10, max(0, (val + 1) / 2 * 10))  # Sharpe 1.0 = 10 pontos, Sharpe -1.0 = 0 pontos
            elif cat == 'TIR Estimada':
                norm_val = min(10, max(0, val / 20 * 10))  # 20% TIR = 10 pontos
            else:
                norm_val = 5  # Valor padrão
            
            values.append(norm_val)
        else:
            values.append(0)
    
    # Adicionar o primeiro valor novamente para fechar o polígono
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=ticker
    ))
    
    # Adicionar média do setor para comparação
    segment = fii_data['Segmento'].values[0]
    segment_fiis = df[df['Segmento'] == segment]
    
    segment_values = []
    for cat in categories[:-1]:  # Excluir o último que é repetido
        if cat in segment_fiis.columns:
            val = segment_fiis[cat].mean()
            
            # Usar a mesma normalização
            if cat == 'DY Anual':
                norm_val = min(10, max(0, val / 15 * 10))
            elif cat == 'P/VP':
                norm_val = min(10, max(0, (2 - val) / 1.5 * 10))
            elif cat == 'Cap Rate':
                norm_val = min(10, max(0, val / 12 * 10))
            elif cat == 'Vacância':
                norm_val = min(10, max(0, (20 - val) / 20 * 10))
            elif cat == 'Sharpe Ratio':
                norm_val = min(10, max(0, (val + 1) / 2 * 10))
            elif cat == 'TIR Estimada':
                norm_val = min(10, max(0, val / 20 * 10))
            else:
                norm_val = 5
            
            segment_values.append(norm_val)
        else:
            segment_values.append(0)
    
    # Adicionar o primeiro valor novamente para fechar o polígono
    segment_values.append(segment_values[0])
    
    fig.add_trace(go.Scatterpolar(
        r=segment_values,
        theta=categories,
        fill='toself',
        name=f'Média {segment}',
        line=dict(color='rgba(255, 0, 0, 0.5)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title=f'Análise Multidimensional - {ticker} vs Média do Segmento {segment}'
    )
    
    return dcc.Graph(figure=fig, id='advanced-analysis-chart')

def create_historical_performance_chart(ticker, history_data):
    """Cria gráfico de desempenho histórico para um FII específico"""
    if history_data is None or history_data.empty:
        return dcc.Graph(figure=go.Figure())
    
    fig = go.Figure()
    
    # Adicionar preço histórico
    fig.add_trace(go.Scatter(
        x=history_data['Data'],
        y=history_data['Preço'],
        name='Preço (R$)',
        line=dict(color='blue')
    ))
    
    # Adicionar P/VP histórico no eixo secundário
    fig.add_trace(go.Scatter(
        x=history_data['Data'],
        y=history_data['P/VP'],
        name='P/VP',
        yaxis='y2',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title=f'Desempenho Histórico - {ticker}',
        xaxis=dict(title='Data'),
        yaxis=dict(
            title='Preço (R$)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='P/VP',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
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
    
    # Adicionar linha de P/VP = 1
    fig.add_hline(y=1, line_dash="dash", line_color="gray", 
                 annotation_text="P/VP = 1", yref='y2')
    
    return dcc.Graph(figure=fig, id='historical-performance-chart')

def create_cap_rate_vacancia_chart(df):
    """Cria gráfico de dispersão relacionando Cap Rate e Vacância"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    fig = px.scatter(
        df,
        x='Vacância',
        y='Cap Rate',
        color='Segmento',
        size='Preço',
        hover_name='Ticker',
        labels={
            'Vacância': 'Vacância (%)',
            'Cap Rate': 'Cap Rate (%)',
            'Segmento': 'Segmento',
            'Preço': 'Preço (R$)'
        },
        title='Relação entre Cap Rate e Vacância'
    )
    
    # Adicionar linhas de referência
    fig.add_hline(y=df['Cap Rate'].median(), line_dash="dash", line_color="green", 
                 annotation_text="Cap Rate Médio")
    fig.add_vline(x=df['Vacância'].median(), line_dash="dash", line_color="red", 
                 annotation_text="Vacância Média")
    
    # Adicionar áreas de quadrantes
    fig.add_shape(
        type="rect",
        x0=0, y0=df['Cap Rate'].median(),
        x1=df['Vacância'].median(), y1=df['Cap Rate'].max() + 1,
        line=dict(color="rgba(0,0,0,0)"),
        fillcolor="rgba(0,255,0,0.1)",
    )
    
    return dcc.Graph(figure=fig, id='cap-rate-vacancia-chart')

def create_yield_curve_chart(df):
    """Cria gráfico da curva de yield por segmento"""
    if df is None or df.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Agrupar por segmento e calcular estatísticas
    segment_stats = df.groupby('Segmento').agg({
        'DY Anual': ['mean', 'min', 'max', 'std'],
        'P/VP': 'mean',
        'Ticker': 'count'
    }).reset_index()
    
    # Renomear colunas
    segment_stats.columns = ['Segmento', 'DY Médio', 'DY Mínimo', 'DY Máximo', 'DY Desvio', 'P/VP Médio', 'Quantidade']
    
    # Ordenar por DY médio
    segment_stats = segment_stats.sort_values('DY Médio', ascending=False)
    
    fig = go.Figure()
    
    # Adicionar barras para DY médio
    fig.add_trace(go.Bar(
        x=segment_stats['Segmento'],
        y=segment_stats['DY Médio'],
        name='DY Médio (%)',
        marker_color='rgb(55, 83, 109)',
        error_y=dict(
            type='data',
            array=segment_stats['DY Desvio'],
            visible=True
        )
    ))
    
    # Adicionar linha para P/VP médio
    fig.add_trace(go.Scatter(
        x=segment_stats['Segmento'],
        y=segment_stats['P/VP Médio'],
        name='P/VP Médio',
        mode='lines+markers',
        yaxis='y2',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title='Curva de Yield por Segmento',
        xaxis=dict(title='Segmento'),
        # Por:
    yaxis=dict(
        title='Dividend Yield Médio (%)',
        title_font=dict(color='rgb(55, 83, 109)'),
        tickfont=dict(color='rgb(55, 83, 109)')
),
    yaxis2=dict(
        title='P/VP Médio',
        title_font=dict(color='rgb(26, 118, 255)'),
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
        ),
        barmode='group'
    )
    
    # Adicionar linha de P/VP = 1
    fig.add_hline(y=1, line_dash="dash", line_color="gray", 
                 annotation_text="P/VP = 1", yref='y2')
    
    return dcc.Graph(figure=fig, id='yield-curve-chart')

