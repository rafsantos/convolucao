import numpy as np

##################################################
# Ajustes no tamanho da imagem
fator = 70  # Tamanho de cada quadrado
pixHoriz = 10  # Numero de quadrados
fontsize = 24  # Tamanho da fonte

IMAGES_PATH = './static/images/'

##################################################
# Vou obter uma imagem da web
#url = ("https://i.ibb.co/D81PNZz/image.png")
url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzFVq9sCTckUxKmHj7YTLlKQH6nkicNS_UQ9XUdvdeLg&s"
url_valida = True

####################################################
filtro = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32) / 9.0