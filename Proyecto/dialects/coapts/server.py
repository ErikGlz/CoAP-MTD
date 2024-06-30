import logging
import asyncio
import hashlib
import random
from coapts import resource, Message, Context, error
from coapts.numbers.codes import CHANGED, CONTENT
from sense_hat import SenseHat
import global_config
from termcolor import colored

def select_dialect(seed):
    random.seed(seed)
    dialect_number = random.randint(0, 4)
    return dialect_number

class TemperatureResource(resource.Resource):
    """Resource that provides temperature readings from the SenseHat."""

    def __init__(self):
        super().__init__()
        self.sense = SenseHat()

    async def render_get(self, request):
        # Verifica si la petición contiene payload
        if request.payload:
            print(colored(f"\nSEED RECEIVED","cyan"))

            # Extrae la semilla del payload
            seed = int(request.payload.decode('utf-8'))
            new_dialect_index = select_dialect(seed)
            global_config.selected_dialect_index = new_dialect_index
            
            print(colored(f"\nSWITCHING TO DIALECT: {global_config.selected_dialect_index+1}\n","light_magenta"))
            global stop_server
            stop_server = True

            temperature = self.sense.get_temperature()
            payload = f"Temperature: {temperature:.2f} C".encode('ascii')
            
            return Message(code=CONTENT, payload=payload)

        else:
            temperature = self.sense.get_temperature()
            payload = f"Temperature: {temperature:.2f} C".encode('ascii')
            return Message(code=CONTENT, payload=payload)

class HumidityResource(resource.Resource):
    """Resource that provides humidity readings from the SenseHat."""

    def __init__(self):
        super().__init__()
        self.sense = SenseHat()

    async def render_get(self, request):
    # Verifica si la petición contiene payload
        if request.payload:
            print(colored(f"\nSEED RECEIVED","cyan"))

            # Extrae la semilla del payload
            seed = int(request.payload.decode('utf-8'))
            new_dialect_index = select_dialect(seed)
            global_config.selected_dialect_index = new_dialect_index

            print(colored(f"\nSWITCHING TO DIALECT: {global_config.selected_dialect_index+1}\n","light_magenta"))
            global stop_server
            stop_server = True

            temperature = self.sense.get_temperature()
            payload = f"Temperature: {temperature:.2f} C".encode('ascii')
            
            return Message(code=CONTENT, payload=payload)

        else:
            humidity = self.sense.get_humidity()
            payload = f"Humidity: {humidity:.2f}%".encode('ascii')
            return Message(code=CONTENT, payload=payload)

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    #Variable para controlar el ciclo del servidor
    global stop_server
    stop_server = False

    # Resource tree creation
    root = resource.Site()

    root.add_resource(['temperature'], TemperatureResource())
    root.add_resource(['humidity'], HumidityResource())

    protocol = await Context.create_server_context(root)
    print(colored("Server initialized\n","green"))

    while not stop_server:
        await asyncio.sleep(1)

    #Detener el contexto actual
    await Context.shutdown(protocol)
    stop_server = False

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(colored("Client stopped manually","light_red"))