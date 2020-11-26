#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import requests


# In[2]:


custtyped ={
    'Customer Type':['atm','bank','mosque','department_store','bakery','accounting',
                    'airport','amusement_park','aquarium','art_gallery','bar','beauty_salon','bicycle_store',
                     'book_store','bowling_alley','bus_station','cafe','campground','car_dealer','car_rental'
                     'car_repair','car_wash','casino','cemetery','church','city_hall','clothing_store','convenience_store',
                     'courthouse','dentist','doctor','drugstore','electrician',
                     'electronics_store','embassy','fire_station','florist','funeral_home','furniture_store',
                     'gas_station','gym','hair_care','hardware_store','hindu_temple','home_goods_store',
                     'hospital','insurance_agency','jewelry_store','laundry','lawyer','library','light_rail_station',
                     'liquor_store','local_government_office','locksmith','lodging','meal_delivery',
                     'meal_takeaway','movie_rental','movie_theater','moving_company','museum','night_club',
                     'painter','park','parking','pet_store','pharmacy','physiotherapist','plumber','police',
                     'post_office','primary_school','real_estate_agency','restaurant','roofing_contractor',
                      'rv_park','school','secondary_school','shoe_store','shopping_mall','spa','stadium',
                      'storage','store','subway_station','supermarket','synagogue','taxi_stand',
                      'tourist_attraction','train_station','transit_station','travel_agency','university',
                      'veterinary_care','zoo']
    #'Keyword':['Mandiri','BCA','istiqlal','matahari','breadtalk']
}


# In[3]:


custtype=pd.DataFrame(custtyped)
custtype


# In[4]:


custtype['Customer Type'].values


# In[5]:


data_cust={}
latitude, longitude, name, place_id, types_places, vicinity = [],[],[],[],[],[]

for types in custtype['Customer Type'].values:
    apik = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'
    urls = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-6.1798024,106.8220712&radius=1000&key={}&type={}'.format(apik,types)
    r = requests.get(urls)
    data_cust[types] = r.json()
    for number in range(len(data_cust[types]['results'])):
        latitude.append(data_cust[types]['results'][number]['geometry']['location']['lat'])
        longitude.append(data_cust[types]['results'][number]['geometry']['location']['lng'])
        name.append(data_cust[types]['results'][number]['name'])
        place_id.append(data_cust[types]['results'][number]['place_id'])
        types_places.append(data_cust[types]['results'][number]['types'][0])
        vicinity.append(data_cust[types]['results'][number]['vicinity'])


# In[7]:


datacustype = pd.DataFrame({'name':name,'place_id':place_id,'types':types_places,'latitude':latitude,
                     'longitude':longitude,'address':vicinity})
datacustype


# # cleaning

# In[8]:


pd.isnull(datacustype).sum()


# In[22]:


len(datacustype['place_id'].unique())


# # phone numb

# In[9]:


data_number = {}
for number in datacustype['place_id'].values:
    apik = 'AIzaSyCi3bprtv8GbZUNpU4rE2eQ8oguxfDkRjg'
    urls = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,rating,formatted_phone_number&key={}'.format(number,apik)
    r = requests.get(urls)
    data_number[number] = r.json()


# In[10]:


data_number


# In[21]:


(list(data_number.keys()))


# In[11]:


datanumb = pd.DataFrame.from_dict(data_number).T.reset_index()
datanumb.columns = ['place_id','html_attributions','result','status']
datanumb


# In[11]:


datanumb['result'][0].keys()


# In[12]:


name= []
phone=[]

for number in range(len(datanumb)):
    name.append(datanumb['result'][number]['name'])
    if 'formatted_phone_number' in (datanumb['result'][number].keys()):
        phone.append(datanumb['result'][number]['formatted_phone_number'])
    else:
        phone.append(0)


# In[13]:


datanumb2 = pd.DataFrame({'name':name,'phone number':phone})
datanumb2['place_id'] = datanumb['place_id']
datanumb2


# # join

# In[14]:


datamerge=datacustype.merge(datanumb2, how='left', on='place_id')
#datagab3=datab2.join(datanumb2.set_index('place_id'),on='place_id')
datamerge


# In[15]:


pd.isnull(datamerge).sum()

