import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as math
%matplotlib inline
import os

#load files, change path
folder=r'C:\Users\mateusz.bak\Desktop\programs\bike'

marzec = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-03.csv"),index_col=0)
kwiecien = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-04.csv"),index_col=0)
maj = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-05.csv"),index_col=0)
czerwiec = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-06.csv"),index_col=0)
lipiec = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-07.csv"),index_col=0)
sierpien = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-08.csv"),index_col=0)
wrzesien = pd.read_csv(os.path.join(folder,r"C:historia_przejazdow_2019-09.csv"),index_col=0)
pazdziernik = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-10.csv"),index_col=0)
listopad = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-11.csv"),index_col=0)
grudzien = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2019-12.csv"),index_col=0)
styczen = pd.read_csv(os.path.join(folder,r"historia_przejazdow_2020-01.csv"),index_col=0)

#PART OF DATA PREPARATION

# Checking if any data does not differ in quantity from the rest due to, for example, a write error
# Removal of unnecessary records and renaming of some stations

# An example of displaying unnecessary records
print(kwiecien['rental_place'].value_counts().tail(10))

# Removal of lines that are redundant in the analysis
def dropValues(df):
    d1=df['rental_place']=="55555"
    d2=df['return_place']=="55555"
    d3=df['rental_place']==".SERWIS - ŁADOWANIE"
    d4=df['return_place']==".SERWIS - ŁADOWANIE"
    d5=df['rental_place']=="NIOL test" 
    d6=df['return_place']=="NIOL test"
    d7=df['rental_place']=="#Rowery zapasowe Warszawa" 
    d8=df['return_place']=="#Rowery zapasowe Warszawa"
    d9=df['return_place']=="# Rowery skradzione Wrocław 2014"
    d10=df['rental_place']=="# Rowery skradzione Wrocław 2014"
        
    #delete of data with negative time
    d11=df['end_time']<df['start_time']
    
    d12=df[d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 | d11]
    df=df.append(d12)[~df.append(d12).index.duplicated(keep=False)]
    return df

#Change name of some values
def rename(df):
    df.replace(['.RELOKACYJNA','.RELOKACYJNA A1-4','Fabryczna  (WSB)','.GOTOWE DO REZERWACJI'],['Poza stacją','Poza stacją','Fabryczna (WSB)','Poza stacją'],inplace=True)
    return df

# Delete of data that should be in another month
def delete(df,t):
    dp=df[df['start_time'].str.contains(t)]
    df=df.append(dp)[~df.append(dp).index.duplicated(keep=False)]
        
    return df

#Delete duplicates
def duplicates(df):
    print('Czy wartosci sa unikalne?: ', df['uid'].is_unique)
    df.drop_duplicates(subset=['uid'],keep='first',inplace=True)
    print('Czy teraz wartosci sa unikalne?: ', df['uid'].is_unique)
    
    return df

#separating the date and time columns, adding the "use_time" column and type conversion
def split(df):
    df[['data_start','time_start']]=df['start_time'].str.split(' ',expand=True)  
    df[['data_end','time_end']]=df['end_time'].str.split(' ',expand=True)
    
    df['start_time']= pd.to_datetime(df['start_time'])
    df['end_time']=pd.to_datetime(df['end_time'])
    
    df['time_start']=pd.to_timedelta(df.time_start)
    df['time_end']=pd.to_timedelta(df.time_end)
    
    df.insert(loc=6, column='use_time', value =df['end_time']-df['start_time'])
    
    return df

month=['marzec','kwiecien','maj','czerwiec','lipiec','sierpien','wrzesien','pazdziernik','listopad','grudzien','styczen']
month2=['2019-03','2019-04','2019-05','2019-06','2019-07','2019-08','2019-09','2019-10','2019-11','2019-12','2020-01']
for i in month:
    exec('{}=dropValues({})'.format(i,i))
    exec('{}=rename({})'.format(i,i))


# Adding the values ​​of cut values ​​from previous months to their proper ones
# only consecutive months are included, distant months were omitted from the analysis    
marzec=marzec.append(kwiecien[kwiecien['start_time'].str.contains('2019-03')])
kwiecien=kwiecien.append(marzec[marzec['start_time'].str.contains('2019-04')])
kwiecien=kwiecien.append(maj[maj['start_time'].str.contains('2019-04')])
maj=maj.append(czerwiec[czerwiec['start_time'].str.contains('2019-05')])
czerwiec=czerwiec.append(lipiec[lipiec['start_time'].str.contains('2019-06')])
lipiec=lipiec.append(sierpien[sierpien['start_time'].str.contains('2019-07')])
sierpien=sierpien.append(wrzesien[wrzesien['start_time'].str.contains('2019-08')])
wrzesien=wrzesien.append(pazdziernik[pazdziernik['start_time'].str.contains('2019-09')])
pazdziernik=pazdziernik.append(listopad[listopad['start_time'].str.contains('2019-10')])
listopad=listopad.append(grudzien[grudzien['start_time'].str.contains('2019-11')])
grudzien=grudzien.append(listopad[listopad['start_time'].str.contains('2019-12')])
grudzien=grudzien.append(styczen[styczen['start_time'].str.contains('2019-12')])   
    
