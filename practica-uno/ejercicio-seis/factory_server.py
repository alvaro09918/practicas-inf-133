from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Base de datos simulada de animales
animales = {}


class Animal:
    def __init__(self,tipo_animal,nombre, genero,edad, peso):
        self.tipo_animal=tipo_animal
        self.nombre=nombre
        self.genero=genero
        self.edad=edad
        self.peso=peso


class Mamifero(Animal):
    def __init__(self,nombre, genero, edad,peso):
        super().__init__("mamifero",nombre, genero, edad, peso)

class Ave(Animal):
    def __init__(self,nombre, genero, edad,peso):
        super().__init__("ave",nombre, genero, edad, peso)

class Reptil(Animal):
    def __init__(self,nombre, genero, edad,peso):
        super().__init__("reptil",nombre, genero, edad, peso)

class Anfibio(Animal):
    def __init__(self,nombre, genero, edad,peso):
        super().__init__("anfibio",nombre, genero, edad, peso)            

class Pez(Animal):
    def __init__(self,nombre, genero, edad,peso):
        super().__init__("pez",nombre, genero, edad, peso)   

class AnimalFactory:
    @staticmethod
    def create_animal(tipo_animal,nombre, genero,edad, peso ):
        if tipo_animal == "mamifero":
            return Mamifero(nombre, genero,edad, peso)
        elif tipo_animal == "ave":
            return Ave(nombre, genero,edad, peso)
        elif tipo_animal == "reptil":
            return Reptil(nombre, genero,edad, peso)
        elif tipo_animal == "anfibio":
            return Anfibio(nombre, genero,edad, peso)
        elif tipo_animal == "pez":
            return Pez(nombre, genero,edad, peso)
        else:
            raise ValueError("Tipo de animal  no válido")

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class AnimalService:
    def __init__(self):
        self.factory = AnimalFactory()

    def add_animal(self, data):
        tipo_animal=data.get("tipo_animal", None)
        nombre=data.get("nombre", None)
        genero=data.get("genero", None)
        edad=data.get("edad", None)
        peso=data.get("peso", None)

        animal = self.factory.create_animal(
            tipo_animal, nombre, genero, edad, peso
        )
        animales[len(animales) + 1] = animal
        return animal
    
    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def list_animales_tipo(self,tipo_animal):
        especie=None
        if tipo_animal == "mamifero":
            especie= Mamifero
        elif tipo_animal == "ave":
            especie= Ave
        elif tipo_animal == "reptil":
            especie=Reptil
        elif tipo_animal == "anfibio":
            especie=Anfibio
        elif tipo_animal == "pez":
            especie= Pez
        
        mamiferos = {}
        for index, animal in animales.items():
            if isinstance(animal, especie):
                mamiferos[index] = animal.__dict__
        return mamiferos

    def list_animales_genero(self, genero):
        animales_filtrados = {}
        for index, animal in animales.items():
            if animal.genero == genero:
                animales_filtrados[index] = animal.__dict__
        return animales_filtrados


    def update_animales(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre=data.get("nombre", None)
            genero=data.get("genero", None)
            edad=data.get("edad", None)
            peso=data.get("peso", None)

            if nombre:
                animal.nombre = nombre
            if genero:
                animal.genero = genero
            if edad:
                animal.edad = edad
            if peso:
                animal.peso = peso
            return animal
        else:
            raise None

    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "animal eliminado"}
        else:
            return None
class AnimalesRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_service = AnimalService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        if self.path == "/animales":
            response_data = self.animal_service.list_animales()
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        elif self.path.startswith("/animales/"):
            animal_tipo= self.path.split("/")[-1]
            response_data = self.animal_service.list_animales_tipo(animal_tipo)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "animal no encontrado"}
                )
                
        elif self.path.startswith("/animales/"):
            genero= self.path.split("/")[-1]
            response_data = self.animal_service.list_animales_genero(genero)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "animal no encontrado"}
                )    
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.update_animales(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.animal_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
    
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, AnimalesRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()