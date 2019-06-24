
from colorama import Fore, init
import gateway1, time, os


def CODECHECKER():
    banner = """
            print()
            print(Fore.YELLOW + "[*] " + Fore.RESET + "Starting Gateway 1...")
            print()
            print("""
        {re}             {g}_____________{re}
        {re}------------{g}|- {r}STRIPE GATEWAY 1 -{g}|{re}------------
        {re}---------------------------------------
        """.format(g=Fore.GREEN, r=Fore.RED, re=Fore.RESET))
            ranges = []
            try:
                with open('cc.txt', 'r') as ccs:
                    for x in ccs.read().split('\n'):
                        ranges.append(x)
                print(Fore.YELLOW + "[*] " + Fore.RESET + 'Checking ' + str(len(ranges)) + ' Credit Cards.')
                input(Fore.RESET + "PRESS ANY KEY TO CONTINUE")
                print(Fore.BLUE + "Start Checking at " + str(time.ctime()))
                print(Fore.RESET)
                
                cc = open('cc.txt', 'r')
                credit_cards = cc.read()
                ccEntry = 0

                if not os.path.exists("lives.txt"):
                    live = open("lives.txt", "w+")
                    live.write(" -- LIVES -- \n")
                    live.close()

                for x in credit_cards.split('\n'):
                    ccEntry += 1
                    try:
                        gateway1.StripeAutomate(x, ccEntry, 'Jason', "Anderson")
                    except KeyboardInterrupt:
                        break
            except KeyboardInterrupt:
                pass
            print()
            print(Fore.GREEN + "[+] " + Fore.RESET + "Done on Gateway 1")
            print()


CODECHECKER()
