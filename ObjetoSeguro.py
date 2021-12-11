from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import base64
import json
import binascii

class ObjetoSeguro:
    def __init__(self, nombre): #Declaramos nuesta clase que va a recibir el parametro de nombre
        self.nombre = nombre
        self.llave_dif = 0
        self.nombre_dif = 0
        self.__id = 0
        self.__registro = {}

    def intercambio(self, nombre, llave):
        self.nombre_dif = nombre
        self.llave_dif = llave


    def gen_llaves(self): #Empieza a generarse las llaves, primero la priv y luego la pub.
        self__private_key = generate_eth_key()
        self.__private_key_hex = self__private_key.to_hex()
        self.public_key = self__private_key.public_key.to_hex()  # La llave esta en string
        print(self.public_key)
        print(self.__private_key_hex)
        print(" ")

    def saludar(self, name, msj):
        codificado = self.__codificar64(msj)  #El mensaje se codifica a bytes
        cifrado = self.__cifrar_msj(self.llave_dif, codificado)  # Se cifra el mensaje con la llave del destinatario
        print(f'{name}{" Saludo: "}{cifrado}')
        return cifrado  # Devuelve un mensaje tipo llave

    def responder(self, msj):
        codificado = self.__codificar64(msj)
        cifrado = self.__cifrar_msj(self.llave_dif, codificado)
        print("Respuesta " + cifrado)
        return cifrado  # l mensaje se cifra para ser enviado

    def llave_publica(self):
        return self.public_key  # Retorna la llave publica

    @staticmethod
    def __cifrar_msj(pub_key, msj):
        msjb = msj.encode()  # EL texto en claro de str pasan a bytes
        cifradollave = encrypt(pub_key, msjb)  #Se cifran la llave publica y el mensaje en bytes
        cifradob = binascii.hexlify(cifradollave)
        cifrado = cifradob.decode()  # Decodifica cifradob de bytes a str
        return cifrado

    def __descifrar_msj(self, msj):
        msjb = msj.encode()
        msjllave = binascii.a2b_hex(msjb)
        descifradollave = decrypt(str(self.__private_key_hex), msjllave)  # Uso de llave privada
        descifrado = descifradollave.decode() #Se decifra el mensaje
        return descifrado  # Saca el texto en claro en bytes

    @staticmethod
    def __codificar64(msj):
        msjb = msj.encode()
        codificado = base64.b64encode(msjb)
        msjnb = codificado.decode()
        return msjnb

    @staticmethod
    def __decodificar64(msj):
        msjb = msj.encode()
        decodificadob = base64.b64decode(msjb)  # Decodifica de base64
        decodificado = decodificadob.decode()  # Decodifica de byte a str
        return decodificado  # Retorna str

    def __almacenar_msj(self, msj):
        self.__id = int(self.__id)
        self.__id = self.__id + 1
        nombrearchivo = "RegistoMsj_<" + self.nombre + ">.json"
        idstr = str(self.__id)
        self.__registro["{ID:<" + idstr + ">}"] = {
            'Numero': self.__id,
            'Receptor': self.nombre,
            'Texto': msj,
            'Emisor': self.nombre_dif}
        with open(nombrearchivo, 'w') as f:
            json.dump(self.__registro, f, indent=4)
        print("{ID:<" + idstr + ">}")
        return "{ID:<" + idstr + ">}"

    def consultar_msj(self, id):
        nombrearchivo = "RegistoMsj_<" + self.nombre + ">.json"
        with open(nombrearchivo, 'r') as consulta:
            objeto_json = json.load(consulta)
            print(objeto_json[str(id)])
        return objeto_json[str(id)]

    def esperar_respuesta(self, msj):
        descifrado = self.__descifrar_msj(msj)  # Descifra con la clave privada y el msj en tipo llave
        decodificado = self.__decodificar64(descifrado)  # Decodifica con el mensaje en bytes
        self.__almacenar_msj(decodificado)