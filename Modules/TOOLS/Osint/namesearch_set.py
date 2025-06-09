
import sys  # To exit the script gracefully
import requests
from colorama import *
from terminaltables import SingleTable
from bs4 import BeautifulSoup

from Modules.TOOLS.Menu.osint_menu import osint_menu

sys.path.append('Modules/TOOLS/Menu/OSINT')

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

def name_search():
    Prénom=input('Prénom : ')
    Nom=input('Nom : ')
    localisation=input('Code Postal :')
    url=("https://www.118000.fr/search?label={}&who={}+{}".format(localisation,Prénom,Nom))
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
    adresse=soup.find_all('div',{'class':"h4 address mtreset"})
    phone=soup.find_all('a',{'class':"clickable atel"})
    name=soup.find_all('h2',{'class':"name title inbl"})

    name2     = []
    adresse2  = []
    phonee2   = []
    if name is not None:
        for nname in name:
            name2.append(nname.text.strip())
    if adresse is not None:
        for nadresse in adresse:
            adresse2.append(nadresse.text.strip())
    if phone is not None:
        for nphone in phone:
            phonee2.append(nphone.text.strip())
    regroup = zip(name2, adresse2,phonee2)
    TABLE_DATA = [('Name(s)','Address(es)','Number(s)')]
    table = SingleTable(TABLE_DATA, title=f"{Fore.YELLOW}Names/Addresses/Numbers {Fore.RESET}")

    listeInfos = []

    for infos in regroup:
        try:
            TABLE_DATA.append(infos)
        except AttributeError:
            pass
    print("\r")
    print(table.table)

def namesearch_menu():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                              Name Searching                                 ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Public Records
    [2] Social Media --OFF--
    [3] Professional Networks -- OFF --
    
    [C] Custom 
    
    [90] Save data
    [99] OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(
            Fore.RED + "name_search" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            print("  Performing Public Records Search...")
            # Add your public records search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "2":
            print("  Performing Social Media Search...")
            # Add your social media search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "3":
            print("  Performing Professional Networks Search...")
            # Add your professional networks search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "C":
            query = input(Fore.CYAN + "  Enter custom name search query: " + Style.RESET_ALL)
            print(f"  Searching for: {query}...")
            # Add your custom name search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "99":
            return osint_menu()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            name_search()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()

if __name__ == "__main__":
    # When this script is run directly, it will start the CAINE guidance menu.
    # To test: python caine_guidance.py
    print(Fore.GREEN + "Starting Andromeda Name Searching Menu..." + Style.RESET_ALL)
    namesearch_menu()
