# Cryptopunks Case Study
Santiago Pedemonte

### Research Analyst (NFT Market)

This case study intends to test a candidate's ability to analyze the price performance of an artist's NFT project or collection of works by demonstrating an ability to work with APIs and perform data analysis on the NFT Market.

We highly encourage writing your code in Python 3.7+ on a Jupyter Notebook, making use of the scikit-learn library.
 
#### Data Collection

- Identify a collection of NFT works or projects with robust trading activity, such as CryptoPunks or Bored Apes.
- Use an API connected to Etherscan, OpenSea or other platform that tracks NFT transactions to pull in a workable database of the transactions of the selected NFTs from step 1.
- Collect all NFT transactions, store them in a table, and include fields for
  - Artwork characteristics
    - Unique identifier
    - Image URL
    - Traits
  - Transactions characteristics
    - Sale Date
    - Price in ETH and USD (at that time)
    - Bonus: Gas fees
Note that if an artwork has been sold multiple times there will be multiple transactions and artwork characteristics will repeat.
Organize the data collected above in a relational way by splitting them into 2 tables, so that every work has only 1 entry for its characteristics, but potentially numerous entries for its transactions.

#### Data Analysis

- Identify how many of the NFTs in the data you collected have traded more than once.
- Of the NFTs that have traded more than once: 
  - What is the median return 
  - What is the average hold period for those NFTs
  - How many unique buyers and sellers have traded that specific NFT
 
- **Bonus:** Are there any inferences you can make about the impact of the characteristics you selected from 3B that may be correlated with price changes? Open-ended question: How does rarity correlate to price?

