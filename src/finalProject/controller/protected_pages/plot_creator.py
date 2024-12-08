import pandas as pd # type: ignore
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import sys, os
from flask import session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .get_crypto_data import GetCryptoData


class Plot_Creator:
    """
    Classe responsável por gerar os gráficos do dashboard
    """
    def __init__(self):
        self.data = GetCryptoData() #cria uma instancia responsavel pra pegar os dados das criptomoedas

    def clean_data(self, df):
        """
        Limpa o DataFrame removendo valores NaN e infinitos.

        Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados a serem limpos.

        Retorna:
        pd.DataFrame: DataFrame limpo, sem valores NaN ou infinitos.
        """
        df = df.replace([np.inf, -np.inf], np.nan)  
        df = df.dropna()  
        return df

    def save_plot(self, filename, fig):
        """
        Salva o gráfico como um arquivo HTML dinâmico na pasta 'static/images/dashboard'.

        Parâmetros:
        filename (str): Nome do arquivo onde o gráfico será salvo.
        fig (go.Figure): Figura do gráfico a ser salva.

        Retorna:
        str: Nome do arquivo salvo.
        """
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
        """
        Cria um gráfico de dispersão mostrando o valor da criptomoeda ao longo dos últimos 6 meses.

        Parâmetros:
        crypto_name (str): Nome da criptomoeda para a qual o gráfico será gerado.

        Retorna:
        str: Nome do arquivo HTML do gráfico salvo, ou None em caso de erro.
        """
        try:
            def format_price(value):
                return f"{int(value):,}".replace(",", " ") + f"{value:.2f}"[-3:]

            # adiciona todos os dados em data
            data = {
                'Period': ['6 Months', '5 Months', '4 Months', '3 Months', 
                        '2 Months', '1 Month', '7 Days', '1 Day', 'Now'],
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
            # cria o dataframe
            df = pd.DataFrame(data)
            df['Formatted Price'] = df['Price'].apply(format_price)  # Adiciona uma coluna com os preços formatados
            
            # cria o grafico com plotly
            fig = go.Figure()

            # Define as cores conforme o tema
            if session.get('theme') == 'dark-theme':
                text_color = '#f8f9fa'
                grid_color = 'rgba(255, 255, 255, 0.1)'

            if session.get('theme') == 'light-theme':
                text_color = '#24292e'  # Cor do texto para o tema claro
                grid_color = '#f8f9fa'

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
                text=df['Formatted Price'],
                line=dict(color=color_hex, width=3, shape='spline'),  # cria a linha
                fill='tozeroy', # cria o preenchimento
                fillcolor=f'rgba({color}, 0.2)',
                hovertemplate='<b>%{x} ago</b><br>$%{text}<extra></extra>', 
                #<extra></extra> remove qualquer informação extra que aparece abaixo dos dados no hover
                name='',  # Remove o nome da série do hover
            ))

            # monta o layout do grafico
            fig.update_layout(
                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                plot_bgcolor=f'rgba({color}, 0.1)', # define a cor do fundo do grafico
                yaxis=dict(
                    tickprefix='$', 
                    ticksuffix='  ', 
                    showgrid=True, 
                    tickfont=dict(color=text_color),
                    gridcolor=grid_color,  # Malha transparente
                    range=[y_min, y_max], 
                    automargin=True,
                ),  
                xaxis=dict(
                    showgrid=True, 
                    tickfont=dict(color=text_color),
                    ticklabelposition="inside",
                    gridcolor=grid_color,  # Malha transparente
                ),  # config do eixo x
                hovermode='x unified',  # efeito de hover
                margin=dict(l=0, r=0, t=40, b=10),  # margem
                title=dict(
                    text=f"<b>Price of {crypto_name.capitalize()} over time</b>", # título do gráfico
                    font=dict(family="Montserrat", size=16, color=text_color),  # aplica a cor do texto aqui
                    x=0.5
                ),  
                hoverlabel=dict(
                bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente para o hover
                font=dict(color=text_color)  # Cor do texto do hover
            )
            )

            # salva o grafico se tudo correr bem
            return self.save_plot(filename=f"{crypto_name}_plot.html", fig=fig)
        except:
            return None


    def create_plot_history(self, crypto_name, user_id):
        """
        Cria um gráfico de barras horizontais com as moedas compradas nos ultimos 3 meses

        Parametros:
            crypto_name (str): Nome da criptomoeda
            user_id (int): Id do usuário

        Retorna:
            str: Nome do arquivo HTML do gráfico salvo, ou None em caso de erro
        """
        try:
            color = ''
            # Define o id da criptomoeda
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
            if session.get('theme') == 'dark-theme':
                text_color = '#f8f9fa'
                grid_color = 'rgba(255, 255, 255, 0.1)'

            if session.get('theme') == 'light-theme':
                text_color = '#24292e'  # Cor do texto para o tema claro
                grid_color = '#f8f9fa'

            if crypto_name == 'bitcoin':
                color_bg = 'rgba(255, 111, 60, 0.1)'  # Opacidade 70%
                color = '#FF6F3C'

            elif crypto_name == 'ethereum':
                color_bg = 'rgba(27, 38, 59, 0.1)'  # Opacidade 70%
                color = '#1B263B'

            # Se só tiver 1 dado, gerá um gráfico diferente
            if len(df_grouped) == 1:
                    fig.add_trace(go.Bar(
                    y=df_grouped['month'],
                    x=df_grouped['value'],
                    orientation='h',
                    marker=dict(color=color, line=dict(width=0)),
                    width=0.4,
                    zorder=2,
                    hovertemplate='<b>Month:</b> %{y}<br><b>Amnt. purchased:</b> %{x:.10f}<extra></extra>',  # Formatação do hover
                    hoverlabel=dict(bgcolor=color_bg) 
            
                   
                ))
            #Se tiver mais de 1 dado gera o gráfico padrão
            else:
                fig.add_trace(go.Bar(
                    y=df_grouped['month'],
                    x=df_grouped['value'],
                    orientation='h',
                    marker=dict(color=color, line=dict(width=0)),
                    zorder=2,
                    hovertemplate='<b>Month:</b> %{y}<br><b>Amnt. purchased:</b> %{x:.10f}<extra></extra>',  # Formatação do hover
                    hoverlabel=dict(bgcolor=color_bg)  # Fundo transparente para o hover,

            
                ))


            # Atualiza a cor para mais escura ao passar o mouse
            fig.update_traces(
                hoverlabel=dict(bgcolor=color_bg, font_color='black'),  # Cor de fundo do rótulo de hover
                selector=dict(type='bar')  # Seleciona apenas os traces de barra
            )

            fig.update_layout(
                paper_bgcolor='rgba(0, 0, 0, 0)',  # Define a cor do papel que fica no fundo
                plot_bgcolor=color_bg, #define a cor do fundo do grafico
                xaxis=dict(showgrid=True, range=[0, x_max], tickfont=dict(size=11, color=text_color),
                            gridcolor=grid_color,
                            zerolinecolor='rgba(0, 0, 0, 0)'
                            ),  # Mostra a grade no eixo X
                yaxis=dict(ticksuffix=' ',showgrid=True, tickfont=dict(size=11, color=text_color),
                            gridcolor=grid_color,),
                margin=dict(l=0, r=0, t=30, b=0),
                #height=150,  # Define uma altura para o gráfico
                #width=380,
                title=dict(text=f"<b>Last {crypto_name.capitalize()} purchased<b>", 
                        font=dict(family="Montserrat", size=16, color=text_color), x=0.5) ,
            
            )           

            return self.save_plot(filename=f"crypto_history_{user_id}_{crypto_id}.html", fig=fig)
        except:
            return None


    #Cria o gráfico do total gasto e quanto foi gasto em cada moeda
    def create_plot_spent(self, time, user_id):
        """
        Cria um gráfico de pizza do total gasto e quanto foi gasto em cada moeda

        Parâmetros:
            time (str): Tempo para o gráfico (6 ou 1 mês)
            user_id (int): Id do User

        Retorno:
            str: Nome do arquivo salvo ou None caso não seja possivel criar o gráfico
        """
        try:
            #começa com 0 por padrão
            total_bitcoin = 0
            total_ethereum = 0

            #pega o tanto que o usuario gastou
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

            #define as cores com base no tema
            if session.get('theme') == 'dark-theme':
                text_color = '#f8f9fa'
                grid_color = 'rgba(255, 255, 255, 0.1)'

            if session.get('theme') == 'light-theme':
                text_color = '#24292e'  # Cor do texto para o tema claro
                grid_color = '#f8f9fa'

            #define as cores com base no tempo, 6 meses ou ao todo
            if time == '6':
                color_bg = 'rgba(255, 111, 60, 0.1)'  
                texto = 'Currencies purchased in the last 6 months'
            elif time == 'all':
                color_bg = 'rgba(27, 38, 59, 0.1)'  
                texto = 'Currencies purchased in total'
                
            # Gera o gráfico de pizza
            fig.add_trace(go.Pie(
                labels=labels,  # Rótulos
                values=values,                   # Valores
                pull=[0.1, 0],                  # "explode" o primeiro setor (Bitcoin)
                marker=dict(colors=['#ff7f0e', '#1f77b4'],),  # Laranja para Bitcoin, Azul para Ethereum
                textinfo='label',  # Mostra rótulo, valor e porcentagem no gráfico
                hovertemplate='<b>Currency:</b> %{label}<br><b>Total spent:</b> $%{value:.2f} <br><b>Percentage:</b> %{percent:.1%}<extra></extra>',  # Formatação do hove
                hoverlabel=dict(bgcolor=color_bg),  # Fundo transparente para o hover,
                textfont=dict(color=text_color)))

            
            # Atualiza o layout
            fig.update_layout(
                paper_bgcolor='rgb(0, 0, 0, 0)',  # Cor do fundo
                plot_bgcolor=color_bg,     # Cor do fundo do gráfico
                margin=dict(l=0, r=20, t=30, b=0),  # Margens
                #height=350,  # Altura do gráfico
                #width=380,
                title=dict(text=f"<b>{texto}<b>", 
                        font=dict(family="Montserrat", size=16, color=text_color), x=0.5),
                                    showlegend=False  # Remove a legenda

            )

            return self.save_plot(filename=f"total_spent_{user_id}_{time}.html", fig=fig), data_1_month
        except:
            return None