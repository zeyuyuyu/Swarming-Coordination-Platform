# Swarming-Coordination-Platform main.py

import asyncio
import random

class SwarmAgent:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.state = 'idle'
        self.task_queue = []

    async def coordinate(self):
        while True:
            if self.state == 'idle':
                await self.negotiate_task()
            elif self.state == 'active':
                await self.execute_task()
            else:
                raise ValueError(f'Invalid state for agent {self.id}: {self.state}')
            await asyncio.sleep(random.uniform(0.1, 1))

    async def negotiate_task(self):
        # Negotiate with neighbors to find a task to work on
        task = await self.find_task()
        if task:
            self.state = 'active'
            self.task_queue.append(task)

    async def execute_task(self):
        # Execute the current task
        task = self.task_queue.pop(0)
        print(f'Agent {self.id} executing task: {task}')
        await asyncio.sleep(random.uniform(1, 5))
        self.state = 'idle'

    async def find_task(self):
        # Communicate with neighbors to find a task to work on
        for neighbor in self.neighbors:
            # Negotiate with neighbor to find a task
            task = await neighbor.propose_task(self.id)
            if task:
                return task
        return None

    async def propose_task(self, agent_id):
        # Check if there are any tasks that can be delegated to the given agent
        if self.task_queue:
            task = self.task_queue.pop(0)
            print(f'Agent {self.id} proposing task {task} to agent {agent_id}')
            return task
        return None

async def main():
    agents = [SwarmAgent(i) for i in range(10)]

    for agent in agents:
        agent.neighbors = [a for a in agents if a.id != agent.id]

    tasks = ['task1', 'task2', 'task3', 'task4', 'task5']
    for agent in agents:
        agent.task_queue = random.sample(tasks, k=random.randint(1, 3))

    await asyncio.gather(*[agent.coordinate() for agent in agents])

if __name__ == '__main__':
    asyncio.run(main())
