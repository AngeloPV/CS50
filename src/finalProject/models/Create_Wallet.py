from web3 import Web3
from bit import PrivateKeyTestnet
import os
from flask import session

from ..helper.helper_insert import Insert

class Create_Wallet:
    def __init__(self):
        self.insert_wallet = Insert()
        self.eth = {}
        self.btc = {}

    def create_eth_wallet(self):
        # Gera uma chave privada Ethereum aleatória
        eth_account = Web3().eth.account.create()
        self.eth['user_id'] = session['user_id']
        self.eth['currency'] = 'ETH'
        self.eth['public_key'] = eth_account.address
        self.eth['private_key'] = eth_account._private_key.hex()  # Chave privada Ethereum (fictícia)

        self.insert_wallet.exe_insert(self.eth, 'wallets', None, False)
        result = self.insert_wallet.getResult()

        if result:
            return True
            
        return False

    # Gerar uma carteira Bitcoin fictícia
    def create_btc_wallet(self):
        btc_wallet = PrivateKeyTestnet()  # Gera uma chave privada BTC na testnet
        self.btc['user_id'] = session['user_id']
        self.btc['currency'] = 'BTC'
        self.btc['public_key'] = btc_wallet.address  # Endereço Bitcoin gerado
        self.btc['private_key'] = btc_wallet.to_wif()  # Chave privada BTC no formato WIF
        
        self.insert_wallet.exe_insert(self.btc, 'wallets', None, True)
    
        result = self.insert_wallet.getResult()

        if result:
            return True
            
        return False

