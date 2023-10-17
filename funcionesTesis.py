from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
import os

base_datos = sqlite3.connect('LaJardinera.bd')
cursor = base_datos.cursor()

cursor.execute('SELECT * FROM producto')
product = cursor.fetchall()

def agregar_proveedor(a):
    ventana_agregar_proveedor = Toplevel(a)
    ventana_agregar_proveedor.title('Agregar Proveedor')

    agregar_proveedor_label = ttk.Label(ventana_agregar_proveedor, text='Agregar Proveedor')
    agregar_proveedor_label.grid(row=0, column=0, columnspan=2)

    proveedor_razon_social_label = ttk.Label(ventana_agregar_proveedor, text='Razon Social: ')
    proveedor_razon_social_label.grid(row=1, column=0)

    proveedor_razon_social_entry = ttk.Entry(ventana_agregar_proveedor)
    proveedor_razon_social_entry.grid(row=1, column=1)

    proveedor_cuit_label = ttk.Label(ventana_agregar_proveedor, text='CUIT: ')
    proveedor_cuit_label.grid(row=2, column=0)

    proveedor_cuit_entry = ttk.Entry(ventana_agregar_proveedor)
    proveedor_cuit_entry.grid(row=2, column=1)

    proveedor_domicilio_label = ttk.Label(ventana_agregar_proveedor, text='Domicilio: ')
    proveedor_domicilio_label.grid(row=3, column=0)

    proveedor_domicilio_entry = ttk.Entry(ventana_agregar_proveedor)
    proveedor_domicilio_entry.grid(row=3, column=1)

    proveedor_telefono_label = ttk.Label(ventana_agregar_proveedor, text='Telefono: ')
    proveedor_telefono_label.grid(row=4, column=0)

    proveedor_telefono_entry = ttk.Entry(ventana_agregar_proveedor)
    proveedor_telefono_entry.grid(row=4, column=1)

    proveedor_email_label = ttk.Label(ventana_agregar_proveedor, text='Email: ')
    proveedor_email_label.grid(row=5, column=0)

    proveedor_email_entry = ttk.Entry(ventana_agregar_proveedor)
    proveedor_email_entry.grid(row=5, column=1)

    def guardar_proveedor():
        razon_social = proveedor_razon_social_entry.get()
        cuit = proveedor_cuit_entry.get()
        domicilio = proveedor_domicilio_entry.get()
        numeroTelefono = proveedor_telefono_entry.get()
        email = proveedor_email_entry.get()

        cursor.execute('INSERT INTO proveedor (razon_social, cuit, domicilio, numero_telefono, email) VALUES (?,?,?,?,?)',
               (razon_social, cuit, domicilio, numeroTelefono, email))
        base_datos.commit()
        
        messagebox.showinfo('Completado','El proveedor ha sido guardado con éxito.')
        ventana_agregar_proveedor.destroy()

    boton_guardar_proveedor = Button(ventana_agregar_proveedor, text='Guardar', command=guardar_proveedor)
    boton_guardar_proveedor.grid(row=6, column=0, columnspan=2)

def consultar_proveedores():
    cursor.execute("SELECT razon_social FROM proveedor")
    proveedores = cursor.fetchall()
    base_datos.commit()
    print(proveedores)
    return ['Seleccionar Proveedor'] + [nombre[0] for nombre in proveedores]

def agregar_categoria(a):
    ventana_agregar_categoria = Toplevel(a)
    ventana_agregar_categoria.title('Agregar Categoria')

    agregar_categoria_label = Label(ventana_agregar_categoria, text='Agregar Categoria')
    agregar_categoria_label.grid(row=0, column=0, columnspan=2)

    categoria_nombre_label = Label(ventana_agregar_categoria, text='Nombre: ')
    categoria_nombre_label.grid(row=1, column=0)

    categoria_nombre_entry = Entry(ventana_agregar_categoria)
    categoria_nombre_entry.grid(row=1, column=1)

    def guardar_categoria():
        nombre = categoria_nombre_entry.get()

        cursor.execute('INSERT INTO categoria (nombre) VALUES (?)',
               (nombre,))
        base_datos.commit()
        
        messagebox.showinfo('Completado','La categoria ha sido guardada con éxito.')
        ventana_agregar_categoria.destroy()

    boton_guardar_proveedor = Button(ventana_agregar_categoria, text='Guardar', command=guardar_categoria)
    boton_guardar_proveedor.grid(row=6, column=0, columnspan=2)

