import sys
import requests
import json
import psycopg2
from psycopg2.extensions import AsIs
import time
from datetime import datetime
from simpleParser import getAVantageKeys

keychoice = True

def get_company_info(secret1, secret2, symbol):
    """

    scrapes data (currently from alphavantage) and returns the response in json format

    Arguments:
        secret1: one of the API keys to scrape data
        secret2: a second API key to scrape data
        symbol: synonymous to ticker

    Returns:
        company stock data in json format

    """
    global keychoice
    key = ""
    if(keychoice == True):
        key = secret1
        keychoice = False
    else:
        key = secret2
        keychoice = True
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ symbol + "&apikey=" + key +"&datatype=json"
    response = json.loads(requests.get(url).text)
    return response

def connect():
    """
    
    primary method to connect to the database and create cursor


    """

    """ Connect to the PostgreSQL database server """
    conn = None
    try:
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host='206.189.181.163',
                            database="rcos",
                                user="rcos",
                            password="hedgehogs_rcos")
 
        # create a cursor
        cur = conn.cursor()
        conn.autocommit = True
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        #Send cursor over to read_input to process tickers
        read_input(cur)

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        if(error == 'Time Series (Daily)'):
            connect()
        else:
            print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def read_input(cur):
    """
        
    parses json data and places it into the appropriate table in the database

    Argument:
        cur: cursor object for the database


    """
    lines = [line.rstrip('\n') for line in open('companies.txt')]
    AVantageKeys = getAVantageKeys()
    secret1 = AVantageKeys[0]
    secret2 = AVantageKeys[1]
    for symbol in lines:
        data = get_company_info(secret1, secret2, symbol)
        dates = []
        for entry in data['Time Series (Daily)']:
            dates.append(entry)
        #sort by date
        dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
        #SQL command setup to create table
        #temp = ("CREATE TABLE %s(date TIMESTAMP, low double precision, high double precision, volume double precision, close double precision, open double precision);" % symbol)
        #execute SQL cmd, with symbol replacing %s
        #cur.execute(temp)
        #print("HERE")
        for date in dates:
            insert = ("INSERT INTO stockData.{}(date,open,high,low,close,volume) VALUES ({}, {}, {}, {}, {}, {})"
            .format(symbol, date, 
                        data['Time Series (Daily)'][str(date)]['3. open'],
                        data['Time Series (Daily)'][str(date)]['2. high'],
                        data['Time Series (Daily)'][str(date)]['5. low'],
                        data['Time Series (Daily)'][str(date)]['4. close'],
                        data['Time Series (Daily)'][str(date)]['1. volume']))
            cur.execute(insert)
        print("added symbol ", symbol)
        #Deletes symbol when it is added to database.
        with open('companies.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('companies.txt', 'w') as fout:
            fout.writelines(data[1:])
        time.sleep(10)

if __name__ == "__main__":
    connect()
    