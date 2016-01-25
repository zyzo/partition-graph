from greedy import Greedy, division
from collections import deque
from math import exp
from random import random
import sys

class Label():
    def __init__(self, node, ori, dest, delta):
        self.core = (node, ori, dest)
        self.node = node
        self.ori = ori
        self.dest = dest
        self.delta = delta

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.core == other.core or self.core == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.core)

    def __str__(self):
        return '(' + str(self.node) + ', p' + str(self.ori) + ' -> p' + str(self.dest) + ')'

    def reverse(self):
        return (self.node, self.dest, self.ori)

class Depth:
    def __init__(self):
        self.value = 0
        self.ori = None
        self.last = None
        self.normal = True
        self.back = False

    def forward(self, label, eval):
        if not self.normal:
            if self.back:
                self.back = False
                self.last = label
        if label.delta[eval] > 0:
            self.value += 1

    def backward(self, label, eval):
        if self.normal:
            if self.ori == label:
                self.last = None
                self.normal = False
                self.back = True
            if label.delta[eval] > 0:
                self.value -= 1
        elif not self.back:
            if label.delta[eval] > 0:
                self.value -= 1
            if self.last == label:
                self.back = True
        elif label.delta[eval] < 0:
            self.value += 1

    def set(self, label=None):
        self.ori = label
        self.value = 0
        self.normal = True
        self.back = False

class Stub:
    def write(self, str):
        pass

def compare(value1, value2, preemption):
    size = len(preemption)
    if len(preemption) == 0:
        return 0
    eval = preemption[0]
    if value1[eval] < value2[eval]:
        return -1
    elif value1[eval] == value2[eval]:
        if len(preemption) != 0:
            return compare(value1, value2, preemption[1:size])
        else:
            return 0
    return 1

