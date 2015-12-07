import random
import urllib

class GreedyPartitioning:
    def __init__(self, graph_filename, partition_number, is_url=False):
        if not is_url: data = open(graph_filename, 'r')
        else: data = urllib.urlopen(graph_filename)
        # data.readline()
        n, e = [int(x) for x in data.readline().split()]
        self.g, self.sum_edges = [[]], [[]]
        self.ge = []
        self.visited = [[]]
        for idx, line in enumerate(data):
            split = line.split()
            self.g.append([[int(x), 1] for x in split])  #
            self.sum_edges.append(sum([x[1] for x in self.g[-1]]))
            self.ge.append((idx, len(split)))
            self.visited.append(False)
        data.close()
        ge = sorted(self.ge, key=lambda node: node[1], reverse=True)
        ## Select starting points
        start = []
        for idx in range(int(partition_number)):
            start.append(ge[idx][0] + 1)
            # self.visited[ge[idx][0] + 1] = True
        start = []
        for x in range(int(partition_number)):
            y = random.randint(1, n)
            while y in start[:x]:
                y = random.randint(1, n)
            start.append(y)
        start = [2204, 1613, 463]
        for id in start:
            self.visited[id] = True
        print "Starting points: " + str(start)
        self.partitions = [[x] for x in start]
        neighbours = []
        for pid, partition in enumerate(self.partitions):
            for edge in self.g[partition[0]]:
                if not self.visited[edge[0]]:
                    cost = self.cost(partition, edge[0])
                    neighbours.append([pid, edge[0], cost, cost])
        neighbours = sorted(neighbours, key=lambda node: node[3])
        ## Launch greedy algorithm
        # print neighbours
        self.partitions_count = [0.5 for x in self.partitions]
        self.partitions_count_sum = sum(self.partitions_count)
        while neighbours:
            next_node = neighbours.pop()
            self.visited[next_node[1]] = True
            self.partitions[next_node[0]].append(next_node[1])
            self.update_partition_cost(next_node[0], next_node[1])
            neighbours = self.update_neighbours(neighbours, next_node[0], next_node[1])

    def update_partition_cost(self, pid, i):
        inc = sum([x[1] for x in self.g[i] if x[0] in self.partitions[pid]])
        self.partitions_count[pid] += inc
        self.partitions_count_sum += inc
        #self.partitions_count[pid] += 1
        #self.partitions_count_sum += 1

    def cost(self, partition, node):
        cnt = 0
        for edge in self.g[node]:
            if edge[0] in partition:
                cnt += edge[1]
        return cnt / float(self.sum_edges[node])

    def weight(self, v1, v2):
        return [x[1] for x in self.g[v1] if x[0] == v2][0]

    def update_neighbours(self, neighbours, pid, inserted):
        # print [[x[0]+1,x[1],x[2]] for x in neighbours]
        neighbours = [x for x in neighbours if x[1] != inserted]
        n_inserted = [x[0] for x in self.g[inserted]]
        for n in neighbours:
            if n[1] in n_inserted and n[0] == pid:
                n[2] += self.weight(inserted, n[1]) / float(self.sum_edges[n[1]])
                n_inserted.remove(n[1])
            n[3] = n[2] * self.partitions_count_sum / self.partitions_count[n[0]]
        for ni in n_inserted:
            if not self.visited[ni]:
                cost = self.cost(self.partitions[pid], ni)
                neighbours.append([pid, ni, cost, cost * self.partitions_count_sum /self.partitions_count[pid]])
        neighbours = sorted(neighbours, key=lambda node: node[3])
        return neighbours

    def get_partitions(self):
        # print [len(x) for x in self.partitions]
        return self.partitions
