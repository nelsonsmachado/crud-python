import sys
import os
from utils import inicia_api
# Adicione o diretório pai ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
   inicia_api()
   
   
if __name__ == '__main__':
    main()