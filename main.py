import EForcer
import os
import time
from colorama import Fore
import argparse
import Utils

logo = r"""

 ██ ▄█▀ ██▓ ███▄    █  ▒█████    ██████  ██░ ██  ██▓    ▄▄▄       ███▄    █  ▒█████   ██▀███  ▄▄▄█████▓ ██░ ██ ▓█████ 
 ██▄█▒ ▓██▒ ██ ▀█   █ ▒██▒  ██▒▒██    ▒ ▓██░ ██▒▓██▒   ▒████▄     ██ ▀█   █ ▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒▓██░ ██▒▓█   ▀ 
▓███▄░ ▒██▒▓██  ▀█ ██▒▒██░  ██▒░ ▓██▄   ▒██▀▀██░▒██▒   ▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░▒██▀▀██░▒███   
▓██ █▄ ░██░▓██▒  ▐▌██▒▒██   ██░  ▒   ██▒░▓█ ░██ ░██░   ░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ 
▒██▒ █▄░██░▒██░   ▓██░░ ████▓▒░▒██████▒▒░▓█▒░██▓░██░    ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░ ░▓█▒░██▓░▒████▒
▒ ▒▒ ▓▒░▓  ░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓      ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░
░ ░▒ ▒░ ▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░     ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░    ░     ▒ ░▒░ ░ ░ ░  ░
░ ░░ ░  ▒ ░   ░   ░ ░ ░ ░ ░ ▒  ░  ░  ░   ░  ░░ ░ ▒ ░     ░   ▒      ░   ░ ░ ░ ░ ░ ▒    ░░   ░   ░       ░  ░░ ░   ░   
░  ░    ░           ░     ░ ░        ░   ░  ░  ░ ░           ░  ░         ░     ░ ░     ░               ░  ░  ░   ░  ░
                                                                                                                                                                                                                                                                                         
"""

import argparse

parser = argparse.ArgumentParser(prog="eokulbruteforce", description="Eokul bruteforce gerçekleştirmek için gerekli bilgiler.", epilog="-t tckn -d dogumgünü -m dogumayı -y dogumyili\nGün sayı olarak\nAy ay ismiyle\nYıl sayı olarak GİRİLMELİDİR!")
parser.add_argument("-t", "--tckn", required=True, type=int)
parser.add_argument("-d", "--day", required=True, type=int)
parser.add_argument("-m", "--month", required=True, type=str)
parser.add_argument("-y", "--year", required=True, type=int)
args = parser.parse_args()

# start program
def main():
    os.system("cls||clear")
    print(Fore.RED + logo + Fore.RESET)
    time.sleep(3)
    print(Fore.RESET)
    EForcer.runner(args.tckn, args.day, args.month, args.year)

# run program
if __name__ == "__main__":
    main()
