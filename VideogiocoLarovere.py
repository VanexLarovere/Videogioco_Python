import sys
import pygame
import random
from pygame.math import Vector2 #Modulo usato per la strada del mostro

#Clock
clock = pygame.time.Clock() #Setto il framerate 
FPS = 60

#Background
room1_image = pygame.image.load('Images/room1.png')
room2_image = pygame.image.load('Images/room2.png')
room3_image = pygame.image.load('Images/room3.png')
room4_image = pygame.image.load('Images/room4.png')
room5_image = pygame.image.load('Images/room5.png')
roomExit = pygame.image.load('Images/Black.png')

backgroundImage = pygame.image.load('Images/sfondo.jpg') #Sfondo principale (Corridoio)
widthB = 800
heightB = 600

#key
keyImage = pygame.image.load('Images/key.png')

#Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Character
charU = pygame.image.load('Images/charUp.png')
charD = pygame.image.load('Images/charDown.png')
charL = pygame.image.load('Images/charLeft.png')
charR = pygame.image.load('Images/charRight.png')

charImage = charD #Le metto come immagine iniziale quella frontale

xC = 680 #Posizione iniziale
yC = 503

#Monster
monster_image = pygame.image.load('Images/monster.png')
##########################################################################################################################################################################

pygame.init() #Inizializzazione
pygame.display.set_caption('Horror') #Caption della finestra
screen = pygame.display.set_mode((widthB, heightB)) #Creazione finestra di grandezza 800 - 600

def Background(image):
    size = pygame.transform.scale(image, (widthB, heightB))
    screen.blit(size, (0, 0))

class Character():
    def __init__(self, image, xC, yC):
        self.image = pygame.transform.scale(image, (60, 60))
        self.charL = pygame.transform.scale(charL, (60, 60))
        self.charR = pygame.transform.scale(charR, (60, 60))
        self.charU = pygame.transform.scale(charU, (60, 60))
        self.charD = pygame.transform.scale(charD, (60, 60))

        self.in_room = False #Per i controlli che avevo nel corridoio riguardo il movimento (Su, Giù, Mezzo...)
        self.middlePart = pygame.Rect(145, 145, 510, 310)

        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (xC, yC)
        self.xC = xC
        self.yC = yC
        self.current_image = self.image  # Variabile per mantenere l'immagine corrente
        self.boolSize = False

    def draw(self):
        screen.blit(self.current_image, self.rect) # Disegna l'immagine corrente

    def rect(self): #Restituisce il rettangolo
        return self.rect
    
    def changeSize(self, boolSize):
        if boolSize == False:
            self.charL = pygame.transform.scale(charL, (60, 60))
            self.charR = pygame.transform.scale(charR, (60, 60))
            self.charU = pygame.transform.scale(charU, (60, 60))
            self.charD = pygame.transform.scale(charD, (60, 60))
        elif boolSize:
            self.charL = pygame.transform.scale(charL, (150, 150))
            self.charR = pygame.transform.scale(charR, (150, 150))
            self.charU = pygame.transform.scale(charU, (150, 150))
            self.charD = pygame.transform.scale(charD, (150, 150))

    def move(self, keys, in_room):
        #new_rect per simulare il movimento del player senza effettuare il 
        #movimento effettivo finche non viene verificato che il movimento non 
        #porti il player a collidere con middlePart.rect. Se la nuova 
        #posizione non causa collisioni, il player si muovera in quella 
        #direzione; altrimenti rimarra fermo

        if in_room:
            if keys[pygame.K_LEFT] and self.rect.x > 20: # Premo il tasto sinistro
                new_rect = self.rect.copy()
                new_rect.x -= self.speed
                self.current_image = self.charL
                self.rect.x -= self.speed
                
            if keys[pygame.K_RIGHT] and self.rect.x < widthB - 80: # Premo il tasto destro
                new_rect = self.rect.copy()
                new_rect.x += self.speed
                self.current_image = self.charR
                self.rect.x += self.speed
                    
            if keys[pygame.K_UP] and self.rect.y > 0: # Premo il tasto su
                new_rect = self.rect.copy()
                new_rect.y -= self.speed
                self.current_image = self.charU
                self.rect.y -= self.speed

            if keys[pygame.K_DOWN] and self.rect.y < heightB - 100: # Premo il tasto giù
                new_rect = self.rect.copy()
                new_rect.y += self.speed
                self.current_image = self.charD
                self.rect.y += self.speed
        else:
            if keys[pygame.K_LEFT] and self.rect.x > 20: # Premo il tasto sinistro
                new_rect = self.rect.copy()
                new_rect.x -= self.speed
                if not new_rect.colliderect(self.middlePart): #Guardo anche la collisione con la parte in mezzo
                    self.current_image = self.charL
                    self.rect.x -= self.speed
                
            if keys[pygame.K_RIGHT] and self.rect.x < widthB - 80: # Premo il tasto destro
                new_rect = self.rect.copy()
                new_rect.x += self.speed
                if not new_rect.colliderect(self.middlePart):
                    self.current_image = self.charR
                    self.rect.x += self.speed
                    
            if keys[pygame.K_UP] and self.rect.y > 0: # Premo il tasto su
                new_rect = self.rect.copy()
                new_rect.y -= self.speed
                if not new_rect.colliderect(self.middlePart):
                    self.current_image = self.charU
                    self.rect.y -= self.speed

            if keys[pygame.K_DOWN] and self.rect.y < heightB - 100: # Premo il tasto giù
                new_rect = self.rect.copy()
                new_rect.y += self.speed
                if not new_rect.colliderect(self.middlePart):
                    self.current_image = self.charD
                    self.rect.y += self.speed
    
