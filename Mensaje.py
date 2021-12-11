import ObjetoSeguro as Fuente

obj1 = Fuente.ObjetoSeguro('Alicia') # Usamos nuestros objetos
obj2 = Fuente.ObjetoSeguro('Bob')
m1 = "Hola, Bob. ¿Como estas? Soy Alicia."
m2 = "Hola, Alicia, muy bien, ¿Nos veremos 4:30?"
m3 = "Si, en el museo barroco"
m4 = "Perfecto, alla te veo."

print("Las llaves de Alicia son:")
obj1.gen_llaves()
print("Las llaves de Bob son:")
obj2.gen_llaves()

obj1.intercambio(obj2.nombre, obj2.llave_publica())
obj2.intercambio(obj1.nombre, obj1.llave_publica())

saludo = obj1.saludar(obj1.nombre, m1)
obj2.esperar_respuesta(saludo)
respuesta = obj2.responder(m2)
obj1.esperar_respuesta(respuesta)
respuesta2 = obj1.responder(m3)
obj2.esperar_respuesta(respuesta2)
respuesta3 = obj2.responder(m4)
obj1.esperar_respuesta(respuesta3)
obj2.consultar_msj('{ID:<1>}')
obj1.consultar_msj('{ID:<1>}')
obj2.consultar_msj('{ID:<2>}')
obj1.consultar_msj('{ID:<2>}')