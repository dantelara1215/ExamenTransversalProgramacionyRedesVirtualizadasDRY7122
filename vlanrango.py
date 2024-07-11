VlanNum = int(input("Cual es el número de ID de la vlan? "))
if VlanNum >= 1 and VlanNum <= 1005:
    print("Es una Vlan de rango Normal.")
elif VlanNum >=1006 and VlanNum <= 4095:
    print("Es una Vlan de rango Extendida")
else:
    print("El número de Vlan ingresado es desconocida.")