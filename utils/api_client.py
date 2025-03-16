import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import os

class APIClient:
    """Cliente para APIs externas de dados financeiros"""
    
    def __init__(self, cache_dir='./cache'):
        self.cache_dir = cache_dir
        self.cache_duration = 24  # horas
        
        # Criar diretório de cache se não existir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get_status_invest_data(self, category_type=2):
        """Obtém dados do Status Invest (category_type=2 para FIIs)"""
        cache_file = os.path.join(self.cache_dir, f'status_invest_{category_type}.json')
        
        # Verificar se existe cache válido
        if self._is_cache_valid(cache_file):
            return self._load_from_cache(cache_file)
        
        url = "https://statusinvest.com.br/category/advancedsearchresult"
        payload = {
            "search": {
                "Segment": "",
                "CategoryType": "",
                "Search": "",
                "Order": {"Field": "name", "Ascending": True},
                "Pagination": {"Page": 1, "PageSize": 200}
            },
            "CategoryType": category_type
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                data = response.json()
                self._save_to_cache(cache_file, data)
                return data
            else:
                print(f"Erro na API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erro ao acessar a API: {e}")
            return None
    
    def get_fii_details(self, ticker):
        """Obtém detalhes específicos de um FII"""
        cache_file = os.path.join(self.cache_dir, f'fii_details_{ticker}.json')
        
        # Verificar se existe cache válido
        if self._is_cache_valid(cache_file):
            return self._load_from_cache(cache_file)
        
        url = f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Em um caso real, você faria web scraping aqui
                # Para simplificar, retornaremos dados fictícios
                data = self._generate_mock_fii_details(ticker)
                self._save_to_cache(cache_file, data)
                return data
            else:
                print(f"Erro na API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erro ao acessar a API: {e}")
            return None
    
    def get_fii_historical_data(self, ticker, period='1y'):
        """Obtém dados históricos de um FII"""
        cache_file = os.path.join(self.cache_dir, f'fii_history_{ticker}_{period}.json')
        
        # Verificar se existe cache válido
        if self._is_cache_valid(cache_file):
            return self._load_from_cache(cache_file)
        
        # Em um caso real, você usaria uma API como Alpha Vantage, Yahoo Finance, etc.
        # Para simplificar, retornaremos dados fictícios
        data = self._generate_mock_historical_data(ticker, period)
        self._save_to_cache(cache_file, data)
        return data
    
    def get_dividend_calendar(self):
        """Obtém o calendário de dividendos"""
        cache_file = os.path.join(self.cache_dir, 'dividend_calendar.json')
        
        # Verificar se existe cache válido
        if self._is_cache_valid(cache_file):
            return self._load_from_cache(cache_file)
        
        # Em um caso real, você usaria uma API ou faria web scraping
        # Para simplificar, retornaremos dados fictícios
        data = self._generate_mock_dividend_calendar()
        self._save_to_cache(cache_file, data)
        return data
    
    def _is_cache_valid(self, cache_file):
        """Verifica se o cache é válido (existe e não está expirado)"""
        if not os.path.exists(cache_file):
            return False
        
        file_time = os.path.getmtime(cache_file)
        file_datetime = datetime.fromtimestamp(file_time)
        now = datetime.now()
        
        return (now - file_datetime).total_seconds() < (self.cache_duration * 3600)
    
    def _save_to_cache(self, cache_file, data):
        """Salva dados no cache"""
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def _load_from_cache(self, cache_file):
        """Carrega dados do cache"""
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _generate_mock_fii_details(self, ticker):
        """Gera dados fictícios para detalhes de um FII"""
        import random
        
        return {
            "ticker": ticker,
            "name": f"FII {ticker}",
            "segment": random.choice(["Logística", "Corporativo", "Recebíveis", "Shopping", "Híbrido"]),
            "price": round(random.uniform(50, 200), 2),
            "dy12m": round(random.uniform(5, 12), 2),
            "pvp": round(random.uniform(0.7, 1.3), 2),
            "vacancyRate": round(random.uniform(0, 15), 2),
            "capRate": round(random.uniform(6, 12), 2),
            "lastDividend": round(random.uniform(0.4, 1.2), 4),
            "lastPaymentDate": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "nextCutDate": (datetime.now() + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d"),
            "nextPaymentDate": (datetime.now() + timedelta(days=random.randint(16, 30))).strftime("%Y-%m-%d"),
            "volatility": round(random.uniform(10, 30), 2),
            "beta": round(random.uniform(0.5, 1.5), 2),
            "sharpeRatio": round(random.uniform(-0.5, 2), 2),
            "managementFee": round(random.uniform(0.5, 2), 2),
            "performanceFee": round(random.choice([0, 20]), 0),
            "netWorth": round(random.uniform(100000000, 2000000000), 2),
            "liquidity": round(random.uniform(500000, 5000000), 2),
        }
    
    def _generate_mock_historical_data(self, ticker, period):
        """Gera dados históricos fictícios para um FII"""
        import random
        import numpy as np
        
        # Determinar número de dias com base no período
        days = 365
        if period == '6m':
            days = 180
        elif period == '3m':
            days = 90
        elif period == '1m':
            days = 30
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Gerar datas de negociação (dias úteis)
        dates = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 0-4 são dias úteis (seg-sex)
                dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Gerar preços com tendência aleatória
        base_price = random.uniform(50, 200)
        trend = random.uniform(-0.0001, 0.0001)
        volatility = random.uniform(0.005, 0.02)
        
        prices = [base_price]
        for i in range(1, len(dates)):
            price_change = trend + random.normalvariate(0, volatility)
            new_price = prices[-1] * (1 + price_change)
            prices.append(max(10, new_price))  # Garantir preço mínimo de R$ 10
        
        # Gerar dividendos mensais
        dividends = []
        last_month = None
        for date in dates:
            if last_month != date.month:
                last_month = date.month
                dividend = round(random.uniform(0.4, 1.2), 4)
            else:
                dividend = 0
            dividends.append(dividend)
        
        # Criar DataFrame
        data = {
            'Date': dates,
            'Price': prices,
            'Dividend': dividends,
            'Volume': [int(random.uniform(100000, 5000000)) for _ in range(len(dates))],
        }
        
        # Adicionar P/VP e outros indicadores
        data['P/VP'] = [round(price / (base_price * random.uniform(0.8, 1.2)), 2) for price in prices]
        data['Vacância'] = [round(random.uniform(0, 15), 2) for _ in range(len(dates))]
        data['Cap Rate'] = [round(random.uniform(6, 12), 2) for _ in range(len(dates))]
        
        return data
    
    def _generate_mock_dividend_calendar(self):
        """Gera um calendário de dividendos fictício"""
        import random
        
        today = datetime.now()
        
        events = []
        for i in range(30):
            event_date = today + timedelta(days=i)
            if i % 3 == 0:  # Apenas para criar alguns eventos de exemplo
                ticker = f"FII{i+1:02d}11"
                events.append({
                    'Date': event_date.strftime("%Y-%m-%d"),
                    'Ticker': ticker,
                    'EventType': 'Cut Date' if i % 2 == 0 else 'Payment Date',
                    'Value': round(0.5 + (i % 10) / 10, 2) if i % 2 != 0 else None
                })
        
        return events
