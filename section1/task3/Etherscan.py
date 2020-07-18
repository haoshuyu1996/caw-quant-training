from etherscan.accounts import Account
from etherscan.blocks import Blocks
from etherscan.contracts import Contract
from etherscan.proxies import Proxies
from etherscan.stats import Stats
from etherscan.tokens import Tokens
from etherscan.transactions import Transactions
import os
import json

# Get API Key
path = os.getcwd()
with open(os.path.join(path, 'api_key.json'), mode='r') as key_file:
    key = json.loads(key_file.read())['key']

# Accounts

address = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
api = Account(address=address, api_key=key)

balance = api.get_balance()
transaction = api.get_transaction_page(
    page=1, offset=10000, sort='des')  # erc20 = True)
transactions = api.get_all_transactions(
    offset=10000, sort='asc', internal=False)
block = api.get_blocks_mined_page(page=1, offset=1, blocktype='blocks')
blocks = api.get_all_blocks_mined(offset=10, blocktype='uncles')

# address = ['0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
#           '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a']
#
#api = Account(address=address, api_key=key)
#balances = api.get_balance_multiple()
# print(balances)

# Blocks

api = Blocks(api_key=key)

reward = api.get_block_reward(2165403)

# Contracts

address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
api = Contract(address=address, api_key=key)

abi = api.get_abi()
sourcecode = api.get_sourcecode()

# Proxies

number = 10453272
block_numb = '0x9f8118'
address = '0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c'
TX_HASH = '0xb03d4625fd433ad05f036abdc895a1837a7d838ed39f970db69e7d832e41205d'
index = '0x0'
api = Proxies(api_key=key)

price = api.gas_price()
block = api.get_block_by_number(number)
tx_count = api.get_block_transaction_count_by_number(block_number=block_numb)
code = api.get_code(address)
block0 = api.get_most_recent_block()
value = api.get_storage_at(address, 0x0)
transaction = api.get_transaction_by_blocknumber_index(block_number=block_numb,
                                                       index=index)
transaction = api.get_transaction_by_hash(tx_hash=TX_HASH)
count = api.get_transaction_count(address)
receipt = api.get_transaction_receipt(TX_HASH)
uncles = api.get_uncle_by_blocknumber_index(block_number=block_numb,
                                            index=index)

# Stats

api = Stats(api_key=key)

last_price = api.get_ether_last_price()
supply = api.get_total_ether_supply()

# Tokens

address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
api = Tokens(contract_address=contract_address,
             api_key=key)

balance = api.get_token_balance(address=address)
supply = api.get_total_supply()

# Transactions

TX_HASH = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'
api = Transactions(api_key=key)

status = api.get_status(tx_hash=TX_HASH)
receipt_status = api.get_tx_receipt_status(tx_hash=TX_HASH)
