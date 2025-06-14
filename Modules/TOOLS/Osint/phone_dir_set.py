import sys
import requests , bs4
from colorama import *
from terminaltables import SingleTable
from bs4 import BeautifulSoup
sys.path.append('Modules/TOOLS/Menu/OSINT')

def phone():
    number=input('Numbers : ')
    url=('https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui={}&univers=annuaireinverse&idOu=', 'https://www.118712.fr/', 'https://www.118712.fr/particuliers'.format(number))
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'referrer': 'https://google.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache'
    }
    request=requests.get(url,headers=headers)
    page=request.content
    soup=BeautifulSoup(page,'lxml')
    number=soup.find_all('div', {'class':'tel-zone noTrad'})
    name=soup.find_all('a',{'class':'denomination-links pj-lb pj-link'})
    address=soup.find_all('div',{'class':'adresse-container noTrad'})

    number2   = []
    name2     = []
    address2  = []
    if number is not None:
        for nnumber in number:
            number2.append(nnumber.text.strip())
    if name is not None:
        for nname in name:
            name2.append(nname.text.strip())
    if address is not None:
        for naddress in address:
            address2.append(naddress.text.strip())
    regroup = zip(number2,name2,address2)
    TABLE_DATA = [('Number(s)','Name(s)','Addresse(s)')]
    table = SingleTable(TABLE_DATA, title=f"{Fore.YELLOW}Numbers/Names/Adresses {Fore.RESET}")

    listeInfos = []

    for infos in regroup:
        try:
            TABLE_DATA.append(infos)
        except AttributeError:
            pass
    print("\r")
    print(table.table)


def phonedir_menu():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                             Phone Directory                                 ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
        [1] Reverse Phone Lookup
        [2] Phone Number Information (Carrier, Location)
        [3] Search for Phone Numbers by Name/Address

        [99] Back to Osint Menu
        ''')
    print('\r')
    try:
        choice = input(Fore.RED + "phone_dir" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            phone_num = input(Fore.CYAN + "  Enter phone number for reverse lookup: " + Style.RESET_ALL)
            print(f"  Performing reverse lookup for {phone_num}...")
            # Add your reverse phone lookup logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "2":
            phone_num = input(Fore.CYAN + "  Enter phone number for information: " + Style.RESET_ALL)
            print(f"  Retrieving info for {phone_num}...")
            # Add your phone info logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "3":
            name_addr = input(Fore.CYAN + "  Enter name/address to search for phone numbers: " + Style.RESET_ALL)
            print(f"  Searching for phone numbers related to {name_addr}...")
            # Add your phone number search by name/address logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "99":
            return main_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            phone()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()
