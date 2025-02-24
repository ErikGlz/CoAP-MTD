import logging
import asyncio
import random
import time
from coaprcs import *
import global_config
from format_response import escape_special_chars, unscape_special_chars, create_response, fieldToNum, assignDialect, predecir_dialecto
from termcolor import colored

logging.basicConfig(level=logging.INFO)

def select_dialect(seed):
    random.seed(seed)
    dialect_number = random.randint(0, 4)
    return dialect_number

async def fetch_resource(protocol, uri, payload=None):
    if payload:
        request = Message(code=GET, uri=uri, payload=payload)
        request.mtype = CON
    else:
        request = Message(code=GET, uri=uri)
        request.mtype = CON

    print(colored("\n--------------------------------------------------------------------------","green"))
    print(colored('====== REQUEST ======',"green"))
    print(f"Message type: {request.mtype}")
    print(f"Message code: {request.code}")
    print(f"Resource URI: {request.get_request_uri()}")
    
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('\nFailed to fetch resource:')
        print(e)
    else:
        #Parseo de la respuesta al formato del arbol
        version = int(response.version)
        tipo_nombre = str(response.mtype)
        tipo_valor = int(response.mtype.value)
        code = str(response.code)
        payload = escape_special_chars(str(response.payload))
        payload_length = len(payload)

        cadena = create_response(version, tipo_nombre, tipo_valor, code, payload, payload_length)
        cadena2 = cadena.replace('\t', ',')

        print(colored('\n====== FORMATTING THE RECEIVED RESPONSE ======',"green"))
        print('\nReceived response')
        print(cadena2)

        cadena_formated = fieldToNum(cadena)
        print('\nFormatted response')
        print(cadena_formated)
        
        respuesta_final = assignDialect(cadena_formated)
        print('\nFinal response for the decision tree')
        print(respuesta_final)

        #Introducir la respuesta al arbol
        dialecto_predicho = predecir_dialecto(respuesta_final)

        if dialecto_predicho != 0 and dialecto_predicho == global_config.selected_dialect_index+1:
            print(colored(f"\nDIALECT DETECTED: {dialecto_predicho}","cyan"))
            print(colored('\n====== RESPONSE ======',"green"))
            print(f"Version: {response.version}")
            print(f"Message type: {response.mtype}")
            print(f"Message type code: {response.mtype.value}")
            print(f"Message TKL: {len(response.token)}")
            print(f"Response code: {response.code}")
            print(f"Message ID: {response.mid}")
            print(f"Message Token: {response.token.hex()}")
            print(f"Payload: {response.payload.decode('utf-8')}")
            print(colored("--------------------------------------------------------------------------","green"))
        
        else:
            print(colored("\nMALICIOUS RESPONSE DETECTED","red"))
            print(colored("Ignoring info","red"))
            print(colored("--------------------------------------------------------------------------","red"))

async def main():
    global stop_client
    stop_client = False

    while not stop_client:
        #Crear contexto del cliente del dialecto en uso
        protocol = await Context.create_client_context()

        #Seleccionar tiempo en el que se usa el dialecto
        dialect_duration = random.randint(5, 20)
        end_time = time.time() + dialect_duration
        print(colored(f"Using dialect for {dialect_duration} seconds","yellow"))
        print(colored("--------------------------------------------------------------------------","yellow"))

        #Uso del dialecto dentro del tiempo de uso
        while time.time() < end_time:
            uri_input = input(colored("\nEnter the full URI of the resource: ","light_yellow"))
            if uri_input.lower() == 'exit':
                break

            await fetch_resource(protocol, uri_input)
            await asyncio.sleep(1)

        #Generar seed para seleccionar el nuevo dialecto
        new_seed = random.randint(0, 100000)
        new_dialect_index = select_dialect(new_seed)

        #Asegura que el nuevo dialecto seleccionado no coincida con el que está en uso
        while global_config.selected_dialect_index == new_dialect_index:
            new_seed = random.randint(0, 100000)
            new_dialect_index = select_dialect(new_seed)

        # Enviar una petición para cambiar el dialecto
        print(colored(f"\nSENDING SEED...","light_grey"))
        payload = str(new_seed).encode('utf-8')
        uri_input = "coap://192.168.0.115/temperature"
        await fetch_resource(protocol, uri_input, payload=payload)

        #Actualiza el dialecto a utilizar
        global_config.selected_dialect_index = new_dialect_index
        print(colored(f"\n\nSWITCHING TO DIALECT: {global_config.selected_dialect_index+1}","light_magenta"))

        #Finaliza el contexto del cliente del dialecto en uso
        stop_client = True
        await Context.shutdown(protocol)

if __name__ == "__main__":
    asyncio.run(main())