import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
from scipy.interpolate import make_interp_spline
import numpy as np

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.get_crypto_data import GetCryptoData


#Classe que cria os graficos do dashboard
class Plot_Creator:
    def __init__(self):
        self.data = GetCryptoData()

    def clean_data(self, df):
        # Remove linhas com valores NaN ou inf
        df = df.replace([np.inf, -np.inf], np.nan)  # Substitui infs por NaN
        df = df.dropna()  # Remove qualquer linha que contenha NaN
        return df

    #Cria o gráfico do valor da cripto moeda ao longo dos 6 meses
    def create_plot_range_value(self, crypto_name):
        self.data.do_update_database()
        if crypto_name == 'bitcoin':
            data = {
                'Period': ['6 months', '5 months', '4 months', '3 months', '2 months', '1 month', '7 days', '1 day', 'Now'],
                'Price': [
                   self.data.crypto_data["bitcoin"]["price_6_months_ago"],
                   self.data.crypto_data["bitcoin"]["price_5_months_ago"],
                   self.data.crypto_data["bitcoin"]["price_4_months_ago"],
                   self.data.crypto_data["bitcoin"]["price_3_months_ago"],
                   self.data.crypto_data["bitcoin"]["price_2_months_ago"],
                   self.data.crypto_data["bitcoin"]["price_1_month_ago"],
                   self.data.crypto_data["bitcoin"]["price_7_days_ago"],
                   self.data.crypto_data["bitcoin"]["price_1_day_ago"],
                   self.data.crypto_data["bitcoin"]["current_price"]
                ]
            }
        elif crypto_name == 'ethereum':
            data = {
                'Period': ['6 months', '5 months', '4 months', '3 months', '2 months', '1 month', '7 days', '1 day', 'Now'],
                'Price': [
                    self.data.crypto_data["ethereum"]["price_6_months_ago"],
                    self.data.crypto_data["ethereum"]["price_5_months_ago"],
                    self.data.crypto_data["ethereum"]["price_4_months_ago"],
                    self.data.crypto_data["ethereum"]["price_3_months_ago"],
                    self.data.crypto_data["ethereum"]["price_2_months_ago"],
                    self.data.crypto_data["ethereum"]["price_1_month_ago"],
                    self.data.crypto_data["ethereum"]["price_7_days_ago"],
                    self.data.crypto_data["ethereum"]["price_1_day_ago"],
                    self.data.crypto_data["ethereum"]["current_price"]
                ]
            }
        else:
            raise ValueError("Unsupported cryptocurrency")

        df = pd.DataFrame(data)
        x = np.arange(len(df['Period']))
        y = df['Price']

        # Limpeza dos dados
        df_clean = self.clean_data(df)

        if len(df_clean) < 2:
            raise ValueError("Not enough data for interpolation")

        x = np.arange(len(df_clean['Period']))
        y = df_clean['Price']

        x_smooth = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)

        y_min = min(y_smooth)
        y_max = max(y_smooth)

        if crypto_name == 'bitcoin':
            fig, ax = plt.subplots(figsize=(18, 10))  
            font = FontProperties(weight='bold', size=16)
            for label in ax.get_yticklabels():
                label.set_fontproperties(font)
                label.set_color('#FF6F3C')
        
            plt.xticks(np.arange(len(df['Period'])), df['Period'], rotation=45, ha='right', fontsize=18, color='#FF6F3C')
            line_width = 5
        else:
            fig, ax = plt.subplots(figsize=(10, 5))  
            font = FontProperties(weight='bold', size=8)
            for label in ax.get_yticklabels():
                label.set_fontproperties(font)
                label.set_color('#FF6F3C')
        
            plt.xticks(np.arange(len(df['Period'])), df['Period'], rotation=45, ha='right', fontsize=10, color='#FF6F3C')
            line_width = 3

        ax.plot(x_smooth, y_smooth, color='#1B263B', linewidth=line_width)
        ax.set_ylim([y_min, y_max])

        ax.fill_between(x_smooth, y_smooth, color='#1B263B', alpha=0.3)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('grey')
        ax.spines['bottom'].set_color('grey')
        ax.yaxis.tick_left()
        ax.xaxis.tick_bottom()
        ax.grid(True, linestyle='--', alpha=0.2)

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.2)

        save_dir = r'app\\static\\images\\dashboard'
        os.makedirs(save_dir, exist_ok=True)
        plot_path = os.path.join(save_dir, f'{crypto_name}.png')

        try:
            plt.savefig(plot_path, transparent=True)
            plt.close()
            print(f"Imagem salva em: {plot_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
            plot_path = None

        return plot_path

    #Cria o gráfico com o historico de compra da moeda
    def create_plot_history(self, crypto_id, user_id):
        data = self.data.get_crypto_buy(crypto_id, user_id)

        valores = [item[0] for item in data]
        datas = [item[1] for item in data]  

        meses = [data.strftime("%Y-%m") for data in datas]

        df = pd.DataFrame({
            'Mês': meses,
            'Valor': valores
        })

        df_grouped = df.groupby('Mês').sum().reset_index()

        df_grouped = self.clean_data(df_grouped)

        fig, ax = plt.subplots(figsize=(7, 8))

        y_max = df_grouped['Valor'].max() * 1.5

        if len(df_grouped) == 1:
            bar_width = 13
            x_max = df_grouped['Valor'].max() * 5
            ax.bar(df_grouped['Mês'], df_grouped['Valor'], color='#1B263B', width=bar_width, zorder=3)
            ax.set_xticks([df_grouped['Mês'].iloc[0]])
            ax.set_ylim(0, y_max)
            ax.set_xlim(0, x_max)
        else:
            ax.bar(df_grouped['Mês'], df_grouped['Valor'], color='#1B263B', zorder=3)

        ax.tick_params(axis='x', rotation=45, labelsize=16, labelcolor='#FF6F3C')
        ax.tick_params(axis='y', labelsize=16, labelcolor='#FF6F3C')

        for tick in ax.get_yticklabels():
            tick.set_fontweight('bold')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('grey')
        ax.spines['bottom'].set_color('grey')
        ax.yaxis.tick_left()
        ax.xaxis.tick_bottom()
        ax.grid(True, linestyle='--', alpha=0.2, zorder=1)

        plt.tight_layout()

        save_dir = os.path.abspath('app/static/images/dashboard/')
        os.makedirs(save_dir, exist_ok=True)
        plot_path = os.path.join(save_dir, f'crypto_history_{crypto_id}_{user_id}.png')

        try:
            plt.savefig(plot_path, transparent=True)
            plt.close()
            print(f"Imagem salva em: {plot_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
            plot_path = None

        return plot_path

    #Cria o gráfico do total gasto e quanto foi gasto em cada moeda
    def create_plot_spent(self, time, user_id):
        total_bitcoin = 0
        total_ethereum = 0

        data = self.data.get_total_spent(user_id, time)

        cleaned_data = [(crypto_id, amount) for crypto_id, amount in data if not pd.isna(amount) and amount > 0]

        for crypto_id, amount in cleaned_data:
            if crypto_id == 1:  # Bitcoin
                total_bitcoin += amount
            elif crypto_id == 2:  # Ethereum
                total_ethereum += amount

        if total_bitcoin == 0 and total_ethereum == 0:
            fig, ax = plt.subplots(figsize=(7, 8))
            ax.text(0.5, 0.5, 'Sem dados disponíveis', horizontalalignment='center', 
                    verticalalignment='center', fontsize=20, color='red', transform=ax.transAxes)
            ax.axis('off')
            valores = [0, 0]
        else:
            valores = [total_bitcoin, total_ethereum]
            labels = ['Bitcoin', 'Ethereum']
            colors = ['#FF6F3C', '#1B263B']  

            fig, ax = plt.subplots(figsize=(7, 8))

            wedges, texts, autotexts = ax.pie(valores, labels=labels, colors=colors, 
                                            autopct=lambda pct: '', startangle=90)
            ax.axis('equal')  

            for text in texts:
                text.set_fontsize(20)
                text.set_color('#F8F9FA') 

            for autotext in autotexts:
                autotext.set_fontsize(20)
                autotext.set_color('#F8F9FA')  

        plt.tight_layout()

        # Caminho para salvar a imagem
        save_dir = os.path.abspath('app/static/images/dashboard/')
        os.makedirs(save_dir, exist_ok=True)
        plot_path = os.path.join(save_dir, f'crypto_spent_{user_id}_{time}.png')

        try:
            plt.savefig(plot_path, transparent=True)
            plt.close()
            print(f"Imagem salva em: {plot_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
            plot_path = None

        return plot_path, valores
