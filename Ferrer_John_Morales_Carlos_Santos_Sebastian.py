COLORS = {
    "reset"  : "\033[0m",
    "red"    : "\033[0;31m",
    "green"  : "\033[1;32m",
    "blue"   : "\033[1;34m",
    "purple" : "\033[1;35m"
}

class Utils:
    @staticmethod
    def clear_console( text : str ):
        from os import system
        system('cls||clear')
        print(text)
    
    @staticmethod
    def validate_input(type = int, text:str = "", limits: tuple = (0,2)):
        try:
            out = type(input(text))
            while not limits[0] <= out >= limits[1]:
                Utils.clear_console(f"{COLORS['red']} [ERROR] Opcion no valida {COLORS['reset']}")
                out = type(input(text))
            Utils.clear_console(f"{COLORS['green']} [Opcion] {out} {COLORS['reset']}")
            return out
        
        except Exception as e:
            Utils.clear_console(f"{COLORS['red']} [ERROR] {e} {COLORS['reset']}")
    
    @staticmethod
    def read( path : str ):
        with open(path) as file:
            return [ i.split(" ") for i in file.read().split("\n") ] 

class Printer:
    @staticmethod
    def opener():
        Printer.separator()
        print(f"""
        {COLORS["purple"]}
                    S I S T E M A     D E    G E S T I Ó N  
            D E    P O R T A F O L I O S    D E    I N V E R S I O N
        {COLORS["reset"]}
        {"=" * 86}
            .
            Menu de opciones:
                - {COLORS["green"]}(1){COLORS["reset"]} Portafolio de máximo beneficio
                - {COLORS["green"]}(2){COLORS["reset"]} Portafolio con riesgo controlado
                - {COLORS["red"]}(0){COLORS["reset"]} Salir

            Opcion: """)
    
    @staticmethod
    def separator():
        print("=" * 86)
    
# =======================================================

ut = Utils()

if __name__ == "__main__":
    while True:
        option = ut.validate_input(text = f"""
{"=" * 86}
        {COLORS["purple"]}
                    S I S T E M A     D E    G E S T I Ó N  
            D E    P O R T A F O L I O S    D E    I N V E R S I O N
        {COLORS["reset"]}
{"=" * 86}
            .
            Menu de opciones:
                - {COLORS["green"]}(1){COLORS["reset"]} Portafolio de máximo beneficio
                - {COLORS["green"]}(2){COLORS["reset"]} Portafolio con riesgo controlado
                - {COLORS["red"]}(0){COLORS["reset"]} Salir

            Opcion: """
        )
        
        if option == 1:
            print(f"""
                {COLORS["green"]} PORTAFOLIO DE MÁXIMO BENEFICIO {COLORS["reset"]}
                * Encuentra el portafolio de acciones con el mayor rendimiento promedio.
                * Se asegura que no se sobrelapen distintas acciones. 
            """
            )

            max_correlation = ut.validate_input(type= float, range=(0.0, ), text=f"{COLORS['blue']} Valor maximo de correlacion:{COLORS['reset']} ")
            min_assets = ut.validate_input(type= float, text=f"{COLORS['blue']} Valor minimo de acciones deseadas:{COLORS['reset']} ")

            

            
            
            input("Press any key to continue...")
            ut.clear_console("")
        
        elif option == 2:
            print("Hace la op 2")
            
            input("Press any key to continue...")
            ut.clear_console("")
        
        elif option == 0:
            ut.clear_console(f"{COLORS['red']} Saliendo del programa {COLORS['reset']}")
            break
        
