import requests
import json

url = "http://localhost:8000/animales"

headers = {"Content-Type": "application/json"}

# POST /animales
nuevo_animal = {
    "tipo_animal": "mamifero",
    "nombre": "Leon",
    "genero": "Macho",
    "edad": 5,
    "peso":"10kg",
    
}
response = requests.post(url=url, json=nuevo_animal, headers=headers)
print(response.json())

# GET /animales
response = requests.get(url=url)
print(response.json())

# GET /animales
tipo_animal="mamifero"
response = requests.get(f"{url}/{tipo_animal}")
print("LISTA POR ESPECIE:",response.json())

# GET /animales
genero="Macho"
response = requests.get(f"{url}/macho")
print("LSITA POR GENERO:",response.json())

# PUT /animales/{animal_id}
animal_id_to_update = 1
updated_animal_data = {
    "peso":"20kg"
}

response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("animal actualizado:", response.json())

# DELETE /animales/{animales_id}
animales_id_to_delete = 1
response = requests.delete(f"{url}/{animales_id_to_delete}")
print("chocolate eliminado:", response.json())