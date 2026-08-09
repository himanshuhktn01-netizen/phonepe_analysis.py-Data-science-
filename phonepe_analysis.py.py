import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sta_txn_user=pd.read_excel('phonepe-pulse_raw-data_q12018-to-q22021-v0-1-5-1720351752.xlsx',sheet_name='State_Txn and Users')
sta_txn_split=pd.read_excel('phonepe-pulse_raw-data_q12018-to-q22021-v0-1-5-1720351752.xlsx',sheet_name='State_TxnSplit')
sta_dev_data=pd.read_excel('phonepe-pulse_raw-data_q12018-to-q22021-v0-1-5-1720351752.xlsx',sheet_name='State_DeviceData')
dist_user=pd.read_excel('phonepe-pulse_raw-data_q12018-to-q22021-v0-1-5-1720351752.xlsx',sheet_name='District_Txn and Users')
dist_demograph=pd.read_excel('phonepe-pulse_raw-data_q12018-to-q22021-v0-1-5-1720351752.xlsx',sheet_name='District Demographics')

# # SUMMARY OF EACH DATA SETS
# print(sta_txn_user.head(5)) 
# print(sta_txn_split.head(5))
# print(sta_dev_data.head(5))
# print(dist_user.head(5))
# print(dist_demograph.head(5))


# print(sta_txn_user.describe()) 
# print(sta_txn_split.describe())
# print(sta_dev_data.describe())
# print(dist_user.describe())
# print(dist_demograph.describe())

# print(sta_txn_user.dtypes) 
# print(sta_txn_split.dtypes)
# print(sta_dev_data.dtypes)
# print(dist_user.dtypes)
# print(dist_demograph.dtypes)



# CHECKING MISSING VALUES
# replacing empty string with null for easy calculation
for i in [sta_dev_data,dist_user,sta_txn_split,sta_txn_user,dist_demograph]:
    i.replace(['',' '],pd.NA,inplace=True)

# print(sta_txn_user.isnull().any().any()) 
# print(sta_txn_split.isnull().any().any())
# print(sta_dev_data.isnull().any().any())
# print(dist_user.isnull().any().any())
# print(dist_demograph.isnull().any().any())


#  missing values in a column 
# print(sta_txn_user.isnull().sum()) 
# print(dist_user.isnull().sum())

# missing_per_txn_user=sta_txn_user.isnull().mean()*100
# missing_per_dict_user=dist_user.isnull().mean()*100


# print(f"missing values in sta_txn_user {missing_per_txn_user[missing_per_txn_user>0.0]}")
# print(f"missing values in dist_user {missing_per_dict_user[missing_per_dict_user>0.0]}")#sum to remove extra things 

# print(f"highese missing data in sta_txn_user {missing_per_txn_user.idxmax()} value {missing_per_txn_user.max()}")
# print(f"highese missing data in dist_user {missing_per_dict_user.idxmax()} value {missing_per_dict_user.max()}")


#  REMOVING NULLS
#  in sta_txn_user there is a null in amount 
sta_txn_user['Amount (INR)']=sta_txn_user['Amount (INR)'].fillna(sta_txn_user['Amount (INR)'].rolling(window=5,min_periods=1,center=True).mean())

# print(sta_txn_user.isnull().sum()) 


dist_user['Code']=dist_user['Code'].fillna(dist_user['Code'].mode().iloc[1])
dist_user['ATV (INR)']=dist_user['ATV (INR)'].fillna(dist_user['ATV (INR)'].rolling(window=3,min_periods=1,center=True).mean())

# print(dist_user.isnull().sum())

# TOTAL NO. OF STATE AND DISTRICTS

# print(dist_user['State'].nunique())
# print(dist_user['District'].nunique())

#  STATE WITH HIGHEST NO. OF DISTRICTS
con_dis=dist_user.groupby('State')['District'].nunique()

# print(con_dis)


# print(f"highest no. of district in {con_dis.idxmax()} value{con_dis.max()}")


