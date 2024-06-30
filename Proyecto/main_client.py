import importlib
import asyncio
import global_config
from termcolor import colored

# Lista de nombres de los módulos de dialecto

dialects = ['dialects.coapts.client', 'dialects.coaprcs.client', 
            'dialects.coapcpv.client', 'dialects.coappbr.client',
            'dialects.coapxorp.client']

async def run_client(selected_dialect):
    dialect_module = importlib.import_module(selected_dialect)
    await dialect_module.main()

async def main():
    print(colored("\n--------------------------------------------------------------------------","yellow"))
    print(colored(f"Selected initial dialect: {dialects[global_config.selected_dialect_index]}","yellow"))

    while True:
        selected_dialect = dialects[global_config.selected_dialect_index]
        print(colored(f"Running dialect...","yellow"))
        await run_client(selected_dialect)
        
        # Leer el nuevo dialecto seleccionado por el cliente
        if global_config.selected_dialect_index is not None:
            print(colored("\n\n--------------------------------------------------------------------------","yellow"))
            print(colored(f"New dialect: {dialects[global_config.selected_dialect_index]}","yellow"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(colored("\nClient stopped manually","light_red"))