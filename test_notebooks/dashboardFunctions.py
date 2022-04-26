'''
WORK IN PROGRESS
===================================================================================
'''

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import glob
import os
import random
from tqdm import tqdm
import cv2 as cv
import PIL
from PIL import Image
import plotly.express as px
from IPython import display
 
# Data for the most up to date transaction information and the full history of calls to the CryptoPunks contract by date. (Sourced from Etherscan.io)

transactions_df = pd.read_csv('data/transactions.csv', index_col = 'DateTime', parse_dates = True, infer_datetime_format = True, low_memory=False)
transactions_df = transactions_df[['Txhash', 'Blockno', 'From','To', 'Value_IN(ETH)', 'TxnFee(ETH)', 'TxnFee(USD)', 'Historical $Price/Eth', 'Method']]
columns = ['txn_hash', 'block', 'from', 'to', 'value_eth', 'txn_fee_eth', 'txn_fee_usd', 'price', 'contract_call']
transactions_df.columns = columns

# Data for transaction history with Cryptopunk attributes. (Sourced from Kaggle) 

tx_attributes_df = pd.read_json("data/txn_history-2021-10-07.jsonl", lines=True)
tx_attributes_df['date'] = pd.to_datetime(tx_attributes_df.date)
tx_attributes_df = tx_attributes_df[["txn_type", "from", "to", "date", "eth", "punk_id", "type", "accessories"]]
tx_attributes_df = tx_attributes_df.explode("type")
tx_attributes_df['num_attributes'] = tx_attributes_df.accessories.apply(lambda x: len(x))

# Data for Artwork Characteristics
punks = pd.read_csv('data/attributes.csv', index_col = 'id')

# Adding image urls (Sourced from Larva Labs. Images for all CryptoPunks can also be found in this notebook's repository [./data/imgs]
url_base = 'https://www.larvalabs.com/cryptopunks/details/'
urls = []
for i in range(10000):
    url = url_base + str(i)
    urls.append(url)
punks['image_url'] = urls

# Building transaction data with punk IDs
punks_transfers = pd.DataFrame(tx_attributes_df[tx_attributes_df.txn_type == 'Transfer'])[['date', 'punk_id']].set_index(['punk_id', 'date'])

# Building sale data with punk IDs
punks_sales = pd.DataFrame(tx_attributes_df[tx_attributes_df.txn_type == 'Sold'])[['date', 'punk_id', 'eth', 'from', 'to']].set_index(['punk_id', 'date'])

'''
============================================================================================
Visualization Functions for Punks Data
============================================================================================
'''

def punks_by_type():
    fig = px.bar(tx_attributes_df.drop_duplicates("punk_id")['type'].value_counts().rename_axis('type').reset_index(name='counts'),
             x="type", y="counts", color="type", title="Cryptopunk Type Counts", width = 1024, height = 500)
    return fig

def max_price_per_type():
    fig = px.bar(tx_attributes_df[tx_attributes_df.txn_type == 'Sold'].groupby("type").agg({"eth": "max"}).sort_values(by="eth").reset_index('type'),
             x="type", y="eth", color="type", title="CryptoPunk Max Sold Price by Type", width = 1024, height = 500)
    return fig

def attribute_dist():
    fig = px.bar(tx_attributes_df.drop_duplicates("punk_id")['num_attributes'].value_counts().rename_axis('num_attributes').reset_index(name='counts'),
             x="num_attributes", y="counts", color = 'counts', title="Cryptopunk Distribution of Number of Attributes", width = 1024, height = 500)
    return fig

def price_num_attributes_human():
    fig = px.bar(tx_attributes_df[(tx_attributes_df.txn_type == "Sold") & ((tx_attributes_df.type == "Female") | (tx_attributes_df.type == "Male"))].groupby("num_attributes").agg({"eth": "mean"}).reset_index("num_attributes"),
             x="num_attributes", y="eth", color="eth", title="Cryptopunk Price per Number of Attributes of Human Punks Only", 
                 labels = {'num_attributes': 'Number of Attributes', 'eth':'Price in ETH'}, width = 512, height = 500)
    return fig
    
def price_num_attributes_zombie():
    fig = px.bar(tx_attributes_df[(tx_attributes_df.txn_type == "Sold") & (tx_attributes_df.type == "Zombie")].groupby("num_attributes").agg({"eth": "mean"}).reset_index("num_attributes"),
             x="num_attributes", y="eth", color="eth", title="Cryptopunk Price per Number of Attributes of Zombie Punks Only", 
                 labels = {'num_attributes': 'Number of Attributes', 'eth':'Price in ETH'}, width = 512, height = 500)
    return fig
    
def price_num_attributes_ape():
    fig = px.bar(tx_attributes_df[(tx_attributes_df.txn_type == "Sold") & (tx_attributes_df.type == "Ape")].groupby("num_attributes").agg({"eth": "mean"}).reset_index("num_attributes"),
             x="num_attributes", y="eth", color="eth", title="Cryptopunk Price per Number of Attributes of Ape Punks Only", 
                 labels = {'num_attributes': 'Number of Attributes', 'eth':'Price in ETH'}, width = 512, height = 500)
    return fig
    
def price_num_attributes_alien():
    fig = px.bar(tx_attributes_df[(tx_attributes_df.txn_type == "Sold") & (tx_attributes_df.type == "Alien")].groupby("num_attributes").agg({"eth": "mean"}).reset_index("num_attributes"),
             x="num_attributes", y="eth", color="eth", title="Cryptopunk Price per Number of Attributes of Alien Punks Only",
                 labels = {'num_attributes': 'Number of Attributes', 'eth':'Price in ETH'},width = 512, height = 500)
    return fig

'''
============================================================================================
Visualization Functions for Transactions Data
============================================================================================
'''

'''
============================================================================================
Visualization Function for Punk Images Preview
============================================================================================
'''

def punk_gallery():
    # look at 225 samples
    
    no_plots = 15*15 # Define number of rows and cols
    
    images = glob.glob("data/imgs/*.png") # Define path to images
    
    fig = plt.figure()
    
    plt.rcParams['figure.figsize'] = (22.3, 22.3)
    plt.subplots_adjust(wspace=0, hspace=0)

    for idx,image in enumerate(images[:no_plots]):
        sample_img = cv.imread(image)
        plt.subplot(15, 15, idx+1)
        plt.axis('off')
        plt.imshow(cv.cvtColor(sample_img,cv.COLOR_BGR2RGB)) #covert color space
    
    plt.close(fig)
    
    return pn.Pane.Matplotlib(fig)