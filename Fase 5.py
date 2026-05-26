# -----------------------------------------------------------
# PROBLEMA 2 - MENÚ DE RESTAURANTE CON PROMOCIÓN
# -----------------------------------------------------------

# Función que calcula el precio final aplicando descuento
def calcular_precio_final(categoria_producto, precio_base, categoria_objetivo, umbral):
    """
    Aplica 15% de descuento si:
      - categoría coincide con categoría objetivo
      - precio_base es mayor al umbral
    """
    if categoria_producto == categoria_objetivo and precio_base > umbral:
        descuento = precio_base * 0.15
        return precio_base - descuento
    else:
        return precio_base


# MATRIZ DEL MENÚ: [Nombre, Categoría, Precio Base]
menu = [
    ["Hamburguesa", "Comida Rápida", 22000],
    ["Perro Caliente", "Comida Rápida", 15000],
    ["Pizza Personal", "Italiana", 30000],
    ["Pasta Alfredo", "Italiana", 28000],
    ["Ensalada César", "Saludable", 18000],
    ["Jugo Natural", "Bebida", 9000]
]

# Parámetros de la promoción
categoria_objetivo = "Italiana"
umbral_precio = 25000

# Salida
print("---- RESULTADOS DE LA PROMOCIÓN ----")
print("Producto | Categoría | Precio Base | Precio Final")

for producto in menu:
    nombre = producto[0]
    categoria = producto[1]
    precio_base = producto[2]

    precio_final = calcular_precio_final(categoria, precio_base, categoria_objetivo, umbral_precio)

    print(f"{nombre} | {categoria} | ${precio_base} | ${precio_final}")