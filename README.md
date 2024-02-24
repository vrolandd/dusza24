# Fogadások
Baráti társaságokban, munkahelyen vagy egyszerűen csak egy konkrét téma kapcsán gyakran előfordul, hogy a felek fogadni szeretnének egymással valamely konkrét események kimeneteleit illetően. Ezeknek a fogadásoknak a lényege általában nem is a nyeremények, hanem a versengés, a szellemi megmérettetés.
A programunk megkönnyíti ezeknek a fogadásoknak és a felhasználók pontszámának nyilvántartását.

## Letöltés / Első lépések
A program legfrissebb verziója letölthető [innen.](https://github.com/vrolandd/dusza24/releases/tag/latest)
Letöltés és egyszeri futtatás után a program létrehoz egy `data` mappát. Ebbe fogja tárolni a fogadások adatait.
Ha a program régebbi verziójából meglévő adatainkat szeretnénk használni, bejelentkezés után a felhasználó menüben van lehetőségünk ezeket importálni.
**!! FIGYELEM !! Hibás fájlok megadása esetén az adatbázis integritása sérülhet.**

[A fejlesztői dokumentáció itt érhető el.](https://github.com/vrolandd/dusza24/blob/master/Developer.md)

## Felhasználói felület
A programot elindítva első látásra a bejelentkező felület fogad minket, ahol lehetőségünk van meglévő felhasználónevünkel és jelszavunkal belépni.

![image](https://github.com/vrolandd/dusza24/assets/60399001/ee123f3b-f354-44db-b6e0-45d059389a68)

Ha a megadott felhasználónév még nincs a rendszerben akkor a program megkérdezi, hogy szeretnénk-e regisztrálni.

![image](https://github.com/vrolandd/dusza24/assets/60399001/f843ba98-4a3e-46fb-bb76-f40c5cb7359e)

## Szerepkör választó
Bejelentkezés után ki kell választanunk, hogy milyen módban szeretnénk használni a programot. Három opciónk van:
 - Szervező: Ebben a módban láthatjuk a meglévő játékainkat, lezárhatjuk azokat és újakat készíthetünk.
 - Fogadó: Itt látjuk és törölhetjük a már leadott fogadásainkat és újakat adhatunk le.
 - Statisztika: Ez a nézet mutatja a felhasználók ranglistját pontok szerint és egyéb statisztikákat.
Ezen kívül jobb felül telálható a felhasználó menü ahol jelszót változtathatunk vagy kijelentjkezhetünk.

![image](https://github.com/vrolandd/dusza24/assets/60399001/a24ea971-89f1-4a00-a51a-3bc37b09086d)

****
### **Szervező**
A felhasználó látja a saját játékait, tud újat létrehozni és meglévőt lezárni.

![image](https://github.com/vrolandd/dusza24/assets/60399001/3e28f57d-5f2c-497d-88de-7962d38aa61c)

#### Új játék
Az `Új játék` gombra kattintva az alábbi felület jelenik meg. Itt meg kell adnunk a játék nevét, az alanyokat és az eseményeket. Az utóbbi kettőt az alattuk lévő szövegmező segítségével tudjuk begtenni. A beírt szöveget az Enter billenyű lenyomásával lehet a listához adni. Törölni az elemekre kattintással lehet.

![image](https://github.com/vrolandd/dusza24/assets/60399001/cd9babfe-3a68-45c5-8786-7de0140159f3)

#### Játék lezárása
Egy játék lezárásához először ki kell választanunk egyet a listából utána a `Játék lezárása` gombra kattintani. Ez megnyit egy ablakot ahol be kell írni az összes alany eredményeit minden eseményre.

![image](https://github.com/vrolandd/dusza24/assets/60399001/b2e29f7a-d41b-4652-8957-c370087f7e7e)

****
### **Fogadó**
Fogadó nézetben látjuk az elérhető játékokat és a saját fogadásainkat. Tudunk új fogadást leadni és meglévőt törölni, ha a játék amire leadtuk még nem zárult le.

![image](https://github.com/vrolandd/dusza24/assets/60399001/e12bffbc-7da5-448c-b2f2-bed75ae31a07)

#### Fogadás leadása
A fogadás leadásához ki kell választani egy játékot a fenti listából majd a `Fogadás leadása` gombra kattintva előjön egy ablak ahol megtehetjük a tétünket.

![image](https://github.com/vrolandd/dusza24/assets/60399001/1b59a10c-13b1-498e-8305-b8ccaa19c967)

#### Fogadás törlése
Ha kiválasztottunk egy fogadást a listából akkor ezt a `Fogadás törlése` gombbal törölhetjük. Fontos, hogy a feltett pontjainkat nem kapjuk vissza.

![image](https://github.com/vrolandd/dusza24/assets/60399001/e6997b0c-ed0f-4322-aa89-5f8f9b6d7fc3)

****
### **Statisztika**
Ezen az oldalon látható a ranglista és a játékok statisztikája. Ha kiválasztunk egy játékot akkor részletesebb statisztika is megjelenik róla.

![image](https://github.com/vrolandd/dusza24/assets/60399001/23c5b652-3cd4-42d7-b9bd-73384d9131da)
