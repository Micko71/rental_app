import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

st.title('Sydney Residential Property Rental Price Estimator  :house:',anchor=False)
st.divider()

#define selections
#map suburbs to postcodes
suburb_mapping_dict = {'SYDNEY': '2000', 'WOOLLOOMOOLOO': '2007/2010/2011', 
                       'POTTS POINT': '2007/2010/2011', 'PYRMONT': '2009', 
                       'DARLINGHURST': '2007/2010/2011', 'ULTIMO': '2007/2010/2011', 
                       'SURRY HILLS': '2007/2010/2011', 'ELIZABETH BAY': '2007/2010/2011', 
                       'BARANGAROO': '2000', 'HAYMARKET': '2000', 'RUSHCUTTERS BAY': '2007/2010/2011', 
                       'MILLERS POINT': '2000', 'WALSH BAY': '2000', 'THE ROCKS': '2000'}

suburb_list = ['SYDNEY', 'WOOLLOOMOOLOO', 'POTTS POINT', 'PYRMONT',
       'DARLINGHURST', 'ULTIMO', 'SURRY HILLS', 'ELIZABETH BAY',
       'BARANGAROO', 'HAYMARKET', 'RUSHCUTTERS BAY', 'MILLERS POINT',
       'WALSH BAY', 'THE ROCKS']
property_type_list = ['Appartment/House', 'Studio']

#collect input data
suburb = st.sidebar.selectbox('Select Suburb',suburb_list)
postcode = suburb_mapping_dict.get(suburb)
property_type = st.sidebar.selectbox('Select Property Type',property_type_list)
if property_type == 'Appartment/House':
    bedroom = st.sidebar.slider('Select number of Bedrooms',1,4,1)
    bathroom = st.sidebar.slider('Select number of Bathrooms',1,3,1)    
else:
    bathroom = 1
    bedroom = 0
parking = st.sidebar.slider('Select number of Parking Spaces',0,2,1)


#dictionary to hold variables for model input
model_input_dict = {'Bed':bedroom,'Bath':bathroom,'Parking':parking,
            'Postcode_2007/2010/2011':0,'Postcode_2009':0}

#update one hot encoded variables
if postcode == '2007/2010/2011':
    model_input_dict['Postcode_2007/2010/2011'] = 1
if postcode == '2009':
    model_input_dict['Postcode_2009'] = 1

#convert dictionary to dataframe for model input
input_df =pd.DataFrame(model_input_dict,index=[0]) 

#load model
model = joblib.load('regression_model4')

#get price estimate
price_estimate = model.predict(input_df)[0]

#select single of plural for parking spaces
space = 'space'
if parking == 2:
    space = 'spaces'
if property_type == 'Studio':
    st.write(f'The estimated weekly rent for a Studio appartment with {parking} parking {space} in {suburb} is: ${round(price_estimate)}')
else:
    st.write(f'The estimated weekly rent for a {bedroom} bedroom, {bathroom} bathroom appartment/house with {parking} parking {space} in {suburb} is:')

#with st.container():
col1, col2, col3 = st.columns(3)
col2.header(f':green[${round(price_estimate)}]',anchor=False)