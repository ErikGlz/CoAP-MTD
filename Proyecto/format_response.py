import os
import pickle
import numpy as np

#Cargar el arbol
arbol_decision = pickle.load(open('ModeloEntrenado', 'rb'))

#Funcion para escapar caracteres especiales que contienen los payloads de los dialectos 4 y 5
def escape_special_chars(s):
    # Escapa primero el backslash para evitar escapar escapes nuevos
    s = s.replace("\\", "\\\\")
    # Escapa comillas simples
    s = s.replace("'", "\\'")
    # Escapa comillas dobles
    s = s.replace('"', '\\"')
    return s

#Funcion para dejar de escapar caracteres especiales que contienen los payloads de los dialectos 4 y 5
def unscape_special_chars(s):
    # Deja de escapar dobles backslashes
    s = s.replace("\\\\", "\\")
    # Deja de escapar comillas simples
    s = s.replace("\\'", "'")
    # Deja de escapar comillas dobles
    s = s.replace('\\"', '"')
    return s

#Función para crear el string con los campos de la respuesta recibida
def create_response(version, tipo_nombre, tipo_valor, code, payload, payload_length):
    response = []
    #response += [str(version),',',tipo_nombre,',',str(tipo_valor),',',code,',']
    response += [str(version),'\t',tipo_nombre,'\t',str(tipo_valor),'\t',code,'\t']

    #response += [payload,',',str(payload_length)]
    response += [payload,'\t',str(payload_length)]

    return ''.join(response)

#Función para formatear una respuesta real en registro que acepte el arbol de decision 
def fieldToNum(input):
    #lista = input.split(',')
    lista = input.split('\t')
    entrada = []

    for i in range(len(lista)):
        if i == 0:
            # Para el campo Version
            if int(lista[0]) == 1:
                entrada.append(1)  
            elif int(lista[0]) != 1:
                entrada.append(-1)
        elif i == 1:
            # Para el nombre del campo Type
            if lista[1] == 'ACK':
                entrada.append(1)
            elif lista[1] == 'RST':
                entrada.append(-1)
        elif i == 2:
            # Para el valor numérico del campo Type
            entrada.append(int(lista[2])) 
        elif i == 3:
            # Para el campo Code
            cadena = lista[3]
            codevalue, codename = cadena.split(' ', 1) # Separar el número y el texto usando split()
            # Verificar las condiciones y agregar valores a la lista de entrada
            if codevalue == '2.05' and codename == 'Content':
                entrada.append(1)
            elif codevalue != '2.05' and codename == 'Content':
                entrada.append(-1)
            else:
                entrada.append(0)
        elif i == 4:
            # Para determinar si el payload contiene caracteres no imprimibles
            if '$' in lista[4] or '&' in lista[4] or '#' in lista[4] or '-' in lista[4] or '!' in lista[4] or ',' in lista[4] or '@' in lista[4]:
                entrada.append(1)
            else:
                entrada.append(0)
            
            # Para determinar si el payload contiene escapes de hexadecimales
            #print(lista[4])
            lista[4] = unscape_special_chars(lista[4])
            #print(lista[4])
            contador = lista[4].count("\\")
            #print(contador)
            if contador == 9 or contador == 15:
                entrada.append(1)
            else:
                entrada.append(0)
        elif i == 5:
            # Para el valor numérico del length del payload
            entrada.append(int(lista[5]))
        
    return entrada

#Función para agregar la etiqueta del dialecto correspondiente a la respuesta formateada
def assignDialect(response):
    if response[1] == 1 and response[2] == 0:
        response.insert(0, 1)
    elif response[3] == -1:
        response.insert(0, 2)     
    elif response[0] == -1:
        response.insert(0, 3)
    elif response[5] == 1:
        response.insert(0, 4)
    elif response[4] == 1:
        response.insert(0, 5)
    else:
        response.insert(0, 0)
    
    return response

#Función para predecir el dialecto de la respuesta del servidor, una vez que ha sido formateada
def predecir_dialecto(respuesta_completa):
    entrada_array = np.array(respuesta_completa).reshape(1, -1)
    dialecto_predicho = arbol_decision.predict(entrada_array)
    return dialecto_predicho[0]