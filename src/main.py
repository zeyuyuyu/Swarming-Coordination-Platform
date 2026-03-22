import random
import time
import json
import requests

class SwarmAgent:
    def __init__(self, agent_id, swarm_size):
        self.agent_id = agent_id
        self.swarm_size = swarm_size
        self.coordination_state = 'uncoordinated'
        self.task_queue = []
        self.task_status = {}

    def coordinate_swarm(self):
        if self.coordination_state == 'uncoordinated':
            self.broadcast_coordination_request()
        elif self.coordination_state == 'coordinating':
            self.process_coordination_responses()
        elif self.coordination_state == 'coordinated':
            self.execute_coordinated_tasks()

    def broadcast_coordination_request(self):
        self.coordination_state = 'coordinating'
        coordination_request = {
            'agent_id': self.agent_id,
            'swarm_size': self.swarm_size
        }
        for i in range(self.swarm_size):
            if i != self.agent_id:
                try:
                    response = requests.post(f'http://agent_{i}/coordination', json=coordination_request)
                    if response.status_code == 200:
                        self.task_queue.append(response.json()['task'])
                        self.task_status[response.json()['task']] = 'pending'
                except requests.exceptions.RequestException:
                    pass
        if len(self.task_queue) == self.swarm_size - 1:
            self.coordination_state = 'coordinated'

    def process_coordination_responses(self):
        for i in range(self.swarm_size):
            if i != self.agent_id:
                try:
                    response = requests.get(f'http://agent_{i}/tasks')
                    if response.status_code == 200:
                        for task in response.json()['tasks']:
                            if task not in self.task_queue:
                                self.task_queue.append(task)
                                self.task_status[task] = 'pending'
                except requests.exceptions.RequestException:
                    pass
        if len(self.task_queue) == self.swarm_size - 1:
            self.coordination_state = 'coordinated'

    def execute_coordinated_tasks(self):
        for task in self.task_queue:
            if self.task_status[task] == 'pending':
                self.execute_task(task)
                self.task_status[task] = 'completed'

    def execute_task(self, task):
        print(f'Executing task: {task}')
        time.sleep(random.uniform(1, 5))

if __name__ == '__main__':
    agent = SwarmAgent(0, 5)
    while True:
        agent.coordinate_swarm()
        time.sleep(5)
