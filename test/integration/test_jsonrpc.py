import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from archimedd import ArchimedDaemon
from archimed_config import ArchimedConfig


def test_archimedd():
    config_text = ArchimedConfig.slurp_config_file(config.archimed_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009f562f067c612425b64d5a62af8bad8fd0e86241489d2f84241739c1c6a'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000b1b8f7c12c93b9b9d685e5139ad070613ab7da22088bfe18ef94aacc68d'

    creds = ArchimedConfig.get_rpc_creds(config_text, network)
    archimedd = ArchimedDaemon(**creds)
    assert archimedd.rpc_command is not None

    assert hasattr(archimedd, 'rpc_connection')

    # Archimed testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = archimedd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert archimedd.rpc_command('getblockhash', 0) == genesis_hash
