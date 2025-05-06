COLORS = {
    "reset"  : "\033[0m",
    "red"    : "\033[0;31m",
    "green"  : "\033[1;32m",
    "blue"   : "\033[1;34m",
    "purple" : "\033[1;35m"
}

# 🗑️ - Clase auxiliar para limpiar los prints pesados
class Printer:
    @staticmethod
    def clear_console( text : str ):
        from os import system
        system('cls||clear')
        print(text)

    @staticmethod
    def opener():
        return f"""{Printer.separator()}
        {COLORS["purple"]}
                    S I S T E M A     D E    G E S T I Ó N  
            D E    P O R T A F O L I O S    D E    I N V E R S I O N
        {COLORS["reset"]}\n{Printer.separator()}"""
        
    @staticmethod
    def options():
        return f"""
        Menu de opciones:
            - {COLORS["green"]}(1){COLORS["reset"]} Portafolio de máximo beneficio
            - {COLORS["green"]}(2){COLORS["reset"]} Portafolio con riesgo controlado
            - {COLORS["red"]}(0){COLORS["reset"]} Salir
        
        Opcion: """
    
    @staticmethod
    def separator():
        return "=" * 86

    @staticmethod
    def error( aux : str = "Opción inválida"):
        return f"{COLORS['red']} [ERROR] {aux} {COLORS['reset']}"


# 💡 - Clase auxiliar de métodos varios
class Utils:
    @staticmethod
    def validate_input(type = int, text:str = "", limits: tuple = (0,2)):
        try:
            out = type(input(text))
            while not limits[0] <= out >= limits[1]:
                Printer.clear_console(Printer.error())
                out = type(input(text))
            Printer.clear_console("")
            return out
        
        except Exception as e:
            Printer.clear_console(Printer.error(str(e)))
    
    @staticmethod
    def read( path : str ):
        if "rendimientos.txt" in path:
            with open(path, mode='r') as file:
                print(next(file))
                return { i.strip().split(" ")[0]: (float(i.strip().split(" ")[1]), float(i.strip().split(" ")[2])) for i in file.readlines()[1:] }
        
        elif "correlaciones.txt" in path:
            with open(path, mode='r') as file:
                return [ i.split(" ") for i in file.read().split("\n") ] 
        
        else:
            Printer.error("Archivos no cumplen el formato")



class PortfolioGraph():
    
    def __init__(self, actions: dict, correlations: list, min_assets : int = None):
        self.actions = actions
        self.correlations = correlations
        self.adjacency = { action: {} for action in actions.keys() }

        for pair in correlations:
            self.adjacency[pair[0]][pair[1]] = float(pair[2])
            self.adjacency[pair[1]][pair[0]] = float(pair[2])
    

    def max_benefit_portfolio(self, max_correlation: float, min_assets: int):
        from itertools import combinations
        total_portfolios = []
        portfolios = []

        # Hallar todos los portfolios posibles de tamaños desde min_assets hasta n
        for i in range(min_assets, len(self.actions.keys())):
            total_portfolios += combinations(list(self.actions.keys()), i)

        # Agregar en portfolios todos aquellos portfolios donde la correlacion maxima se cumpla
        for portfolio in total_portfolios:
            if self.correlation_is_in_bounds(portfolio, max_correlation):
                portfolios.append(portfolio)


        max_benefit = 0
        winner_portfolio = []
        for combination in portfolios:
            mean_benefit = self.get_mean_benefit(combination)
            if mean_benefit > max_benefit:
                max_benefit = mean_benefit
                winner_portfolio = combination
        
        return winner_portfolio, max_benefit, len(portfolios)

    def correlation_is_in_bounds(self, portfolio: list, max_correlation: float, ):
        for i in range(len(portfolio)-1):
            for j in range(len(portfolio)):
                if i == j :
                    continue
                else:
                    if self.adjacency[portfolio[i]][portfolio[j]] > max_correlation:
                        return False
        return True

    def get_mean_benefit(self, portfolio: list):
        benefit = 0.0
        for action in portfolio:
            benefit+= float(self.actions[action][0])
        benefit = benefit/len(portfolio)
        return benefit

    #def max_benefit_portfolio(graph = None):
    #    max_correlation = float(input("Valor maximo correlacion: "))
    #    min_assets = int(input("Valor minimo de acciones en el portafolio: "))
    #
    #    portfolioGraph = PortfolioGraph(stocks, portfolio)
    #    print(portfolioGraph.max_benefit_portfolio(max_correlation, min_assets))
            





ut = Utils()
p = Printer()

if __name__ == "__main__":
    Printer.clear_console("")
    while True:
        option = ut.validate_input( int, Printer.opener() + Printer.options(), (0,2))

        if option == 0:
            break

        elif option == 1:
            Printer.clear_console("")
            ut.read("rendimientos.txt")   
            pass
        
        elif option == 2:
            Printer.clear_console("")
            pass
