from datetime import datetime, timedelta
from decimal import Decimal
import rlp
import web3
import secrets
import hashlib
from ethereum.transactions import Transaction

from clove.network.base import BaseNetwork


def left_pad(s, l=64):
    while len(s) < l:
        s = '0' + s
    return s


def right_pad(s, l=64):
    while len(s) < l:
        s = s + '0'
    return s

def check_address(a, m=None):
    assert len(a) == 42 or len(a) == 40, m
    if len(a) == 42:
        a = a[2:]
    int(a, 16)
    return a

def generate_secret(bytes=32):
    return secrets.token_bytes(bytes)

def method_id(m):
    return web3.Web3.sha3(m.encode('ascii'))[2:10]

# Method IDs for transaction building. Built on the fly for developer reference (keeping away from magics)
PARTICIPATE = method_id('participate(uint256,bytes20,address)')
REFUND = method_id('refund(bytes20)')
REDEEM = method_id('redeem(bytes32,bytes20)')
INITIATE = method_id('initiate(uint256,bytes20,address)')
SWAPS = method_id('swaps(bytes20)')

# Gas limits for each method. A.k.a the transaction cost. Manually calculated via MyEtherWallet on the deployed
# contract to the Kovan network.
INITIATE_GAS_LIMIT = 0

class Ethereum(BaseNetwork):
    """
    Class with all the necessary ETH network information and transaction building.
    """
    name = 'ethereum'
    symbols = ('ETH',)
    seeds = (
        'https://infura.io/WsUXSFPvO9t86xDAAhNi',
    )
    port = None

    # Contract is static on Ethereum rather than having to be built each time like on Bitcoin
    web3_connection = web3.Web3.HTTPProvider(seeds[0])
    contract_address = '0x0'

    @staticmethod
    # will return the transactional payload which will just be a transcation against the smart contract we deployed to kovan
    # aka, the initiate transaction
    # initiate (uint _refundTime,bytes20 _hashedSecret,address _participant)
    def atomic_swap_contract(recipient_address: str,
                             secret: bytes,
                             hours_to_expiration: int=24,
                             ):

        recipient_address = check_address(recipient_address, 'Provided recipient address is not properly formatted.')

        # test if the secret is bytes32 compatible
        assert len(secret) == 32, 'Secret provided must be 32 bytes. Use secrets.token_bytes(32).'
        int(secret.hex(), 16)

        h = hashlib.new('ripemd160')
        h.update(secret)
        secret_hash = h.digest().hex()

        unix_time_until_expiration = int((datetime.now() + timedelta(hours=hours_to_expiration)).timestamp())
        expiration_arg = left_pad(hex(unix_time_until_expiration)[2:])
        recipient_arg = left_pad(recipient_address)
        secret_arg = right_pad(str(secret_hash))

        swap = '{}{}{}{}'.format(INITIATE, expiration_arg, secret_arg, recipient_arg)
        return web3.Web3.toAscii(swap), s

    @staticmethod
    def redeem_transaction(secret: bytes):
        # test if the secret is bytes20 compatible
        assert len(secret) == 32, 'Secret provided must be 32 bytes. Use secrets.token_bytes(32).'
        int(secret.hex(), 16)

        secret_hex = secret.hex()

        h = hashlib.new('ripemd160')
        h.update(secret)
        secret_hash = h.digest().hex()

        secret_hex_arg = right_pad(secret_hex)
        secret_hash_arg = right_pad(secret_hash)

        redeem = '{}{}{}'.format(REDEEM, secret_hex, secret_hash)
        return web3.Web3.toAscii(redeem)

    @staticmethod
    def refund_transaction(secret_hash: bytes):
        assert len(secret_hash) == 20, 'Secret hash provided must be 20 bytes.'
        int(secret_hash.hex(), 16)
        return web3.Web3.toAscii(right_pad(secret_hash.hex()))

# Helper for building transactions in Ethereum. Super simple.
def build_tx(sender_address, recipient_address, payload, value, gas_limit, sender_private_key, gas_price):
    tx = Transaction(
        nonce=Ethereum.web3_connection.eth.getTransactionCount(sender_address),
        gasprice=gas_price,
        to=recipient_address,
        startgas=gas_limit,
        data=payload,
        value=value
    )

    tx.sign(sender_private_key)
    raw_tx = rlp.encode(tx)
    raw_tx_hex = web3.Web3.toHex(raw_tx)

    # send it across infura
    return Ethereum.web3_connection.eth.sendRawTransaction(raw_tx_hex)


class TestNetKovanEthereum(Ethereum):
    """
    Infura connector to the Kovan network
    """
    name = 'kovan-ethereum'
    seeds = (
        'https://kovan.infura.io/WsUXSFPvO9t86xDAAhNi',
    )
    port = None

    contract_address = '0x0'

s = generate_secret()
print(Ethereum.atomic_swap_contract('0x0123456789012345678901234567890123456789', '0x0123456789012345678901234567890123456789', '0x0123456789012345678901234567890123456789', s))