class Room():
    def __init__(self, image, rectangles):
        self.image = image
        self.rectangles = rectangles #numero rettangoli presenti nella stanza
        self.rects_to_draw = []  #Lista degli oggetti Rect da disegnare

        if self.rectangles == 1:
            self.rects_to_draw.append(pygame.Rect(765, 210, 35, 160))
        elif self.rectangles == 7:
            self.rects_to_draw.append(pygame.Rect(55, 10, 50, 25))
            self.rects_to_draw.append(pygame.Rect(235, 10, 50, 25))
            self.rects_to_draw.append(pygame.Rect(315, 135, 50, 25))
            self.rects_to_draw.append(pygame.Rect(512, 445, 50, 25))
            self.rects_to_draw.append(pygame.Rect(400, 555, 50, 25))
            self.rects_to_draw.append(pygame.Rect(634, 295, 30, 50))
            self.rects_to_draw.append(pygame.Rect(145, 145, 510, 310))

    def draw(self, in_room):
        if in_room == True:
            Background(self.image) #Cambio il background
        else: Background(backgroundImage) #Sfondo corridoio
        #DEBUG
        #for rect in self.rects_to_draw:
        #    pygame.draw.rect(screen, WHITE, rect, 2)

    def image(self):
        return self.image

    def clear_rectangles(self):
        #print("Rettangoli prima della cancellazione:", self.rectangles)
        self.rects_to_draw = []  #Tolgo tutti i rettangoli presenti nella stanza
        #print("Rettangoli dopo della cancellazione:", self.rectangles)

current_room = Room(backgroundImage, 7) #Metto il numero di rettangoli così so già a che stanza mi sto riferendo

class Key():
    def __init__(self):
        self.image = pygame.transform.scale(keyImage, (90, 50))
        self.random = random.randint(1, 5) #Posizione casuale tra le 5 stanze
        self.possession = False
        print(self.random) #Stampo per debug la stanza in cui si trova la chiave

    def drawKey(self, n_room):
        if not self.possession and n_room == self.random:
            pygame.Rect(50, 250, 100, 50)
            screen.blit(self.image, pygame.Rect(50, 250, 100, 50))
            #pygame.draw.rect(screen, WHITE, self.rect, 2)
            print("CHIAVE DISEGNATAAAAAAAAAAAAAAAAAAA")
            print(f"POSSESSIONE: {self.possession}")
    
    def collision_key(self, player_rect, in_room):
        if not self.possession and pygame.Rect(50, 250, 100, 50).colliderect(player_rect) and in_room: #Il player prende la chiave
            self.possession = True
            print("CHIAVE COLLISIONE")
            print(f"POSSESSIONE: {self.possession}")

    def keyPossession(self):
        return self.possession

class Enemy(): #Riguardarsi minuto 15:30 video Tower Defence
    def __init__(self, waypoints, image):
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 6
        self.image = pygame.transform.scale(image, (370, 350)) #Grandezza mostro (Quindi scalo l'immagine)

        self.rect = pygame.Rect(0, 0, 175, 175) #cordinate, grandezza rettangolo

    def update(self): 
        self.move()
    
    def draw(self, in_room): #Disegna il mostro
        if in_room == False:
            screen.blit(self.image, (self.rect.x -90, self.rect.y -75))
            self.rect = pygame.Rect(0, 0, 175, 175)
            self.rect.center = self.pos
        #pygame.draw.rect(screen, WHITE, self.rect, 2) #DA TOGLIERE POI
    
    def move(self):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #Monster has reached the end of the path so we have to redo
            self.target_waypoint = -1
        #calculate distance to target
        dist = self.movement.length()
        #check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1 

        self.rect.center = self.pos
    
    def check_collision(self, player_rect, in_room): #Verifica se il rettangolo del mostro ha fatto collisione con quello del player
        if in_room == False:
            return self.rect.colliderect(player_rect) #O True o False
        else: return False

    def clear_monster(self):
        self.rect = pygame.Rect(0, 0, 0, 0) #Non self.rect = [] perché sennò starei operando su una stringa vuota col check_collision

############################################
#create monster
waypoints = [  #Combinazioni di x e y per guidare il mostro, sarebbe la strada che va a compiere
    (85, 80),
    (710, 80),

    (710, 520),
    (85, 520),
]

