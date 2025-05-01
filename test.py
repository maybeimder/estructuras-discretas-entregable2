from math import factorial

with open("rendimientos.txt", mode='r') as file:
    stocks = { i.strip().split(" ")[0]: (i.strip().split(" ")[1], i.strip().split(" ")[2]) for i in file.readlines()[1:] }

with open("correlaciones.txt", mode='r') as file:
    portfolio = [ i.split(" ") for i in file.read().split("\n") ]


def max_benefit_portfolio():
    max_correlation = float(input("Valor maximo correlacion: "))
    min_assets = int(input("Valor minimo de acciones en el portafolio: "))

    out = []
    [ out.append(acc) for acc in portfolio if abs(float(acc[2])) < max_correlation ]
    
    if len(out) < min_assets : 
        print("nosecumple")
    else:
        out.sort( key= lambda x :float(stocks[x[0]][0]) + float(stocks[x[1]][0]), reverse=True )
        print("Lista de acciones del portafolio (Ordenada)")
        pato = set()
        list(map(lambda x : pato.update([x[0], x[1]]), out))
        print(pato)
        print("="*86)
        print("Promedio")


max_benefit_portfolio()


