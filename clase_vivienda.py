import sys
import csv


class Vivienda:

    dic_res = {
        "cu": {"PVC": 1 / 48, "XLPE": 1 / 44},
        "al": {"PVC": 0.033, "XLPE": 0.037},
    }
    secciones = (
        1.5,
        2.5,
        4,
        6,
        10,
        16,
        25,
        35,
        50,
        70,
        95,
        120,
        150,
        185,
        240,
        300,
        350,
        400,
    )
    dic_metodos = {
        "A1": "unipolar en pared térmicamente aislante",
        "A2": "multipolar en pared térmicamente aislante",
        "B1": "unipolar en tubo empotrado en pared o canal",
        "B2": "multipolar en tubo empotrado en pared o canal",
        "C": "fijado directamente en superficie",
        "E": "al aire sobre bandeja",
        "F": "al aire sobre soporte",
    }

    def __init__(
        self,
        instal="interior",
        conts="no",
        caida_max=3,
        fases=1,
        material="cu",
        aislamiento="PVC",
        metodo="B1",
        voltage=230,
        potencia=1000,
        longitud=40,
        cos_phi=1,
    ):
        self.instal = instal
        self.conts = conts
        self.caida_max = float(caida_max)
        self.fases = int(fases)
        self.material = material
        self.aislamiento = aislamiento
        self.metodo = metodo
        self.voltage = float(voltage)
        self.potencia = float(potencia)
        self.longitud = float(longitud)
        self.cos_phi = float(cos_phi)

    def __str__(self):
        return f"""-------------------------------------------------------
Tipo de instalación: {self.instal}
Centralización de contadores: {self.conts}
Caída de tensión máxima: {self.caida_max}% en {self.voltage} V
Número de fases del circuito: {self.fases}
Composición de los cables: {self.material.title()} / {self.aislamiento}
Método de intalación: {self.dic_metodos[self.metodo].capitalize()}
Poténcia a subministrar: {self.potencia} W
Longitud del conductor: {self.longitud} m
Factor de poténcia de la instalación: {self.cos_phi}
-------------------------------------------------------
"""

    @property
    def instal(self):
        return self._instal  # lga, di, interior

    @instal.setter
    def instal(self, instal):
        if instal.strip().lower() in ["lga", "di", "interior"]:
            self._instal = instal.strip().lower()
        else:
            raise ValueError("Instalación no válida.")

    @property
    def conts(self):
        return self._conts  # total,parcial,no

    @conts.setter
    def conts(self, conts):
        if conts.strip().lower() in ["total", "parcial", "no"]:
            self._conts = conts.strip().lower()
        else:
            raise ValueError(
                "Configuración de la centralización de contadores no válida."
            )

    @property
    def caida_max(self):
        return self._caida_max  # 3, 1.5,1,0.5

    @caida_max.setter
    def caida_max(self, caida_max):
        if self.instal == "interior":
            self._caida_max = 3
        elif self.conts == "no":
            if self.instal == "di":
                self._caida_max = 1.5
            else:
                raise ValueError("No puede no haber CC y LGA")
        elif self.conts == "total" and self.instal == "di":
            self._caida_max = 1
        elif self.conts == "total" and self.instal == "lga":
            self._caida_max = 0.5
        elif self.conts == "parcial" and self.instal == "di":
            self._caida_max = 0.5
        elif self.conts == "parcial" and self.instal == "lga":
            self._caida_max = 1
        else:
            raise ValueError(
                "No existe esta configuración de CC con el tipo de instalación"
            )

    @property
    def fases(self):
        return self._fases  # 1,3

    @fases.setter
    def fases(self, fases):
        if int(fases) == 1 or int(fases) == 3:
            self._fases = int(fases)
        else:
            raise ValueError("Número de fases no válido para el cálculo.")

    @property
    def voltage(self):
        return self._voltage  # 230,400

    @voltage.setter
    def voltage(self, voltage):
        if self.fases == 1:
            self._voltage = 230
        elif self.fases == 3:
            self._voltage = 400
        else:
            raise ValueError("Valor de tensión no válido para el cálculo.")

    @property
    def material(self):
        return self._material  # cu, al

    @material.setter
    def material(self, material):
        if material.strip().lower() in ["cu", "al"]:
            self._material = material.strip().lower()
        else:
            raise ValueError("Material no válido.")

    @property
    def aislamiento(self):
        return self._aislamiento  # PVC,XLPE

    @aislamiento.setter
    def aislamiento(self, aislamiento):
        if aislamiento.strip().upper() in ["PVC", "XLPE"]:
            self._aislamiento = aislamiento.strip().upper()
        else:
            raise ValueError("Aislamiento no válido.")

    @property
    def metodo(self):
        return self._metodo

    @metodo.setter
    def metodo(self, metodo):
        if metodo.strip().upper() in ["A1", "A2", "B1", "B2", "C", "E", "F"]:
            self._metodo = metodo.strip().upper()
        else:
            raise ValueError("Método no válido.")

    @property
    def potencia(self):
        return self._potencia  # (2,150.000.000)

    @potencia.setter
    def potencia(self, potencia):
        if 2 < float(potencia) < 150000000:
            self._potencia = float(potencia)
        else:
            raise ValueError("Valor de poténcia no válido para el cálculo.")

    @property
    def longitud(self):
        return self._longitud  # [0.1,500]

    @longitud.setter
    def longitud(self, longitud):
        if 0.1 <= float(longitud) < 500:
            self._longitud = float(longitud)
        else:
            raise ValueError("Valor de distáncia no válido para el cálculo.")

    @property
    def cos_phi(self):
        return self._cos_phi  # (0,1]

    @cos_phi.setter
    def cos_phi(self, cos_phi):
        if 0 < float(cos_phi) <= 1:
            self._cos_phi = float(cos_phi)
        else:
            raise ValueError("factor de poténcia no válido.")

    def saving_options(self):
        self.instal = input("Que tipo de instalación (LGA/DI/interior): ")
        self.conts = input("Tiene centralización de contadores (total/parcial/no)?: ")
        self.caida_max = 0
        # ahora se calcula automaticamente la caída de tensión máxima
        if self.instal == "lga":
            self.fases = 3
        else:
            self.fases = input("Cuantas fases tiene su instalación (1/3): ")
        # aqui se calcula automaticamente la tensión
        self.material = input("Material de los conductores (Cu/Al): ")
        self.aislamiento = input("Que tipo de aislamiento (PVC/XLPE): ")
        self.metodo = input(f"""Método de instalación:
- A1: unipolar en pared térmicamente aislante
- A2: multipolar en pared térmicamente aislante
- B1: unipolar en tubo empotrado en pared o canal
- B2: multipolar en tubo empotrado en pared o canal
- C: fijado directamente en superficie
- E: al aire sobre bandeja
- F: al aire sobre soporte\n""")
        self.potencia = input("Poténcia a subministrar: ")
        self.longitud = input("Longitud del conductor que desea instalar: ")
        if self.instal == "interior":
            self.cos_phi = 1
        else:
            self.cos_phi = input("FP del circuito: ")

    def fase_caidatension(self):
        res = self.dic_res[self.material][self.aislamiento]

        if self.fases == 1:
            s = round(
                (2 * res * self.potencia * self.longitud)
                / (self.cos_phi * self.voltage * self.voltage * (self.caida_max / 100)),
                3,
            )
        else:
            s = round(
                (res * self.potencia * self.longitud)
                / (self.cos_phi * self.voltage * self.voltage * (self.caida_max / 100)),
                3,
            )

        for seccion in self.secciones:
            if seccion >= s:
                return seccion

        raise ValueError("No ha sido posible calcular una sección por caida de tensión")

    def fase_calentamiento(self):
        if self.fases == 1:
            i_adm = self.potencia / (self.voltage * self.cos_phi)
        else:
            i_adm = self.potencia / (1.73205 * self.voltage * self.cos_phi)

        if self.metodo == "A1" and self.aislamiento == "PVC" and self.fases == 1:
            num = 4
        elif self.metodo == "A1" and self.aislamiento == "PVC" and self.fases == 3:
            num = 3
        elif self.metodo == "A1" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 6
        elif self.metodo == "A1" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 7
        elif self.metodo == "A2" and self.aislamiento == "PVC" and self.fases == 3:
            num = 2
        elif self.metodo == "A2" and self.aislamiento == "PVC" and self.fases == 1:
            num = 3
        elif self.metodo == "A2" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 5
        elif self.metodo == "A2" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 6
        elif self.metodo == "B1" and self.aislamiento == "PVC" and self.fases == 3:
            num = 5
        elif self.metodo == "B1" and self.aislamiento == "PVC" and self.fases == 1:
            num = 6
        elif self.metodo == "B1" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 8
        elif self.metodo == "B1" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 10
        elif self.metodo == "B2" and self.aislamiento == "PVC" and self.fases == 3:
            num = 4
        elif self.metodo == "B2" and self.aislamiento == "PVC" and self.fases == 1:
            num = 5
        elif self.metodo == "B2" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 7
        elif self.metodo == "B2" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 8
        elif self.metodo == "C" and self.aislamiento == "PVC" and self.fases == 3:
            num = 6
        elif self.metodo == "C" and self.aislamiento == "PVC" and self.fases == 1:
            num = 8
        elif self.metodo == "C" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 9
        elif self.metodo == "C" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 11
        elif self.metodo == "E" and self.aislamiento == "PVC" and self.fases == 3:
            num = 7
        elif self.metodo == "E" and self.aislamiento == "PVC" and self.fases == 1:
            num = 9
        elif self.metodo == "E" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 10
        elif self.metodo == "E" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 12
        elif self.metodo == "F" and self.aislamiento == "PVC" and self.fases == 3:
            num = 8
        elif self.metodo == "F" and self.aislamiento == "PVC" and self.fases == 1:
            num = 10
        elif self.metodo == "F" and self.aislamiento == "XLPE" and self.fases == 3:
            num = 11
        elif self.metodo == "F" and self.aislamiento == "XLPE" and self.fases == 1:
            num = 13

        if self.material == "cu":
            s = self.corriente_admisible[self.material][num][1.5]
        if self.material == "al":
            s = self.corriente_admisible[self.material][num][2.5]

        for sec in self.corriente_admisible[self.material][num]:
            if self.corriente_admisible[self.material][num][sec] <= i_adm:
                s = sec
            else:
                return s

        raise ValueError("No se puedo asignar una sección válida por calentamiento. ")

    def fase(self):
        fase1 = self.fase_caidatension()
        fase2 = self.fase_calentamiento()
        if fase1 >= fase2:
            return fase1
        elif fase2 > fase1:
            return fase2

    def neutro(self):
        s = self.fase()
        if self.instal == "lga" or self.instal == "di":
            if s <= 16:
                return s
            else:
                n = s / 2
                for _ in self.secciones:
                    if _ >= n:
                        return _
        else:  #  para interiores
            return s

    def tierra(self):
        s = self.fase()
        if s <= 16:
            t = s
        elif s > 35:
            t = s / 2
        else:
            t = 16
        for _ in self.secciones:
            if _ >= t:
                return _
        raise ValueError

    corriente_admisible = {
        "cu": {
            2: {
                1.5: 11,
                2.5: 15,
                4: 20,
                6: 25,
                10: 34,
                16: 45,
                25: 59,
                35: 72,
                50: 86,
                70: 109,
                95: 130,
                120: 150,
                150: 171,
                185: 194,
                240: 227,
                300: 259,
            },
            3: {
                1.5: 11.5,
                2.5: 16,
                4: 21,
                6: 27,
                10: 37,
                16: 49,
                25: 64,
                35: 77,
                50: 94,
                70: 118,
                95: 143,
                120: 164,
                150: 189,
                185: 213,
                240: 249,
                300: 285,
            },
            4: {
                1.5: 13,
                2.5: 17.5,
                4: 23,
                6: 30,
                10: 40,
                16: 54,
                25: 70,
                35: 86,
                50: 103,
                70: 130,
                95: 156,
                120: 188,
                150: 205,
                185: 233,
                240: 272,
                300: 311,
            },
            5: {
                1.5: 13.5,
                2.5: 18.5,
                4: 24,
                6: 32,
                10: 44,
                16: 59,
                25: 77,
                35: 96,
                50: 117,
                70: 149,
                95: 180,
                120: 208,
                150: 236,
                185: 268,
                240: 315,
                300: 349,
            },
            6: {
                1.5: 15,
                2.5: 21,
                4: 27,
                6: 36,
                10: 50,
                16: 66,
                25: 84,
                35: 104,
                50: 125,
                70: 160,
                95: 194,
                120: 225,
                150: 260,
                185: 297,
                240: 350,
                300: 396,
            },
            7: {
                1.5: 16,
                2.5: 22,
                4: 30,
                6: 37,
                10: 52,
                16: 70,
                25: 89,
                35: 110,
                50: 133,
                70: 171,
                95: 207,
                120: 240,
                150: 278,
                185: 317,
                240: 374,
                300: 423,
            },
            8: {
                1.5: 16.5,
                2.5: 23,
                4: 31,
                6: 40,
                10: 54,
                16: 73,
                25: 95,
                35: 119,
                50: 145,
                70: 185,
                95: 224,
                120: 260,
                150: 299,
                185: 341,
                240: 401,
                300: 461,
            },
            9: {
                1.5: 19,
                2.5: 26,
                4: 34,
                6: 44,
                10: 60,
                16: 81,
                25: 103,
                35: 127,
                50: 155,
                70: 199,
                95: 241,
                120: 280,
                150: 322,
                185: 368,
                240: 435,
                300: 516,
            },
            10: {
                1.5: 20,
                2.5: 26.5,
                4: 36,
                6: 46,
                10: 65,
                16: 87,
                25: 110,
                35: 137,
                50: 167,
                70: 214,
                95: 259,
                120: 301,
                150: 343,
                185: 391,
                240: 468,
                300: 547,
            },
            11: {
                1.5: 21,
                2.5: 29,
                4: 38,
                6: 49,
                10: 68,
                16: 91,
                25: 116,
                35: 144,
                50: 175,
                70: 224,
                95: 271,
                120: 314,
                150: 363,
                185: 415,
                240: 490,
                300: 640,
            },
        },
        "al": {
            2: {
                2.5: 11.5,
                4: 15,
                6: 20,
                10: 27,
                16: 36,
                25: 46,
                35: None,
                50: None,
                70: None,
                95: None,
                120: None,
                150: None,
                185: None,
                240: None,
                300: None,
            },
            3: {
                2.5: 12,
                4: 16,
                6: 21,
                10: 28,
                16: 38,
                25: 50,
                35: 61,
                50: 79,
                70: None,
                95: None,
                120: None,
                150: None,
                185: None,
                240: None,
                300: None,
            },
            4: {
                2.5: 13.5,
                4: 18.5,
                6: 24,
                10: 32,
                16: 42,
                25: 54,
                35: 67,
                50: 80,
                70: None,
                95: None,
                120: None,
                150: None,
                185: None,
                240: None,
                300: None,
            },
            5: {
                2.5: 14,
                4: 19,
                6: 25,
                10: 34,
                16: 46,
                25: 61,
                35: 75,
                50: 90,
                70: 118,
                95: 140,
                120: 162,
                150: 187,
                185: 212,
                240: 249,
                300: 285,
            },
            6: {
                2.5: 16,
                4: 22,
                6: 28,
                10: 38,
                16: 51,
                25: 64,
                35: 78,
                50: 96,
                70: 122,
                95: 148,
                120: 171,
                150: 197,
                185: 225,
                240: 265,
                300: 313,
            },
            7: {
                2.5: 17,
                4: 24,
                6: 30,
                10: 42,
                16: 56,
                25: 71,
                35: 88,
                50: 108,
                70: 136,
                95: 167,
                120: 193,
                150: 223,
                185: 236,
                240: 300,
                300: 343,
            },
            8: {
                2.5: 18,
                4: 24,
                6: 31,
                10: 42,
                16: 57,
                25: 72,
                35: 89,
                50: 108,
                70: 139,
                95: 169,
                120: 196.5,
                150: 227,
                185: 259,
                240: 306,
                300: 353,
            },
            9: {
                2.5: 20,
                4: 26.5,
                6: 33,
                10: 46,
                16: 63,
                25: 78,
                35: 97,
                50: 118,
                70: 151,
                95: 183,
                120: 213,
                150: 246,
                185: 281,
                240: 332,
                300: 400,
            },
            10: {
                2.5: 20,
                4: 27.5,
                6: 36,
                10: 50,
                16: 66,
                25: 84,
                35: 104,
                50: 127,
                70: 162,
                95: 197,
                120: 228,
                150: 264,
                185: 301,
                240: 355,
                300: 429,
            },
            11: {
                2.5: 22,
                4: 29,
                6: 38,
                10: 53,
                16: 70,
                25: 89,
                35: 109,
                50: 133,
                70: 170,
                95: 207,
                120: 239,
                150: 277,
                185: 316,
                240: 372,
                300: 462,
            },
        },
    }