def consultar_categorias():
    cursor.execute("SELECT nombre FROM categoria")
    categoria = cursor.fetchall()
    base_datos.commit()
    return ['Seleccionar Categoria'] + [nombre[0] for nombre in categoria]

def ventana_nuevo_producto(a):

    def guardar_producto():
        nombre = producto_nombre_entry.get()
        precio = producto_precio_entry.get()
        cantidad = producto_cantidad_entry.get()
        proveedor = proveedor_seleccionada.get()
        categoria = categoria_seleccionada.get()
        
        cursor.execute('SELECT id_proveedor FROM proveedor WHERE razon_social = ?', (proveedor, ))
        id_proveedor = cursor.fetchone()

        cursor.execute('SELECT id_categoria FROM categoria WHERE nombre = ?', (categoria, ))
        id_categoria = cursor.fetchone()

        cursor.execute('INSERT INTO producto (nombre, precio, cantidad, id_proveedor, id_categoria) VALUES (?,?,?,?,?)',
                    (nombre, precio, cantidad, id_proveedor[0], id_categoria[0]))
        base_datos.commit()

        messagebox.showinfo('Completado','El producto ha sido guardado con éxito.')

        cursor.execute('SELECT * FROM producto')
        product = cursor.fetchall()
        print(product)
        producto_nombre_entry.delete(0, 'end')
        producto_precio_entry.delete(0, 'end')
        producto_cantidad_entry.delete(0, 'end')
        proveedor_seleccionada.set('Seleccionar Proveedor')
        categoria_seleccionada.set('Seleccionar Categoria')


    ventana_agregar_producto = Toplevel(a)

    ventana_agregar_producto.title('Agregar Producto')
    ventana_agregar_producto.resizable(height=False, width=False)

    agregar_producto_titulo = ttk.Label(ventana_agregar_producto, text='Agregar Productos')
    agregar_producto_titulo.grid(row=0, column=0, columnspan=3)

    producto_nombre_label = ttk.Label(ventana_agregar_producto, text='Nombre: ')
    producto_nombre_label.grid(row=1, column=0)

    producto_nombre_entry= ttk.Entry(ventana_agregar_producto)
    producto_nombre_entry.grid(row=1, column=1)

    producto_precio_label = ttk.Label(ventana_agregar_producto, text='Precio: ')
    producto_precio_label.grid(row=2, column=0)

    producto_precio_entry = ttk.Entry(ventana_agregar_producto)
    producto_precio_entry.grid(row=2, column=1)

    producto_cantidad_label = ttk.Label(ventana_agregar_producto, text='Cantidad: ')
    producto_cantidad_label.grid(row=3, column=0)

    producto_cantidad_entry = ttk.Entry(ventana_agregar_producto)
    producto_cantidad_entry.grid(row=3, column=1)

    producto_proveedor_label = ttk.Label(ventana_agregar_producto, text='Proveedor: ')
    producto_proveedor_label.grid(row=4, column=0)

    proveedor_opciones = consultar_proveedores()
    proveedor_seleccionada = StringVar()
    proveedor_seleccionada.set(proveedor_opciones[0])

    producto_proveedor_opciones = OptionMenu(ventana_agregar_producto, proveedor_seleccionada, *proveedor_opciones )
    producto_proveedor_opciones.grid(row=4, column=1)

    boton_agregar_proveedor = ttk.Button(ventana_agregar_producto, text='+', command=lambda:agregar_proveedor(ventana_agregar_producto))
    boton_agregar_proveedor.grid(row=4, column=2)

    producto_categoria_label = ttk.Label(ventana_agregar_producto, text='Categoria: ')
    producto_categoria_label.grid(row=5, column=0)

    categoria_opciones = consultar_categorias()
    categoria_seleccionada = StringVar()
    categoria_seleccionada.set(categoria_opciones[0])

    producto_categoria_opciones = OptionMenu(ventana_agregar_producto, categoria_seleccionada, *categoria_opciones)
    producto_categoria_opciones.grid(row=5, column=1)

    boton_agregar_categoria = ttk.Button(ventana_agregar_producto, text='+', command=lambda:agregar_categoria(ventana_agregar_producto))
    boton_agregar_categoria.grid(row=5, column=2)

    boton_agregar_producto = ttk.Button(ventana_agregar_producto, text='Agregar Prodcuto', command=guardar_producto)
    boton_agregar_producto.grid(row=8, column=0, columnspan=3)

    ventana_agregar_producto.mainloop()


