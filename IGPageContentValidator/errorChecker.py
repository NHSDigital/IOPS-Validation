# -*- coding: utf-8 -*-
""" 
This script checks webpages for any error messages
"""

from linkScraper import *


''' Interates over ListOfLinks returning any pages that have errors '''
def FindErrors(url):
    websites = ListOfLinks(url)
    for e in websites:
        url_check = 'https://simplifier.net'+ e
        data_check  = requests.get(url_check).text
        soup_check = BeautifulSoup(data_check,"html.parser")
        error = soup_check.find_all('div',{'class':"error"})
        if error:
            print(url_check)
            for err in error:
                print(err)
            print("\n")
        script_tags = soup_check.find_all('script')
        ''' finds all console.log items, then finds the text associated with it. expect 'console.log(<eror type>,<error var>)' & '<error var> = JSON.stringify(`<text>`). Retuns <error var><text> '''
        for script in script_tags:
            script_text = script.get_text()
            log_messages = re.findall(r'console\.log\((.*?)\)', script_text)
            for msg in log_messages:
                msg = (msg.replace("'", "").replace(' ', '').split(','))
                try:
                    lines = script_text.splitlines()
                    for line in lines:
                        if msg[1] in line and 'var' not in line and 'console.log' not in line:
                            print(msg[0],line.split("`")[1].rsplit("`", 0)[0])
                except IndexError:
                    pass
    print("Check Complete")
    

FindErrors(data)
