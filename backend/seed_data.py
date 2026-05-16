import sys
import os
from datetime import datetime, timedelta, timezone

# Hozzáadjuk a backend mappát a Python útvonalához
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
POSTERS_DIR = os.path.join(PROJECT_ROOT, "frontend", "img", "posters")

sys.path.append(BACKEND_DIR)

from app.database import SessionLocal, engine, Base
from app.models.movie import Movie
from app.models.screening import Screening

def get_local_poster_path(title):
    """
    A film címe alapján generál egy letisztult, ember által olvasható fájlnevet.
    Pl.: 'The Dark Knight' -> 'the_dark_knight.jpg'
    """
    # Mivel magyarosítottuk a címeket, itt összekötjük őket az eredeti angol fájlnevekkel, amiket már lementettél!
    file_mapping = {
        "A sötét lovag": "the_dark_knight.jpg",
        "Schindler listája": "schindlers_list.jpg",
        "A Gyűrűk Ura: A Gyűrű Szövetsége": "the_lord_of_the_rings_the_fellowship_of_the_ring.jpg",
        "Harcosok klubja": "fight_club.jpg",
        "Star Wars: V. rész - A Birodalom visszavág": "star_wars_5.jpg",
        "Száll a kakukk fészkére": "cuckoos_nest.jpg",
        "Az élet csodaszép": "its_a_wonderful_life.jpg",
        "Ryan közlegény megmentése": "saving_private_ryan.jpg",
        "Halálsoron": "the_green_mile.jpg",
        "Vissza a jövőbe": "back_to_the_future.jpg",
        "A zongorista": "the_pianist.jpg",
        "Az oroszlánkirály": "the_lion_king.jpg",
        "A tégla": "the_departed.jpg",
        "Whiplash": "whiplash.jpg",
        "Harakiri": "harakiri.jpg",
        "Volt egyszer egy Vadnyugat": "once_upon_a_time_in_the_west.jpg",
        "Nagyvárosi fények": "city_lights.jpg",
        "Memento": "memento.jpg",
        "WALL·E": "walle.jpg",
        "A dicsőség ösvényei": "paths_of_glory.jpg",
        "A vád tanúja": "witness_for_the_prosecution.jpg",
        "Amerikai szépség": "american_beauty.jpg",
        "A sötét lovag - Felemelkedés": "the_dark_knight_rises.jpg",
        "Amadeus": "amadeus.jpg",
        "A rettenthetetlen": "braveheart.jpg",
        "A vadon hercegnője": "princess_mononoke.jpg",
        "Volt egyszer egy Amerika": "once_upon_a_time_in_america.jpg",
        "Ének az esőben": "singin_in_the_rain.jpg",
        "Star Wars: VI. rész - A Jedi visszatér": "star_wars_6.jpg",
        "Kutyaszorítóban": "reservoir_dogs.jpg",
        "Jöjj és lásd!": "come_and_see.jpg",
        "Észak-Északnyugat": "north_by_northwest.jpg",
        "Blöff": "snatch.jpg"
    }
    
    if title in file_mapping:
        return f"img/posters/{file_mapping[title]}"
        
    clean = "".join(c for c in title.lower() if c.isalnum() or c == ' ')
    clean = " ".join(clean.split())
    filename = clean.replace(' ', '_') + ".jpg"
    return f"img/posters/{filename}"

