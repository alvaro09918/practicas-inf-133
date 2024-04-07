from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "Leon",
        "especie": "Mamifero",
        "genero": "Macho",
        "edad": "3",
        "peso": "30",
    },
]
class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def listar_animales(self,campo, atibuto):
        animales_filtrados = [
                    animal
                    for animal in animales
                    if animal[campo] == atibuto
                ]
        return animales_filtrados
        
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_especie =self.listar_animales("especie", especie)
                if animales_especie != []:
                    self.response_handler(200, animales_especie)
                else:
                    self.response_handler(204,[])
                    
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_genero =self.listar_animales("genero", genero)
                if animales_genero != []:
                    self.response_handler(200,animales_genero)
                else:
                    self.response_handler(204,[])
            else: 
                    self.response_handler(200,animales)
       
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente =self.buscar_paciente(ci)
            if paciente:
                self.response_handler(200,[paciente])
        else:
                self.response_handler(404,[])
    
    def do_POST(self):
        if self.path == "/animales":
            post_data=self.read_data()
            post_data["id"] = len(animales) + 1
            animales.append(post_data)
            self.response_handler(201,animales)

        else:
            self.response_handler(404,[])
    
    def do_PUT(self):
        if self.path.startswith("/animales"):
            data=self.read_data()
            id = data["id"]
            animal = next(
                (animal for animal in animales if animal["id"] == id),
                None,
            )
            if animal:
                animal.update(data)
                self.response_handler(200,[animal])
        else:
            self.response_handler(404,[])
               
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal =next(
                (animal for animal in animales if animal["id"] == id),
                None,
            )
            if animal:
                animales.remove(animal)
                self.response_handler(200,animales)
            else:
                self.response_handler(404,[])   
        else:
            self.response_handler(404,[])
            
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()