def consultar_producto(a):        
    
    ventana_consulta = Toplevel(a)
    ventana_consulta.title('Consultar productos')
    ancho_ventana = 1220  # Cambia este valor al ancho deseado de la ventana
    alto_ventana = 500   # Cambia este valor a la altura deseada de la ventana
    """ ventana_consulta.config(bg="#010101")"""
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_consulta.winfo_screenwidth()
    alto_pantalla = ventana_consulta.winfo_screenheight()

    # Calcular las coordenadas x e y para centrar la ventana
    x = (ancho_pantalla - ancho_ventana) 
    y = (alto_pantalla - alto_ventana) 

    # Establecer el tamaño y la posición de la ventana
    ventana_consulta.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    titulo_label = Label(ventana_consulta, text="Buscar Productos")
    titulo_label.grid(row=0, column=0, columnspan=3)

    label_filtro = ttk.Label (ventana_consulta, text= 'Filtro')
    label_filtro.grid(row=1, column=0, pady=(10), padx=(30,0))
   
    def obtener_categorias_existentes():
        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()
        cursor.execute("SELECT nombre FROM categoria")
        categorias = cursor.fetchall()
        return ['Seleccionar Categorias'] + [nombre[0] for nombre in categorias]

    opciones = obtener_categorias_existentes()
  
    categoria_seleccionada = StringVar()
    categoria_seleccionada.set(opciones[0])

    marca_producto = OptionMenu(ventana_consulta, categoria_seleccionada, *opciones)
    marca_producto.grid(row=1, column=1, padx=5, pady=5)

    buscar_nombre = ttk.Label (ventana_consulta, text= "Buscar por nombre: ")
    buscar_nombre.grid(row=2, column=0)
    busqueda = ttk.Entry(ventana_consulta)
    busqueda.grid(row=2, column=1)

    tree_consulta = ttk.Treeview(ventana_consulta, columns=("ID Producto","Nombre","Precio por metro", "Cantidad","Id_proveedeor", "id_categoria"))
    
    tree_consulta.column("#0", width=0, stretch=tk.NO)
    tree_consulta.heading("#1", text='Codigo Producto',anchor=tk.CENTER) 
    tree_consulta.heading("#2", text="Nombre", anchor=tk.CENTER)  # Centrar el encabezado 'Nombre'
    tree_consulta.heading("#3", text="Precio Por Metro", anchor=tk.CENTER)  
    tree_consulta.heading("#4", text="Stock", anchor=tk.CENTER)
    tree_consulta.heading("#5", text="Proveedor", anchor=tk.CENTER)   
    tree_consulta.heading("#6", text="Categoria", anchor=tk.CENTER)  
        
    for i in range(1, 7):  
        tree_consulta.column(f"#{i}", anchor=tk.CENTER)

    tree_consulta.grid(row=3, column=0, padx=10, pady=20, columnspan=3)

    base_datos = sqlite3.connect('LaJardinera.bd')
    cursor = base_datos.cursor()
    cursor.execute('SELECT * FROM producto')
    productos = cursor.fetchall()


    for resultado in productos:
        id, nombre, precio, cantidad, proveedor_id, categoria_id = resultado

        cursor.execute("SELECT razon_social FROM proveedor WHERE id_proveedor=?", (proveedor_id,))
        proveedor_nombre = cursor.fetchone()[0]

        cursor.execute("SELECT nombre FROM categoria WHERE id_categoria=?", (categoria_id,))
        categoria_nombre = cursor.fetchone()[0]

        tree_consulta.insert('','end', values=[id, nombre, precio, cantidad, proveedor_nombre, categoria_nombre])

    nuevo_button = ttk.Button(ventana_consulta, text="Nuevo", command= lambda : ventana_nuevo_producto(ventana_consulta) )
    nuevo_button.grid(row=5, column=0)

    editar_button = ttk.Button(ventana_consulta, text="Editar")
    editar_button.grid(row=5, column=1)

    eliminar_button= ttk.Button(ventana_consulta, text="Eliminar")
    eliminar_button.grid(row=5, column=2)

    


        