# TOTAL NO. AND AMOUNT OF TRANSACTION AMOUNT FOR EACH STATE OVER THE YEARS 

trans_no_trans_amount=sta_txn_user.groupby(['Year','State'])[['Transactions','Amount (INR)']].sum().reset_index()

# print(trans_no_trans_amount)

# HIGHEST TOP 5 STATE and lowest 
# Transaction volume
vo_high=sta_txn_user.groupby('State')['Transactions'].sum().sort_values(ascending=False).head(5)
# print(vo_high)

vo_low=sta_txn_user.groupby('State')['Transactions'].sum().sort_values().head(5)
# print(vo_low)

# Transaction value
va_high=sta_txn_user.groupby('State')['Amount (INR)'].sum().sort_values(ascending=False).head(5)
# print(va_high)

va_low=sta_txn_user.groupby('State')['Amount (INR)'].sum().sort_values().head(5)
# print(va_low)


# MOST COMMON TRANSACTION TYPE IN EVERY STATE AND EVERY QUARTER 

q_s=sta_txn_split.groupby(['State','Quarter'])['Transaction Type'].value_counts().reset_index().sort_values('count',ascending=False).groupby(['State','Quarter']).first().reset_index()
# print(q_s)



 
# HIGHEST USER BRAND IN EVERY STATE 

state_brand=sta_dev_data.groupby(['State','Brand'])['Registered Users'].sum().reset_index()
brand=state_brand.loc[state_brand.groupby('State')['Registered Users'].idxmax()].reset_index(drop=True)
# print(brand)


# DISTRICT WITH HIGHEST POPULATION IN EACH STATE 

high_dist=dist_demograph.groupby(['State','District'])['Population'].sum().reset_index()
state_dist=high_dist.loc[high_dist.groupby('State')['Population'].idxmax()].reset_index(drop=True)
# print(state_dist)


plt.figure(figsize=(30,30))
sns.barplot(state_dist.sort_values('Population',ascending=False),x='State',y='Population',hue='District')
plt.xticks(rotation=45)
plt.title('Highest Population District by State')
# plt.show()

# AVERAGE TRANSACTION VALUE(ATV) OF EACH STATE 

avg_trans_value=sta_txn_user.groupby('State')['Amount (INR)'].mean()
# print(avg_trans_value)
high_ATV=avg_trans_value.sort_values(ascending=False).head(5)
low_ATV=avg_trans_value.sort_values().head(5)

# print(high_ATV,low_ATV)


# TOTAL NO. OF APPS OPEN OVER THE YEARS AND  QUARTERs FOR EACH STATE display it in tabular form 

app_open=sta_txn_user.groupby(['State','Year','Quarter'])['App Opens'].sum().reset_index()



# LINE GRAPH FOR PARTICULAR STATE 
app_open['Year_Quarter']=app_open['Year'].astype(str) +'_' + app_open['Quarter'].astype(str)
# print(app_open.head(20))
def app_open_graph(State):
    state_data=app_open[app_open['State']==State]

    plt.figure(figsize=(15,15))
    sns.lineplot(data=state_data,x=state_data['Year_Quarter'],y=state_data['App Opens'],hue='State')
    plt.xticks(rotation=45)
    # plt.show()

# app_open_graph('Andhra Pradesh')

# DISTRIBUTION OF DIFFERENT TRANSACTION TYPES FOR EACH STATE FOR THE MOST RECENT QUARTER 

recent_y_q=sta_txn_split[['Year','Quarter']].drop_duplicates().sort_values(['Year','Quarter'],ascending=False).iloc[0]

State_trans_typee=sta_txn_split[(sta_txn_split['Year']==recent_y_q['Year']) & (sta_txn_split['Quarter']==recent_y_q['Quarter'])]
# print(State_trans_typee)


distribution=State_trans_typee.groupby(['State','Transaction Type'])['Transactions'].sum().reset_index()

# print(distribution)



