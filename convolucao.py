from urllib.request import urlopen

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
import parameters as const
import validators

###################################################
## Vou obter uma imagem da web
##url = ("https://i.ibb.co/D81PNZz/image.png")
#url = "https://encrypted-tbn0.gstatic.com/images?#q=tbn:ANd9GcSzFVq9sCTckUxKmHj7YTLlKQH6nkicNS_UQ9XUdvdeLg&s"
#url = 'https://live.staticflickr.com/4830/44200095760_4d993be1cb_b.jpg'

filtro = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32) / 9.0

#Verifica se a url é válida e é uma imagem
def url_eh_imagem(image_url):
  url_ok = True
  image_formats = ("image/png", "image/jpeg", "image/jpg")
  #Verifico se a URL é de uma imagem.
  try:
    response = requests.get(image_url)
    if response.headers["content-type"] in image_formats:
      const.url_valida = True
      return True
  except Exception as e:
    const.url_valida = False
    return False

# Função convolução
def convolve(image, filter):
  image = np.array(image)
  padding = (int(filter.shape[0] / 2), int(filter.shape[1] / 2))
  if (image.ndim == 2):
    image = np.expand_dims(image, axis=-1)
  if (filter.ndim == 2):
    filter = np.repeat(np.expand_dims(filter, axis=-1),
                       image.shape[-1],
                       axis=-1)
  if (filter.shape[-1] == 1):
    filter = np.repeat(filter, image.shape[-1], axis=-1)
  assert image.shape[-1] == filter.shape[-1]
  size_x, size_y = filter.shape[:2]
  width, height = image.shape[:2]
  padded_image = np.pad(image, [(padding[0], padding[0]),
                                (padding[1], padding[1]), (0, 0)],
                        mode='edge')
  output_array = image
  for x in range(padded_image.shape[0] - size_x + 1):
    for y in range(padded_image.shape[1] - size_y + 1):
      # Janela movel do filtro
      window = padded_image[x:x + size_x, y:y + size_y]
      # Soma do produto da janela fo filtro e área da imagem
      output_values = np.sum(filter * window, axis=(0, 1))
      # Guarda resultado no array resultado
      output_array[x, y] = np.asarray(output_values)

  if (output_array.shape[-1] == 1):
    output_array = output_array[:, :, 0]
  img = Image.fromarray(output_array.astype('uint8'))
  return img


#Desenha grade em uma imagem com um determinado intervalo
def desenhaGrade(img, intervalo):
  img = np.array(img)
  img[::intervalo] = 0
  img[:, ::intervalo] = 0
  img = Image.fromarray(img.astype('uint8'), 'L')
  return img


def leImagemWeb(url):
  im = Image.open(requests.get(url, stream=True).raw).convert('L')
  return im


#pixelando imagem
def ajustaVisual(img, pixH, fator):
  #compacta primeiro
  img = encolhe(img, pixH)
  img = img.resize((img.size[0] * fator, img.size[1] * fator),
                   resample=Image.NEAREST)
  return img


#Reduz imagem para quantidade de pixels na horizontal
def encolhe(img, pixH):
  img = img.resize((pixH, int(pixH * img.height / img.width)),
                   resample=Image.NEAREST)
  return img


# Escreve os pixels por cima da imagem ajustada a const.fator
def escrevePixels(img, fator):
  img = inverter(img) #inverte escala 0 - 255
  draw = ImageDraw.Draw(img)
  font = ImageFont.load_default()
  #font = ImageFont.truetype("Arial.ttf", const.fontsize)
  truetype_url = "https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-LightItalic.ttf"
  font = ImageFont.truetype(urlopen(truetype_url), fontsize)
  img_arr = np.transpose(np.array(img))
  for y in range(0, img_arr.shape[1], fator):
    for x in range(0, img_arr.shape[0], fator):
      txt = str((img_arr)[x, y])
      txtbox = font.getbbox(txt)
      #Alinhando o texto no centro do quadrado
      draw.text((x + fator / 2, y + fator / 2),
                txt,
                anchor='mm',
                font=font,
                stroke_width=1)
  return img


# Escreve os pixels por cima da imagem ajustada a const.fator
# Saida: imagem em branco com Pixels
def escrevePixelsSemImagem(img, fator):
  img_out = Image.new(mode="L", size=(img.size[0], img.size[1]), color=(255))
  draw = ImageDraw.Draw(img_out)
  font = ImageFont.load_default()
  #font = ImageFont.truetype("Arial.ttf", const.fontsize)
  truetype_url = "https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-LightItalic.ttf"
  font = ImageFont.truetype(urlopen(truetype_url), const.fontsize)
  img_arr = np.transpose(np.array(img))
  for y in range(0, img_arr.shape[1], fator):
    for x in range(0, img_arr.shape[0], fator):
      txt = str((img_arr)[x + round(fator / 2), y + round(fator / 2)])
      draw.text((x + fator / 2, y + fator / 2),
                txt,
                anchor='mm',
                font=font,
                stroke_width=1)
  return img_out


# Inverter a escala 0 - 255 para 255 - 0
def inverter(img):
  #img_arr = np.transpose(np.array(img))
  img_arr = np.array(img)
  img_arr = -img_arr + 255
  img = Image.fromarray(img_arr.astype('uint8'), 'L')
  return img

##### Funcoes #########
# Função convolução


def novaImagem(minhaUrl):
  if(minhaUrl == ""):
    minhaUrl = const.url
  img = leImagemWeb(minhaUrl) if url_eh_imagem(minhaUrl) else leImagemWeb(const.url) 

  img.save(const.IMAGES_PATH + "img_in.png")

  #Ajustando exibicao da imagem de entrada
  img_in = ajustaVisual(img, const.pixHoriz, const.fator)
  img_in = desenhaGrade(img_in, const.fator)
  img_in.save(const.IMAGES_PATH + "img_in_pix.png")

  #processando a imagem
  img = encolhe(img, const.pixHoriz)
  img_out = convolve(img, filtro)
  img_out = ajustaVisual(img_out, const.pixHoriz, const.fator)
  img_out.save(const.IMAGES_PATH +  "img_out.png")
 
  img_in_pix = escrevePixelsSemImagem(img_in, const.fator)
  img_in_pix = desenhaGrade(img_in_pix, const.fator)  
  img_in_pix.save(const.IMAGES_PATH + "img_in_pixVal.png")

  img_out_pix = escrevePixelsSemImagem(img_out, const.fator)
  img_out_pix = desenhaGrade(img_out_pix, const.fator)
  img_out_pix.save(const.IMAGES_PATH + "img_out_pixVal.png")
