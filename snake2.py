from terminal import clear_terminal
from terminal import timed_input
from random import randint
import csv

def armar_tablero (filas,columnas):
	'''Recibe un numero de filas y columnas para armar el tablero con las dimensiones deseadas'''
	tablero=[]
	for f in range (filas):
		fila = []
		for c in range (columnas):
			fila.append("_ ")
		tablero.append(fila)
	return tablero

def imprimir_tablero(tablero):
	'''Imprime el tablero sobre el cual se van a realizar los movimientos'''
	for f in range (len(tablero)):
		for c in range (len(tablero[0])):
			print (tablero[f][c], end='')
		print()
	return tablero

def crear_snake(tablero):
	'''Crea la serpiente y asigna la posicion inicial de su cabeza'''
	snake = [(1,1)]
	tablero[snake[0][0]][snake[0][1]] = 'o '
	return snake

def insertar_fruta(tablero):
	'''Determina la posicion inicial para la manazana y la coloca en el tablero'''
	fruta = [(3,3)]
	tablero[3][3] = "@ "
	return fruta

def realizar_movimiento(movimiento_anterior,tiempo_reaccion,dict_mochila,snake,tablero,contador_nivel,dict_especiales):
	'''Recibe la posicion de la serpiente y la manzana y pide al usuario que determine la direccion de los movimientos'''
	estado = ['No disponible','No disponible','No disponible','No disponible']
	cursor = {'w':'arriba','s':'abajo','a':'izquierda','d':'derecha'}
	for i in range (1,5):
		if i in dict_mochila:
			estado[i-1] = 'Disponible'
	texto_en_pantalla (estado,dict_mochila,tiempo_reaccion,contador_nivel,snake)
	movimiento = timed_input(tiempo_reaccion[0]).lower()
	if not movimiento:
		movimiento = movimiento_anterior[0]
	else:
		if movimiento in cursor:
			movimiento_anterior[0] = movimiento
		else:
			if movimiento in str(dict_mochila):
				activar_especial(dict_mochila,tiempo_reaccion,snake,tablero,movimiento)
				movimiento = movimiento_anterior[0]
	return movimiento

def texto_en_pantalla (estado,dict_mochila,tiempo_reaccion,contador_nivel,snake):
	print ("Realizar movimientos con w (arriba), a (izquierda), s (abajo), d (derecha)")
	print()
	print ("MOCHILA")
	print (f"TECLA | SIMBOLO  | FUNCION                            | ESTADO")
	print (f"1:    | +        | Aumenta la velocidad de la snake   | {estado[0]}")
	print (f"2:    | =        | Disminuye la velocidad de la snake | {estado[1]}")
	print (f"3:    | $        | Aumenta el tamaño de la snake      | {estado[2]}")
	print (f"4:    | €        | Disminuye el tamaño de la snake    | {estado[3]}")
	print()
	print(f"Nivel actual: {contador_nivel} / 4")
	print(f"Velocidad actual: {tiempo_reaccion} km/h")
	print(f"Ubicacion de la snake: {snake}")

def activar_especial(dict_mochila,tiempo_reaccion,snake,tablero,movimiento):
	a = snake[len(snake)-1][0]
	b = snake[len(snake)-1][1]
	while movimiento in str(dict_mochila):
		if movimiento == '1':
			tiempo_reaccion[0] -= 0.1
			dict_mochila.pop(1)
			return
		if movimiento == '2':
			tiempo_reaccion[0] += 0.1
			dict_mochila.pop(2)
			return
		if movimiento == '3':
			snake.append((a,b))
			dict_mochila.pop(3)
			return
		if movimiento == '4':
			if len(snake) > 1:
				snake.pop(0)
				tablero[a][b] = '_ '
				dict_mochila.pop(4)
				return

