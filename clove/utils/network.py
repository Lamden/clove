from bitcoin import GenericParams


def generate_params_object(
    message_start=b'', default_port=None, rpc_port=None,
    dns_seeds=(), base58_prefixes={}, max_money=None, genesis_block=None,
    proof_of_work_limit=None, subsidy_halving_interval=None, name=None
) -> GenericParams:

    params_obj = GenericParams()
    params_obj.MESSAGE_START = message_start
    params_obj.DEFAULT_PORT = default_port
    params_obj.RPC_PORT = rpc_port
    params_obj.DNS_SEEDS = dns_seeds
    params_obj.BASE58_PREFIXES = base58_prefixes
    params_obj.MAX_MONEY = max_money
    params_obj.GENESIS_BLOCK = genesis_block
    params_obj.PROOF_OF_WORK_LIMIT = proof_of_work_limit
    params_obj.SUBSIDY_HALVING_INTERVAL = subsidy_halving_interval
    params_obj.NAME = name

    return params_obj
