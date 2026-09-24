# Burger Training

Statisches Trainingsspiel für die 32 Burger-, Frühstücks- und Wrap-Rezepte in `data/recipes.json`. Die erste Schicht eines Rezepts wird beim umgedrehten Aufbau zuerst gelegt. Bestellungen kommen aus `src/order-generator.mjs`; Änderungen werden mit den `expectedLayers` der jeweiligen Ticketzeile geprüft.

## Lokal starten

```sh
python -m http.server 8000
```

Danach `http://localhost:8000/` öffnen. Die Seite benötigt keine Pakete, Konten oder externen Dienste. Ein direkter `file://`-Aufruf funktioniert wegen des JSON-Fetchs nicht.

## Tests

```sh
node --test tests/*.test.mjs
```

## GitHub Pages

Die Startseite liegt im Repository-Stamm. In **Settings → Pages → Build and deployment** als Quelle **Deploy from a branch**, Branch **main**, Ordner **/(root)** wählen und speichern. Danach ist die Seite unter `https://wzzzodiac.github.io/hamburguesa-pro-max/` erreichbar. Alle Pfade sind relativ, damit die Projekt-Unteradresse funktioniert.