def actualizar_tablero (tablero,snake,movimiento,fruta,filas,columnas):
	'''Actualiza las posiciones de la serpiente y la fruta segun el último movimiento realizado'''
	cola_f = snake[len(snake)-1][0]
	cola_c = snake[len(snake)-1][1]
	fruta_f = fruta[0][0]
	fruta_c = fruta[0][1]
	tablero[fruta_f][fruta_c] = '@ '
	tablero[cola_f][cola_c] = '_ '
	for i in range (1, len(snake)):
		snake[len(snake)-i] = snake[len(snake)-1-i]
	if movimiento == 'd':
			mover_derecha(movimiento,snake,tablero,filas,columnas)
	if movimiento == 'a':
			mover_izquierda(movimiento,snake,tablero,filas,columnas)
	if movimiento == 's':
			mover_abajo(movimiento,snake,tablero,filas,columnas)
	if movimiento == 'w':
			mover_arriba(movimiento,snake,tablero,filas,columnas)
	return tablero

def mover_derecha(movimiento,snake,tablero,filas,columnas):
	"""Determina la dirección que va a tomar la snake cuando va hacia la derecha"""
	cabeza_c = snake[0][1]
	cabeza_f = snake[0][0]
	cabeza_c += 1
	if cabeza_c == columnas:
		snake[0] = (-1, -1)
		return tablero
	snake[0] = (cabeza_f, cabeza_c)
	tablero[cabeza_f][cabeza_c] = 'o '

def mover_izquierda(movimiento,snake,tablero,filas,columnas):
	"""Determina la dirección que va a tomar la snake cuando va hacia la izquierda"""
	cabeza_c = snake[0][1]
	cabeza_f = snake[0][0]
	cabeza_c -= 1
	if cabeza_c == columnas:
		snake[0] = (-1, -1)
		return tablero			
	snake[0] = (cabeza_f, cabeza_c)
	tablero[cabeza_f][cabeza_c] = 'o '

def mover_abajo(movimiento,snake,tablero,filas,columnas):
	"""Determina la dirección que va a tomar la snake cuando va hacia abajo"""
	cabeza_c = snake[0][1]
	cabeza_f = snake[0][0]
	cabeza_f += 1
	if cabeza_f == filas:
		snake[0] = (-1, -1)
		return tablero
	snake[0] = (cabeza_f, cabeza_c)
	tablero[cabeza_f][cabeza_c] = 'o '

def mover_arriba(movimiento,snake,tablero,filas,columnas):
	"""Determina la dirección que va a tomar la snake cuando va hacia arriba"""
	cabeza_c = snake[0][1]
	cabeza_f = snake[0][0]
	cabeza_f -= 1
	if cabeza_f == filas:
		snake[0] = (-1, -1)
		return tablero
	snake[0] = (cabeza_f, cabeza_c)
	tablero[cabeza_f][cabeza_c] = 'o '

def comer_fruta(fruta,snake,tablero,filas,columnas,lista_obst,dict_mochila):
	'''Revisa si en el movimiento actual la snake ha comido una fruta. Si comió una fruta hace crecer a la snake en una unidad'''
	cola_f = snake[len(snake)-1][0]
	cola_c = snake[len(snake)-1][1]
	fruta_f = fruta[0][0]
	fruta_c = fruta[0][1]
	if fruta[0][0] == snake [0][0] and fruta[0][1] == snake [0][1]:
		snake.append((cola_f,cola_c))
		for i in range (len(snake)):
			for elemento in lista_obst:
				x = int(elemento[0])
				y = int(elemento[1])
				while (fruta[0] == snake [i]) or (fruta[0][0] == x and fruta[0][1] == y) or (tablero[fruta_f][fruta_c] != '_ '):
					fruta_f = randint(0,filas-1)
					fruta_c = randint(0,columnas-1)
					fruta[0] = (fruta_f,fruta_c)
		return True

def comprobar_ganador(snake,nivel_actual,largo_max,lista_obst):
	'''Define las condiciones necesarias para ganar o perder el juego'''
	game_over = 0
	if (len(snake)-1) == largo_max:
		print ("FELICIDADES!! Ganaste!!")
		game_over = 1
	if snake[0][1] < 0 or snake[0][0] < 0 or snake[0] == (-1,-1):
		print ("PERDISTE!! Te saliste del tablero")
		game_over = -1
	for i in range (1,len(snake)):
		if snake[0] == snake [i]:
			print ("PERDISTE!! Te comiste a vos mismo")
			game_over = -1
	for elemento in lista_obst:
		x = int(elemento[0])
		y = int(elemento[1])
		if snake[0][0] == x and snake[0][1] == y:
			print ("PERDISTE!! No podés atravesar obstáculos!")
			game_over = -1
	return game_over

