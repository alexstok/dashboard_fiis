import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import json
from datetime import datetime, timedelta
import numpy as np

class FIIDataHandler:
    def __init__(self):
        self.data = None
        self.last_update = None
        self.update_interval = 4  # horas
        
    def should_update(self):
        if self.last_update is None:
            return True
        elapsed = datetime.now() - self.last_update
        return elapsed > timedelta(hours=self.update_interval)
    
    def fetch_data(self):
        """Busca dados de FIIs de fontes externas"""
        if not self.should_update() and self.data is not None:
            return self.data
            
        # Aqui você pode implementar a coleta de dados de diferentes fontes
        # Exemplo: web scraping de sites como Funds Explorer, Status Invest, etc.
        
        # Método simplificado para demonstração - em produção, use APIs reais
        try:
            # Exemplo usando Status Invest (você precisará adaptar conforme a estrutura do site)
            url = "https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Segment%22%3A%22%22%2C%22CategoryType%22%3A%22%22%2C%22Search%22%3A%22%22%2C%22Order%22%3A%7B%22Field%22%3A%22name%22%2C%22Ascending%22%3Atrue%7D%2C%22Pagination%22%3A%7B%22Page%22%3A1%2C%22PageSize%22%3A200%7D%7D&CategoryType=2"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.post(url, headers=headers)
            data = response.json()
            
            # Verificar se data contém a chave 'list' antes de acessá-la
            if isinstance(data, dict) and 'list' in data:
                # Converter para DataFrame
                df = pd.DataFrame(data['list'])
                
                # Adicionar informações adicionais como P/VP, vacância, etc.
                # Isso normalmente exigiria chamadas adicionais para cada FII
                
                self.data = self.process_data(df)
                self.last_update = datetime.now()
                return self.data
            else:
                print(f"Formato de dados inesperado: {type(data)}")
                return self.get_sample_data()
            
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            # Fallback para dados de exemplo caso a API falhe
            return self.get_sample_data()
    
    def process_data(self, df):
        """Processa os dados brutos e calcula indicadores adicionais"""
        # Renomear colunas e calcular indicadores
        df = df.rename(columns={
            'ticker': 'Ticker',
            'price': 'Preço',
            'dy12m': 'DY Anual',
            'pvp': 'P/VP',
            'segment': 'Segmento'
        })
        
        # Calcular DY mensal (média)
        df.loc[:, 'DY Mensal'] = df['DY Anual'] / 12
        
        # Calcular preço justo (exemplo simplificado)
        df.loc[:, 'Preço Justo'] = df['Preço'] / df['P/VP']
        
        # Indicador de oportunidade (exemplo simples)
        df.loc[:, 'Oportunidade'] = ((df['DY Anual'] > 8) & (df['P/VP'] < 1)).map({True: 'Sim', False: 'Não'})
        
        # Adicionar indicadores avançados
        df.loc[:, 'Cap Rate'] = np.random.uniform(5, 12, len(df))  # Simulado - em produção, use dados reais
        df.loc[:, 'Vacância'] = np.random.uniform(0, 20, len(df))  # Simulado - em produção, use dados reais
        df.loc[:, 'Liquidez'] = np.random.uniform(100000, 5000000, len(df))  # Volume médio diário em R$
        df.loc[:, 'Taxa de Administração'] = np.random.uniform(0.5, 2, len(df))
        
        # Calcular Spread do P/VP (simulado - em produção, use média histórica real)
        df.loc[:, 'P/VP Médio Histórico'] = df['P/VP'] * np.random.uniform(0.8, 1.2, len(df))
        df.loc[:, 'Spread P/VP'] = ((df['P/VP'] / df['P/VP Médio Histórico']) - 1) * 100
        
        # Calcular Índice de Sharpe adaptado (simulado)
        df.loc[:, 'Volatilidade'] = np.random.uniform(10, 30, len(df))  # % anual
        df.loc[:, 'Sharpe Ratio'] = (df['DY Anual'] - 4.5) / df['Volatilidade']  # 4.5% como taxa livre de risco
        
        # Calcular TIR estimada (simulado)
        df.loc[:, 'TIR Estimada'] = df['DY Anual'] + np.random.uniform(-2, 8, len(df))
        
        return df
    
    def get_sample_data(self):
        """Retorna dados de exemplo caso a API falhe"""
        # Criar dados fictícios para demonstração
        segments = ['Logística', 'Corporativo', 'Recebíveis', 'Shopping', 'Híbrido', 'Residencial', 'Hospital']
        tickers = [f"FII{i+1:02d}11" for i in range(150)]
        
        data = {
            'Ticker': tickers,
            'Segmento': np.random.choice(segments, size=150),
            'Preço': np.random.uniform(10, 200, 150),
            'DY Anual': np.random.uniform(4, 15, 150),
            'P/VP': np.random.uniform(0.6, 1.4, 150),
            'Último Dividendo': np.random.uniform(0.3, 2, 150),
            'Vacância': np.random.uniform(0, 20, 150),
            'Cap Rate': np.random.uniform(5, 12, 150),
            'Liquidez': np.random.uniform(100000, 5000000, 150),
            'Taxa de Administração': np.random.uniform(0.5, 2, 150),
            'Volatilidade': np.random.uniform(10, 30, 150),
        }
        
        df = pd.DataFrame(data)
        df.loc[:, 'DY Mensal'] = df['DY Anual'] / 12
        df.loc[:, 'Preço Justo'] = df['Preço'] / df['P/VP'] * np.random.uniform(0.9, 1.1, 150)
        df.loc[:, 'Oportunidade'] = ((df['DY Anual'] > 8) & (df['P/VP'] < 1)).map({True: 'Sim', False: 'Não'})
        df.loc[:, 'P/VP Médio Histórico'] = df['P/VP'] * np.random.uniform(0.8, 1.2, 150)
        df.loc[:, 'Spread P/VP'] = ((df['P/VP'] / df['P/VP Médio Histórico']) - 1) * 100
        df.loc[:, 'Sharpe Ratio'] = (df['DY Anual'] - 4.5) / df['Volatilidade']
        df.loc[:, 'TIR Estimada'] = df['DY Anual'] + np.random.uniform(-2, 8, 150)
        
        return df
    
    def filter_data(self, df, segment=None, min_dy=None, max_price=None, ticker=None, max_pvp=None, min_liquidez=None):
        """Aplica filtros aos dados"""
        filtered_df = df.copy()
        
        if segment and segment != 'Todos':
            filtered_df = filtered_df[filtered_df['Segmento'] == segment]
            
        if min_dy is not None:
            filtered_df = filtered_df[filtered_df['DY Anual'] >= min_dy]
            
        if max_price is not None:
            filtered_df = filtered_df[filtered_df['Preço'] <= max_price]
            
        if ticker:
            filtered_df = filtered_df[filtered_df['Ticker'].str.contains(ticker, case=False)]
            
        if max_pvp is not None:
            filtered_df = filtered_df[filtered_df['P/VP'] <= max_pvp]
            
        if min_liquidez is not None:
            filtered_df = filtered_df[filtered_df['Liquidez'] >= min_liquidez]
            
        return filtered_df
    
    def get_top_fiis_by_price(self, max_price=25, limit=30):
        """Retorna os melhores FIIs abaixo de um preço máximo"""
        df = self.fetch_data()
        filtered = df[df['Preço'] <= max_price].copy()
        # Ordenar por uma combinação de DY e P/VP
        filtered.loc[:, 'Score'] = filtered['DY Anual'] - (filtered['P/VP'] * 2) + (filtered['Sharpe Ratio'] * 3)
        return filtered.sort_values('Score', ascending=False).head(limit)
    
    def get_all_fiis(self, limit=150):
        """Retorna todos os FIIs limitados a um número"""
        df = self.fetch_data()
        return df.head(limit)
    
    def get_dividend_calendar(self):
        """Retorna o calendário de dividendos"""
        # Implementação simplificada - em produção, buscar dados reais
        today = datetime.now()
        
        # Criar datas fictícias para os próximos 2 meses
        calendar = []
        for i in range(30):
            date = today + timedelta(days=i)
            if i % 5 == 0:  # Apenas para criar alguns eventos de exemplo
                fii = f"FII{i+1:02d}11"
                calendar.append({
                    'Ticker': fii,
                    'Data de Corte': date.strftime('%d/%m/%Y'),
                    'Data de Pagamento': (date + timedelta(days=10)).strftime('%d/%m/%Y'),
                    'Valor Previsto': round(0.5 + (i % 10) / 10, 2)
                })
        
        return pd.DataFrame(calendar)
    
    def get_advanced_indicators(self, ticker):
        """Retorna indicadores avançados para um FII específico"""
        df = self.fetch_data()
        fii_data = df[df['Ticker'] == ticker]
        
        if fii_data.empty:
            return None
        
        # Verificar se fii_data não está vazio
        if fii_data.empty:
            raise ValueError("fii_data está vazio. Não é possível gerar dados históricos.")

        # Em produção, você buscaria dados históricos reais
        # Aqui, vamos simular alguns dados históricos
        dates = pd.date_range(end=datetime.now(), periods=24, freq='M')

        historical_data = {
            'Data': dates,
            'Preço': np.random.normal(fii_data['Preço'].values[0], fii_data['Preço'].values[0] * 0.1, 24),
            'Dividendo': np.random.normal(fii_data['Último Dividendo'].values[0], fii_data['Último Dividendo'].values[0] * 0.2, 24),
            'P/VP': np.random.normal(fii_data['P/VP'].values[0], 0.1, 24),
            'Vacância': np.random.normal(fii_data['Vacância'].values[0], 2, 24),
            'Cap Rate': np.random.normal(fii_data['Cap Rate'].values[0], 1, 24),
        }

        # Garantir que os valores façam sentido
        historical_data['Preço'] = np.maximum(historical_data['Preço'], 5)  # Preço mínimo de R$ 5
        historical_data['Dividendo'] = np.maximum(historical_data['Dividendo'], 0)  # Dividendo não negativo
        historical_data['P/VP'] = np.maximum(historical_data['P/VP'], 0.3)  # P/VP mínimo de 0.3
        historical_data['Vacância'] = np.clip(historical_data['Vacância'], 0, 100)  # Vacância entre 0% e 100%
        historical_data['Cap Rate'] = np.clip(historical_data['Cap Rate'], 3, 20)  # Cap Rate entre 3% e 20%

        return pd.DataFrame(historical_data)