def seed_db():
    # Adatbázis táblák létrehozása (biztonság kedvéért)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Definiáljuk a filmeket előre az új, sokkal pontosabb műfajokkal
        movies = [
            Movie(
                title="A sötét lovag", 
                description="Batman megküzd a Jokerrel Gotham városában.",
                duration_minutes=152, 
                genre="Akció", 
                poster_url="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
            ),
            Movie(
                title="Schindler listája", 
                description="Oskar Schindler megmenti több mint ezer zsidó életét a holokauszt idején.",
                duration_minutes=195, 
                genre="Életrajzi", 
                poster_url="https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg" 
            ),
            Movie(
                title="A Gyűrűk Ura: A Gyűrű Szövetsége", 
                description="Egy szerény hobbit útnak indul, hogy elpusztítson egy hatalmas gyűrűt.",
                duration_minutes=178, 
                genre="Fantasy", 
                poster_url="https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg" 
            ),
            Movie(
                title="Harcosok klubja", 
                description="Egy álmatlanságban szenvedő irodai munkás földalatti harcos klubot alapít.",
                duration_minutes=139, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg" 
            ),
            Movie(
                title="Star Wars: V. rész - A Birodalom visszavág", 
                description="A lázadók a jégbolygón küzdenek a Birodalom ellen, miközben Luke Jodát keresi.",
                duration_minutes=124, 
                genre="Sci-Fi", 
                poster_url="https://image.tmdb.org/t/p/w500/7BuH8itoSrLExs2GIrFNRo9243c.jpg"
            ),
            Movie(
                title="Száll a kakukk fészkére", 
                description="Egy bűnöző elmegyógyintézetbe kerül, ahol fellázad az elnyomó nővér ellen.",
                duration_minutes=133, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/3jcbjzovs00Dz8HPhXQ9v6z6L3B.jpg"
            ),
            Movie(
                title="Az élet csodaszép", 
                description="Egy angyal megmutatja egy kétségbeesett üzletembernek, milyen lenne az élet nélküle.",
                duration_minutes=130, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/bSqt9rhDZx1Q7UZ86dBPKdNomp2.jpg" 
            ),
            Movie(
                title="Ryan közlegény megmentése", 
                description="Normandia partraszállása után egy osztag egyetlen túlélő testvért próbál hazajuttatni.",
                duration_minutes=169, 
                genre="Háborús", 
                poster_url="https://image.tmdb.org/t/p/w500/uqx37cS8cpLq31hXvUeHkZ1EANe.jpg"
            ),
            Movie(
                title="Halálsoron", 
                description="Csodák és tragédiák a halálsoron a harmincas évek Amerikájában.",
                duration_minutes=189, 
                genre="Fantasy", 
                poster_url="https://image.tmdb.org/t/p/w500/8VG8fDNiy50H4FedGwdSVUPoaJe.jpg" 
            ),
            Movie(
                title="Vissza a jövőbe", 
                description="Egy tinédzser véletlenül visszautazik az időben és találkozik a szüleivel.",
                duration_minutes=116, 
                genre="Sci-Fi", 
                poster_url="https://image.tmdb.org/t/p/w500/fNOH9f1aA7XRTzl1sAOSkK6e6L.jpg"
            ),
            Movie(
                title="A zongorista", 
                description="Egy zsidó zongorista hihetetlen túlélése a lerombolt Varsóban.",
                duration_minutes=150, 
                genre="Életrajzi", 
                poster_url="https://image.tmdb.org/t/p/w500/2hFvxCCWrTmCYw00vX0dEDHWeF.jpg"
            ),
            Movie(
                title="Az oroszlánkirály", 
                description="Egy trónörökös oroszlánkölyök útja, hogy visszaszerezze a királyságot.",
                duration_minutes=89, 
                genre="Animáció", 
                poster_url="https://image.tmdb.org/t/p/w500/sKCr78AS8o6O_71M0KxJ2T11vJw.jpg"
            ),
            Movie(
                title="A tégla", 
                description="Beépített zsaru a maffiában és egy tégla a rendőrségen macska-egér játékot játszik.",
                duration_minutes=151, 
                genre="Krimi", 
                poster_url="https://image.tmdb.org/t/p/w500/jyA2oEGmXnU03n8Hk0k4l1G9p89.jpg"
            ),
            Movie(
                title="Whiplash", 
                description="Egy fiatal jazzdobos és kíméletlen tanárának feszült kapcsolata.",
                duration_minutes=106, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg" 
            ),
            Movie(
                title="Harakiri", 
                description="Egy rónin a klán ura előtt elmondja tragikus történetét, mielőtt szeppukut követne el.",
                duration_minutes=133, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/1s1s2FqEikW1f3rVn0oK40XyL6T.jpg"
            ),
            Movie(
                title="Volt egyszer egy Vadnyugat", 
                description="Klasszikus spagettiwestern bosszúról, kapzsiságról és a vasút érkezéséről.",
                duration_minutes=165, 
                genre="Western", 
                poster_url="https://image.tmdb.org/t/p/w500/7a0f6RkEq9r1o7eA8T3x4r3tN1C.jpg"
            ),
            Movie(
                title="Nagyvárosi fények", 
                description="A Csavargó mindent megtesz, hogy pénzt szerezzen egy vak virágáruslány műtétjére.",
                duration_minutes=87, 
                genre="Vígjáték", 
                poster_url="https://image.tmdb.org/t/p/w500/bXNvzjULc9jrOVhGfjcc64uAee0.jpg"
            ),
            Movie(
                title="Memento", 
                description="Egy rövidtávú memóriavesztésben szenvedő férfi a felesége gyilkosát keresi.",
                duration_minutes=113, 
                genre="Thriller", 
                poster_url="https://image.tmdb.org/t/p/w500/yuNs09hvVf0QG9m6H1dZ7oN5kF.jpg"
            ),
            Movie(
                title="WALL·E", 
                description="A távoli jövőben egy kis hulladékgyűjtő robot az űrbe utazik egy szerelem reményében.",
                duration_minutes=98, 
                genre="Animáció", 
                poster_url="https://image.tmdb.org/t/p/w500/hpfCP71911DMBHkQ5K4Ua1A3J.jpg"
            ),
            Movie(
                title="A dicsőség ösvényei", 
                description="Egy ezredes védi katonáit a hadbíróság előtt egy öngyilkos küldetés megtagadása miatt.",
                duration_minutes=88, 
                genre="Háborús", 
                poster_url="https://image.tmdb.org/t/p/w500/lH2ySZeYjZ0J7Fh7T8v6z2XmC4.jpg"
            ),
            Movie(
                title="A vád tanúja", 
                description="Egy briliáns ügyvéd egy gazdag özvegy meggyilkolásával vádolt férfit véd.",
                duration_minutes=116, 
                genre="Krimi", 
                poster_url="https://image.tmdb.org/t/p/w500/9yX3w205M8Uq8oF2l2pL00E0fA.jpg"
            ),
            Movie(
                title="Amerikai szépség", 
                description="Egy kapuzárási pánikkal küzdő családapa beleszeret lánya barátnőjébe.",
                duration_minutes=122, 
                genre="Dráma", 
                poster_url="https://image.tmdb.org/t/p/w500/wby9315QAECRXU92eD1hR8L7S0z.jpg"
            ),
            Movie(
                title="A sötét lovag - Felemelkedés", 
                description="Batman visszatér a száműzetésből, hogy megmentse Gothamet Bane fenyegetésétől.",
                duration_minutes=164, 
                genre="Akció", 
                poster_url="https://image.tmdb.org/t/p/w500/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg" 
            ),
            Movie(
                title="Amadeus", 
                description="Mozart zsenialitása és tragikus vége kortársa és riválisa, Salieri szemszögéből.",
                duration_minutes=160, 
                genre="Életrajzi", 
                poster_url="https://image.tmdb.org/t/p/w500/1nBf8pUfQYc4G1B6o8Zz4F8Q6W9.jpg"
            ),
            Movie(
                title="A rettenthetetlen", 
                description="William Wallace skót nemzeti hős vezeti népét az angol elnyomás ellen.",
                duration_minutes=178, 
                genre="Történelmi", 
                poster_url="https://image.tmdb.org/t/p/w500/or1gBugZ8eA6O2tWn3x2S4H8X0.jpg"
            ),
            Movie(
                title="A vadon hercegnője", 
                description="Egy ifjú harcos egy erdő isteneit védő lány és a helyi ipari település konfliktusába keveredik.",
                duration_minutes=134, 
                genre="Fantasy", 
                poster_url="https://image.tmdb.org/t/p/w500/jHWmNr7m544fJ8eEfiN3J2Z2AOM.jpg"
            ),
            Movie(
                title="Volt egyszer egy Amerika", 
                description="New York-i zsidó gengszterek élete az alkoholtilalom idején és azután.",
                duration_minutes=229, 
                genre="Krimi", 
                poster_url="https://image.tmdb.org/t/p/w500/gOofHjKzYQv6J3k2Fk7g9bA2E9.jpg"
            ),
            Movie(
                title="Ének az esőben", 
                description="Egy némafilmsztár párosnak alkalmazkodnia kell a hangosfilmek betöréséhez Hollywoodba.",
                duration_minutes=103, 
                genre="Musical", 
                poster_url="https://image.tmdb.org/t/p/w500/4vIqR8q5A6FfO8mG4W3yT4VwF0.jpg"
            ),
            Movie(
                title="Star Wars: VI. rész - A Jedi visszatér", 
                description="A lázadók mindent egy lapra tesznek fel az új Halálcsillag és a Császár elpusztításáért.",
                duration_minutes=132, 
                genre="Sci-Fi", 
                poster_url="https://image.tmdb.org/t/p/w500/8bA2i0T0mJ2z4B2mJ7xX8hL9w4b.jpg"
            ),
            Movie(
                title="Kutyaszorítóban", 
                description="Egy ékszerüzlet balul elsült kirablása után a bűnözők egymásban kezdik keresni az árulót.",
                duration_minutes=99, 
                genre="Krimi", 
                poster_url="https://image.tmdb.org/t/p/w500/eP5ZdE6rQ0X7E5oB1I3N0qA8gZ.jpg"
            ),
            Movie(
                title="Jöjj és lásd!", 
                description="Egy belarusz fiú szörnyű megpróbáltatásai a nácik által megszállt falvakban.",
                duration_minutes=142, 
                genre="Háborús", 
                poster_url="https://image.tmdb.org/t/p/w500/8n9xR0QfJ0T0J9E7Q0L0Xk5A6.jpg"
            ),
            Movie(
                title="Észak-Északnyugat", 
                description="Egy ártatlan reklámszakembert kémnek néznek, és kénytelen menekülni az életéért.",
                duration_minutes=136, 
                genre="Thriller", 
                poster_url="https://image.tmdb.org/t/p/w500/iS9oT1R0W3W0Y3A8d9N7w9uF7F.jpg"
            ),
            Movie(
                title="Blöff", 
                description="Egy lopott gyémánt és egy illegális bokszmeccs körül bonyolódó szövevényes történet.",
                duration_minutes=104, 
                genre="Vígjáték", 
                poster_url="https://image.tmdb.org/t/p/w500/50H0E2yE6e5hP0i5k7u7O5H6z3.jpg"
            )
        ]
        
        existing_movies = db.query(Movie).all()
        if existing_movies:
            print("Az adatbázis már tartalmaz filmeket! Műfajok és lokális poszterek ellenőrzése...")
            updated = False
            for movie in existing_movies:
                # Műfajok frissítése az új, pontosított listából
                matching_new = next((m for m in movies if m.title == movie.title), None)
                if matching_new:
                    if movie.genre != matching_new.genre:
                        print(f"  - {movie.title} műfajának frissítése ({movie.genre} -> {matching_new.genre})...")
                        movie.genre = matching_new.genre
                        updated = True
                    
                    # Ellenőrizzük, hogy a poszter le van-e töltve lokálisan
                    new_poster = get_local_poster_path(matching_new.title)
                    if movie.poster_url != new_poster:
                        movie.poster_url = new_poster
                        updated = True
            
            if updated:
                db.commit()
                print("Filmek adatai sikeresen frissítve!")
            else:
                print("Minden adat rendben van.")
            return

        print("Filmek feltöltése folyamatban...")
        
        print("Lokális poszter útvonalak beállítása...")
        for m in movies:
            m.poster_url = get_local_poster_path(m.title)
        
        db.add_all(movies)
        db.commit()
        
        # Vetítések (Screenings) hozzáadása
        print("Vetítések feltöltése folyamatban...")
        # Pontos órára kerekítjük az időt, hogy szép kerek időpontok legyenek (pl. 14:00, 16:00)
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        
        screenings = []
        # Minden filmhez generálunk 2 vetítést, elosztva a napok és termek között
        for i, movie in enumerate(movies):
            # Délutáni/Korai vetítés
            screenings.append(
                Screening(
                    movie_id=movie.id,
                    screen_number=(i % 3) + 1,  # 1, 2, vagy 3-as terem
                    # 5 filmenként új napra rakja, és 10:00-tól 2 óránként növeli
                    screening_datetime=now + timedelta(days=1 + (i // 5), hours=10 + ((i % 5) * 2)),
                    available_seats=100,
                    total_seats=100,
                    price_per_ticket=2500 if movie.genre == "Akció" else 2200
                )
            )
            # Esti/Késői vetítés (2 nappal később)
            screenings.append(
                Screening(
                    movie_id=movie.id,
                    screen_number=(i % 3) + 1,
                    screening_datetime=now + timedelta(days=3 + (i // 5), hours=11 + ((i % 5) * 2)),
                    available_seats=100,
                    total_seats=100,
                    price_per_ticket=2000
                )
            )
            
        db.add_all(screenings)
        db.commit()

        print("Sikeresen feltöltöttük az adatbázist a teszt filmekkel és vetítésekkel! 🎬🍿")
        
    except Exception as e:
        print(f"Hiba történt az adatok feltöltésekor: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()