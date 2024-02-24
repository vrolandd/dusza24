# Fogadások (fejlesztői dokumentáció)

## Hello, world!
Segítség azoknak a fejlesztőknek, akik szerkesztenék vagy javítanák a kódot, vagy éppen együttműködnének velünk az alkalmazásunk fejlesztésében.
A kód átláthatóságán van mit dolgozni így minden segítséget szívesen fogadunk.

## Felhasznált technológiák
- A program futtatásához minimum `Python 3.10`-re van szükség
- A szükséges könyvtárak a `requirements.txt` fájlban találhatóak
- Adatbázisnak `SQLite`-ot használ
- A jelszavak titkosítására pedig `Argon2`-t

## A `main.py` fájl
Ebben a fájlban található minden amit a felhasználó lát. Az összes nézet és ablak felépítése itt van. Minden nézet vagy felugró ablak külön metódusban található, hogy könnyű legyen köztük váltani. A felhasználó állapota is itt van eltárolva a `currentUser` globális változóban.

## A `db.py` fájl
Ez a fájl felel az adatbázissal való kommunikációért. Itt az összes lekérdezésre és frissítésre használt metódus.

## A `models.py` fájl
Itt találhatóak az adatbázis és a program közötti egyfajta "hídként" működő osztályok. Ezek segítségével a programban egyszerűbb az adatokat felhasználni.

## A `queries.py` fájl
Ennek a fájlnak nagyrészt a statisztikában van szerepe, mindenféle adatok kiszámításához használt metódusok vannak benne.

## Egyéb fájlok
- `.gitignore`: Ebben találhatóak azok a mappák és fájlok nevei amiket nem szeretnénk, hogy verziókezelve legyenek
- `feladat.pdf` és `feladat-donto.pdf`: Ezek alapján készült a program :)