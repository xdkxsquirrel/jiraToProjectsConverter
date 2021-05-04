import datetime as dt
import pandas as pd
import argparse
import csv
import string

df = []
df2 = []

def getCommandlineInputsAndDataFrame( ):
    global df
    parser = argparse.ArgumentParser( description='Jira Converter' )
    parser.add_argument( '-f', '--file', type=argparse.FileType('rb'), help='-f file-name' )
    results = parser.parse_args( )
    if results.file:
        df = pd.read_csv( results.file, encoding='latin1' )
        df.columns = df.columns.str.replace('[^a-zA-Z0-9-_/%&@.,:"()\s]', '', regex=True)
        for index, row in df.iterrows():
            df.loc[index] = row.str.replace('[^a-zA-Z0-9-_/%&@.,:"()\s]', '', regex=True)
    else:
        print( "Please input filename" )
        exit( )

def grabNeededColumns( ):
    global df2
    columnsForDf2 = ['Task Number', 'Task Name', 'Duration', 'Start', 'Finish', 'Predecessors', 'Resource Names',
                     '% Complete', 'Ready for Verification', 'Notes', 'EE Epic?']
    columnsFromDf = ['Issue key', 'Summary', 'Due-Start', 'Custom field (Start date)', 'Due date', '', 'Assignee',
                     'Work Ratio', '', '', 'EE']
    df2 = pd.DataFrame()
    for i in range(len(columnsFromDf)):
        if columnsFromDf[i] == 'Due-Start':
            df2[columnsForDf2[i]] = (pd.to_datetime(df['Due date']) - pd.to_datetime(df['Custom field (Start date)'])).dt.days
        elif columnsFromDf[i] == 'EE':
            eeStrings = []
            for _ in range(df.shape[0]):
                eeStrings.append('EE Epic')
            df2[columnsForDf2[i]] = eeStrings
        elif columnsFromDf[i] == '':
            emptyStrings = []
            for _ in range(df.shape[0]):
                emptyStrings.append('')
            df2[columnsForDf2[i]] = emptyStrings
        else:
            df2[columnsForDf2[i]] = df[columnsFromDf[i]]
    df2['% Complete'] = df2['% Complete'].fillna('0%')

def outputsCsvFile( ):
    global df2
    df2.to_csv('JIRAoutput.csv', index=False)

def main( ):
    getCommandlineInputsAndDataFrame( )
    grabNeededColumns( )
    outputsCsvFile( )

if __name__ == "__main__":
    main( )
