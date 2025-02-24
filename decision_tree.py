import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn import tree
import pickle

# Columnas de entrada y salida
columnas_entrada = ['Dialect', ' Version', ' Type Name', ' Type Value', ' Code', ' non_printable_chars', ' bytes_sequence', ' payload_length']
columna_salida = ['Dialect']
todas_columnas = columnas_entrada + columna_salida
clases = ['Dialect 0','Dialect 1', 'Dialect 2', 'Dialect 3', 'Dialect 4', 'Dialect 5']

def cargar_datos():
    datos = pd.read_csv("coap_dataset.csv")
    datos['Dialect'] = datos['Dialect'].apply(lambda x: int(x[8:]))
    return datos

def dividir_datos_prueba(datos):
    division = int(0.7 * datos.shape[0])
    datos_entrenamiento = datos[:division]
    datos_prueba = datos.iloc[division:]
    entradas_entrenamiento = datos_entrenamiento[columnas_entrada].to_numpy()
    salidas_entrenamiento = datos_entrenamiento[columna_salida].to_numpy()
    entradas_prueba = datos_prueba[columnas_entrada].to_numpy()
    salidas_prueba = datos_prueba[columna_salida].to_numpy()
    return entradas_entrenamiento, entradas_prueba, salidas_entrenamiento, salidas_prueba

def entrenar_modelo(entradas_entrenamiento, salidas_entrenamiento):
    arbol_decision = DecisionTreeClassifier(criterion='entropy', max_depth=10)
    arbol_decision.fit(entradas_entrenamiento, salidas_entrenamiento)
    pickle.dump(arbol_decision, open('ModeloEntrenado', 'wb'))
    return arbol_decision

def evaluar_modelo(arbol_decision, entradas_prueba, salidas_prueba):
    return arbol_decision.score(entradas_prueba, salidas_prueba)

def predecir(arbol_decision, entrada):
    entrada_lista = datos(entrada)
    entrada_array = np.array(entrada_lista)
    entrada_array = entrada_array.reshape(1, -1)
    salida = arbol_decision.predict(entrada_array)
    return 'Dialect ' + str(salida[0])

def importancia_caracteristicas(arbol):
    importancia = arbol.feature_importances_
    for i, v in enumerate(importancia):
        print(f"{columnas_entrada[i]} Score: {v:.5f}")
    plt.bar([x for x in range(len(importancia))], importancia)
    plt.show()

def dibujar_arbol(arbol):
    fig, axes = plt.subplots(figsize= (52,32), dpi=500)
    tree.plot_tree(arbol, feature_names=columnas_entrada, class_names=clases, filled=True, fontsize=10)
    fig.savefig('Arbol.png')
    plt.show()


datos = cargar_datos()
entradas_entrenamiento, entradas_prueba, salidas_entrenamiento, salidas_prueba = dividir_datos_prueba(datos)
arbol_decision = entrenar_modelo(entradas_entrenamiento, salidas_entrenamiento)
puntaje = evaluar_modelo(arbol_decision, entradas_prueba, salidas_prueba)
print(puntaje)
dibujar_arbol(arbol_decision)
importancia_caracteristicas(arbol_decision)