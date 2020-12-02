#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import requests


# # coba input

# In[2]:


lat_ori = input('Masukkan lat asal:')
long_ori = input('Masukkan long asal:')
radius = input('Masukkan radius(dalam meter):')
types_user = input('Masukkan types:')
keyword_user = input('Masukkan keyword:')
#-6.2097
#106.90166


# In[3]:


data_cust={}
latitude, longitude, name, place_id, types_places, vicinity = [],[],[],[],[],[]

apik = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'
urls = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&key={}&type={}&keyword={}'.format(lat_ori,long_ori,radius,apik,types_user,keyword_user)
r = requests.get(urls)
data_cust[types_user] = r.json()
for number in range(len(data_cust[types_user]['results'])):
    latitude.append(data_cust[types_user]['results'][number]['geometry']['location']['lat'])
    longitude.append(data_cust[types_user]['results'][number]['geometry']['location']['lng'])
    name.append(data_cust[types_user]['results'][number]['name'])
    place_id.append(data_cust[types_user]['results'][number]['place_id'])
    types_places.append(data_cust[types_user]['results'][number]['types'][0])
    vicinity.append(data_cust[types_user]['results'][number]['vicinity'])


# In[5]:


datacustype = pd.DataFrame({'customer_name':name,'customer_address':vicinity,'customer_type':types_places,'place_id':place_id,
                            'keyword':keyword_user,'radius':radius,'latitude_origin':lat_ori,'longitude_origin':long_ori,'latitude_destination':latitude,
                            'longitude_destination':longitude})
datacustype


# # phone numb

# In[8]:


data_number = {}
for number in datacustype['place_id'].values:
    apik = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'
    urls = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,rating,formatted_phone_number&key={}'.format(number,apik)
    r = requests.get(urls)
    data_number[number] = r.json()


# In[9]:


data_number


# In[10]:


datanumb = pd.DataFrame.from_dict(data_number).T.reset_index()
datanumb.columns = ['place_id','html_attributions','result','status']
datanumb


# In[11]:


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


# In[12]:


datanumb2 = pd.DataFrame({'customer_name':name,'phone_number':phone})
datanumb2['place_id'] = datanumb['place_id']
datanumb2


# # merge

# In[13]:


datamerge=datacustype.merge(datanumb2, how='left', on='place_id')
#datagab3=datab2.join(datanumb2.set_index('place_id'),on='place_id')
datamerge


# # dummy

# In[14]:


datadummy=datamerge.copy()
datadummy


# In[15]:


datadummydrop=datadummy.drop(['customer_name_y'], axis = 1)
datadummydrop.columns = ['customer_name','customer_address','customer_type','place_id','keyword','radius','latitude_origin','longitude_origin','latitude_destination','longitude_destination','phone_number']
datadummydrop2=datadummydrop[['customer_name','customer_address','customer_type','keyword','radius', 'place_id','latitude_origin','longitude_origin','latitude_destination','longitude_destination','phone_number']]
datadummydrop2


# # distance matrix

# In[16]:


import pandas as pd
import googlemaps


# In[17]:


API_key = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)


# In[18]:


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
    result = gmaps.distance_matrix(origins, destination, mode='driving',avoid='tolls',units='metric',departure_time=1703981100)["rows"][0]["elements"][0]["distance"]["value"]
    result1 = gmaps.distance_matrix(origins, destination, mode='walking',avoid='tolls',units='metric',departure_time=1703981100)["rows"][0]["elements"][0]["distance"]["value"]
 #1703981100    #1606867500 
      #append result to list
    distancedrive.append(result)
    distancewalks.append(result1)


# In[19]:


datadummydrop2['Distance to Infra(m)(driving)']=distancedrive
datadummydrop2['Distance to Infra(m)(walking)']=distancewalks
datadummydrop3=datadummydrop2.sort_values(by=['Distance to Infra(m)(driving)'],ascending=True,ignore_index=True)
datadummydrop3


# In[ ]:




