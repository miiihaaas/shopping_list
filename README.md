# Workspace Shopping List Aplikacija

Flask aplikacija za upravljanje listama za kupovinu u više različitih workspace-ova, sa podrškom za više korisnika.

## Funkcionalnosti

- Registracija i prijava korisnika
- Admin panel za upravljanje workspace-ovima i korisnicima
- Dodela korisnika workspace-ovima
- Dodavanje, izmena, brisanje i označavanje stavki za kupovinu
- Responzivan UI prilagođen mobilnim uređajima

## Tehnologije

- Flask (Python web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Autentifikacija korisnika)
- Flask-WTF (Forme i CSRF zaštita)
- Bootstrap 5 (Frontend)
- SQLite (Baza podataka)

## Instalacija

1. Klonirajte repozitorijum:
```
git clone <url-repozitorijuma>
cd workspace-shopping-list
```

2. Kreirajte i aktivirajte virtualno okruženje:
```
# Za Windows
python -m venv venv
venv\Scripts\activate

# Za Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instalirajte potrebne zavisnosti:
```
pip install -r requirements.txt
```

4. Kopirajte `.env.example` u `.env` fajl i postavite vrednosti:
```
cp .env.example .env
```
Uredite `.env` fajl sa željenim vrednostima.

## Pokretanje aplikacije

```
python run.py
```

Aplikacija će biti dostupna na `http://localhost:5000`

## Početni pristup

Prilikom prvog pokretanja, kreira se admin korisnik:
- Korisničko ime: `admin`
- Email: `admin@example.com`
- Lozinka: `admin`

Preporučujemo da promenite admin lozinku nakon prve prijave.

## Korišćenje aplikacije

1. Prijavite se kao admin korisnik
2. Kreirajte nove workspace-ove u admin panelu
3. Dodajte korisnike u workspace-ove
4. Korisnici se mogu prijaviti i videti liste za kupovinu svog workspace-a
5. Korisnici mogu dodavati, menjati i označavati stavke kao kupljene

## Testiranje

Za pokretanje testova:
```
pytest
```

Za proveru kodnog stila:
```
ruff check .
```

Za proveru tipova:
```
mypy .
```
