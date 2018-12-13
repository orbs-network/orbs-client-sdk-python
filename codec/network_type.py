from enum import Enum


class NetworkType(Enum):
    NETWORK_TYPE_MAIN_NET = 'MAIN_NET'
    NETWORK_TYPE_TEST_NET = 'TEST_NET'


def network_type_encode(network_type: NetworkType) -> int:
    if network_type == NetworkType.NETWORK_TYPE_MAIN_NET.value:
        return 77
    elif network_type == NetworkType.NETWORK_TYPE_TEST_NET.value:
        return 84
    else:
        raise ValueError(f'unsupported NetworkType given: {network_type}')
