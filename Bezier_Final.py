import uctypes
import machine
import struct
import array

# Se debe modificar el valor de "n" requerido
n = array.array("l", [10])
dir_n = uctypes.addressof(n)

# Funciones auxiliares para trabajar con float en memoria
def leer_float(dir):
    b = bytes([machine.mem8[dir + i] for i in range(4)])
    return struct.unpack('f', b)[0]

def escribir_float(dir, val):
    b = struct.pack('f', val)
    for i in range(4):
        machine.mem8[dir + i] = b[i]

# Funciones de cálculo Bezier
def calcular_c1(dir_t, dir_c1):
    t = leer_float(dir_t)
    escribir_float(dir_c1, (1 - t) ** 3)

def calcular_c2(dir_t, dir_c2):
    t = leer_float(dir_t)
    escribir_float(dir_c2, 3 * ((1 - t) ** 2) * t)

def calcular_c3(dir_t, dir_c3):
    t = leer_float(dir_t)
    escribir_float(dir_c3, 3 * (1 - t) * (t ** 2))

def calcular_c4(dir_t, dir_c4):
    t = leer_float(dir_t)
    escribir_float(dir_c4, t ** 3)

def sumar(dir_vectorA, dir_vectorB, dir_Resultado):
    for i in range(2):
        a = leer_float(dir_vectorA + 4*i)
        b = leer_float(dir_vectorB + 4*i)
        escribir_float(dir_Resultado + 4*i, a + b)

def multiplicar(dir_numero, dir_vector, dir_resultado):
    num = leer_float(dir_numero)
    for i in range(2):
        val = leer_float(dir_vector + 4*i)
        escribir_float(dir_resultado + 4*i, num * val)

# Definiendo las constantes C1, C2, C3 y C4
c1 = array.array("f", [0])
dir_c1 = uctypes.addressof(c1)

c2 = array.array("f", [0])
dir_c2 = uctypes.addressof(c2)

c3 = array.array("f", [0])
dir_c3 = uctypes.addressof(c3)

c4 = array.array("f", [0])
dir_c4 = uctypes.addressof(c4)

# Definiendo los puntos de Bezier referencia
p0 = array.array("f", [0, 0])
dir_p0 = uctypes.addressof(p0)

p1 = array.array("f", [0, 3])
dir_p1 = uctypes.addressof(p1)

p2 = array.array("f", [3, 3])
dir_p2 = uctypes.addressof(p2)

p3 = array.array("f", [3, 0])
dir_p3 = uctypes.addressof(p3)

# Constantes A, B, C, D
A = array.array("f", [0]*2)
dir_A = uctypes.addressof(A)

B = array.array("f", [0]*2)
dir_B = uctypes.addressof(B)

C = array.array("f", [0]*2)
dir_C = uctypes.addressof(C)

D = array.array("f", [0]*2)
dir_D = uctypes.addressof(D)

# Vector t
t = array.array("f", [0]*(n[0]+1))
dir_t = uctypes.addressof(t)

# Resultado
Resultado = array.array("f", [0]*(2*n[0]+2))
dir_Resultado = uctypes.addressof(Resultado)

# Implementación de la curva de Bézier
for i in range(n[0]+1):
    escribir_float(dir_t, i / n[0])
    calcular_c1(dir_t, dir_c1)
    calcular_c2(dir_t, dir_c2)
    calcular_c3(dir_t, dir_c3)
    calcular_c4(dir_t, dir_c4)
    multiplicar(dir_c1, dir_p0, dir_A)
    multiplicar(dir_c2, dir_p1, dir_B)
    multiplicar(dir_c3, dir_p2, dir_C)
    multiplicar(dir_c4, dir_p3, dir_D)
    sumar(dir_A, dir_B, dir_Resultado+(8*i))
    sumar(dir_Resultado+(8*i), dir_C, dir_Resultado+(8*i))
    sumar(dir_Resultado+(8*i), dir_D, dir_Resultado+(8*i))

for i in range(n[0]+1):
    x = leer_float(dir_Resultado + 8*i)
    y = leer_float(dir_Resultado + 8*i + 4)
    print(x, ",", y)

