from tkinter import *
import numpy as np

ventana = Tk()
ventana.title("Calculadora")
ventana.geometry("400x190") #tamaño
ventana.resizable(0,0) #bloquear tamaño para que el usuario no la modifique

# Textos
# Label anañde texto a la ventana, con grid la pocicion dentro de la ventana 

textoUno = Label(ventana, text="Valor 1")
textoDos = Label(ventana, text="Valor 2")
textoUno.grid(row=0, column=0, padx=5, pady=5)
textoDos.grid(row=0, column=3, padx=5, pady=5)


# Entradas

entradaUno = Entry(ventana)
entradaDos = Entry(ventana)
entradaSuma = Entry(ventana, state="readonly")
entradaResta = Entry(ventana, state=DISABLED)
entradaMultiplicacion = Entry(ventana, state=DISABLED)
entradaDivision = Entry(ventana, state=DISABLED)

#con grid la pocicion dentro de la ventana
entradaUno.grid(row=0, column=1,padx=5,pady=5)
entradaDos.grid(row=0, column=4,padx=5,pady=5)
entradaSuma.grid(row=1,column=1,padx=5,pady=5)
entradaResta.grid(row=2,column=1,padx=5,pady=5)
entradaMultiplicacion.grid(row=3, column=1, padx=5, pady=5)
entradaDivision.grid(row=4,column=1,padx=5,pady=5)


# Botones
# Command nos indica que funcion se reproducira al hacer click en el boton

botonSuma = Button(ventana, text="Suma", width=8, height=1, command= lambda:clickBotonSuma(entradaUno.get(), entradaDos.get()))
botonResta = Button(ventana, text="Resta", width=8,height=1, command= lambda:clickBotonResta(entradaUno.get(), entradaDos.get()))
botonMultiplicacion = Button(ventana, text="Multiplicar", width=8,height=1, command=lambda:clickBotonMultiplicacion(entradaUno.get(), entradaDos.get()))
botonDivision = Button(ventana, text="Dividir", width=8,height=1,command=lambda:clickBotonDivision(entradaUno.get(), entradaDos.get()))

#con grid la pocicion dentro de la ventana
botonSuma.grid(row=1, column=0, padx=5, pady=5)
botonResta.grid(row=2, column=0, padx=5, pady=5)
botonMultiplicacion.grid(row=3, column=0, padx=5, pady=5)
botonDivision.grid(row=4, column=0, padx=5, pady=5)

#Funciones calculadora

# recibe los parametros x,y
def clickBotonSuma(x,y):
    entradaSuma.configure(state=NORMAL) #NORMAL permite editar la caja de texto "entradaSuma"
    entradaSuma.delete(0,END) # Borra el contenido desde la posicion 0 hasta END (final del texto)
    entradaSuma.insert(0,f"{int(x)+int(y)}") # convierte x e y en enteros y los suma, los inserta en la posicion 0
    entradaSuma.configure(state=DISABLED) # DISABLED NO es editable
    botonSuma.configure(background="BLUE") # Cambia el color de fondo del botón a

def clickBotonResta(x,y):
    entradaResta.configure(state=NORMAL)
    entradaResta.delete(0,END)
    entradaResta.insert(0,f"{int(x)-int(y)}")
    entradaResta.configure(state=DISABLED)
    botonResta.configure(background="BLUE")

def clickBotonMultiplicacion(x,y):
    entradaMultiplicacion.configure(state=NORMAL)
    entradaMultiplicacion.delete(0,END)
    entradaMultiplicacion.insert(0,f"{int(x)*int(y)}")
    entradaMultiplicacion.configure(state=DISABLED)
    botonMultiplicacion.configure(background="BLUE")

def clickBotonDivision(x,y):
    entradaDivision.configure(state=NORMAL)
    entradaDivision.delete(0,END)
    entradaDivision.insert(0,f"{np.double(x)/np.double(y)}")
    entradaDivision.configure(state=DISABLED)
    botonDivision.configure(background="BLUE")

ventana.mainloop()