plt.figure(figsize=(15,15))
sns.barplot(distribution,x=distribution['State'],y=distribution['Transactions'],hue='Transaction Type')

plt.xticks(rotation=45)
plt.title('DISTRIBUTION OF DIFFERENT TRANSACTION TYPES FOR EACH STATE FOR THE MOST RECENT QUARTER ')
# plt.show()


#  MAPPING DISTRICT NAME AND CODE 

# UNIQUE DISTRICT NAME 
map_dist=dist_demograph.drop_duplicates(subset='District').set_index('District')['Code']
# print(map_dist)

# map_dist.to_csv('map_dist.csv',index=True)


# calculate the total number of transactions, total transaction amount,and 
# total registered users by summing up the values from the district level data.
# same with state level data

dist_level=dist_user.groupby(['State'])[['Transactions','Amount (INR)','Registered Users']].sum().reset_index()
# print(dist_level)

sta_level=sta_txn_user.groupby(['State'])[['Transactions','Amount (INR)','Registered Users']].sum().reset_index()
# print(sta_level)


# FOR COMPARISION

dist_sta=pd.merge(dist_level,sta_level,on=['State'],suffixes=('_district','_state'))

# print(dist_sta)


# discrepancies
discrepancies=dist_sta[(dist_sta['Transactions_district']!=dist_sta['Transactions_state'] )|
                       (dist_sta['Amount (INR)_district']!=dist_sta['Amount (INR)_state']) |
                       (dist_sta['Registered Users_district']!=dist_sta['Registered Users_state'])
                       ]

# print(discrepancies)




# MERGING STATE_TXN_USER WITH DISTRICT DEMOGRAPHY TO  CALCULATE THE RATIO OF REGISTERED USER TO THE POPULATION FOR EVERY STATE 

state_sta_txn_user=sta_txn_user.groupby('State')['Registered Users'].sum()
district_dist_demograph=dist_demograph.groupby('State')['Population'].sum()
state_district=pd.merge(state_sta_txn_user,district_dist_demograph,on=['State'])

user_by_population=(state_district['Registered Users'])/(state_district['Population'])


plt.figure(figsize=(15,15))

user_by_population.plot(kind='bar',color='red')
plt.xlabel('State')
plt.ylabel('Registered Users Percentage')
plt.title("REGISTERED USERS FOR EVERY STATE ")
# plt.show()
# print(user_by_population)




# CORELATION BETWEEN POPULATION DENSITY AND TRANSACTION VOLUME 
trasn_vol_district=dist_user.groupby('State')['Transactions'].sum()
pop_district=dist_demograph.groupby('State')['Population'].sum()

dist_user_demographic=pd.merge(trasn_vol_district,pop_district,on='State')

corelation=dist_user_demographic[['Transactions','Population']].corr()
# print(corelation)


plt.figure(figsize=(15,15))

sns.scatterplot(dist_user_demographic ,x='Population',y='Transactions')
plt.title(" CORELATION BETWEEN POPULATION DENSITY AND TRANSACTION VOLUME")
# plt.show()

# RELEVANT DATA SET FOR AVERAGE USER TRANSACTION VOLUME FOR EVERY STATE.
a=sta_txn_split.groupby('State')['Amount (INR)'].sum()
b=sta_txn_user.groupby('State')['Amount (INR)'].sum()

# print(a,b)

user=sta_txn_user.groupby('State')['Registered Users'].sum()
amount=sta_txn_split.groupby('State')['Amount (INR)'].sum()

user_amount=pd.merge(user,amount,on='State')

avg_volume=(user_amount['Amount (INR)'])/(user_amount['Registered Users'])
# print(avg_volume.round(2))

high_amount=avg_volume.sort_values(ascending=False).head(5)
low_amount=avg_volume.sort_values().head(5)


# print(high_amount)
# print(low_amount)



# RATION OF USER USING EACH DEVICE BRAND TO THE TOTAL NO. OF REGISTERED USER 
user_state= sta_txn_user.groupby('State')['Registered Users'].sum()
state_brand_user=sta_dev_data.groupby(['State','Brand'])['Registered Users'].sum()

