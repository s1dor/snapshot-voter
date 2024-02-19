from logger import get_logger
import random
import time

from utils import vote, get_proposals, get_proposal_info, get_voting_power, get_follows
from const import RPC, MIN_SLEEP, MAX_SLEEP
from web3 import Web3

logger = get_logger()
w3 = Web3(Web3.HTTPProvider(RPC))


def doWork(pkey, space, proposal, num, total, retries=3):
    try:
        account_evm = w3.eth.account.from_key(pkey)
        address = account_evm.address

        proposal_info = get_proposal_info(proposal)
        title = proposal_info['title']

        logger.info(f'[{num}/{total}] WALLET:{address} SPACE:{space} PROPOSAL:{title}')

        if space not in get_follows(address):
            logger.info(f'[{num}/{total}] Space {space} is not followed')

        snapshot = proposal_info['snapshot']
        vp = get_voting_power(address, space, snapshot)

        if vp > 0:
            scores = proposal_info['scores']
            choices = proposal_info['choices']
            choice = scores.index(max(scores))
            logger.info(f'[{num}/{total}] VOTING: VP:{vp} | CHOICE:{choices[choice]}')
            vote(account_evm, space, proposal, choice + 1)
            return True
        else:
            logger.warn(f'[{num}/{total}] NO VOTING POWER, SKIPPING')
            return False
    except Exception as e:
        if retries > 0:
            logger.warn(f'[{num}/{total}] FAILED, RETRYING')
            return doWork(pkey, space, proposal, num, total, retries - 1)
        else:
            logger.error(f'[{num}/{total}] FAILED, SKIPPING')
            return False


with open("pkeys.txt", "r") as f:
    pkeys = [row.strip() for row in f]

with open("spaces.txt", "r") as f:
    spaces = [row.strip() for row in f]

proposals = []
for space in spaces:
    proposal_ids = [el['id'] for el in get_proposals(space)]
    for proposal_id in proposal_ids:
        proposals.append((space, proposal_id))

wallet_proposals = []
for pkey in pkeys:
    for proposal in proposals:
        wallet_proposals.append((pkey, proposal[0], proposal[1]))

total = len(wallet_proposals)
current = 1
random.shuffle(wallet_proposals)
for wp in wallet_proposals:
    if doWork(wp[0], wp[1], wp[2], current, total):
        to_sleep = random.randint(MIN_SLEEP, MAX_SLEEP)
        logger.info(f'Sleeping for {to_sleep}s...')
        time.sleep(to_sleep)
    current += 1
