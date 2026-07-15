import sys
import csv
import os
from clase_vivienda import Vivienda


def main():
    while True:
        os.system("cls")
        index()
        com = input().strip()
        os.system("cls")
        if com == "1":
            try:
                vivienda1 = Vivienda()
                vivienda1.saving_options()
                fase = vivienda1.fase()
                neutro = vivienda1.neutro()
                tierra = vivienda1.tierra()
                print(f"""Será necesario: 
                Fase: {vivienda1.fases} x {fase} mm^2 
                Neutro: 1 x {neutro} mm^2 (en caso de ser incluido)
                Tierra: 1 x {tierra} mm^2.
                """)
                arch = input(
                    "Quieres guardar estos resultados en un archivo (pulse 1)? "
                ).strip()
                os.system("cls")
                if arch == "1":
                    name = input("Com quieres que se llame el archivo? ").strip()
                    os.system("cls")
                    archivo(name, vivienda1)
                    print("Archivo guardado correctamente! ")
                a = input("")

            except ValueError:
                print(
                    "Error durante el proceso de guardado, comprueve el dato introducido y vuelva a provar."
                )
                a = input("")
                pass

        elif com == "2":
            print("Cerrando...")
            sys.exit()
        else:
            print("Opción no válida.")
            a = input("")


def index():
    print("""OPCIONES DEL PROGRAMA:       
    1.Calcular las secciones de los conductores en un circuito eléctrico en una vivienda (Con opción a guardado).
    2.Salir del programa.""")


def archivo(nombre, vivienda):
    with open(f"{nombre}.csv", "w") as file:
        f = vivienda.fase()
        n = vivienda.neutro()
        t = vivienda.tierra()
        file.write(f"""CON UNA INSTALACIÓN CON ESTAS CARACTERÍSTICAS:
- Tipo de instalación: {vivienda.instal}
- Centralización de contadores: {vivienda.conts}
- Caída de tensión máxima: {vivienda.caida_max}% en {vivienda.voltage} V
- Número de fases del circuito: {vivienda.fases}
- Composición de los cables: {vivienda.material.title()} / {vivienda.aislamiento}
- Método de intalación: {vivienda.dic_metodos[vivienda.metodo].capitalize()}
- Poténcia a subministrar: {vivienda.potencia} W
- Longitud del conductor: {vivienda.longitud} m
- Factor de poténcia de la instalación: {vivienda.cos_phi}
            
SERAN RECOMENDABLES UNAS SECCIONES MÍNIMAS:
- Fase: {vivienda.fases} x {f} mm^2 
- Neutro: 1 x {n} mm^2 (en caso de ser incluido)
- Tierra: 1 x {t} mm^2.
""")


if __name__ == "__main__":
    main()
