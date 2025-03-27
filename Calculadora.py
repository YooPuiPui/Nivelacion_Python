#titulo 
print("         CALCULADORA         ")
print("Ingrese las variables para calcular su suma, resta y multiplicacion.")

# Ingresemos el primer numero
print("\nIngrese el primer numero:")

# Y lo guardamos en la variable llamada numero1

numero1 = int(input())

# Segundo numero
print("\nIngrese el segundo numero:")
numero2 = int(input())

# Sumaremos los numeros 

suma = numero1 + numero2

print(f"El valor de la suma es: {suma}")

resta = numero1 - numero2

print(f"El valor de la resta es: {resta}")

mul = numero1*numero2
print(f"La multiplicacion es: {mul}")

print("\nDivision")
print("\nIngrese el primer valor a dividir:")
x = int(input())
print("\nIngrese el segundo valor a dividir:")
y = int(input())

div = x/y
print(f"El valor de la division es: {div} ")