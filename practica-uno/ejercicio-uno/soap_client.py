from zeep import Client

client=Client('http://localhost:8000')
result=client.service.SumaDosNumeros(10,2)
print("LA SUMA ES:",result)
result=client.service.RestaDosNumeros(10,2)
print("LA RESTA ES:",result)
result=client.service.MultiplicarDosNumeros(10,2)
print("LA MULTIPLICACION ES:",result)
result=client.service.DividirDosNumeros(10,2)
print("LA DIVISION ES:",result)
