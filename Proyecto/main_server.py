import importlib
import asyncio
import global_config
from termcolor import colored

# Lista de nombres de los módulos de dialecto
dialects = ['dialects.coapts.server', 'dialects.coaprcs.server', 
            'dialects.coapcpv.server', 'dialects.coappbr.server',
            'dialects.coapxorp.server']

async def run_server(selected_dialect):
    dialect_module = importlib.import_module(selected_dialect)
    await dialect_module.main()

async def main():

    print(colored("\n--------------------------------------------------------------------------","yellow"))
    print(colored(f"Selected initial dialect: {dialects[global_config.selected_dialect_index]}","yellow"))

    while True:
        selected_dialect = dialects[global_config.selected_dialect_index]
        print(colored(f"Running dialect...","yellow"))
        print(colored("--------------------------------------------------------------------------\n","yellow"))
        await run_server(selected_dialect)
        
        if global_config.selected_dialect_index is not None:
            print(colored("\n--------------------------------------------------------------------------","yellow"))
            print(colored(f"Switching to new dialect: {dialects[global_config.selected_dialect_index]}","yellow"))

if __name__ == "__main__":
    asyncio.run(main())