# jogo-da-velha

Jogo da velha em rede feito em Python, utilizando protocolo TCP e arquitetura híbrida.

Baseado em: https://pt.stackoverflow.com/questions/168060/sockets-jogo-da-velha-jogo-do-galo-multiplayer <br/>
e em: https://www.pythonprogressivo.net/2018/10/Como-Criar-Jogo-Velha-Python.html

## Requisitos
* python3
* [pip](https://pip.pypa.io/en/stable/installation/)

## Quick-Start
```
  pip install -r requirements.txt
```
Após isso, reiniciar a IDE caso esteja aberta.

Para gerar arquivos executáveis, use os comandos:
```
  pyinstaller servidor.py
```
```
  pyinstaller cliente.py
```
Os executáveis são gerados dentro da pasta **dist**.<br/>
Para mais informações, consulte o site do [PyInstaller](http://www.pyinstaller.org/).

## Executando diretamente pelo prompt/terminal

```
  python servidor.py
```
```
  python cliente.py
```

## Vídeo sobre o trabalho
Clique na imagem abaixo para assistir o vídeo.

[![Vídeo do jogo](https://img.youtube.com/vi/MqAX5lmx3T8/maxresdefault.jpg)](https://youtu.be/MqAX5lmx3T8)
