import numpy as np
import pandas as pd
from datetime import datetime

def calculate_dividend_yield(price, dividend):
    """Calcula o dividend yield anual"""
    if price <= 0 or dividend <= 0:
        return 0
    annual_dividend = dividend * 12
    return (annual_dividend / price) * 100

def calculate_pvp(price, equity_value):
    """Calcula o P/VP (Preço sobre Valor Patrimonial)"""
    if equity_value <= 0:
        return 0
    return price / equity_value

def calculate_fair_price(price, pvp):
    """Calcula o preço justo baseado no P/VP"""
    if pvp <= 0:
        return price
    return price / pvp

def calculate_cap_rate(annual_income, property_value):
    """Calcula o Cap Rate"""
    if property_value <= 0:
        return 0
    return (annual_income / property_value) * 100

def calculate_sharpe_ratio(returns, risk_free_rate, volatility):
    """Calcula o Sharpe Ratio"""
    if volatility <= 0:
        return 0
    return (returns - risk_free_rate) / volatility

def calculate_gordon_growth_model(dividend, growth_rate, discount_rate):
    """Calcula o preço justo usando o modelo de Gordon"""
    if discount_rate <= growth_rate:
        return float('inf')
    return dividend * 12 / ((discount_rate - growth_rate) / 100)

def calculate_yield_on_cost(current_dividend, purchase_price):
    """Calcula o Yield on Cost"""
    if purchase_price <= 0:
        return 0
    return (current_dividend * 12 / purchase_price) * 100

def calculate_tir(cash_flows, periods=10):
    """Calcula a Taxa Interna de Retorno (TIR) estimada"""
    try:
        # Cria um array de fluxos de caixa começando com o investimento inicial (negativo)
        # seguido pelos dividendos projetados (positivos)
        flows = np.array(cash_flows)
        return np.irr(flows) * 100
    except:
        return 0

def calculate_portfolio_metrics(portfolio_df, all_fiis_df):
    """Calcula métricas agregadas para um portfólio de FIIs"""
    if portfolio_df.empty:
        return {}
    
    # Calcular valor total investido e atual
    portfolio_df['Valor Investido'] = portfolio_df['Quantidade'] * portfolio_df['Preço Médio']
    portfolio_df['Valor Atual'] = portfolio_df['Quantidade'] * portfolio_df['Preço Atual']
    
    # Calcular rentabilidade
    total_invested = portfolio_df['Valor Investido'].sum()
    total_current = portfolio_df['Valor Atual'].sum()
    total_return = ((total_current / total_invested) - 1) * 100 if total_invested > 0 else 0
    
    # Calcular dividendos
    portfolio_df['Dividendos Mensais'] = portfolio_df['Valor Atual'] * (portfolio_df['DY Mensal'] / 100)
    portfolio_df['Dividendos Anuais'] = portfolio_df['Valor Atual'] * (portfolio_df['DY Anual'] / 100)
    total_monthly_dividends = portfolio_df['Dividendos Mensais'].sum()
    total_annual_dividends = portfolio_df['Dividendos Anuais'].sum()
    
    # Calcular dividend yield do portfólio
    portfolio_dy = (total_annual_dividends / total_current) * 100 if total_current > 0 else 0
    
    # Calcular yield on cost do portfólio
    portfolio_df['Yield on Cost'] = (portfolio_df['Dividendos Anuais'] / portfolio_df['Valor Investido']) * 100
    portfolio_yoc = portfolio_df['Yield on Cost'].mean()
    
    # Calcular diversificação
    segment_count = portfolio_df['Segmento'].nunique()
    total_segments = all_fiis_df['Segmento'].nunique()
    diversification = (segment_count / total_segments) * 100 if total_segments > 0 else 0
    
    # Calcular métricas comparativas com o mercado
    market_dy = all_fiis_df['DY Anual'].mean()
    market_pvp = all_fiis_df['P/VP'].mean()
    portfolio_pvp = portfolio_df['P/VP'].mean() if 'P/VP' in portfolio_df.columns else 1.0
    
    # Retornar dicionário com todas as métricas
    return {
        'total_invested': total_invested,
        'total_current': total_current,
        'total_return': total_return,
        'total_monthly_dividends': total_monthly_dividends,
        'total_annual_dividends': total_annual_dividends,
        'portfolio_dy': portfolio_dy,
        'portfolio_yoc': portfolio_yoc,
        'diversification': diversification,
        'segment_count': segment_count,
        'total_segments': total_segments,
        'market_dy': market_dy,
        'market_pvp': market_pvp,
        'portfolio_pvp': portfolio_pvp,
    }
