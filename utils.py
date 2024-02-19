import time
import requests
import json

from const import DOMAIN, TYPES, VOTE_URL, PROXIES, GET_PROPOSALS_QUERY, GRAPHQL_URL, \
    GET_PROPOSAL_INFO_QUERY, VOTING_POWER, GET_SCORE_URL, GET_FOLLOWS_PAYLOAD_QUERY
from pyuseragents import random as random_user_agent
from eth_account.messages import encode_typed_data


def get_message(space: str, proposal: str, choice: int, address: str, timestamp: int = int(time.time())):
    return {
        "space": space,
        "proposal": proposal,
        "choice": choice,
        "app": "snapshot", "reason": "", "metadata": "{}",
        "from": address,
        "timestamp": timestamp
    }


def get_signable(message):
    return encode_typed_data(
        domain_data=DOMAIN,
        message_types=TYPES,
        message_data=message
    )


def get_vote_payload(address, sig, message):
    return {
        "address": address,
        "sig": sig,
        "data": {
            "domain": DOMAIN,
            "types": TYPES,
            "message": message
        }
    }


def get_proposals_payload(space):
    return {
        "operationName": "Proposals",
        "variables": {
            "first": 6,
            "skip": 0,
            "space_in": [space],
            "state": "all",
            "title_contains": "",
            "flagged": False
        },
        "query": GET_PROPOSALS_QUERY
    }


def get_proposals(space):
    response = requests.post(GRAPHQL_URL, json=get_proposals_payload(space), proxies=PROXIES).text
    proposals = json.loads(response)['data']['proposals']
    active_proposals = [el for el in proposals if el['state'] == 'active']
    return active_proposals


def get_proposal_info_payload(proposal_id):
    return {
        "operationName": "Proposal",
        "variables": {"id": proposal_id},
        "query": GET_PROPOSAL_INFO_QUERY
    }


def get_proposal_info(proposal_id):
    response = requests.post(GRAPHQL_URL, json=get_proposal_info_payload(proposal_id), proxies=PROXIES).text
    proposal = json.loads(response)['data']['proposal']
    return proposal


def get_voting_power_payload(address, space, snapshot):
    return {
        "jsonrpc": "2.0",
        "method": "get_vp",
        "params": {
            "address": address,
            "network": "1",
            "strategies": VOTING_POWER[space],
            "snapshot": snapshot,
            "space": space,
            "delegation": False
        }
    }


def get_voting_power(address, space, snapshot):
    response = requests.post(GET_SCORE_URL, json=get_voting_power_payload(address, space, snapshot), proxies=PROXIES).text
    vp = json.loads(response)['result']['vp']
    return float(vp)


def follow_check_payload(address):
    return {
        "operationName": "Follows",
        "variables": {
            "follower_in": address
        },
        "query": GET_FOLLOWS_PAYLOAD_QUERY
    }


def get_follows(address):
    response = requests.post(GRAPHQL_URL, json=follow_check_payload(address), proxies=PROXIES).text
    follows = json.loads(response)['data']['follows']
    spaces = [follow['space']['id'] for follow in follows]
    return spaces


def get_data_size(message):
    return len(str(message).replace(' ', ''))


def get_headers(payload):
    return {
        'Accept': 'application/json',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.9",
        'Content-Length': str(get_data_size(payload)),
        'Content-Type': 'application/json',
        "Origin": "https://snapshot.org",
        "Referer": "https://snapshot.org/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        'User-Agent': str(random_user_agent()),
    }


def vote(account_evm, space, proposal, choice):
    address = account_evm.address

    message = get_message(
        space=space,
        proposal=proposal,
        choice=choice,
        address=address)
    signable = get_signable(message)
    sig = account_evm.sign_message(signable).signature.hex()

    payload = get_vote_payload(address, sig, message)
    headers = get_headers(payload)

    requests.post(VOTE_URL, headers=headers, json=payload, proxies=PROXIES)
