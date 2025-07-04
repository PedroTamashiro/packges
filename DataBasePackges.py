import mariadb
import pandas as pd
import socket
from datetime import datetime, time
from time import sleep
import os
import sys
import logging
sys.path.append('C:\MiraiCodes\Packges')  # Adicione o caminho do diretório pai

def loggingPredef(logfilename):
    logger = logging.getLogger(__name__)
    log_dir = r'C:\Users\cliente\Desktop\logs'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = log_dir + '//' + {logfilename}

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    return logging

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

def verifyHour(minute):
    if is_time_between(time(5,00), time(4,00)):
        if datetime.now().minute == minute or datetime.now().minute == minute/3:
            return 1
    elif is_time_between(time(4,00), time(5,00)):
        if datetime.now().minute == minute or datetime.now().minute == minute/3:
            return 2
    return 0

def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
        logging.info('connection True')
        return True
    except OSError:
        pass
    
    logging.info('connection False')
    return False

def wifi_connect():
    logging.info('Verify Connection')
    isConnec = isConnected()
    while not isConnec:
        # connect to the given wifi network
        logging.error('Erro Wifi Connection Retrying in 10 sec...')
        sleep(10)
        os.system(f'''cmd /c "netsh wlan connect name=\"Mirai Platinum\""''')
        sleep(3)
        isConnec = isConnected()
    logging.info('Connection OK')

## getting Connection
def connectBD(DataBase, host):
    try:
        connection = mariadb.connect(
            user = 'root',
            password = 'M1r@i2024',
            host = host,
            port = 3306,
            database = DataBase
        )
        connection.auto_reconnect = True
        logging.info('Connected to DB')
        cursor = connection.cursor()
        return connection, cursor
    except:
        raise Exception (ConnectionError)

## Define delete function
def delete(connection, cursor, Keys, DataBaseTable, ColumnName, mode):
    try:
        if mode == 0:
            str_Keys = [str(key) for key in Keys]
            if str_Keys == []:
                return
            placeholders = ','.join(['%s'] * len(str_Keys))
            DeleteQuery = f"DELETE FROM {DataBaseTable} WHERE {ColumnName} IN ({placeholders})"
            
            cursor.execute(DeleteQuery, str_Keys)
        
        elif mode == 1:
            DeleteQuery = f"DELETE FROM {DataBaseTable}"
            cursor.execute(DeleteQuery)
        
        else:
            raise ValueError("Invalid mode. Use 0 for filtered delete, 1 for full delete.")
        
        connection.commit()
        logging.info('Located items deleted successfully.')

    except Exception as e:
        logging.error(f"Error while executing delete: {e}")
        raise Exception('ExecutingError') from e

    
## Define insertMany function
def insertMany(connection, cursor, newTable:pd.DataFrame, DataBaseTable):
    try:
        quant = newTable.columns
        
        columns = ','.join(column for column in quant)
        quant = ['?'] * len(quant)
        quant = ','.join(column for column in quant)
        
        insertQuery = f'INSERT INTO {DataBaseTable} ({columns}) VALUES ({quant})'
        
        data_to_insert = [tuple(row) for row in newTable.values]

        cursor.executemany(insertQuery, data_to_insert)
        connection.commit()
        logging.info('All the Values inserted in the DataBase')
    except:
        raise Exception('ExecutingError')
    
## Define insert function
def insert(connection, cursor, row, query):
    try:
        cursor.execute(query, row)
        
        connection.commit()
        logging.info('All the Values inserted in the DataBase')
        
    except Exception as e:
        logging.error(f'Error during insert: {str(e)}')
        raise Exception('ExecutingError')

## Define Select Function
def select(cursor, dataBaseTable, selectType='*'):
    try:
        selectQuery = f'SELECT {selectType} FROM {dataBaseTable}'
        cursor.execute(selectQuery)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        
        dataFrame = pd.DataFrame(rows, columns=columns)
        logging.info('The Values are selected with sucesfull')
        return dataFrame
    except Exception as error:
        raise error
    
def mainUpdate(DataFrame: pd.DataFrame, DataBase: str ,DataBaseTableName: str, DataBaseColumnName: str, logging, host = 'localhost', mode = 0,cont=0):
    try:
        if cont < 10:
            connection, sql = connectBD(DataBase, host)
            Key = DataFrame[DataBaseColumnName]
            
            delete(connection, sql, Key, DataBaseTableName, DataBaseColumnName, mode)
            insertMany(connection, sql, DataFrame, DataBaseTableName)
            
            sql.close()
            connection.close()
            logging.info('closing connection')
            return 1
        
        logging.warning('not been possible execute the program')
        sql.close()
        connection.close()
        return 0
    except (ConnectionError):
        logging.error('Connection Error, trying again')
        cont += 1
        sql.close()
        connection.close()
        sleep(1)
        mainUpdate(DataFrame, DataBase, DataBaseTableName, DataBaseColumnName, logging, cont=cont)
        
    except Exception as error:
        logging.error(error)
        cont += 1
        mainUpdate(DataFrame, DataBase, DataBaseTableName, DataBaseColumnName, logging, cont=cont)
        
def mainExport(DataBase: str ,DataBaseTableName: str, path:str, logging, host = 'localhost', selectType='*', cont=0):
    try:
        if cont < 10:
            connection, sql = connectBD(DataBase, host)
            dataFrame = select(sql, DataBaseTableName, selectType)
            dataFrame.to_excel(path, index=False)
            logging.info('The Values are exported with sucesfull')
            
            sql.close()
            connection.close()
            logging.info('closing connection')
            return 1
        logging.warning('not been possible execute the program')
        sql.close()
        connection.close()
        return 0   
    except (ConnectionError):
        logging.error('Connection Error, trying again')
        cont += 1
        sql.close()
        connection.close()
        sleep(1)
        mainExport(DataBase ,DataBaseTableName, path, logging, selectType=selectType, cont=cont)
    except Exception as error:
        logging.error(error)
        cont += 1        
        mainExport(DataBase ,DataBaseTableName, path, logging, selectType=selectType, cont=cont)
