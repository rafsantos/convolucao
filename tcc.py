from urllib.request import urlopen

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

##################################################
# Ajustes no tamanho da imagem
fator = 70  # Tamanho de cada quadrado
pixHoriz = 15  # Numero de quadrados
fontsize = 24  # Tamanho da fonte

##################################################
# Vou obter uma imagem da web
#url = ("https://i.ibb.co/D81PNZz/image.png")
url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzFVq9sCTckUxKmHj7YTLlKQH6nkicNS_UQ9XUdvdeLg&s"
#url = 'https://live.staticflickr.com/4830/44200095760_4d993be1cb_b.jpg'

filtro = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32) / 9.0


# Função convolução
def convolve(image, filter):
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
  #Para fazer a animacao vou armazenar os frames em uma lista
  frames = []
  # So vou pegar 30 imagens de todo o processo
  keyFrame = int(image.shape[0] * image.shape[1] / 30)
  count = 0
  for x in range(padded_image.shape[0] - size_x + 1):
    for y in range(padded_image.shape[1] - size_y + 1):
      # Janela movel do filtro
      window = padded_image[x:x + size_x, y:y + size_y]
      # Soma do produto da janela fo filtro e área da imagem
      output_values = np.sum(filter * window, axis=(0, 1))
      # Guarda resultado no array resultado
      output_array[x, y] = np.asarray(output_values)

      # Se for um frame para animacao, vou guardar
      if (count) % keyFrame == 0:
        if (output_array.shape[-1] == 1):
          output_array = output_array[:, :, 0]
        img = Image.fromarray(output_array.astype('uint8'))
        frames.append(img)
      count += 1
  if (output_array.shape[-1] == 1):
    output_array = output_array[:, :, 0]
  img = Image.fromarray(output_array.astype('uint8'))
  return output_array, frames


#Desenha grade em uma imagem com um determinado intervalo
def grade(img, intervalo):
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


# Escreve os pixels por cima da imagem ajustada a fator
def escrevePixels(img, fator):
  draw = ImageDraw.Draw(img)
  font = ImageFont.load_default()
  #font = ImageFont.truetype("Arial.ttf", fontsize)
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


# Escreve os pixels por cima da imagem ajustada a fator
# Saida: imagem em branco com Pixels
def escrevePixelsSemImagem(img, fator):
  img_out = Image.new(mode="L", size=(img.size[0], img.size[1]), color=(255))
  draw = ImageDraw.Draw(img_out)
  font = ImageFont.load_default()
  #font = ImageFont.truetype("Arial.ttf", fontsize)
  truetype_url = "https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-LightItalic.ttf"
  font = ImageFont.truetype(urlopen(truetype_url), fontsize)
  img_arr = np.transpose(np.array(img))
  for y in range(0, img_arr.shape[1], fator):
    for x in range(0, img_arr.shape[0], fator):
      txt = str((img_arr)[x + round(fator / 2), y + round(fator / 2)])
      txtbox = font.getbbox(txt)
      #Alinhando o texto no centro do quadrado
      #draw.text((x + fator/2 - txtbox[2]/2, y + fator/2 - txtbox[3]/2 ), txt, anchor='mm', font = font)
      draw.text((x + fator / 2, y + fator / 2),
                txt,
                anchor='mm',
                font=font,
                stroke_width=1)
  return img_out


def animacaoGIF(frames_arr, fator):
  #Os frames sao uma lista de imagens de cada frae da animacao
  #Preciso ampliar cada um primeiro
  frames_out = []
  for frame in frames:
    #Para cada frame, vou ampliar e gravar na lista de saida
    frame = frame.resize((frame.size[0] * fator, frame.size[1] * fator),
                         resample=Image.NEAREST)
    #display(frame)
    frames_out.append(frame)
  return frames_out


# Inverter a escala 0 - 255 para 255 - 0
def inverter(img):
  #img_arr = np.transpose(np.array(img))
  img_arr = np.array(img)
  img_arr = -img_arr + 255
  img = Image.fromarray(img_arr.astype('uint8'), 'L')
  return img


def convolucao(image, filter):
  return image


##### Funcoes #########
# Função convolução


def novaImagem(minhaUrl):
  img = leImagemWeb(url) if minhaUrl == "" else leImagemWeb(minhaUrl)
  img.save("img_in.png", "PNG")

  #Ajustando exibicao da imagem de entrada
  img_in = ajustaVisual(img, pixHoriz, fator)
  img_pix = grade(img_in, fator)
  img_pix.save("img_pix.png", "PNG")

  #processando a imagem
  img = encolhe(img, pixHoriz)
  img_arr = np.array(img)
  img_arr, frames = convolve(img_arr, filtro)
  img_conv = Image.fromarray(img_arr.astype('uint8'))
  img_conv = ajustaVisual(img_conv, pixHoriz, fator)
  img_pix.save("img_pix.png", "PNG")

  #escrevendo os valores de cada pixel
  #img = escrevePixels(img,fator)

  #Desenha grade
  img_conv = grade(img_conv, fator)
  img_conv.save("img_conv.png", "PNG")

  #display(img_conv)

  frames = animacaoGIF(frames, fator)
  frames[0].save('saida.gif',
                 format='GIF',
                 append_images=frames[1:],
                 save_all=True,
                 duration=100,
                 loop=0)

  ##############################################
  #Imagem invertida.
  img_inv = inverter(img_in)
  #img_inv = escrevePixels(img_inv,fator)
  img_inv = escrevePixelsSemImagem(img_inv, fator)
  img_inv = grade(img_inv, fator)
  print('')
  #display(img_inv)
  img_inv.save("img_inv.png", "PNG")

  img_conv_inv = inverter(img_conv)
  img_conv_inv = escrevePixelsSemImagem(img_conv_inv, fator)
  img_conv_inv = grade(img_conv_inv, fator)
  print('')
  #display(img_conv_inv)
  img_conv_inv.save("img_conv_inv.png", "PNG")
