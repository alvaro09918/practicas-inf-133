from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 1,
        "nombre": "Juan",
        "apellido": "Medrano",
        "edad": 23,
        "genero": "Masculino",
        "diagnostico": "Reumatismo",
        "doctor": "Pedro Perez",
    },
]

class PacienteService:
    @staticmethod
    def buscar_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )
    
    @staticmethod
    def listar_pacientes(campo, atibuto):
        pacientes_filtrados = [
                    paciente
                    for paciente in pacientes
                    if paciente[campo] == atibuto
                ]
        return pacientes_filtrados
    
    @staticmethod
    def add_paciente(post_data):
        post_data["ci"] = len(pacientes) + 1
        pacientes.append(post_data)
        return pacientes
    @staticmethod
    def update_paciente(data,ci):
        paciente =PacienteService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None
    
    @staticmethod
    def delete_paciente(ci):
        
        paciente =PacienteService.buscar_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return pacientes
        else:
            return None
            
class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
class RESTRequestHandler(BaseHTTPRequestHandler):
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                
                pacientes_filtrados=PacienteService.listar_pacientes("diagnostico", diagnostico)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.response_handler(self, 200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.response_handler(self, 204,[])
                    
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                
                pacientes_filtrados =PacienteService.listar_pacientes("doctor", doctor)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.response_handler(self,200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.response_handler(self,204,[])
            else: 
                    HTTPResponseHandler.response_handler(self,200,pacientes)
    
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente =PacienteService.buscar_paciente(ci)
            if paciente:
                HTTPResponseHandler.response_handler(self,200,[paciente])
        else:
                HTTPResponseHandler.response_handler(self,404,[])
    
    def do_POST(self):
        if self.path == "/pacientes":
            post_data=self.read_data()
            post_data=PacienteService.add_paciente(post_data)
            HTTPResponseHandler.response_handler(self, 201,post_data)

        else:
            HTTPResponseHandler.response_handler(self,404,[])
    
    def do_PUT(self):
        if self.path.startswith("/pacientes"):
            data=self.read_data()
            ci = data["ci"]
            paciente=PacienteService.update_paciente(data, ci)
            HTTPResponseHandler.response_handler(self,200,[paciente])
        else:
            HTTPResponseHandler.response_handler(self, 404,[])              
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente=PacienteService.delete_paciente(ci)
            if paciente:
                HTTPResponseHandler.response_handler(self, 200,pacientes)
            else:
                HTTPResponseHandler.response_handler(self, 404,[])   
        else:
            HTTPResponseHandler.response_handler(self, 404,[])
            
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