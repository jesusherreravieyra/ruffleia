import pygame
from random import randint

ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)
VERDE_BANDERA = (27, 94, 32)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)

MENU = 1
JUGANDO = 2
GANAR=3
PERDER =4
QUITAR=5



QUIETO = 1
ABAJO = 2
ARRIBA = 3
IZQUIERDA = 4
DERECHA =5

APARECE = 2
INVISIBLE = 1
VIAJANDO=3

estadoBalon = INVISIBLE
estado = MENU

ARCHIVO = open("settings.txt", "r+")
record = float(ARCHIVO.readlines()[len(ARCHIVO.readlines())-1])


def dibujarMenu(ventana, imgBtnJugar):
    fuente = pygame.font.SysFont("monospace", 30)
    texto = fuente.render("High Score:20", 1, ROJO)
    ventana.blit(texto, (ANCHO//2 + 80, +80))
    ventana.blit(imgBtnJugar, (80, +400))


def dibujarBalones(ventana, listaBalones):
    for balon in listaBalones:
        ventana.blit(balon.image, balon.rect)


def moverBalones(listaBalones):
    for balones in listaBalones:
        balones.rect.left += 7


def dibujarPersonaje(ventana, spritePersonaje):
    ventana.blit(spritePersonaje.image, spritePersonaje.rect)


def dibujarEnemigos(ventana, listaEnemigos):
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)


def verificarColision(listaEnemigos,listaBalones,listaPorterias):
    global estadoBalon
    global estado
    efecto3 = pygame.mixer.Sound("golpe.wav")
    for k in range (len(listaBalones)-1,-1,-1):
        balon = listaBalones[k]
        for e in range(len(listaEnemigos)-1,-1,-1):
            enemigo = listaEnemigos[e]
            xe,ye,ae,alte = enemigo.rect
            xb,yb,ab,altb = balon.rect
            if xb>=xe and xb<=xe+ae and yb >= ye and yb <=ye+alte: #Le pegó
                efecto3.play()
                listaEnemigos.remove(enemigo)
                listaBalones.remove(balon)
                estadoBalon=INVISIBLE
                listaPorterias.append(1)

                break


def verificarSlida (listaBalones):
    global estadoBalon
    for k in range (len(listaBalones)-1,-1,-1):
        balon = listaBalones[k]
        xb, yb, ab, altb = balon.rect
        ancho = 801
        if xb>=ancho:
            listaBalones.remove(balon)
            estadoBalon = INVISIBLE
            break


def dibujar():
    global estadoBalon
    global estado
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    termina = False

    #Porterias destruidas
    listaPorterias = []

    # Personaje
    imgPersonaje = pygame.image.load('alex.png')
    spritePersonaje = pygame.sprite.Sprite()
    spritePersonaje.image = imgPersonaje
    spritePersonaje.rect = imgPersonaje.get_rect()
    spritePersonaje.rect.left = 0

    listaEnemigos = []
    imgEnemigo = pygame.image.load("porteriae.gif")
    for k in range(20):
        spriteEnemigo = pygame.sprite.Sprite()
        spriteEnemigo.image = imgEnemigo
        spriteEnemigo.rect = imgEnemigo.get_rect()
        spriteEnemigo.rect.left = randint(200, ANCHO-100)
        spriteEnemigo.rect.bottom = randint(spriteEnemigo.rect.height+50, ALTO-10)
        listaEnemigos.append(spriteEnemigo)

    listaBalones = []
    imgBalon = pygame.image.load("balone.png")

    imgBtnJugar = pygame.image.load("button.png")
    imgFondo = pygame.image.load ("canchae.png")
    imgFondoMenu = pygame.image.load ("f.png")
    img2 = pygame.image.load("segundoLugar.png")
    img3 = pygame.image.load("champs.png")


    moviendo = QUIETO

    # Audio
    if estado == MENU:
        pygame.mixer.init()
        pygame.mixer.music.load("musicaFondo.mp3")
        pygame.mixer.music.play(-1)  # el -1 es para que se repita en un loop

    efecto = pygame.mixer.Sound ("SILBATO.wav")
    efecto2 = pygame.mixer.Sound ("patada.wav")
    efecto3 = pygame.mixer.Sound("aplausoss.wav")
    efecto4 = pygame.mixer.Sound("trompteta.wav")

    # Tiempo
    timer = 0
    fuente = pygame.font.SysFont("monospace", 30)
    fuente2 = pygame.font.SysFont("nordvesr", 60)
    fuente3 = pygame.font.SysFont("stencil",27)
    fuente4 = pygame.font.SysFont("nordvesr",50)
    fuente5 = pygame.font.SysFont("nordvesr", 30)
    fuente6 = pygame.font.SysFont("monospace", 30)

    while not termina:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                termina = True
            elif evento.type == pygame.KEYUP:
                moviendo = QUIETO
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    moviendo = ARRIBA
                elif evento.key == pygame.K_DOWN:
                    moviendo=ABAJO
                elif evento.key == pygame.K_LEFT:
                    moviendo = IZQUIERDA
                elif evento.key == pygame.K_RIGHT:
                    moviendo = DERECHA
                elif evento.key == pygame.K_g:
                    if estadoBalon == INVISIBLE:
                        estadoBalon = APARECE

                elif evento.key == pygame.K_SPACE:
                    if estado==GANAR or estado==PERDER:
                        efecto.play()
                        efecto3.stop()
                        efecto4.stop()
                        listaPorterias = []
                        estado = JUGANDO
                        efecto.play()

                elif evento.key == pygame.K_ESCAPE:
                    ARCHIVO.close()
                    termina = True


            elif evento.type == pygame.MOUSEBUTTONUP:
                if estado==MENU:
                    xm, ym = pygame.mouse.get_pos()
                    print(xm, ", ", ym)
                    xb = 80
                    yb = +400
                    if xm>=xb and xm<=xb+450 and ym >= yb and ym <=yb+100:
                        efecto.play(0)
                        pygame.mixer.music.stop()
                        estado = JUGANDO

        ventana.fill(BLANCO)

        if estado == JUGANDO:
            ventana.blit(imgFondo,(0,0))
            dibujarPersonaje(ventana, spritePersonaje)
            dibujarEnemigos(ventana, listaEnemigos)
            dibujarBalones(ventana, listaBalones)
            moverBalones(listaBalones)
            verificarColision(listaEnemigos,listaBalones,listaPorterias)
            verificarSlida(listaBalones)
            moverBalones(listaBalones)
            if moviendo == ARRIBA and spritePersonaje.rect.bottom>125:
                spritePersonaje.rect.bottom -=5
            elif moviendo == ABAJO and spritePersonaje.rect.bottom<ALTO:
                spritePersonaje.rect.bottom += 5
            elif moviendo == IZQUIERDA and spritePersonaje.rect.left>0:
                spritePersonaje.rect.left -= 5
            elif moviendo == DERECHA and spritePersonaje.rect.left<736:
                spritePersonaje.rect.left += 5

            if estadoBalon == APARECE:
                efecto2.play(0)
                spriteBala = pygame.sprite.Sprite()
                spriteBala.image = imgBalon
                spriteBala.rect = imgBalon.get_rect()
                spriteBala.rect.left = spritePersonaje.rect.left + spritePersonaje.rect.width
                spriteBala.rect.bottom = spritePersonaje.rect.bottom
                listaBalones.append(spriteBala)
                estadoBalon=VIAJANDO

            texto = fuente.render("Tiempo: %d" % (timer), 1, NEGRO)
            ventana.blit(texto, ( ANCHO//2+ 200, 20))
            texto6 = fuente6.render("Score: %d" % (len(listaPorterias)), 1, NEGRO)
            ventana.blit(texto6, ( ANCHO//2+ 200, 50))

            if timer > 15:
                efecto4.play()
                estado=PERDER

        if estado == PERDER:
            ventana.blit(img2, (0, 0))
            texto2 = fuente2.render("Pulsa space para continuar", 1, NEGRO)
            ventana.blit(texto2, ( 0, ALTO-80))
            texto4 = fuente4.render("Score: %d" % (len(listaPorterias)), 1, ROJO)
            ventana.blit(texto4, (ANCHO - 200, 0))
            listaEnemigos =[]
            listaBalones=[]
            timer = 0

            # Personaje
            imgPersonaje = pygame.image.load('alex.png')
            spritePersonaje = pygame.sprite.Sprite()
            spritePersonaje.image = imgPersonaje
            spritePersonaje.rect = imgPersonaje.get_rect()
            spritePersonaje.rect.left = 0

            imgEnemigo = pygame.image.load("porteriae.gif")
            for k in range(20):
                spriteEnemigo = pygame.sprite.Sprite()
                spriteEnemigo.image = imgEnemigo
                spriteEnemigo.rect = imgEnemigo.get_rect()
                spriteEnemigo.rect.left = randint(200, ANCHO - 100)
                spriteEnemigo.rect.bottom = randint(spriteEnemigo.rect.height + 50, ALTO - 10)
                listaEnemigos.append(spriteEnemigo)

        if len(listaPorterias) == 6:
            efecto3.play()
            estado = GANAR
            if timer < record and timer>10:
                ARCHIVO.write ("\n"+str(timer))
                timer=0

        if estado == GANAR:
            ventana.blit(img3, (0, 0))
            listaEnemigos =[]
            listaBalones=[]
            timer = 0
            texto3 = fuente3.render("Pulsa space para volver a jugar", 1, NEGRO)
            ventana.blit(texto3, (170, 100))

            # Personaje
            imgPersonaje = pygame.image.load('alex.png')
            spritePersonaje = pygame.sprite.Sprite()
            spritePersonaje.image = imgPersonaje
            spritePersonaje.rect = imgPersonaje.get_rect()
            spritePersonaje.rect.left = 0

            imgEnemigo = pygame.image.load("porteriae.gif")
            for k in range(20):
                spriteEnemigo = pygame.sprite.Sprite()
                spriteEnemigo.image = imgEnemigo
                spriteEnemigo.rect = imgEnemigo.get_rect()
                spriteEnemigo.rect.left = randint(200, ANCHO - 100)
                spriteEnemigo.rect.bottom = randint(spriteEnemigo.rect.height + 50, ALTO - 10)
                listaEnemigos.append(spriteEnemigo)

        if estado == MENU:
            timer = 0
            ventana.blit(imgFondoMenu, (0, 0))
            dibujarMenu(ventana, imgBtnJugar)

        pygame.display.flip()
        reloj.tick(20)
        timer += 1/40
    ARCHIVO.close()
    pygame.quit()


def main():
    dibujar()

main()