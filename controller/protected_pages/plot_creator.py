import pandas as pd # type: ignore
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.interpolate import make_interp_spline # type: ignore
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from scipy.interpolate import make_interp_spline
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .get_crypto_data import GetCryptoData


#Classe que cria os graficos do dashboard
class Plot_Creator:
    def __init__(self):
        self.data = GetCryptoData()

    def clean_data(self, df):
        # Remove linhas com valores NaN(not a number) ou inf(numero infinito)
        df = df.replace([np.inf, -np.inf], np.nan)  
        df = df.dropna()  
        return df

    #salva os plots na pasta static/images/dashboard
    def save_plot(self, filename, fig):
        # salva o gráfico como um arquivo HTML dinâmico
        current_dir = os.path.dirname(__file__)
        save_dir = os.path.join(current_dir, '..', '..', 'static', 'images', 'dashboard')
        os.makedirs(save_dir, exist_ok=True)
        plot_path = os.path.join(save_dir, filename)

        # escreve como html
        try:
            pio.write_html(fig, file=plot_path, auto_open=False, config={'displayModeBar': False})
            print(f"Gráfico salvo em: {plot_path}")
        except Exception as e:
            print(f"Erro ao salvar o gráfico Plotly: {e}")

        return filename

    #Cria o gráfico do valor da cripto moeda ao longo dos 6 meses
    def create_plot_range_value(self, crypto_name):
        try:
            # adiciona todos os dados em data
            data = {
                'Period': ['6 Months', '5 Months', '4 Months', '3 Months', '2 Months', 
                        '1 Month', '7 Days', '1 Day', 'Now'],
                'Price': [
                    self.data.crypto_data[crypto_name]["price_6_months_ago"],
                    self.data.crypto_data[crypto_name]["price_5_months_ago"],
                    self.data.crypto_data[crypto_name]["price_4_months_ago"],
                    self.data.crypto_data[crypto_name]["price_3_months_ago"],
                    self.data.crypto_data[crypto_name]["price_2_months_ago"],
                    self.data.crypto_data[crypto_name]["price_1_month_ago"],
                    self.data.crypto_data[crypto_name]["price_7_days_ago"],
                    self.data.crypto_data[crypto_name]["price_1_day_ago"],
                    self.data.crypto_data[crypto_name]["current_price"]
                ]
            }
            #cria o dataframe
            df = pd.DataFrame(data)
            
            # cria o grafico com plotly
            fig = go.Figure()

            if crypto_name.lower() == 'bitcoin':
                color = '255, 111, 60'
                color_hex = '#FF6F3C'
                # define o limite minimo e maximo do eixo y, pra n ficar valores sobrando
                y_min = min(df['Price']) - 1500  
                y_max = max(df['Price']) + 1500  
            elif crypto_name.lower() == 'ethereum':
                color = '27, 38, 59'
                color_hex = '#1B263B'
                # define o limite minimo e maximo do eixo y, pra n ficar valores sobrando
                y_min = min(df['Price']) - 300  
                y_max = max(df['Price']) + 300  

            # adiciona os dados no grafico
            fig.add_trace(go.Scatter(
                x=df['Period'],
                y=df['Price'],
                line=dict(color=color_hex, width=3, shape='spline'),  #cria a linha
                fill='tozeroy', #cria o preenchimento
                fillcolor=f'rgba({color}, 0.2)', # da cor ao preenchimento
            ))

            #monta o layout do grafico
            fig.update_layout(
                paper_bgcolor='#f8f9fa', #define a cor papel que fica no fundo
                plot_bgcolor=f'rgba({color}, 0.1)', #define a cor do fundo do grafico
                yaxis=dict(tickprefix='$', ticksuffix='  ',showgrid=True, 
                        range=[y_min, y_max], automargin=True),  # config do eixo y
                xaxis=dict(showgrid=True, ticklabelposition="inside"),  # config do eixo x
                hovermode='x unified', #efeito de hover
                margin=dict(l=0, r=0, t=40, b=10),  # margem
                #height=350, #altura
                #width=800, #largura
                title=dict(text=f"<b>Preço do {crypto_name.capitalize()} ao longo do tempo</b>", 
                        font=dict(family="Montserrat", size=16), x=0.5)  # título do gráfico
            )

            return self.save_plot(filename=f"{crypto_name}_plot.html", fig=fig)
        except:
            return None
    #Cria o gráfico com o historico de compra da moeda
    def create_plot_history(self, crypto_name, user_id):
        try:
            color = ''

            crypto_id = 1 if crypto_name == 'bitcoin' else 2
            data = self.data.get_crypto_buy(crypto_id, user_id)

            # Extração dos valores e datas
            valores = [item[0] for item in data]
            datas = [item[1] for item in data]  

            # Formatando as datas em "Ano-Mês"
            meses = [f"{data.strftime('%Y')}/{data.strftime('%m')}" for data in datas]


            # Criando o DataFrame
            df = pd.DataFrame({
                'month': meses,
                'value': valores
            })

            # Agrupar e somar os valores por mês para evitar duplicação
            df_grouped = df.groupby('month', as_index=False).sum()

            # Criando o gráfico
            fig = go.Figure()

            df_grouped = df_grouped.sort_values(by='month', ascending=True)
            df_grouped.reset_index(drop=True, inplace=True)

            x_max = max(df_grouped['value']) * 1.5

            # Definindo as cores com base no nome da criptomoeda
            if crypto_name == 'bitcoin':
                color_bg = 'rgba(255, 111, 60, 0.1)'  # Opacidade 70%
                color = '#FF6F3C'

            elif crypto_name == 'ethereum':
                color_bg = 'rgba(27, 38, 59, 0.1)'  # Opacidade 70%
                color = '#1B263B'

            # Adiciona a barra normal
            if len(df_grouped) == 1:
                    fig.add_trace(go.Bar(
                    y=df_grouped['month'],
                    x=df_grouped['value'],
                    orientation='h',
                    marker=dict(color=color),
                    hovertext=[f"<b>Mês:</b> {mes}<br><b>Qntd. comprada:</b> {valor}<br>" for mes, valor in zip(df['month'], df['value'])],
                    hoverinfo='text',
                    width=0.4,
                    zorder=2
                ))
            else:
                fig.add_trace(go.Bar(
                    y=df_grouped['month'],
                    x=df_grouped['value'],
                    orientation='h',
                    marker=dict(color=color),
                    hovertext=[f"<b>Mês:</b> {mes}<br><b>Qntd. comprada:</b> {valor}<br>" for mes, valor in zip(df['month'], df['value'])],
                    hoverinfo='text',
                    zorder=2
                ))


            # Atualiza a cor para mais escura ao passar o mouse
            fig.update_traces(
                hoverlabel=dict(bgcolor=color_bg, font_color='black'),  # Cor de fundo do rótulo de hover
                selector=dict(type='bar')  # Seleciona apenas os traces de barra
            )

            fig.update_layout(
                paper_bgcolor='#f8f9fa',  # Define a cor do papel que fica no fundo
                plot_bgcolor=color_bg, #define a cor do fundo do grafico
                xaxis=dict(showgrid=True, range=[0, x_max], tickfont=dict(size=11)),  # Mostra a grade no eixo X
                yaxis=dict(showgrid=True, tickfont=dict(size=11)),
                margin=dict(l=0, r=0, t=30, b=0),  # margem
                #height=150,  # Define uma altura para o gráfico
                #width=380,
                title=dict(text=f"<b>Ultimos {crypto_name.capitalize()}s comprados<b>", 
                        font=dict(family="Montserrat", size=16), x=0.5) ,
            )

            return self.save_plot(filename=f"crypto_history_{user_id}_{crypto_id}.html", fig=fig)
        except:
            return None


    #Cria o gráfico do total gasto e quanto foi gasto em cada moeda
    def create_plot_spent(self, time, user_id):
        try:
            total_bitcoin = 0
            total_ethereum = 0

            data, data_1_month = self.data.get_total_spent(user_id, time)

            if data == False:
                return None
            
            # Limpa a data fazendo uma list comprehension, verificando se o valor é nulo ou não é um número
            cleaned_data = [(crypto_id, amount) for crypto_id, amount in data if not pd.isna(amount) and amount > 0]

            for crypto_id, amount in cleaned_data:
                if crypto_id == 1:  # Bitcoin
                    total_bitcoin += amount
                elif crypto_id == 2:  # Ethereum
                    total_ethereum += amount
                    
            # Cria uma lista com os valores a serem usados no gráfico
            labels = ['Bitcoin', 'Ethereum']
            values = [total_bitcoin, total_ethereum]
            
            fig = go.Figure()

            if time == '6':
                color_bg = 'rgba(255, 111, 60, 0.1)'  
                texto = 'Moedas compradas nos últimos 6 meses'
            elif time == 'all':
                color_bg = 'rgba(27, 38, 59, 0.1)'  
                texto = 'Moedas compradas ao todo'
                
            # Gráfico de pizza
            fig.add_trace(go.Pie(
                labels=labels,  # Rótulos
                values=values,                   # Valores
                pull=[0.1, 0],                  # "explode" o primeiro setor (Bitcoin)
                marker=dict(colors=['#ff7f0e', '#1f77b4']),  # Laranja para Bitcoin, Azul para Ethereum
                textinfo='label',  # Mostra rótulo, valor e porcentagem no gráfico
                hovertemplate='<b>Moeda:</b> %{label}<br><b>Total gasto:</b> $%{value:.2f} <br><b>Porcentagem:</b> %{percent:.1%}<extra></extra>',  # Formatação do hove
                hoverlabel=dict(bgcolor=color_bg),
            ))

            
            # Atualiza o layout
            fig.update_layout(
                paper_bgcolor='#f8f9fa',  # Cor do fundo
                plot_bgcolor=color_bg,     # Cor do fundo do gráfico
                margin=dict(l=0, r=20, t=30, b=0),  # Margens
                #height=350,  # Altura do gráfico
                #width=380,
                title=dict(text=f"<b>{texto}<b>", 
                        font=dict(family="Montserrat", size=16), x=0.5)
            )

            return self.save_plot(filename=f"total_spent_{user_id}_{time}.html", fig=fig), data_1_month
        except:
            return None