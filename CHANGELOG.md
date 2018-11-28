# CHANGELOG

## v1.2.16

* Ignore tokens without symbol

## v1.2.15

* New Ethereum tokens
* requests version upgrade

## v1.2.14

* Remove Bitcoin Cash from API
* Raise error if token details are not extracted from contract

## v1.2.13

* Speed-up for publishing transactions in networks that use Insight API.

## v1.2.12

* Fix for extracting secret from redeem transaction for Insight API
* More docstrings with usage examples

## v1.2.11

* Switching Bitcoin, BitcoinTestNet, BitcoinCash, BitcoinCashTestNet and Dash to Insight API (from blockcypher)

## v1.2.10

* Switching bitcoin-gold to Insight API
* Marking 23 networks as NoAPI
* Using requests lib for clove requests to external APIs

## v1.2.9

* Generating new wallets based on longer secret
* Fix for auditing non-existing contract in Ethereum

## v1.2.8

* Fix for subdomains in etherscan url

## v1.2.7

* Counting fee moved from Clove API to Clove


## v1.2.6

* Separate adapter classes for each block explorer


## v1.2.5

* Changing SCRIPT_ADDR for Monacoin network


## v1.2.4

* Fix for getting contract balance on MonacoinTestnet


## v1.2.3

* Getting contract balance in Monacoin
* Extracting secret in Monacoin network
* Integration with Monacoin block explorer API (mona.chainseeker.info)
* Showing `transaction_link` in `show_details()` after signing the transaction
* Support for the new networks: EtherGem, Ellaism, Musicoin, Expanse, Ethereum Classic
