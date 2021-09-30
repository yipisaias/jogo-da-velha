# jogo-da-velha

Jogo da velha em rede feito em Python, utilizando protocolo TCP e arquitetura híbrida.

Baseado em: https://pt.stackoverflow.com/questions/168060/sockets-jogo-da-velha-jogo-do-galo-multiplayer <br/>
e em: https://www.pythonprogressivo.net/2018/10/Como-Criar-Jogo-Velha-Python.html

## Quick-Start
Instale os requisitos (dependências):

```
  pip install -r requirements.txt
```
Após isso, reiniciar a IDE caso esteja aberta.

Para gerar arquivos executáveis, use os comandos:
```
  pyinstaller .\servidor.py
```
```
  pyinstaller .\cliente.py
```
Os executáveis são gerados dentro da pasta **dist**.<br/>
Para mais informações, consulte o site do [PyInstaller](http://www.pyinstaller.org/).

## Executando diretamente pelo prompt/terminal

```
  python .\servidor.py
```
```
  python .\cliente.py
```
