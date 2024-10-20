import os
from flask import Flask, render_template, request, redirect
import convolucao
import parameters as const

convolucao.novaImagem("")
#os.rename('img_in.png','static/images/img_in.png')
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
      return render_template('img_in.html', pixHoriz=const.pixHoriz)
    if request.method == 'POST':
      #Recebendo nova URL da imagem
      myurl = request.form['url']
      #Recebendo nova definição de tamanho do processamento
      try:
        mypixHoriz = int(request.form['pixHoriz'])
      except Exception as e:
        mypixHoriz = const.pixHoriz
      if  1 < mypixHoriz <= 30:
        const.pixHoriz = mypixHoriz
      else:
        mypixHoriz = const.pixHoriz
      
      #Reprocessa a imagem com estes novos parâmetros
      convolucao.novaImagem(myurl)
      mensagem_imagem = "Link é de uma imagem" if const.url_valida else "Link não é imagem"
      return render_template('img_in.html', url=myurl, pixHoriz=mypixHoriz, mensagem_imagem=mensagem_imagem)    

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))