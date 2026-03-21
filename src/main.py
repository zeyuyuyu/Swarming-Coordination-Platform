import asyncio
import random

class Agent:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = neighbors
        self.state = 'IDLE'
        self.vote = None

async def propose_vote(agent):
    agent.state = 'PROPOSING'
    proposal = random.randint(0, 1)
    agent.vote = proposal
    print(f'Agent {agent.id} proposed vote: {proposal}')
    await asyncio.gather(*[vote_on_proposal(neighbor, proposal) for neighbor in agent.neighbors])
    agent.state = 'IDLE'

async def vote_on_proposal(agent, proposal):
    agent.state = 'VOTING'
    await asyncio.sleep(random.uniform(0.1, 1))
    agent.vote = proposal
    print(f'Agent {agent.id} voted: {proposal}')
    agent.state = 'IDLE'

async def main():
    agents = [
        Agent(1, [2, 3, 4]),
        Agent(2, [1, 3, 5]),
        Agent(3, [1, 2, 4, 5]),
        Agent(4, [1, 3, 5]),
        Agent(5, [2, 3, 4])
    ]

    while True:
        await asyncio.gather(*[propose_vote(agent) for agent in agents])
        print('Voting round complete')

if __name__ == '__main__':
    asyncio.run(main())
