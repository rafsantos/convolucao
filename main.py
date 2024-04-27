import os

from flask import Flask, render_template, request

import convolucao as tcc

tcc.novaImagem("")
#os.rename('img_in.png','static/images/img_in.png')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    url = request.form['url']
    tcc.novaImagem(url)
    return render_template('img_in.html', url=url)    
  if request.method == 'GET':
    return render_template('img_in.html')
  else:
     return 'Hello from Flask!'

@app.route('/img_in', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    url = request.form['url']
    return render_template('img_in.html', url=url)    
  if request.method == 'GET':
    return render_template('img_in.html')
  else:
     return 'Hello from Flask!'

@app.route('/submit', methods=['GET','POST'])
def submit():  
  if request.method == 'POST':
    url = request.form['url']
    return render_template('img_in.html', url=url)  
  else:
    return " ola mundo "
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)