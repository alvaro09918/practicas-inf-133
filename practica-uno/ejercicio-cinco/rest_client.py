import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"

# POST crear un nuevo animal

ruta_post = url + "animales"
nuevo_animal = {
    
    "nombre": "Rana",
    "especie": "Anfibio",
    "genero": "Hembra",
    "edad": "1",
    "peso": "10",
}

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("NUEVO ANIMAL: ",post_response.text)

# POST crear un nuevo animal

ruta_post = url + "animales"
nuevo_animal = {
    
    "nombre": "Aguila",
    "especie": "Oviparo",
    "genero": "Macho",
    "edad": "5",
    "peso": "15",
}

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("NUEVO ANIMAL: ",post_response.text)

# GET obtiene todo los animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA ANIMALES: ", get_response.text)



# GET obtiene a todo los animales por especie
ruta_get = url + "animales?especie=Anfibio"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA_ANIMALES_ESPECIE: ", get_response.text)

# GET obtener  a todo los animales por genero
ruta_get = url + "animales?genero=Macho"
get_response = requests.request(method="GET", url=ruta_get)
print("LISTA_ANIMALES_GENERO: ", get_response.text)

# PUT actualiza un animal por la ruta /animales
ruta_actualizar = url + "animales"
animal_actualizado = {
    "id":2,
    "nombre": "Ballena",
    "especie": "Mamifero",
    "genero": "Macho",
    "edad": "5",
    "peso": "200",
}
put_response = requests.request( method="PUT", url=ruta_actualizar, json=animal_actualizado)
print("ANIMAL_ACTUALIZADO: ",put_response.text)

# DELETE elimina un animal por la ruta /animales
ruta_eliminar = url + "animales/2"

eliminar_response = requests.request(method="DELETE",  url=ruta_eliminar)
print("ANIMAL_ELIMINADO: ",eliminar_response.text)
