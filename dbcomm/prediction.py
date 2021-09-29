# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import tempfile
import tensorflow as tf

def SmartBagRecommendations(user_number):
  with tempfile.TemporaryDirectory() as tmp:
    path = '/home/yellowsubmarine/GridRESTApi/dbcomm/Flipkart Grid/TFRS_model'

    # Load it back; can also be done in TensorFlow Serving.
    loaded = tf.saved_model.load(path)

    # Pass a user id in, get top predicted products back.
    scores, titles = loaded([user_number])
    
    # Loading the orders data frame
    ords = pd.read_csv('/home/yellowsubmarine/GridRESTApi/dbcomm/Flipkart Grid/orders.csv').drop(columns = ['Unnamed: 0'])
    ords['User'] = ords['User'].astype(str)
    ords['Item ID'] = ords['Item ID'].astype(str)

    # Loading the products data frame
    products = pd.read_csv('/home/yellowsubmarine/GridRESTApi/dbcomm/Flipkart Grid/products.csv').drop(columns = ['Unnamed: 0']) 
    products['Item ID'] = products['Item ID'].astype(str)

    rec_ids = []
    for rec in titles[0]:
      rec_ids.append(products[products['Item ID'] == np.array(rec).astype(str)].values[0][0])

    recommendations = {}
    if len(ords[ords['User'] == user_number]) > 0:
      # Initializing the dictionary of labeled predictions

      # Adding model's top 10 predictions to the 'top' list
      recommendations['Top 10 Predicted:'] = rec_ids

      # Adding the 2 most frequently ordered products
      user_data = ords[ords.User == user_number]
      frequent = user_data['Item ID'].value_counts().index.tolist()[:3]
      values = list(user_data['Item ID'].value_counts())
      recommendations['Frequently Bought'] = frequent

      # Adding discount/larger/sponsored product recommendations
      recommendations['Best Deals'], recommendations['Family Deals'], recommendations['Sponsored Deals'] = [], [], []
      user_data = user_data.merge(products, on = 'Item ID')
      freq_types = user_data['Type'].value_counts().index.tolist()[:3]
      for ptype in freq_types:
        subset = products[products['Type'] == ptype]
        disc = str(subset['Discount'].idxmax())
        biggest = str(subset['Quantity'].idxmax())
        spons = subset[subset['Sponsored'] == True].values
        if subset[subset['Item ID'] == disc].values[0][-3]: recommendations['Best Deals'].append(disc)
        recommendations['Family Deals'].append(biggest)
        if len(spons) > 0: recommendations['Sponsored Deals'].append(spons[0][0])

    else:
      recommendations = {'Predicted by Model': rec_ids}
      pop = ords[['Order ID', 'Item ID']].groupby(by = 'Item ID').count().sort_values(by = 'Order ID', ascending = False).index.tolist()[:10]
      recommendations['Top 10 frequently bought'] = pop
    return recommendations

def FrontPage():
  # Loading the orders data frame
  ords = pd.read_csv('/home/yellowsubmarine/GridRESTApi/dbcomm/Flipkart Grid/orders.csv').drop(columns = ['Unnamed: 0'])
  ords['User'] = ords['User'].astype(str)
  ords['Item ID'] = ords['Item ID'].astype(str)

  # Loading the products data frame
  products = pd.read_csv('/home/yellowsubmarine/GridRESTApi/dbcomm/Flipkart Grid/products.csv').drop(columns = ['Unnamed: 0']) 
  products['Item ID'] = products['Item ID'].astype(str)

  display = {}
  
  # Most Purchased Products
  display['Popular'] = ords[['Order ID', 'Item ID']].groupby(by = 'Item ID').count().sort_values(by = 'Order ID', ascending = False).index.tolist()[:10]
  
  # Biggest Discounts
  discounts = products.nlargest(10, ['Discount']).values
  display['Top Discounts'] = [i[0] for i in discounts]

  # Sponsored products
  sponsored = products[products['Sponsored'] == True].sample(frac = 1).values[:10]
  display['Sponsored'] = [i[0] for i in sponsored]

  return display