for i in month:
    for m in month2:
        if month.index(i)!=month2.index(m):
            exec('{}=delete({},m)'.format(i,i))
        else:
            continue
    print(i)
    exec('{}=duplicates({})'.format(i,i))
    exec('{}=split({})'.format(i,i))
       

#VISUALIZATION PART

#Monthly variability 
for i in month:
    exec("{}.data_start.value_counts().sort_index().plot(kind='bar',figsize=(15,5),title=i,rot=45)".format(i))    
    plt.show()

size=[len(marzec),len(kwiecien),len(maj),len(czerwiec),len(lipiec),len(sierpien),len(wrzesien),len(pazdziernik),len(listopad),len(grudzien),len(styczen)]
plt.figure(figsize=(12, 8))
plt.ylabel("Ilość wypożyczeń")
plt.title('Zmienność miesięczna')
plt.bar(month,size)
plt.show()

#Weekly variation
def to_plot(df):
    tp=df.start_time.dt.day_name().value_counts()
    return tp
  
for i in month:
    exec('t_{}=to_plot({})'.format(i,i))
    
week=t_marzec+t_kwiecien+t_maj+t_czerwiec+t_lipiec+t_sierpien+t_wrzesien+t_pazdziernik+t_listopad+t_grudzien+t_styczen
week=week/44 # it results from the number of weeks taken for the analysis, due to the low impact on the results, the first 22 days of March were also included  
week=week.reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])    
week.plot(kind='bar',figsize=(12, 8))
    
#time of use
calosc=pd.concat(objs=[marzec,kwiecien,maj,czerwiec,lipiec,sierpien,wrzesien,pazdziernik,listopad,grudzien,styczen])

use=calosc[['use_time','uid']]
use_w=use.groupby(pd.Grouper(key='use_time',freq='1Min')).count()
use_w[:90].plot(figsize=(12, 8),title='Czas użytkowania')
    
#Daily variability
# daily variability over the entire data range
rental=calosc[['time_start','uid']]
rental_w=rental.groupby(pd.Grouper(key='time_start',freq='1Min')).count()
rental_w.plot(figsize=(12, 8),title='Zmiennosc dobowa')

#adding a new column with the name of the day of the week
calosc['days']=calosc.start_time.dt.day_name()

#Creating daily volatility on non-working and working days
saturday=calosc['days']=='Saturday'
sunday=calosc['days']=='Sunday'
weekend=calosc[saturday | sunday]
swieta=calosc.query('data_start=="2019-04-22" | data_start=="2019-05-01" | data_start=="2019-05-03" | data_start=="2019-06-20" | data_start=="2019-08-15" | data_start=="2019-11-01" | data_start=="2019-11-11" | data_start=="2019-12-25" | data_start=="2019-12-26" | data_start=="2020-01-01" | data_start=="2020-01-06"')

#Non-working days
wolne=weekend.append(swieta)

w=wolne[['time_start','uid']]
w2=w.groupby(pd.Grouper(key='time_start',freq='1Min')).count()
w2.plot(figsize=(12, 8),title='Zmiennosc dobowa w dni wolne')

#Working days
tydzien=calosc.append(wolne)
tydzien.drop_duplicates(subset=['uid'],keep=False,inplace=True)

t=tydzien[['time_start','uid']]
t2=t.groupby(pd.Grouper(key='time_start',freq='1Min')).count()
t2.plot(figsize=(12, 8),title='Zmiennosc dobowa w dni robocze')

#Presentation of charts on one

rental_w.rename({'uid':'calosc'},axis='columns',inplace=True)
w2.rename({'uid':'weekend'},axis='columns',inplace=True)
t2.rename({'uid':'dni pracujace'},axis='columns',inplace=True)

wyk=rental_w.join(w2)
wyk=wyk.join(t2)

wyk.plot(figsize=(12, 8))
#plt.savefig(r'D:\python_scripts\figure.pdf')
wyk.plot(figsize=(12, 18),subplots=True)

#Save the necessary data
#Count of rentals for each month
for i in month:
    exec('v_{}={}["rental_place"].value_counts()'.format(i,i))

#Count of rentals from any period
wyc1=lipiec['data_start']>='2019-07-01'
wyc2=lipiec['data_start']<'2019-07-08'
wyc3=lipiec[wyc1 & wyc2]
wycinek=wyc3['rental_place'].value_counts()

wycinek.to_csv(os.path.join(folder,'wycinek.csv'),sep=' ',mode='w',encoding='CP1250')
wycinek.to_string(os.path.join(folder,'wycinek2.txt'))


