import requests


# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los pacientes por la ruta /pacientes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA PACIENTES: ", get_response.text)

# POST agrega un nuevo paciente por la ruta /pacientes
#areglar la generacion de ci
ruta_post = url + "pacientes"
nuevo_paciente = {
    
    "nombre": "Dayana",
    "apellido": "Ramirez",
    "edad": 24,
    "genero": "Femenino",
    "diagnostico": "Artritis",
    "doctor": "Pedro",
}

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print("CREAR PACIENTES: ",post_response.text)
ruta_post = url + "pacientes"
nuevo_paciente = {
    
    "nombre": "Dayana",
    "apellido": "Ramirez",
    "edad": 24,
    "genero": "Femenino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro",
}

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print("CREAR PACIENTES: ",post_response.text)

# GET busca a un paciente por ci /pacientes/
ruta_filtrar_paciente = url + "pacientes/2"
filtrar_paciente_response = requests.request(method="GET", url=ruta_filtrar_paciente)
print("BUSCA PACIENTE POR ID: ",filtrar_paciente_response.text)

# GET obtener a todos los pacientes con diagnostico de diabetes por la ruta /pacientes
ruta_get = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA PACIENTES CON DIABETES: ", get_response.text)

# GET obtener a todos los pacientes que tienen por doctor Pedro Perez por la ruta /pacientes
ruta_get = url + "pacientes?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA PACIENTES CON MISMO DOCTOR: ", get_response.text)

# PUT actualiza un paciente por la ruta /pacientes
ruta_actualizar = url + "pacientes"
paciente_actualizado = {
    "ci": 2,
    "nombre": "Dayana",
    "apellido": "Gutierrez",
    "edad": 25,
    "genero": "Femenino",
    "diagnostico": "Artritis",
    "doctor": "Ruben Lopez",
}
put_response = requests.request( method="PUT", url=ruta_actualizar, json=paciente_actualizado)
print("ACTUALIZA PACIENTES: ",put_response.text)

# DELETE elimina paciente por CI
ruta_eliminar = url + "pacientes/2"

eliminar_response = requests.request(method="DELETE",  url=ruta_eliminar)
print("ELIMINA PACIENTES: ",eliminar_response.text)