monster = Enemy(waypoints, monster_image)

#create Character
character = Character(charImage, xC, yC)

#create Key
key = Key()

#create rooms
roomP = Room(backgroundImage, 7)
roomExit = Room(roomExit, 1)
room1 = Room(room1_image, 1)
room2 = Room(room2_image, 1)
room3 = Room(room3_image, 1)
room4 = Room(room4_image, 1)
room5 = Room(room5_image, 1)

#####################################################################

current_n_room = None

#CAMBIO STANZA
def change_room(character, in_room, monsters_removed, rectangles_removed, key):
    global current_room, current_n_room, win

    #Dizionario dove mi salvo le coordinate dei rettangoli
    doors = {
        "doorExit": {"position": (55, 10, 50, 25), "room": roomExit, "num": 0},
        "door1": {"position": (235, 10, 50, 25), "room": room1, "num": 1},
        "door2": {"position": (315, 135, 50, 25), "room": room2, "num": 2},
        "door3": {"position": (512, 445, 50, 25), "room": room3, "num": 3},
        "door4": {"position": (400, 555, 50, 25), "room": room4, "num": 4},
        "door5": {"position": (634, 295, 30, 50), "room": room5, "num": 5},
    }

    for door_key, door_info in doors.items():  #Controllo tutte le porte per vedere se si ha colliso
        door_rect = pygame.Rect(door_info["position"])  #Creo un oggetto Rect utilizzando le coordinate della porta corrente
        if not in_room and character.rect.colliderect(door_rect):  #Collisione con queste coordinate
            print("COLLISIONE SEEEEEEEEEEEEEEEEEEEE\n")
            if door_key == "doorExit" and key.possession:
                #VINCITA GIOCO
                win = True
            else:
                in_room = True
                monsters_removed = True
                rectangles_removed = True
                current_room = door_info["room"] #Assegno la stanza corrispondente alla porta dove è avvenuta la collisione
                current_n_room = door_info["num"]

    if in_room:
        #Giocatore presente nella stanza
        print("PRESENTE NELLA STANZAAAAAAAAAAAAAAAAAAAAAA")
        character.changeSize(True) #Cambio la grandezza del personaggio
        print(current_n_room)
        if rectangles_removed == True:
            current_room.clear_rectangles() #Tolgo rettangoli

        if monsters_removed == True:
            monster.clear_monster() #Tolgo mostro 
        
        if character.rect.colliderect(pygame.Rect(765, 210, 35, 160)):
            #Se il giocatore nella stanza entra in collisione con la porta trovatasi dentro la stanza
            character.changeSize(False) #Cambio la grandezza del personaggio
            in_room = False
            monsters_removed = False
            rectangles_removed = False
    return in_room, current_n_room, win #current_n_room serve per la chiave
pygame.display.update()

#####################################################################

#GAME OVER ZONE
game_over = False
game_over_font = pygame.font.Font('Font/Punk Typewriter.otf', 36)
game_over_text = game_over_font.render('Game Over', True, WHITE)

#WIN ZONE
win = False
win_font = pygame.font.Font('Font/Punk Typewriter.otf', 45)
win_text = game_over_font.render('You Won!', True, WHITE)

#####################################################################

running = True

in_room = False  #Indica se il giocatore è nella stanza
monsters_removed = False  #Indica se i mostri sono stati rimossi
rectangles_removed = False  #Indica se i rettangoli sono stati rimossi

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    clock.tick(FPS)

    in_room, current_n_room, win = change_room(character, in_room, monsters_removed, rectangles_removed, key) #Vedo se sono nella stanza, mi serve per move di character e x lo sfondo
    current_room.draw(in_room)

    if monster.check_collision(character.rect, in_room): #Controllo se il mostro ed il player hanno avuto una collisione
        game_over = True 
        running = False #Esco
    if win:
        screen.fill(BLACK)
        running = False #Esco
    keys = pygame.key.get_pressed() #Salva il tasto premuto
    character.move(keys, in_room) #Muove il personaggio seguendo le frecce
    #Muovo il mostro
    monster.update()
    #Disegna il player
    character.draw()
    #Disegna il mostro
    monster.draw(in_room)
    #Disegna la chiave
    key.drawKey(current_n_room) #Se la stanza è quella disegno la chiave
    key.collision_key(character.rect, in_room)
    #pygame.draw.lines(screen, "grey0", False, waypoints) DEBUG Usato per vedere la strada del mostro

    pygame.display.flip()

if game_over:
    screen.blit(game_over_text, (widthB // 2 - 50, heightB // 2 - 10))
    pygame.display.flip()
    pygame.time.wait(2000) #Aspetto 2 secondi per uscire

if win:
    screen.blit(win_text, (widthB // 2 - 50, heightB // 2 - 10))
    pygame.display.flip()
    pygame.time.wait(4000) #Aspetto 4 secondi per uscire