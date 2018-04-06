from decimal import Decimal, localcontext


class TokenMixin(object):

    abi = [{
        "constant": False,
        "inputs": [{
            "name": "_expiration",
            "type": "uint256"
        }, {
            "name": "_hash",
            "type": "bytes20"
        }, {
            "name": "_participant",
            "type": "address"
        }, {
            "name": "_token",
            "type": "address"
        }, {
            "name": "_value",
            "type": "uint256"
        }],
        "name": "initiate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_hash",
            "type": "bytes20"
        }],
        "name": "refund",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_secret",
            "type": "bytes32"
        }],
        "name": "redeem",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    approve_abi = [{
        "constant": False,
        "inputs": [{
            "name": "spender",
            "type": "address"
        }, {
            "name": "tokens",
            "type": "uint256"
        }],
        "name": "approve",
        "outputs": [{
            "name": "success",
            "type": "bool"
        }],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    name = None
    symbol = None
    token_address = None
    decimals = 18

    @classmethod
    def from_namedtuple(cls, token):
        token_instance = cls()
        token_instance.symbol = token.symbol
        token_instance.token_address = token.address
        token_instance.name = token.name
        token_instance.decimals = token.decimals
        return token_instance

    def value_to_base_units(self, value):
        with localcontext() as ctx:
            ctx.prec = 999
            dec_value = Decimal(value=str(value), context=ctx)
            self.validate_precision(dec_value)
            unit_value = Decimal('1' + self.decimals * '0')
            return int(dec_value * unit_value)

    def value_from_base_units(self, value):
        with localcontext() as ctx:
            ctx.prec = 999
            dec_value = Decimal(value=value, context=ctx)
            unit_value = Decimal('1' + self.decimals * '0')
            return dec_value / unit_value

    def validate_precision(self, value: Decimal):
        str_value = f'{value:.50f}'

        frac_part = str_value.split('.')[1]
        precision = len(frac_part.rstrip('0'))
        if precision > self.decimals:
            raise ValueError(f'{self.name} token supports at most {self.decimals} decimal places.')

    def get_value_text(self, value):
        return f'{value:.{self.decimals}f} {self.symbol}'


class EthereumToken(TokenMixin):

    pass


class EthereumTestnetToken(TokenMixin):

    contract_address = '0x7657Ca877Fac31D20528B473162E39B6E152fd2e'