ratio_brand =state_brand_user.div(user_state).reset_index(name='Ratio')

# print(ratio_brand)



plt.figure(figsize=(15,15))
sns.barplot(ratio_brand,x='State',y='Ratio',hue='Brand')
plt.xticks(rotation=45)
plt.title('RATIO OF USER USING EACH DEVICE BRAND TO THE TOTAL NO. OF REGISTERED USER ')
# plt.show()


# A LINE PLOT SHOWING THE TOTAL NO. OF TRANSACTION AND THE TOTAL TRANSACTION AMOUNT OVER TIME(YEAR-QUARTER) FOR ANY STATE 
state_transaction =sta_txn_user.groupby(['State','Year','Quarter'])[['Transactions','Amount (INR)']].sum().reset_index()

state_transaction['Year_Quarter']=state_transaction['Year'].astype(str)+'_'+state_transaction['Quarter'].astype(str)

def state_transaction_line(state):
    data=state_transaction[state_transaction['State']==state] 
    # data['Amount (INR)']=  data['Amount (INR)']/1e11
    plt.figure(figsize=(15,15))

    sns.lineplot(data,x=data['Year_Quarter'],y=data['Transactions'], marker='o',label='Transactions',errorbar=None)
    sns.lineplot(data,x=data['Year_Quarter'],y=(data['Amount (INR)']),marker='o',label='Amount (INR)',errorbar=None)

    plt.xticks(rotation=45)
    plt.title(f"TOTAL NO. OF TRANSACTION AND THE TOTAL TRANSACTION AMOUNT OVER TIME FOR {state}")
    plt.show()

# state_transaction_line('Delhi')

# DISTRIBUTION OF DIFFERENT TRANSACTION TYPES FOR A SELECTED STATE AND QUARTER (SHOW IN PI CHART)

quarter_state=sta_txn_split.groupby(['State','Quarter'])['Transaction Type'].value_counts().reset_index(name='Count')
# print(quarter_state)

quarter_state['State_Quarter']= quarter_state['State'].astype(str)+'_'+quarter_state['Quarter'].astype(str)

def distribution_types(state,quarter):
    x=state+'_'+str(quarter)
    data=quarter_state[quarter_state['State_Quarter']==x][['Transaction Type','Count']]
    plt.figure(figsize=(8,8))
    plt.pie(data['Count'],labels=data['Transaction Type'],startangle=140, autopct='%1.1f%%',)
    plt.title(f"DISTRIBUTION OF DIFFERENT TRANSACTION TYPES FOR {state} in {quarter}quarter")
    plt.show()



# distribution_types('Delhi',1)

# DENSITY OF DISTRICTS IN SELECTED CITY WITH  BAR GRAPH 

state_density=dist_demograph.groupby(['State','District'])['Population'].sum().reset_index(name='count')


def density_population(state):
    data=state_density[state_density['State']==state]
    plt.figure(figsize=(12,12))

    sns.barplot(data,x=data['District'],y=data['count'],hue='State')
    plt.xticks(rotation=45)
    plt.xlabel('District')
    plt.ylabel('Density of population')
    plt.title(f"DENSITY OF DISTRICTS IN {state}")
    # plt.show()


# density_population('Delhi')

# A line graph to analyse the transaction data 

trans_year=sta_txn_user.groupby('Year')['Transactions'].sum()
plt.figure( figsize=(12,12))
sns.lineplot(trans_year)
# plt.show()
# With this we can discuss the trends and pattern 

# CORELATION BETWEEN DEMOGRAPHIC AND TRANSACTION DATA 

trans_data=sta_txn_user.groupby('State')['Transactions'].sum()
demograph_data=dist_demograph.groupby('State')['Population'].sum()

demo_trans=pd.merge(trans_data,demograph_data,on='State')

demo_trans_relation= demo_trans[['Transactions','Population']].corr()
# print(demo_trans_relation)

