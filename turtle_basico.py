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
         
    
actions : dict = read("adas/rendimientos.txt")
correlations = read("adas/correlaciones.txt")
print(correlations)
print()

blacklist = []
[ blacklist.append([pair[0], pair[1]]) for pair in correlations if abs(float(pair[2])) > 0.5 ]
print(blacklist)
print()

portfolios = []
for size in range(3, len(actions)):
    portfolios += list(combinations(actions.keys(), size))
print(portfolios)
print()

avaliable = [ portfolio for portfolio in portfolios if all([not (a in portfolio and b in portfolio) for a, b in blacklist])]
print(avaliable)

print(len(avaliable))