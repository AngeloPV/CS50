from flask import Flask, render_template
from models.crypto_data import CryptoInfo

app = Flask(__name__)
USER_ID = 1
class My_Deposits:
    def __init__(self):
        self.data = CryptoInfo()

my_deposits = My_Deposits()

@app.route('/', methods=['GET', 'POST'])
def index():
    #pega todos os depositos e passa pra my_deposits.html
    data = my_deposits.data.get_deposit_history(user_id=USER_ID)
    return render_template('my_deposits.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)