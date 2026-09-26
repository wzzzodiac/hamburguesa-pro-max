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

## Purpose and third-party rights

This is a free, independently made practice game that was originally created to help one specific person learn how to assemble menu items. It is not an official training tool, and it was not created to attract a large audience, compete with a restaurant business, or profit from anyone else's work. Because the repository and GitHub Pages site are public, anyone can still access them.

This project is not affiliated with, sponsored by, or endorsed by McDonald's or any of its franchisees. References to McDonald's and product names identify the items being practiced. I do not claim ownership of their trademarks, official recipes, training materials, or other third-party intellectual property. No photographs or scans of the reference pages are included in this repository. The ingredient illustrations were made for this project; the practice data contains manually entered ingredient sequences and quantities based on reference diagrams.

The exercises may be incomplete, outdated, or different from procedures at a particular restaurant. They are not a substitute for current instructions from an employer. If you are a rights holder and believe specific material here should be changed or removed, please [open an issue](https://github.com/wzzzodiac/hamburguesa-pro-max/issues) or contact the repository owner so the concern can be reviewed. This statement describes the project's purpose; it does not grant permission to publish protected material or prevent a rights holder from making a claim.
