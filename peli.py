import pygame
import sys
from pygame.locals import *
import random

# screen

pygame.init()
pygame.font.init()
pygame.mixer.init()

koko = (800,650)
ruutu = pygame.display.set_mode(koko)
pygame.display.set_caption("best game ever")



fontti = pygame.font.SysFont("Roboto",30)
fontti2 = pygame.font.SysFont("Roboto",30)
tekativari = (20, 255, 247)
gameovervari = (255, 47, 20)


bush = pygame.image.load("bush.png")
pelaaja = pygame.image.load("pelaaja.png")
tausta = pygame.image.load("tausta.png")

pelaaja = pygame.transform.scale(pelaaja, (69,69))
bush = pygame.transform.scale(bush, (49,49))

pygame.mixer.music.load("taustamusa.mp3")
pygame.mixer.music.play(-1)


pelx = 400
pely = 325
nopeus = 5
vihunopeus = 0.5 
hp = 5
highscore = 0

vihut = [[20,100],[200,200],[300,300]]

on_kirjoitettu = False

with open("higscore","r") as tiedosto:
    luettu = tiedosto.read()
    highscore = float(luettu)


# aika
ajastin = pygame.time.Clock()
FPS = 40
alkuaika = pygame.time.get_ticks()
loppuaika = 0

def peruna():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Pelilogikka
def porkkana():
    global vihunopeus
    global pelx
    global pely
    global hp
    global highscore
    ruutu.fill((0,0,0))
    ruutu.blit(tausta, (0,0))
    # pelaaja likunta
    nappaimet = pygame.key.get_pressed()
    if nappaimet[pygame.K_RIGHT]:
        pelx += nopeus

        nappaimet = pygame.key.get_pressed()
    if nappaimet[pygame.K_LEFT]:
        pelx -= nopeus

    if pelx <0:
        pelx = 0
    if pelx >731:
        pelx = 731


        #viholisen likunta
    for vihu in vihut:
        vihu[1] += vihunopeus
        if vihu[1] > 650:
            vihu[1] = -50
            vihu[0] = random.randint(50, 550)




        # vihollisten pirto
    for vihu in vihut :
         ruutu.blit(bush,vihu)

# kostketuksen tarkistus
    for vihu in vihut:
        if vihu[1] + 49 > pely  and  vihu[1] < pely + 64:
            if vihu[0] + 49 > pelx  and  vihu[0] < pelx + 64:

                #KOskee
                hp -= 1
            vihu[1] = -180
            vihu[0] = random.randint(50, 550)


        

#tekstin piirto
    teksti = fontti.render("Lives:" + str(hp), True, tekativari)
    ruutu.blit(teksti, (30,30))

#pelajan pirto # ja time
    aika = pygame.time.get_ticks() - alkuaika
    teksti = fontti.render("aika:" + str(aika//1000), True, tekativari)
    ruutu.blit(teksti, (150,30))


    if aika > highscore:
        highscore = aika//1000


    if aika//1000 % 10 == 0:
        vihunopeus += 00.1

    #pelajanpirto
    ruutu.blit(pelaaja,(pelx,pely))
    pygame.display.flip()

    # pelin loppu
def lanttu():
    global on_kirjoitettu
    global loppuaika
    ruutu.fill(gameovervari)
    teksti = fontti2.render("died your bad at this game and coding get lost kid :" + str(hp), True, tekativari)
    ruutu.blit(teksti, (30,30))

    if not on_kirjoitettu:
        on_kirjoitettu = True
        loppuaika = pygame.time.get_ticks()
        pygame.mixer.music.stop()
        with open("higscore","w") as tiedosto:
            tiedosto.write(str(highscore))

    if pygame.time.get_ticks() - loppuaika > 5000:
        pygame.quit()  
        sys.exit()     
    


    teksti = fontti2.render("korkein pistemärä :" + str(highscore), True, tekativari)
    ruutu.blit(teksti, (60,60))
    pygame.display.flip()
    
    


      
# Pelin silmukka
while True:
    peruna()
    if hp > 0:
        porkkana()
    else:
        lanttu()
    ajastin.tick(FPS)
