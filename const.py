MIN_SLEEP = 100
MAX_SLEEP = 300

RPC = 'https://rpc.ankr.com/eth'

VOTE_URL = 'https://seq.snapshot.org'
GRAPHQL_URL = 'https://hub.snapshot.org/graphql'
GET_SCORE_URL = 'https://score.snapshot.org'

DOMAIN = {"name": "snapshot", "version": "0.1.4"}

TYPES = {"Vote": [{"name": "from", "type": "address"}, {"name": "space", "type": "string"},
                  {"name": "timestamp", "type": "uint64"}, {"name": "proposal", "type": "bytes32"},
                  {"name": "choice", "type": "uint32"}, {"name": "reason", "type": "string"},
                  {"name": "app", "type": "string"}, {"name": "metadata", "type": "string"}]}

PROXY_URL = ''
PROXY_USERNAME = ''
PROXY_PASS = ''

PROXIES = {
    'http': f'http://{PROXY_USERNAME}:{PROXY_PASS}@{PROXY_URL}',
    'https': f'http://{PROXY_USERNAME}:{PROXY_PASS}@{PROXY_URL}'
}

GET_PROPOSALS_QUERY = 'query Proposals($first: Int!, $skip: Int!, $state: String!, $space: String, $space_in: [' \
                      'String], $author_in: [String], $title_contains: String, $space_verified: Boolean, ' \
                      '$flagged: Boolean) {\n  proposals(\n    first: $first\n    skip: $skip\n    where: {space: ' \
                      '$space, state: $state, space_in: $space_in, author_in: $author_in, title_contains: ' \
                      '$title_contains, space_verified: $space_verified, flagged: $flagged}\n  ) {\n    id\n    ' \
                      'ipfs\n    title\n    body\n    start\n    end\n    state\n    author\n    created\n    ' \
                      'choices\n    space {\n      id\n      name\n      members\n      avatar\n      symbol\n      ' \
                      'verified\n      turbo\n      plugins\n    }\n    scores_state\n    scores_total\n    scores\n  ' \
                      '  votes\n    quorum\n    symbol\n    flagged\n  }\n} '
GET_PROPOSAL_INFO_QUERY = "query Proposal($id: String!) {\n  proposal(id: $id) {\n    id\n    ipfs\n    title\n    " \
                          "body\n    discussion\n    choices\n    start\n    end\n    snapshot\n    state\n    " \
                          "author\n    created\n    plugins\n    network\n    type\n    quorum\n    symbol\n    " \
                          "privacy\n    validation {\n      name\n      params\n    }\n    strategies {\n      name\n " \
                          "     network\n      params\n    }\n    space {\n      id\n      name\n    }\n    " \
                          "scores_state\n    scores\n    scores_by_strategy\n    scores_total\n    votes\n    " \
                          "flagged\n  }\n} "
GET_FOLLOWS_PAYLOAD_QUERY = "query Follows($space_in: [String], $follower_in: [String]) {\n  follows(where: {" \
                            "space_in: $space_in, follower_in: $follower_in}, first: 500) {\n    id\n    follower\n   " \
                            " space {\n      id\n    }\n  }\n} "

VOTING_POWER = {
    'stgdao.eth': [{"name": "erc20-balance-of-with-delegation", "network": "1",
                    "params": {"symbol": "sveSTG", "address": "0x9485DbDa44B279311e3eEe374CED60b5364A97d9",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "1",
                    "params": {"symbol": "veSTG", "address": "0x0e42acBD23FAee03249DAFF896b78d7e79fBD58E",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "56",
                    "params": {"symbol": "veSTG", "address": "0xD4888870C8686c748232719051b677791dBDa26D",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "43114",
                    "params": {"symbol": "veSTG", "address": "0xCa0F57D295bbcE554DA2c07b005b7d6565a58fCE",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "137",
                    "params": {"symbol": "veSTG", "address": "0x3AB2DA31bBD886A7eDF68a6b60D3CDe657D3A15D",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "10",
                    "params": {"symbol": "veSTG", "address": "0x43d2761ed16C89A2C4342e2B16A3C61Ccf88f05B",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "42161",
                    "params": {"symbol": "veSTG", "address": "0xfBd849E6007f9BC3CC2D6Eb159c045B8dc660268",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}},
                   {"name": "erc20-balance-of-with-delegation", "network": "250",
                    "params": {"symbol": "veSTG", "address": "0x933421675cDC8c280e5F21f0e061E77849293dba",
                               "decimals": 18, "delegationSpace": "stgdao.eth", "delegationNetwork": "1"}}],
}
