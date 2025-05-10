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
            while not limits[0] <= out <= limits[1]:
                Printer.clear_console(Printer.error())
                out = type(input(text))
            Printer.clear_console("")
            return out
        
        except Exception as e:
            Printer.clear_console(Printer.error(str(e)))
    
    @staticmethod
    def read(mode: str):
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()

        if "rendimientos" in mode:
            path = filedialog.askopenfilename(title="Seleccione archivo de rendimientos", defaultextension="*, .txt", initialfile="rendimientos.txt")
            root.deiconify()
            root.destroy()
            with open(path, mode='r') as file:
                print(f"Ruta de rendimientos: {path}")
                return { i.strip().split(" ")[0]: (float(i.strip().split(" ")[1]), float(i.strip().split(" ")[2])) for i in file.readlines()}
        elif "correlaciones" in mode:
            path = filedialog.askopenfilename(title="Seleccione archivo de correlaciones", defaultextension=("*", ".txt"), initialfile="correlaciones.txt")
            root.deiconify()
            root.destroy()
            with open(path, mode='r') as file:
                print(f"Ruta de correlaciones: {path}")
                return [ i.split(" ") for i in file.readlines()[1:] ] 

# 🧠 - Clase principal para manejo de portafolios
class PortfolioGraph():
    
    def __init__(self, actions_dict: dict, correlations_list: list, min_assets : int = None):
        self.actions_dict = actions_dict
        self.correlations_list = correlations_list
        self.adjacency = { action: {} for action in actions_dict.keys() }

        for pair in correlations_list:
            self.adjacency[pair[0]][pair[1]] = float(pair[2])
            self.adjacency[pair[1]][pair[0]] = float(pair[2])
    

    def max_benefit_portfolio(self, max_correlation: float, min_assets: int, option: int = 1, lim_risk:float = 0.0):
        from itertools import combinations
        
        total_portfolios = [] #Lista preliminar
        selected_portfolios = [] #Lista de salida
        
        # Hallar todos los portfolios posibles de tamaños desde min_assets hasta n
        for i in range(min_assets, len(self.actions_dict.keys())):
            total_portfolios += combinations(list(self.actions_dict.keys()), i)

        # Agregar en portfolios todos aquellos portfolios donde las condiciones se cumplan
        for combination in total_portfolios:
            #Comprobaciones de opción 1
            if option == 1 and self.correlation_is_in_bounds(max_correlation, combination):
                selected_portfolios.append(combination)
            #Comprobaciones de opción 2
            elif option == 2 and self.correlation_is_in_bounds(max_correlation, combination) and self.risk_is_in_bounds(lim_risk, combination):
                selected_portfolios.append(combination)
                
        
        winner_benefit = 0.0
        winner_risk = 0.0
        winner_portfolio = []
    
        for combination in selected_portfolios:                         #Revisar cada combinación seleccionada
        
            mean_benefit = self.get_mean_benefit(combination)           #Calcular beneficio medio
            if mean_benefit > winner_benefit:                           #Si el beneficio medio es máximo
                winner_portfolio = combination                              #Seleccionar la combinación como ganadora
                winner_benefit = mean_benefit
                if option == 2:                                         #Si es opción 2
                    winner_risk = self.get_mean_risk(combination)             #Calcular riego medio

        #Salidas por opción
        if option == 1:
            return winner_portfolio, round(winner_benefit, 3), len(selected_portfolios)
        elif option == 2: 
            return winner_portfolio, round(winner_benefit, 3), round(winner_risk, 3), len(selected_portfolios)

    #Retorna verdadero si la correlación media del portafolio está dentro del limite
    def correlation_is_in_bounds(self, max_correlation: float, portfolio: list):
        for i in range(len(portfolio)-1):
            for j in range(len(portfolio)):
                if i == j :
                    continue
                else:
                    if self.adjacency[portfolio[i]][portfolio[j]] > max_correlation:
                        return False
        return True
    
    #Retorna verdadero si el riesgo medio del portafolio está dentro del limite
    def risk_is_in_bounds(self, max_risk: float, portfolio: list):
        return self.get_mean_risk(portfolio) < max_risk

    #Retorna el beneficio medio del portafolio
    def get_mean_benefit(self, portfolio: list):
        benefit = 0.0
        for action in portfolio:
            benefit+= float(self.actions_dict[action][0])
        benefit = benefit/len(portfolio)
        return benefit
    
    #Retorna el riesgo medio del portafolio
    def get_mean_risk(self, portfolio:list):
        risk = 0.0
        for action in portfolio:
            risk+= float(self.actions_dict[action][1])
        risk = risk/len(portfolio)
        return risk



if __name__ == "__main__":
    Printer.clear_console("")
    while True:
        option = Utils.validate_input( int, Printer.opener() + Printer.options(), (0,2))
        if option == 0:
            break

        Printer.clear_console("")
        try:
            print("Seleccione el archivo de rendimientos: ")
            actions = Utils.read("rendimientos")
            
            print("Seleccione el archivo de correlaciones: ")
            correlations = Utils.read("correlaciones")
        except Exception as e:
            print(Printer.error(e))
            break
        graph = PortfolioGraph(actions, correlations)
        
        if option == 1:
            max_correlation = Utils.validate_input(float, "Valor máximo de correlación: ", (-1, 1))
            min_assets = Utils.validate_input(int, "Valor minimo de acciones en el portafolio: ", (1, len(actions)))
            
            print(graph.max_benefit_portfolio(max_correlation,min_assets))
            input("Press any key to continue...")
        
        elif option == 2:
            max_correlation = Utils.validate_input(float, "Valor máximo de correlación: ", (-1, 1))
            min_assets = Utils.validate_input(int, "Valor minimo de acciones en el portafolio: ", (1, len(actions)))
            max_risk = Utils.validate_input(float, "Valor máximo de riesgo medio en el portafolio: ", (1, 10))
            
            print(graph.max_benefit_portfolio(max_correlation, min_assets, 2, max_risk))
            input("Press any key to continue...")