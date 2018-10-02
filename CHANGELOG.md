# CHANGELOG

## Unreleased

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
