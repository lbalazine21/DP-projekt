import pygame
import sys
from pyswip import Prolog

# KONFIGURIRANJE PROZORA
pygame.init()
sirina, visina, UI_HEIGHT = 1500, 1250, 100
ROWS, COLS = 13, 15
TILE_SIZE = sirina // COLS
TOTAL_HEIGHT = visina + UI_HEIGHT

# UCITAVANJE ZVUKOVA
zvuk_pokupljeno = pygame.mixer.Sound("Glazba/pokupljeno.mp3")
zvuk_pobjeda = pygame.mixer.Sound("Glazba/pobjeda.mp3")
zvuk_poraz = pygame.mixer.Sound("Glazba/poraz.mp3")
zvuk_zamrznut = pygame.mixer.Sound("Glazba/zamrznut.wav")
zvuk_uspori = pygame.mixer.Sound("Glazba/uspori.ogg")

# UCITAVANJE TEKSTURA
tekstura_pod = pygame.image.load("Slike/pod.jpg")
tekstura_pod = pygame.transform.scale(tekstura_pod, (TILE_SIZE, TILE_SIZE))
tekstura_zid = pygame.image.load("Slike/zid.png")
tekstura_zid = pygame.transform.scale(tekstura_zid, (TILE_SIZE, TILE_SIZE))
tekstura_igrac = pygame.image.load("Slike/igrac.png")
tekstura_igrac = pygame.transform.scale(tekstura_igrac, (TILE_SIZE, TILE_SIZE))
tekstura_duh = pygame.image.load("Slike/duh.png")
tekstura_duh = pygame.transform.scale(tekstura_duh, (TILE_SIZE, TILE_SIZE))
tekstura_kljuc = pygame.image.load("Slike/kljuc.png")
tekstura_kljuc = pygame.transform.scale(tekstura_kljuc, (TILE_SIZE, TILE_SIZE))
tekstura_vrata = pygame.image.load("Slike/vrata.png")
tekstura_vrata = pygame.transform.scale(tekstura_vrata, (TILE_SIZE, TILE_SIZE))
tekstura_snijeg = pygame.image.load("Slike/snijeg.png")
tekstura_snijeg = pygame.transform.scale(tekstura_snijeg, (TILE_SIZE // 2, TILE_SIZE // 2))
tekstura_led = pygame.image.load("Slike/led.svg")
tekstura_led = pygame.transform.scale(tekstura_led, (TILE_SIZE * 1.5, TILE_SIZE * 1.5))
tekstura_sat = pygame.image.load("Slike/sat.png")
tekstura_sat = pygame.transform.scale(tekstura_sat, (TILE_SIZE // 1.5, TILE_SIZE // 1.5))
tekstura_usporen = pygame.image.load("Slike/usporen.png")
tekstura_usporen = pygame.transform.scale(tekstura_usporen, (TILE_SIZE * 2, TILE_SIZE * 2))

# KREIRANJE LABIRINTA
labirint = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# POSTAVLJANJE RADA PROGRAMA
prozor = pygame.display.set_mode((sirina, TOTAL_HEIGHT))
pygame.display.set_caption("Dungeon Explorer")
clock = pygame.time.Clock()
prolog = Prolog()
prolog.consult("logika.pl")

def nacrtaj_pod():
    for red, redovi in enumerate(labirint):
        for stupac, celija in enumerate(redovi):
            if celija == 0:
                prozor.blit(tekstura_pod, (stupac * TILE_SIZE, red * TILE_SIZE))

def nacrtaj_labirint():
    for red, redovi in enumerate(labirint):
        for stupac, celija in enumerate(redovi):
            if celija == 1:
                prozor.blit(tekstura_zid, (stupac * TILE_SIZE, red * TILE_SIZE))

def nacrtaj_UI(broj_pokupljenih, ukupno_kljuceva, proslo_vrijeme):
    pygame.draw.rect(prozor, (0, 0, 0), (0, visina, sirina, UI_HEIGHT))
    font = pygame.font.SysFont("Courier", 32, bold=True)
    tekst_kljuc = font.render(f" KEYS: {broj_pokupljenih}/{ukupno_kljuceva}", True, (255, 255, 255))
    tekst_vrijeme = font.render(f"TIME: {format_time(proslo_vrijeme)} ", True, (255, 255, 255))
    okvir_kljuc = tekst_kljuc.get_rect(midleft=(10, visina + UI_HEIGHT // 2))
    okvir_vrijeme = tekst_vrijeme.get_rect(midright=(sirina - 10, visina + UI_HEIGHT // 2))
    prozor.blit(tekst_kljuc, okvir_kljuc)
    prozor.blit(tekst_vrijeme, okvir_vrijeme)

# DEFINIRANJE FORMATA VREMENA
def format_time(proslo_vrijeme):
    minute = proslo_vrijeme // 60000 
    sekunde = (proslo_vrijeme // 1000) % 60
    return f"{minute:02}:{sekunde:02}"

# GLOBALNI REZULTATI IGRE
rezultati = []

def end_screen(prozor, sirina, visina, poruka, proslo_vrijeme):
    pokrenuto = True
    font = pygame.font.SysFont("Courier", 48, bold=True)
    button_font = pygame.font.SysFont("Courier", 32, bold=True)
    small_font = pygame.font.SysFont("Courier", 28)

    rezultat = f"{len(rezultati) + 1}. GAME - {'WON' if 'WON' in poruka else 'LOST'} - {format_time(proslo_vrijeme)}"
    rezultati.append(rezultat)

    while pokrenuto:
        prozor.fill((0, 0, 0))

        # PORUKA
        tekst_poruka = font.render(poruka, True, (255, 255, 0) if "WON" in poruka else (255, 0, 0))
        okvir_poruka = tekst_poruka.get_rect(center=(sirina // 2, visina // 2 - 120))
        prozor.blit(tekst_poruka, okvir_poruka)

        # GUMB ZA IGRAJ PONOVNO
        pygame.draw.rect(prozor, (255, 255, 255), (sirina // 2 - 150, visina // 2 - 20, 300, 70))
        tekst_igraj_ponovno = button_font.render("PLAY AGAIN", True, (0, 0, 0))
        prozor.blit(tekst_igraj_ponovno, (sirina // 2 - tekst_igraj_ponovno.get_width() // 2, visina // 2 - 5))

        # GUMB ZA IZLAZAK
        pygame.draw.rect(prozor, (255, 255, 255), (sirina // 2 - 150, visina // 2 + 70, 300, 70))
        tekst_izlaz = button_font.render("EXIT", True, (0, 0, 0))
        prozor.blit(tekst_izlaz, (sirina // 2 - tekst_izlaz.get_width() // 2, visina // 2 + 85))

        # REZULTATI
        razmak = 80
        y_offset = visina // 2 + 150 + razmak
        for rezultat in rezultati[-5:]:
            tekst_rezultat = small_font.render(rezultat, True, (255, 255, 255))
            okvir_rezultat = tekst_rezultat.get_rect(center=(sirina // 2, y_offset))
            prozor.blit(tekst_rezultat, okvir_rezultat)
            y_offset += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # IGRAJ PONOVNO
                if sirina // 2 - 150 <= mouse_pos[0] <= sirina // 2 + 150 and visina // 2 - 20 <= mouse_pos[1] <= visina // 2 + 50:
                    return "restart"
                # IZLAZAK
                elif sirina // 2 - 150 <= mouse_pos[0] <= sirina // 2 + 150 and visina // 2 + 70 <= mouse_pos[1] <= visina // 2 + 140:
                    pygame.quit()
                    sys.exit()

class Igrac:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vrijeme_proslog_poteza = 0

    def kretanje(self, dx, dy):
        trenutno_vrijeme = pygame.time.get_ticks()
        if trenutno_vrijeme - self.vrijeme_proslog_poteza > 100:
            new_x = self.x + dx
            new_y = self.y + dy
            if labirint[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0:
                self.x = new_x
                self.y = new_y
            self.vrijeme_proslog_poteza = trenutno_vrijeme

    def draw(self):
        prozor.blit(tekstura_igrac, (self.x, self.y))

class Duh:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.brojac = 0
        self.zamrznut_do = 0
        self.usporen_do = 0
        self.status = "normalna"

    def azuriraj(self, igrac_x, igrac_y):
        trenutni_vrijeme = pygame.time.get_ticks()

        # DUH JE ZAMRZNUT
        if trenutni_vrijeme < self.zamrznut_do:
            return

        # DUH JE USPOREN
        if trenutni_vrijeme > self.usporen_do and self.status == "usporena":
            query = f"resetiraj_brzinu(usporena, Status)"
            prolog_rezultat = list(prolog.query(query))
            self.status = prolog_rezultat[0]['Status']

        # DOHVACANJE BRZINE IZ PROLOGA
        query = f"brzina_duha({self.status}, Brzina)"
        prolog_rezultat = list(prolog.query(query))
        trenutna_brzina = prolog_rezultat[0]['Brzina']

        # AZURIRANJE DUHOVE POZICIJE
        self.brojac += 1
        if self.brojac % trenutna_brzina == 0:
            start_x, start_y = self.x // TILE_SIZE, self.y // TILE_SIZE
            igrac_x, igrac_y = igrac_x // TILE_SIZE, igrac_y // TILE_SIZE
            query = f"kretanje_duha({start_x}, {start_y}, {igrac_x}, {igrac_y}, NX, NY)"
            prolog_rezultat = list(prolog.query(query))
            if prolog_rezultat:
                self.x = prolog_rezultat[0]['NX'] * TILE_SIZE
                self.y = prolog_rezultat[0]['NY'] * TILE_SIZE

    def zamrzni(self, trajanje):
        self.zamrznut_do = pygame.time.get_ticks() + trajanje

    def uspori(self, trajanje):
        self.status = "usporena"
        self.usporen_do = pygame.time.get_ticks() + trajanje

    def draw(self):
        if pygame.time.get_ticks() < self.zamrznut_do:
            offset_x = (TILE_SIZE - tekstura_led.get_width()) // 2
            offset_y = (TILE_SIZE - tekstura_led.get_height()) // 2
            prozor.blit(tekstura_led, (self.x + offset_x, self.y + offset_y))

        if pygame.time.get_ticks() < self.usporen_do:
            offset_x = (TILE_SIZE - tekstura_usporen.get_width()) // 2
            offset_y = (TILE_SIZE - tekstura_usporen.get_height()) // 2
            prozor.blit(tekstura_usporen, (self.x + offset_x, self.y + offset_y))
        
        prozor.blit(tekstura_duh, (self.x, self.y))

class Kljuc:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pokupljen = False

    def draw(self):
        if not self.pokupljen:
            prozor.blit(tekstura_kljuc, (self.x, self.y))

    def pokupi(self, igrac_x, igrac_y):
        if not self.pokupljen and self.x == igrac_x and self.y == igrac_y:
            self.pokupljen = True
            zvuk_pokupljeno.play()
            return True
        return False

class Vrata:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        prozor.blit(tekstura_vrata, (self.x, self.y))

    def provjeri_zavrsetak(self, broj_pokupljenih, ukupno_kljuceva):
        return broj_pokupljenih >= ukupno_kljuceva

class EfektZamrzavanja:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pokupljen = False

    def draw(self):
        if not self.pokupljen:
            efekt_x = self.x + (TILE_SIZE - TILE_SIZE // 2) // 2
            efekt_y = self.y + (TILE_SIZE - TILE_SIZE // 2) // 2
            prozor.blit(tekstura_snijeg, (efekt_x, efekt_y))

    def pokupi(self, igrac_x, igrac_y):
        if not self.pokupljen and self.x == igrac_x and self.y == igrac_y:
            self.pokupljen = True
            zvuk_zamrznut.play()
            zvuk_zamrznut.set_volume(0.4)
            return True
        return False

class EfektUsporavanja:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pokupljen = False

    def draw(self):
        if not self.pokupljen:
            efekt_x = self.x + (TILE_SIZE - TILE_SIZE // 2) // 2
            efekt_y = self.y + (TILE_SIZE - TILE_SIZE // 2) // 2.5
            prozor.blit(tekstura_sat, (efekt_x, efekt_y))

    def pokupi(self, igrac_x, igrac_y):
        if not self.pokupljen and self.x == igrac_x and self.y == igrac_y:
            self.pokupljen = True
            zvuk_uspori.play()
            zvuk_uspori.set_volume(0.3)
            return True
        return False

def main():
    pygame.mixer.music.load("Glazba/pozadina.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    zvuk_pobjeda.stop()
    zvuk_poraz.stop()

    global broj_pokupljenih, kljucevi, igrac, duh, vrata
    broj_pokupljenih = 0
    start_time = pygame.time.get_ticks()

    # POSTAVLJANJE OBJEKATA UNUTAR LABIRINTA
    kljucevi = [Kljuc(TILE_SIZE * 12, TILE_SIZE * 1), Kljuc(TILE_SIZE * 5, TILE_SIZE * 9)]
    igrac = Igrac(TILE_SIZE, TILE_SIZE)
    duh = Duh(TILE_SIZE * 7, TILE_SIZE * 6)
    vrata = Vrata(TILE_SIZE * 8, TILE_SIZE * 6)
    efekt_zamrzavanja = [EfektZamrzavanja(TILE_SIZE * 9, TILE_SIZE * 3)]
    efekt_usporavanja = [EfektUsporavanja(TILE_SIZE * 2, TILE_SIZE * 11)]

    pokrenuto = True
    while pokrenuto:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tipka = pygame.key.get_pressed()
        if tipka[pygame.K_LEFT]:
            igrac.kretanje(-TILE_SIZE, 0)
        if tipka[pygame.K_RIGHT]:
            igrac.kretanje(TILE_SIZE, 0)
        if tipka[pygame.K_UP]:
            igrac.kretanje(0, -TILE_SIZE)
        if tipka[pygame.K_DOWN]:
            igrac.kretanje(0, TILE_SIZE)

        proslo_vrijeme = pygame.time.get_ticks() - start_time

        for kljuc in kljucevi:
            if kljuc.pokupi(igrac.x, igrac.y):
                broj_pokupljenih += 1

        for efektZamrzavanja in efekt_zamrzavanja:
            if efektZamrzavanja.pokupi(igrac.x, igrac.y):
                duh.zamrzni(3000)

        for efektUsporavanja in efekt_usporavanja:
            if efektUsporavanja.pokupi(igrac.x, igrac.y):
                duh.uspori(5000)

        if igrac.x == vrata.x and igrac.y == vrata.y:
            query = f"provjeri_pobjedu({broj_pokupljenih}, {len(kljucevi)}, {igrac.x}, {igrac.y}, {vrata.x}, {vrata.y}, pobjeda)"
            if list(prolog.query(query)):
                zvuk_pobjeda.play()
                zvuk_pobjeda.set_volume(0.3)
                prolog_rezultat = end_screen(prozor, sirina, visina, "PLAYER WON!", proslo_vrijeme)
                if prolog_rezultat == "restart":
                    main()
                return

        query = f"provjeri_poraz({igrac.x}, {igrac.y}, {duh.x}, {duh.y}, poraz)"
        if list(prolog.query(query)):
            zvuk_poraz.play()
            zvuk_poraz.set_volume(0.4)
            prolog_rezultat = end_screen(prozor, sirina, visina, "PLAYER LOST!", proslo_vrijeme)
            if prolog_rezultat == "restart":
                main()
            return

        duh.azuriraj(igrac.x, igrac.y)

        nacrtaj_pod()
        nacrtaj_labirint()
        nacrtaj_UI(broj_pokupljenih, len(kljucevi), proslo_vrijeme)
        vrata.draw()
        igrac.draw()
        duh.draw()

        for kljuc in kljucevi:
            kljuc.draw()
        for efektZamrzavanja in efekt_zamrzavanja:
            efektZamrzavanja.draw()
        for efektZamrzavanja in efekt_usporavanja:
            efektZamrzavanja.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()