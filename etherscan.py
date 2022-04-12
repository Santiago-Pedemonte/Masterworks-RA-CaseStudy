import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

url = 'https://api.etherscan.io/api?'
contract_address = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB' # CryptoPunks contract address.
load_dotenv('es_key.env')
key = os.getenv('api_key')

# Read in data used for `get_txs_punk`:

tx_attributes_df = pd.read_json("data/txn_history-2021-10-07.jsonl", lines=True)
tx_attributes_df['date'] = pd.to_datetime(tx_attributes_df.date)
tx_attributes_df = tx_attributes_df[["txn_type", "from", "to", "date", "eth", "punk_id", "type", "accessories"]]
tx_attributes_df = tx_attributes_df.explode("type")
tx_attributes_df['num_attributes'] = tx_attributes_df.accessories.apply(lambda x: len(x))


def get_punk_balance(address, contract_address = contract_address, key = key):
    '''
    Get number of punks for a specific address using Etherscan.io API.
    
    Parameters:
    - address
    - contract_address: Defaults to CryptoPunks contract address if none is given.
    
    Returns:
    - Integer with number of ERC20 token balance for address (Number of CryptoPunks that belong to an address, by default).
    
    '''
    request_url = url + f'module=account&action=tokenbalance' \
                        f'&contractaddress={contract_address}' \
                        f'&address={address}' \
                        f'&tag=latest' \
                        f'&apikey={key}' 
    response = requests.get(request_url)
    response = response.json()
    return int(response['result'])

def get_txs_punk(punk_id, start = None, end = None):
    '''
    
    Get all transactions info for a specific punk ID.
    
    Parameters:
    - punk_id: The integer for the CryptoPunk ID.
    - start: String to set a start date for transaction history. Optional- Defaults to None.
    - end: String to set an end date for transaction history. Optional- Defaults to None.
    
    Returns:
    - DataFrame object with columns for transaction type and value in Ether and index for the Punk ID and Date.
    
    '''
    punk_tx = tx_attributes_df[tx_attributes_df['punk_id'] == punk_id]
    punk_tx = punk_tx[['date', 'txn_type', 'eth', 'punk_id', 'from', 'to']]
    punk_tx.set_index(['punk_id', 'date'], inplace=True)
    if start and end:
        return punk_tx.loc[start:end]
    elif start and not end:
        return punk_tx.loc[start:]
    elif end and not start:
        return punk_tx.loc[:end]
    elif not end and not start:
        return punk_tx

    return tx_attributes_df[tx_attributes_df['punk_id'] == punk_id]

    
def get_txs_address(address, contract_address = contract_address, 
                    start = '0', end = '14561810', offset = '100', sort= 'desc', key = key):
    '''
    
    Usage:
    
    - ERC-20 transfers from an address, specify the address parameter.
    - ERC-20 transfers from a contract address, specify the contract address parameter.
    - ERC-20 transfers from an address filtered by a token contract, specify both address
             and contract address parameters.
    
    Parameters:
    - address: The string representing the address to check for transactions.
    - contract_address: The string representing the token contract address to check for transactions. Defaults to CryptoPunks contract.
    - start: The integer block number to start searching for transactions. Defaults to 0.
    - end: The integer block number to stop searching for transactions. Defaults to 14561810 [Mined on April 11, 2022]
    - sort: The sorting preference, use asc to sort by ascending [oldest at the top] and desc to sort by descending [most recent at the top].
    
    Returns:
    - DataFrame object with 
    
    '''
    request_url = url + f'module=account&action=tokentx' \
                        f'&contractaddress={contract_address}' \
                        f'&address={address}' \
                        f'&page=1' \
                        f'&offset={offset}' \
                        f'&startblock={str(start)}' \
                        f'&endblock={str(end)}' \
                        f'&sort={sort}' \
                        f'&apikey={key}'
    response = requests.get(request_url)
    response = response.json()
    return pd.DataFrame(response['result'])

def get_txn_from_hash(txn_hash, gas_in_wei = True, key = key):
    '''
    
    Get information for a transaction through its transaction hash.
    
    Parameters:
    - txn_hash: String for the transaction hash.
    - gas_in_wei: Boolean. If set to `True`, gas prices will be converted to Ether.
    
    Returns:
    - Dictionary with Block Hash, Block Number, Transaction Index, Nonce, Value, & Gas.
    
    '''
    request_url = url + 'module=proxy&action=eth_getTransactionByHash' \
                        f'&txhash={txn_hash}' \
                        f'&apikey={key}'
    response = requests.get(request_url)
    response = response.json()
    data = response['result']
    wei_to_eth = 1000000000000000000
    data['blockNumber'] = int(data['blockNumber'], 16)
    data['transactionIndex'] = int(data['transactionIndex'], 16)
    data['nonce'] = int(data['nonce'], 16)
    data['value'] = round(int(data['value'], 16) / wei_to_eth, 6)
    if gas_in_wei:
        data['gas'] = int(data['gas'], 16)
        data['gasPrice'] = int(data['gasPrice'], 16)
    elif not gas_in_wei:
        data['gas'] = round(int(data['gas'], 16), 6)
        data['gasPrice'] = round(int(data['gasPrice'], 16), 6)
    return data
    