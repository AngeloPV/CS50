from datetime import datetime
import calendar
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..helper.helper_select import Select
from ..helper.helper_insert import Insert
from ..helper.helper_update import Update 

from models.db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py

class Dashboard_data:
    """
    Classe responsável por coletar e processar informações relacionadas ao painel de dados de um usuário,
    como compras de criptomoedas, gastos totais e transações recentes.
    """
    def __init__(self):
        self.connection = Conn().connect() #instacia a classe responsavel pela conexão e inicia a conexão com o banco
        self.insert = Insert() #cria uma instancia responsavel pra inserir dados no banco
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.update = Update() #cria uma instancia responsavel pra atualizar dados do banco
        
    def get_crypto_buy(self, crypto_id, user_id):
        """
        Recupera os dados de compras de criptomoedas do usuário dos ultimos 3 meses, pegando o total recuperado
        em vendas de moedas e subtraindo dos gastos em compras

        Parametros:
            crypto_id (int): ID da criptomoeda
            user_id (int): ID do usuário

        Retorno:
            tuple: Tupla contendo varias tuplas onde em cada tupla tem a quantidade resultante de compras
            e vendas do mes, e um datetime com o mes e o ano (o dia, hora, minuto e segundo sao irrelevantes,
            é usado apenas um valor aleatorio pois a verificação é feita com base no mes e no ano somente)
        """
        cursor = self.connection.cursor()

        #pega o mes e o ano
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        #pega o mes inicial e o ano inicial
        start_month = current_month - 2
        start_year = current_year
        if start_month <= 0:
            start_month += 12
            start_year -= 1

        query = """
        SELECT amount, created 
        FROM buy 
        WHERE criptocurrencies_id = %s 
        AND user_id = %s 
        AND DATE_FORMAT(created, '%%Y-%%m') BETWEEN %s AND %s
        """

        #pega os valores do 3° mes
        start_date_str = f"{start_year}-{start_month:02d}"
        end_date_str = f"{current_year}-{current_month:02d}"

        #executa a query
        cursor.execute(query, (crypto_id, user_id, start_date_str, end_date_str))
        
        data_buy = cursor.fetchall()


        query = """
        SELECT amount, created
        from sell
        WHERE criptocurrencies_id = %s
        AND user_id = %s
        AND DATE_FORMAT(created, '%%Y-%%m') BETWEEN %s AND %s
        """

        cursor.execute(query, (crypto_id, user_id, start_date_str, end_date_str))
        
        data_sell = cursor.fetchall()
        cursor.close()


        # Loop para comparar as datas de compra e venda
        buy_dict = {}  # Dicionário para armazenar o total de buy por mês
        for amount, created in data_buy:
            buy_month = created.month
            if buy_month not in buy_dict:
                buy_dict[buy_month] = 0
            buy_dict[buy_month] += amount

        sell_dict = {}  # Dicionário para armazenar o total de sell por mês
        for amount, created in data_sell:
            sell_month = created.month
            if sell_month not in sell_dict:
                sell_dict[sell_month] = 0
            sell_dict[sell_month] += amount

        result_data = ()
        # Agora vamos comparar as compras e vendas
        for month in range(start_month, current_month + 1):
            buy_amount = buy_dict.get(month, 0)
            sell_amount = sell_dict.get(month, 0)

            # Subtrair o valor de sell do buy
            result_amount = buy_amount - sell_amount
            result_amount = max(round(result_amount, 10), 0) #arredonda e retira o negativo

            
            # Cria a datetime
            date = datetime(current_year if month >= current_month else start_year, month, 5, 5, 5, 5)

            result_tmp = (result_amount, date)
            result_data += (result_tmp,)


        return result_data
            
    def get_total_spent(self, time, user_id=1):
        """
        Recupera o total gasto pelo usuario, podendo ser do mes atual, dos ultimos 6 meses ou ao todo.
        No entanto, caso o usuario venda alguma criptomoeda, será descontado do total comprado

        Parametros:
            time (str): Mes atual, ultimos 6 meses ou ao todo
            user_id (int): ID do usuário

        Retorno:
            tuple, float: Retorna uma tupla com outras tuplas, onde em cada tupla vai ter (id da moeda, 
            quantidade total gasta no mes) e um float com o total gasto do mes
        """
        cursor = self.connection.cursor()

        now = datetime.now()
        current_year = now.year
        current_month = now.month

        #pega o mes inicial e o ano inicial
        start_date = f"{current_year}-{current_month:02d}-01"
        end_date = f"{current_year}-{current_month:02d}-{calendar.monthrange(current_year, current_month)[1]}"


        #pega o tanto gasto no mes atual e armazena na variavel spent_month
        query = """
        SELECT criptocurrencies_id, SUM(cost) as total_cost
        FROM buy
        WHERE user_id = %s
        AND created BETWEEN %s AND %s
        GROUP BY criptocurrencies_id
        """
        cursor.execute(query, (user_id, start_date, end_date))
        spent_month = cursor.fetchall()

        query = """
        SELECT criptocurrencies_id, SUM(value) 
        FROM sell
        WHERE user_id = %s
        AND created BETWEEN %s AND %s
        GROUP BY criptocurrencies_id
        """
        cursor.execute(query, (user_id, start_date, end_date))
        spent_month_sell = cursor.fetchall()

        # Inicializar os valores com 0 para evitar problemas
        spent_month_all = spent_month[0][1] if spent_month else 0
        spent_month_sell_all = spent_month_sell[0][1] if spent_month_sell else 0

        # Se o usuario tiver  comprado bitcoin e ethereum no mesmo mes
        if len(spent_month) > 1:
            spent_month_all += spent_month[1][1]

        # Se o usuario tiver vendido bitcoin e ethereum no mesmo mes
        if len(spent_month_sell) > 1:
            spent_month_sell_all += spent_month_sell[1][1]

        # Calcular o total
        spent_month_total = spent_month_all - spent_month_sell_all
        spent_month_total = max(round(spent_month_total, 2), 0)
      

        #se a entrada for 6 pega o valor dos ultimos 6 meses

        if time == '6':
            start_month = current_month - 5
            start_year = current_year
            if start_month <= 0:
                start_month += 12
                start_year -= 1

            last_day_current_month = calendar.monthrange(current_year, current_month)[1]

            start_date = f"{start_year}-{start_month:02d}-01"
            end_date = f"{current_year}-{current_month:02d}-{last_day_current_month}"

            # Consultas para os últimos 6 meses
            query = """
            SELECT criptocurrencies_id, SUM(cost) as total_cost
            FROM buy
            WHERE user_id = %s
            AND created BETWEEN %s AND %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id, start_date, end_date))
            spent_data_6 = cursor.fetchall()

            query = """
            SELECT criptocurrencies_id, SUM(value) 
            FROM sell
            WHERE user_id = %s
            AND created BETWEEN %s AND %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id, start_date, end_date))
            sell_data_6 = cursor.fetchall()

        elif time == 'all':
            # Consultas para todos os períodos
            query = """
            SELECT criptocurrencies_id, SUM(cost) as total_cost
            FROM buy
            WHERE user_id = %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id,))
            spent_data_all = cursor.fetchall()

            query = """
            SELECT criptocurrencies_id, SUM(value) 
            FROM sell
            WHERE user_id = %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id,))
            sell_data_all = cursor.fetchall()

        # Fechar o cursor
        cursor.close()

        # Processar os dados com base no tempo selecionado ( se foi 6 meses ou ao todo)
        if time == '6':
            spent_data = spent_data_6
            sell_data = sell_data_6
        elif time == 'all':
            spent_data = spent_data_all
            sell_data = sell_data_all

        # Inicializar variáveis
        spent_data_eth = 0
        sell_data_eth = 0

        # Calcula valores de Bitcoin
        spent_data_btc = spent_data[0][1] if spent_data else 0
        sell_data_btc = sell_data[0][1] if sell_data else 0

        # Verificar se o usuário comprou Ethereum
        if len(spent_data) > 1:
            spent_data_eth = spent_data[1][1]

        # Verifica se o usuário vendeu Ethereum
        if len(sell_data) > 1:
            sell_data_eth = sell_data[1][1]

        # Calcular o total de Bitcoins (comprados e vendidos)
        spent_total_btc = max(round(spent_data_btc - sell_data_btc, 2), 0)

        # Calcular o total de Ethereums (comprados e vendidos)
        spent_total_eth = max(round(spent_data_eth - sell_data_eth, 2), 0)

        # Consoliar os dados totais
        spent_total_data = ((1, spent_total_btc), (2, spent_total_eth))


        # Se nao tiver dados retorna falso
        if not spent_total_data:
            return False
        
        print('spent_total_data',spent_total_data)
        print('spent_month_total',spent_month_total)
        # Se tiver retorna os dados do mes atual e o total ou os 6 ultimos meses
        return spent_total_data, spent_month_total
    
    def get_last_buy_date(self, user_id):
        """
        Pega a data da ultima compra do usuario

        Parametros:
            user_id (int): ID do usuário

        Retorno:
            str: Data da ultima compra
        """
        cursor = self.connection.cursor()

        query = """SELECT created FROM buy WHERE user_id = %s ORDER BY id DESC LIMIT 1;"""
        cursor.execute(query, (user_id,))
        
        last_buy_date_row = cursor.fetchone()
        cursor.close()

        #formata a data pra ficar no modelo y/m/d
        if last_buy_date_row:
            last_buy_date = last_buy_date_row[0]
            formatted_date = last_buy_date.strftime('%Y-%m-%d')
        else:
            formatted_date = ''

        return formatted_date
    
        
    def get_last_trade(self, user_id):
        """
        Recupera as informações da ultima troca realizada pelo usuario, como a criptomoeda enviada, 
        a criptomoeda recebida, a quantidade enviada e a quantidade recebida e a data da troca

        Parametros:
            user_id (int): ID do usuário

        Retorno:
            tuple: Dados da ultima troca

        """
        cursor = self.connection.cursor()

        query = """SELECT cripto_sender_id, cripto_recipient_id, amount_sender, amount_recipient, created 
                FROM trades 
                WHERE user_sender_id = %s OR user_recipient_id = %s 
                ORDER BY id DESC 
                LIMIT 1;"""
        cursor.execute(query, (user_id, user_id))
        
        data = cursor.fetchall()
        cursor.close()

        return data

   

    