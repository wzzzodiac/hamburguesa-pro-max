# Pedidos de práctica

La fuente de verdad de las capas base es `recipes.json`. `src/order-generator.mjs` genera pedidos sin modificar ese archivo. Son reglas de **entrenamiento configurables**, no una lista oficial de modificaciones admitidas por el restaurante.

## Configuración inicial

| Regla | Valor inicial |
| --- | --- |
| Productos por pedido | 2: 35 %, 3: 35 %, 4: 20 %, 5: 10 % |
| Productos del sorteo normal | `category = burger` |
| Oportunidad inicial de modificación por producto | 35 % |
| Tipo de modificación, cuando toca | Omitir: 70 %, extra ingrediente: 25 %, extra patty: 5 % |
| Mezcla en cada pedido | Al menos uno normal y uno modificado |
| Complejidad | Máximo una modificación por producto |

La obligación de mezclar productos normales y modificados ajusta el 35 % inicial. En un pedido de dos productos habrá exactamente uno de cada tipo. Se puede desactivar con `ensureMixedOrder: false` o cambiar los pesos en `DEFAULT_ORDER_CONFIG`. Se permiten productos repetidos: dos Cheeseburgers en un pedido son válidos.

## Cambios permitidos por el generador

- "Ohne X": solo si X forma parte de esa receta. Se quitan **todas** sus capas, incluso los dos niveles de lechuga o salsa del Big Mac. No se quitan panes ni el patty principal.
- "Ohne Zwiebeln": quita la cebolla fresca y sustituye cada `patty_beef_10_1` con cebolla incorporada por la variante gráfica `patty_beef_10_1_ohne_zwiebeln`. No deja cebolla escondida dentro del patty.
- "Extra X": solo para queso, pepinillos, tomate o bacon que ya formen parte de la receta. Aumenta en una unidad la cantidad de la primera capa correspondiente.
- "Extra Fleisch": solo si la receta contiene exactamente un patty apto de carne o pollo. Inserta un segundo patty junto al original. Las recetas dobles del folleto siguen existiendo como productos independientes.
- La marinada del McRib, la mantequilla del McMuffin y el vapor del pan Filet-o-Fish siguen siendo propiedades de preparación. El sorteo no los presenta como capas removibles.

## Para conectarlo a la interfaz

```js
import { generateOrder } from './src/order-generator.mjs';
const data = await fetch('./data/recipes.json').then(response => response.json());
const order = generateOrder(data.recipes);
// order.items: line, recipeId, ticketText, modifier, expectedLayers
```

La interfaz debe comparar la hamburguesa montada con `expectedLayers`, no con la receta base cuando haya modificación. Las cantidades en g o ml del recetario siguen siendo cantidades; el juego puede representarlas con un solo sprite más una etiqueta en lugar de exigir clics por cada gramo.

Pruebas: `node --test tests/order-generator.test.mjs`.
