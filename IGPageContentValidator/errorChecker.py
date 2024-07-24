# -*- coding: utf-8 -*-
""" 
This script checks webpages for any error messages and console logs (not including stack trace)
"""

from linkScraper import *
import re

def classErrors(warnings, soup):
    '''returns all class errors within the webpage'''
    class_errors = soup.find_all('div',{'class':"error"})
    if class_errors:
        for err in class_errors:
            warnings.append(err)
    return warnings

def consoleLog(warnings,soup):
    ''' finds all console.log items, then finds the text associated with it. expect 'console.log(<eror type>,<error var>)' & '<error var> = JSON.stringify(`<text>`). Retuns wanings as <error var><text> '''
    script_tags = soup.find_all('script')
    for script in script_tags:
        script_text = script.get_text()
        log_messages = re.findall(r'console\.log\((.*?)\)', script_text)
        for msg in log_messages:
            msg = (msg.replace("'", "").replace(' ', '').split(','))
            lines = script_text.splitlines()
            for line in lines:
                try:
                    if 'Stacktrace' not in msg[1] and 'var' not in line and 'console.log' not in line:
                        warnings.append(msg[0]+" "+line.split("`")[1].rsplit("`", 0)[0].replace(' At','\nAt'))
                except IndexError:
                    pass
    return(warnings)

def printWarnings(warnings, url):
    '''prints all warnings'''
    print(url)
    for x in warnings:
        print(x,"\n")
            
''' Interates over ListOfLinks returning any pages that have errors '''
def getSoup(url):
    data  = requests.get(url).text
    soup = BeautifulSoup(data,"html.parser")
    return soup
        
    
websites = ListOfLinks(data)
for suffix in websites:
    warnings = []
    soup = getSoup('https://simplifier.net'+ suffix)
    warnings = classErrors(warnings, soup)
    warnings = consoleLog(warnings,soup)
    if warnings:
        printWarnings(warnings, 'https://simplifier.net'+ suffix)
        
print("Check Complete")