def insertar_obstaculos(obstaculos,tablero):
	"""Ubica una lista de obstáculos en el tablero"""
	obstaculos = obstaculos.split(';')
	lista_obst = []
	for elemento in obstaculos:
		l_elemento = []
		for i in elemento:
			if i.isdigit():
				l_elemento.append(i)
		lista_obst.append(l_elemento)
	for elemento in lista_obst:
		x = int(elemento[0])
		y = int(elemento[1])
		tablero[x][y] = 'X '
	return lista_obst

def insertar_especiales(tablero,snake,fruta,contador_movimientos,filas,columnas,dict_especiales,elem_mochila):
	for i in range (0,8):
		if contador_movimientos == ((20 * i) + 15):
			a = randint(0,filas-1)
			b = randint(0,columnas-1)
			while tablero[a][b] != '_ ':
				a = randint(0,filas-1)
				b = randint(0,columnas-1)
			tablero[a][b] = elem_mochila[randint(0,3)] + ' '
			dict_especiales[(a,b)] = tablero[a][b]
	return dict_especiales

def mochila_especiales (elem_mochila,snake,tablero,dict_especiales,dict_mochila):
	simbolos = []
	teclas = []
	with open ('especiales.csv') as archivo:
		csv_reader = csv.reader(archivo)	
		for campos in csv_reader:
			simbolos.append(campos[0])
			teclas.append(int(campos[3]))
	for valor in dict_especiales:
		if snake[0] == valor:
			for i in range(len(simbolos)):
				if dict_especiales[valor] == simbolos[i] + ' ':
					dict_mochila[teclas[i]] = simbolos[i]
	return dict_mochila

def guardar_elementos(elementos):
	elem_mochila = []
	for elemento in elementos:
		if elemento != ',':
			elem_mochila.append(elemento)
	return elem_mochila

def main(ruta):
	nivel_actual = ['nivel_1.txt','nivel_2.txt','nivel_3.txt','nivel_4.txt']
	contador_nivel = 1
	while nivel_actual:
		archivo = open (nivel_actual[0])
		lineas = archivo.readlines()
		tiempo_reaccion = [float(lineas[1])]
		largo_max = int(lineas[0])
		dimension = lineas[2].split('X')
		filas = int(dimension[0])
		columnas = int(dimension[1])
		tablero = armar_tablero(filas,columnas)
		snake = crear_snake(tablero)
		fruta = insertar_fruta(tablero)
		lista_obst = insertar_obstaculos(lineas[3],tablero)
		elem_mochila = guardar_elementos(lineas[4])
		movimiento_anterior = ['d']
		contador_movimientos = 0
		dict_especiales = {}
		dict_mochila = {}
		while True:
			clear_terminal()
			imprimir_tablero(tablero)
			mochila_especiales(elem_mochila,snake,tablero,dict_especiales,dict_mochila)
			insertar_especiales(tablero,snake,fruta,contador_movimientos,filas,columnas,dict_especiales,elem_mochila)
			movimiento = realizar_movimiento(movimiento_anterior,tiempo_reaccion,dict_mochila,snake,tablero,contador_nivel,dict_especiales)
			comer_fruta(fruta,snake,tablero,filas,columnas,lista_obst,dict_mochila)
			actualizar_tablero(tablero,snake,movimiento,fruta,filas,columnas)
			contador_movimientos += 1
			game_over = comprobar_ganador(snake,nivel_actual,largo_max,lista_obst)
			if game_over == 1:
				if len(nivel_actual) > 1:
					contador_nivel += 1
					print (f"¿Listo para el NIVEL {contador_nivel}?")
					print ("Pulsa enter para continuar")
					input()
					archivo.close()
					nivel_actual.pop(0)
					break
				return
			else:
				if game_over == -1:
					archivo.close()
					return

main('/Documentos/Python/TP_2_snake/Entrega')