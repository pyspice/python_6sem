import numpy as np
import sys
from itertools import chain

class RandomDialog(object):
    
    def __init__(self, agents, max_len=5):
        self.agents = agents
        self.max_len = max_len

    def generate(self):
        """
        Генерирует случайный диалог состоящий из 1-max_len цепочек.
        При генерации вызывает функцию turn.
        Возвращаемый объект является генератором.
        """
        yield from chain(*map(lambda x: self.turn(x), range(np.random.randint(1, self.max_len))))

    def turn(self, number):
        """
        Генерирует одну случайную цепочку следующим образом: выбирается случайный агент.
        Он "говорит" случайное сообщение (msg) из своей Agent.kb (используйте next или send(None)).
        (правила того, как выбирать никак не регулируются, вы можете выбирать случайный твит из Agent.kb никак не учитывая
        переданное msg).
        Это сообщение передается с помощью send (помним, что агент - это объект-генератор).
        Далее получаем ответ от всех агентов и возвращаем (генерируем) их (включая исходное сообщение).
        Возвращаемый объект является генератором.
        """
        np.random.shuffle(self.agents)
        yield 'turn {}:\n'.format(number)
        yield from map(next, self.agents)        

    def eval(self, dialog=None):
        if dialog is None:
            dialog = self.generate()
        return list(dialog)

    def write(self, dialog=None, target=sys.stdout):
        if dialog is None:
            dialog = self.eval()
        
        target.writelines(dialog)