class Local(Greedy):
    def __init__(self):
        super(Local, self).__init__()
        self.best = {'state': None, 'step': None,
                     'from': {
                     'cut': float('+inf'), 
                     'balance': float('+inf'), 
                     'ratio': float('+inf')},
                     'to': {
                     'cut': float('+inf'), 
                     'balance': float('+inf'), 
                     'ratio': float('+inf')}        }

    def partition(self, k=2, depth=None, theta=None, preemption=['ratio'], replays=0, rand=False, log=Stub()):
        eval = preemption[0]

        # Get P, E and C from a greedy solution
        super(Local, self).partition(k, select='weight', rand=rand)

        self.eval = {'from': {}, 'to': {}}
        self.eval['from']['cut'] = self.cut()
        self.eval['to']['cut'] = self.eval['from']['cut']
        self.eval['from']['balance'] = self.balance()
        self.eval['to']['balance'] = self.eval['from']['balance']
        self.eval['from']['ratio'] = sum([division(self.K[p], self.W[p]) for p in range(k)])
        self.eval['to']['ratio'] = self.eval['from']['ratio']

        min = {e: self.eval['to'][e] for e in self.eval['to']}
 
        iter = 0
        path = []
        best = []

        done = set()
        pool = [self.set_pool(eval, done)]

        move = Depth()

        step = 0

        try:

            while iter >= 0:
                while len(pool[iter]) != 0:
                    label = pool[iter].pop()
                    delta = label.delta[eval]

                    self.do(label)
                    if not self.broke(label, move.value, eval=eval, depth=depth, theta=theta):
                        step += 1
                        path.append(label)

                        log.write('Iteration ' + str(step) + '\n')
                        log.write('Eval(' + eval + ') ' + str(self.eval['to'][eval]) + '\n')
        
                        if compare(self.eval['to'], min, preemption) < 0:
                            min = {e: self.eval['to'][e] for e in self.eval['to']}
                            best = [l for l in path]
                            move.set(label=label)
                        move.forward(label, eval=eval)
                        pool.append(self.set_pool(eval, done, label=label))
                        iter += 1
                    else:
                        self.undo(label)

                if iter != 0: 
                    label = path.pop()
                    self.undo(label)
                    move.backward(label, eval=eval)
                    if self.broke(label, move.value, eval=eval, back=True, depth=depth, theta=theta):
                        break
                pool.pop()
                iter -= 1

            while len(path) != 0:
                label = path.pop()
                self.undo(label)

            for label in best:
                self.do(label)

            if compare(self.eval['to'], self.best['to'], preemption) < 0:
                P = [set() for p in range(self.k)]
                for n in self.nodes_iter():
                    P[self.node[n]['partition']].add(n)
                self.best['state'] = P
                self.best['step'] = step
                self.best['from'] = {e: self.eval['from'][e] for e in self.eval['from']}
                self.best['to'] = {e: self.eval['to'][e] for e in self.eval['to']}

            log.write('Operation success in ' + str(step) + ' iterations\n')
            log.write(str(self) + '\n\n')

        except KeyboardInterrupt:
            if compare(self.eval['to'], self.best['to'], preemption) < 0:
                self.best['state'] = P
                self.best['step'] = step
                self.best['from'] = {e: self.eval['from'][e] for e in self.eval['from']}
                self.best['to'] = {e: self.eval['to'][e] for e in self.eval['to']}
            eval  = 'Operation interrupted during process\n'
            eval += 'Iteration ' + str(self.best['step']) + '\n'
            eval += 'Best solution found:\n'
            eval += str(self) + '\n'
            raise KeyboardInterrupt(eval)

        if replays > 0:
            self.partition(k=k, depth=depth, theta=theta, preemption=preemption, replays=replays - 1, rand=True, log=log)
        else:
            self.apply(self.best)
                
    def delta(self, n, o, d):
        dK = 0
        dW = {o:0, d:0}
        nE = set()
        dE = set()
        for v in self.neighbors(n):
            w = self[n][v]['weight']
            e = self[n][v]['edge']
            p = self.node[v]['partition']
            if p == d:
                dK -= w
                dW[d] += w
                dE.add(e)
            elif p == o:
                dK += w
                dW[o] -= w
                nE.add(e)
        W = {p: self.W[p] for p in self.W}
        W[o] += dW[o]
        W[d] += dW[d]
        dB = max(W.values()) * self.k / float(sum(W.values())) - self.eval['to']['balance']
        Wop = self.W[o] + dW[o]
        Wdp = self.W[d] + dW[d]
        Ko = self.K[o] * self.W[d] * Wop * Wdp
        Kd = self.K[d] * self.W[o] * Wop * Wdp
        Kop = (self.K[o] + dK) * self.W[o] * self.W[d] * Wdp
        Kdp = (self.K[d] + dK) * self.W[o] * self.W[d] * Wop
        Dn = self.W[o] * self.W[d] * Wop * Wdp
        dR = division(Kop + Kdp - Ko - Kd , Dn)
        return {'+e': nE, '-e': dE, 'dK': dK, 'dW': dW,
                'cut': dK, 'balance': dB, 'ratio': dR}

    def do(self, label):
        delta = label.delta
        self.node[label.node]['partition'] = label.dest
        self.S[label.ori] -= 1
        self.S[label.dest] += 1
        self.C |= delta['+e']
        self.C -= delta['-e']
        for p in (label.ori, label.dest):
            self.K[p] += delta['dK']
            self.W[p] += delta['dW'][p]
        delta['old'] = {}
        for e in self.eval['to']:
            delta['old'][e] = self.eval['to'][e]
            self.eval['to'][e] += delta[e]

    def undo(self, label):
        delta = label.delta
        self.node[label.node]['partition'] = label.ori
        self.S[label.ori] += 1
        self.S[label.dest] -= 1
        self.C -= delta['+e']
        self.C |= delta['-e']
        for p in (label.ori, label.dest):
            self.K[p] -= delta['dK']
            self.W[p] -= delta['dW'][p]
        for e in self.eval['to']:
            self.eval['to'][e] = delta['old'][e]

    def set_pool(self, eval, done, label=None):
        pool = set()
        for e in self.C:
            n1, n2 = e
            o = self.node[n1]['partition']
            d = self.node[n2]['partition']
            self.add_in_pool(n1, o, d, pool, done)
            self.add_in_pool(n2, d, o, pool, done)
        return sorted(pool, key=lambda label: label.delta[eval], reverse=True)

    def add_in_pool(self, node, ori, dest, pool, done):
        delta = self.delta(node, ori, dest)
        C = {e for e in self.C}
        C |= delta['+e']
        C -= delta['-e']
        if not C in done:
            done.add(frozenset(C))
            label = Label(node, ori, dest, delta)
            if self.legal(C, label):
                pool.add(label)

    def broke(self, label, move, eval, back=False, depth=None, theta=None):
        delta = label.delta[eval]
        if back:
            delta *= -1
        if delta <= 0:
            return False
        elif depth != None:
            return move >= depth
        elif theta != None:
            return random() > exp(-delta/theta)
        else:
            return True

    def legal(self, C, label):
        n, o, d = label.core
        if self.S[o] == 1:
            return False

        target = {v for v in self.neighbors(n) if self.node[v]['partition'] == o}
        start = target.pop()
        pool = deque([start])
        done = set([n, start])
        while len(target) != 0 and len(pool) != 0:
            n = pool.pop()
            for v in self.neighbors(n):
                if self.node[v]['partition'] == o and not v in done:
                    pool.appendleft(v)
                    done.add(v)
                    target.discard(v)
                        
        if len(target) == 0:
            return True
        else:
            return False

    def is_better_than(self, min, preemption, solution=None):
        size = len(preemption)
        if len(preemption) == 0:
            return False
        eval = preemption[0]
        if self.eval['to'][eval] < min[eval]:
            return True
        elif self.eval['to'][eval] == min[eval]:
            if len(preemption) != 0:
                return self.is_better_than(min, preemption[1:size])
        return False

    def apply(self, solution):
        self.P = solution['state']
        for p, P in enumerate(solution['state']):
            for n in P:
                self.node[n]['partition'] = p
        self.compute()
        self.eval['from'] = {e: solution['from'][e] for e in solution['from']} 
        self.eval['to'] = {e: solution['to'][e] for e in solution['to']} 

    def __str__(self):
       eval  = 'Cut     from ' + str(self.best['from']['cut']) + ' to ' +  str(self.best['to']['cut']) + '\n'
       eval += 'Balance from ' + str(self.best['from']['balance']) + ' to ' +  str(self.best['to']['balance']) + '\n'
       eval += 'Ratio   from ' + str(self.best['from']['ratio']) + ' to ' +  str(self.best['to']['ratio'])
       return eval
        
