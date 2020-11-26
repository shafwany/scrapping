#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import requests


# In[2]:


# Reading the json as a dict
with open('fomandiri.json') as json_data:
    data = json.load(json_data)

data = pd.DataFrame.from_dict(data,orient='index').T
data


# In[3]:


# Reading the json as a dict
with open('fomandiri2.json') as json_data:
    data2 = json.load(json_data)

data2 = pd.DataFrame.from_dict(data2,orient='index').T
data2


# In[4]:


# Reading the json as a dict
with open('fomandiri3.json') as json_data:
    data3 = json.load(json_data)

data3 = pd.DataFrame.from_dict(data3,orient='index').T
data3


# # concat

# In[5]:


datac=pd.concat([data, data2,data3], ignore_index=True)
datac


# # cleaning

# In[6]:


datab= datac.loc[datac['results'].isna()==False].reset_index()
del datab['index']
datab


# In[7]:


latitude, longitude, name, place_id, types, vicinity = [],[],[],[],[],[]

for number in range(len(datab)):
    latitude.append(datab['results'][number]['geometry']['location']['lat'])
    longitude.append(datab['results'][number]['geometry']['location']['lng'])
    name.append(datab['results'][number]['name'])
    place_id.append(datab['results'][number]['place_id'])
    types.append(datab['results'][number]['types'][0])
    vicinity.append(datab['results'][number]['vicinity'])


# In[8]:


datab2 = pd.DataFrame({'name':name,'place_id':place_id,'types':types,'latitude':latitude,
                     'longitude':longitude,'address':vicinity})
datab2


# # phone numb

# In[9]:


data_number = {}
for number in datab2['place_id'].values:
    apik = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'
    urls = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,rating,formatted_phone_number&key={}'.format(number,apik)
    r = requests.get(urls)
    data_number[number] = r.json()


# In[10]:


data_number


# In[11]:


datanumb = pd.DataFrame.from_dict(data_number).T.reset_index()
datanumb.columns = ['place_id','html_attributions','result','status']
datanumb


# In[57]:


name= []
phone=[]

for number in range(len(datanumb)):
    if datanumb['status'][number] == 'NOT_FOUND':
        name.append('Unknown')
        phone.append(0)
    else:
        name.append(datanumb['result'][number]['name'])
        if 'formatted_phone_number' in (datanumb['result'][number].keys()):
            phone.append(datanumb['result'][number]['formatted_phone_number'])
        else:
            phone.append(0)


# In[58]:


datanumb2 = pd.DataFrame({'name':name,'phone_number':phone})
datanumb2['place_id'] = datanumb['place_id']
datanumb2


# # merge

# In[59]:


datamerge=datab2.merge(datanumb2, how='left', on='place_id')
datamerge


# # data dummy

# In[60]:


datadummy=datamerge.copy()
datadummy


# In[61]:


datadummydrop=datadummy.drop(['name_y'], axis = 1)
datadummydrop


# In[63]:


datadummydrop=datadummydrop[['name_x', 'place_id', 'types','latitude','longitude','address','phone_number']]
datadummydrop.columns=['Customer_name','place_id', 'types','latitude','longitude','Customer_address','phone_number']
datadummydrop


# In[64]:


datadummydrop['keyword']='mandiri'
datadummydrop['lat_ori']=-6.2097
datadummydrop['long_ori']=106.90166
datadummydrop['radius']='2000 m'
datadummydrop.head()


# In[65]:


datadummydrop2=datadummydrop[['Customer_name','Customer_address','types','keyword','radius', 'place_id','lat_ori','long_ori','latitude','longitude','phone_number']]
datadummydrop2.columns=['customer_name','customer_address','customer_type','keyword','radius','place_id','latitude_origin','longitude_origin','latitude_destination','longitude_destination','phone_number']
datadummydrop2.head


# In[66]:


datadummydrop2


# # distance matrix

# In[67]:


import pandas as pd
import googlemaps


# In[68]:


API_key = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)


# In[69]:


distancedrive,distancewalks = [],[]

# Loop through each row in the data frame using pairwise
for number in range(datadummydrop2.shape[0]):
      #Assign latitude and longitude as origin/departure points
    LatOrigin = datadummydrop2['latitude_origin'][number]
    LongOrigin = datadummydrop2['longitude_origin'][number]
    origins = (LatOrigin,LongOrigin)

      #Assign latitude and longitude from the next row as the destination point
    LatDest = datadummydrop2['latitude_destination'][number]  # Save value as lat
    LongDest = datadummydrop2['longitude_destination'][number] # Save value as lat
    destination = (LatDest,LongDest)

      #pass origin and destination variables to distance_matrix function# output in meters
    result = gmaps.distance_matrix(origins, destination, mode='driving',avoid='tolls',units='metric',departure_time=1606490410)["rows"][0]["elements"][0]["distance"]["value"]
    result1 = gmaps.distance_matrix(origins, destination, mode='walking',avoid='tolls',units='metric',departure_time=1606490410)["rows"][0]["elements"][0]["distance"]["value"]
      
      #append result to list
    distancedrive.append(result)
    distancewalks.append(result1)


# In[71]:


datadummydrop2['Distance to Infra(m)(driving)']=distancedrive
datadummydrop2['Distance to Infra(m)(walking)']=distancewalks
datadummydrop3=datadummydrop2.sort_values(by=['Distance to Infra(m)(driving)'],ascending=True,ignore_index=True)
datadummydrop3


# # export to csv/json

# In[44]:


datadummydrop2.to_json(r'maap2.json',orient='records')


# In[72]:


datadummydrop3.to_csv('distance.csv',index=False)


# In[ ]:




