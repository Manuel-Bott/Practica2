import random
import mysql.connector

class Personaje:
    def __init__(self, nombre, atributos):
        self.nombre = nombre
        self.atributos = atributos

class JuegoAdivinaQuien:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor()
        self.personajes = self.obtener_personajes()

    def obtener_personajes(self):
        self.cursor.execute("SELECT nombre, atributos FROM Personajes")
        rows = self.cursor.fetchall()
        personajes = []
        for row in rows:
            personajes.append(Personaje(row[0], eval(row[1])))
        return personajes

    def hacer_pregunta(self, atributo, valor):
        respuesta = input(f"¿El personaje es de {atributo} {valor}? (s/n): ").lower()
        #atributos_compartidos = [a for a, v in random.choice(self.personajes).atributos.items() if v == valor]
        atributos_compartidos = [a for a, v in self.personajes[0].atributos.items() if v == valor]
        
        if respuesta == 's':
            self.personajes = [p for p in self.personajes if p.atributos[atributo] == valor]
        else:
            self.personajes = [p for p in self.personajes if p.atributos[atributo] != valor]

        # Filtrar personajes basados en atributos compartidos
        for atributo_compartido in atributos_compartidos:
            if atributo_compartido != atributo:
                self.personajes = [p for p in self.personajes if p.atributos[atributo_compartido] == self.personajes[0].atributos[atributo_compartido]]

        return len(self.personajes) > 0

    def jugar(self):
        
        print("Piensa en un personaje de 'El Señor de los Anillos', y yo intentaré adivinar quién es haciendo preguntas sobre sus atributos.")
        print("Responde con 's' para sí y 'n' para no.")
        input("Presiona Enter cuando estés listo para comenzar...")
        adivinado = False
        
        while not adivinado:
            
            try:
                personaje_secreto = random.choice(self.personajes)
                
            except IndexError:
                print("No quedan personajes para adivinar. Reiniciando el juego...")
                self.personajes = self.obtener_personajes()
            
            
            for atributo, valor in personaje_secreto.atributos.items():
                
                if self.hacer_pregunta(atributo, valor):
                    pass
                
                else:
                    break

                if len(self.personajes) == 1:
                    adivinado = True
                    break

            if len(self.personajes) == 0:
                print("No pude adivinar el personaje. Intentemos con otros atributos.")
                continue

            if len(self.personajes) == 1:
                print(f"¡Tu personaje es {self.personajes[0].nombre}!")
                Decision = input("Quieres buscar otro personaje? 'S' para sí y 'n' para no.").lower()
                if Decision =='n':
                    print("Has concluido con la busqueda.")
                    break
                    exit()
                
                elif Decision == 's':
                    print("¡¡Vamos de Nuevo!!.")
                    self.personajes = self.obtener_personajes()
                    juego.jugar()
                    
                else:
                    print("Por favor elige una opcion valida.")
                    

        agregar_nuevo = input("¿Te gustaría agregar un nuevo personaje? (s/n): ").lower()
        if agregar_nuevo == 's':
            self.agregar_personaje()
            
        elif agregar_nuevo =='n':
            print("Has concluido con el programa. Hasta Luego.")
            exit()
            
        else:
            print("Por favor elige una opcion valida...")

    def agregar_personaje(self):
        nombre = input("Ingresa el nombre del nuevo personaje: ")
        atributos = {}
        for atributo in self.personajes[0].atributos.keys():
            valor = input(f"Ingresa el valor del atributo '{atributo}': ")
            atributos[atributo] = valor

        sql = "INSERT INTO Personajes (nombre, atributos) VALUES (%s, %s)"
        self.cursor.execute(sql, (nombre, str(atributos)))
        self.conn.commit()
        print("Personaje agregado correctamente.")
        Decision2 = input("Volver a Menu Inicial 'v', Salir 'S' ").lower()
        if Decision2 =='s':
            print("Has concluido con el programa. Hasta Luego.")
            exit()
                
        elif Decision2 == 'v':
            print("¡¡Vamos de Nuevo!!.")
            print("Bienvenido al juego Adivina Quién.")
            juego.jugar()
                    
        else:
            print("Por favor elige una opcion valida333.")

# Parámetros de conexión a la base de datos MySQL
connection_params = {
    'host': 'localhost',
    'user': 'ManuelPena00',
    'password': 'Khtb453749.Dt',
    'database': 'adivinaquiendb',
    'port':'3306'
}

# Iniciar el juego
juego = JuegoAdivinaQuien(connection_params)
print("Bienvenido al juego Adivina Quién.")
juego.jugar()



#Khtb453749.Dt
