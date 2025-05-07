from itertools import combinations

max_correlation = 0.5

def read( path : str ):
    if "rendimientos.txt" in path:
        with open(path, mode='r') as file:
            print(next(file))
            return { i.strip().split(" ")[0]: (float(i.strip().split(" ")[1]), float(i.strip().split(" ")[2])) for i in file.readlines()[1:] }
    
    elif "correlaciones.txt" in path:
        with open(path, mode='r') as file:
            return [ i.split(" ") for i in file.read().split("\n") ] 
         
    
actions : dict = read("rendimientos.txt")
correlations = read("correlaciones.txt")

blacklist = []
[ blacklist.append([pair[0], pair[1]]) for pair in correlations if abs(float(pair[2])) > 0.5 ]

portfolio = []
portfolio = list( [ portfolio.append(combinations(actions, size)) for size in range(3, len(actions.keys())) ])

avaliable = []
[ avaliable.append([pair[0], pair[1]]) for pair in portfolio if [pair[0], pair[1]] not in blacklist ]


print(correlations)
print()
print(blacklist)
print()
print(portfolio)
print()
print(avaliable)



