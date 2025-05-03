from math import factorial
import itertools

with open("rendimientos.txt", mode='r') as file:
    stocks = { i.strip().split(" ")[0]: (i.strip().split(" ")[1], i.strip().split(" ")[2]) for i in file.readlines()[1:] }

with open("correlaciones.txt", mode='r') as file:
    portfolio = [ i.split(" ") for i in file.read().split("\n") ]

class Graph():
    
    adj_list: dict = {}
    
    def __init__(self, nodes: dict, edges: list):
        self.nodes = nodes
        self.edges = edges
        self.adj_list = { i: {} for i in nodes.keys() }
        for edge in edges:
            self.adj_list[edge[0]][edge[1]] = float(edge[2])
            self.adj_list[edge[1]][edge[0]] = float(edge[2])
        
    def max_benefit_portfolio(self, max_correlation: float, min_assets: int):
        
        total_portfolios = []
        portfolios = []
        for i in range(min_assets,len(self.nodes.keys())):
            total_portfolios += itertools.combinations(list(self.nodes.keys()), i)
        for i in total_portfolios:
            if self.correlation_is_in_bounds(max_correlation,i):
                portfolios.append(i)
        max_benefit = 0
        winner_portfolio = []
        for combination in portfolios:
            mean_benefit = self.get_mean_benefit(combination)
            if mean_benefit > max_benefit:
                max_benefit = mean_benefit
                winner_portfolio = combination
        
        return winner_portfolio, max_benefit, len(portfolios)

    def correlation_is_in_bounds(self, max_correlation: float, portfolio: list):
        for i in range(len(portfolio)-1):
            for j in range(len(portfolio)):
                if i == j :
                    continue
                else:
                    if self.adj_list[portfolio[i]][portfolio[j]] > max_correlation:
                        return False
        return True

    def get_mean_benefit(self, portfolio: list):
        benefit = 0.0
        for action in portfolio:
            benefit+= float(self.nodes[action][0])
        benefit = benefit/len(portfolio)
        return benefit

def max_benefit_portfolio(graph: Graph = None):
    max_correlation = float(input("Valor maximo correlacion: "))
    min_assets = int(input("Valor minimo de acciones en el portafolio: "))

    portfolioGraph = Graph(stocks, portfolio)
    print(portfolioGraph.max_benefit_portfolio(max_correlation, min_assets))
    


max_benefit_portfolio()


