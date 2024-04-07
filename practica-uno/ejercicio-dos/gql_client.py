import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
           
        }
    }
"""
# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query_lista})
print(response.text)

# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta(nombre: "Cedro", especie: "Cedrus", edad: 8, altura: 300, frutos: true) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
                
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Definir la consulta GraphQL buscar plantas por especie
query = """
    {
        plantasPorEspecie(especie:"Cedrus"){
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query})
print(response.text)

# Definir la consulta GraphQL buscar las plantas que tienen frutos
query = """
    {
        plantasPorFrutos{
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query})
print(response.text)

# Definir la consulta GraphQL con la mutación para actualizar una planta
query_actualizar = """
    mutation {
        actualizarPlanta(id:3, nombre: "Orquideas", especie: "Orchidaceae", edad: 1, altura: 20, frutos: false) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_actualizar})
print(response_mutation.text)

# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id: 2) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

