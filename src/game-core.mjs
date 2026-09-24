/** Rules shared by the browser and focused tests. Recipe data stays authoritative. */
export function ingredientCatalog(recipes) {
  const catalog = new Map();
  for (const recipe of recipes) {
    for (const layer of recipe.layers) {
      if (!catalog.has(layer.ingredient)) catalog.set(layer.ingredient, layer.unit);
    }
  }
  // The onion-free patty is a selectable graphic for modified orders.
  catalog.set('patty_beef_10_1_ohne_zwiebeln', 'piece');
  return catalog;
}

export function checkProduct(actual, expected) {
  const errors = [];
  const count = Math.max(actual.length, expected.length);
  for (let index = 0; index < count; index++) {
    const placed = actual[index];
    const wanted = expected[index];
    if (!wanted) errors.push({ type: 'extra', index, placed });
    else if (!placed) errors.push({ type: 'missing', index, wanted });
    else if (placed.ingredient !== wanted.ingredient) {
      errors.push({ type: 'ingredient', index, placed, wanted });
    } else if (placed.unit !== wanted.unit || Number(placed.quantity) !== wanted.quantity) {
      errors.push({ type: 'quantity', index, placed, wanted });
    }
  }
  return errors;
}
