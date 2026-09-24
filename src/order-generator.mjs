/** Pure order generator. Pass data/recipes.json's `recipes` array as input. */

export const DEFAULT_ORDER_CONFIG = Object.freeze({
  orderSizeWeights: { 2: 35, 3: 35, 4: 20, 5: 10 },
  modifierProbability: 0.35,
  ensureMixedOrder: true,
  modifierTypeWeights: { remove: 70, extra: 25, extraPatty: 5 },
});

const removable = new Map([
  ['salzgurke', 'Gurken'], ['eisbergsalat', 'Salat'],
  ['tomate', 'Tomaten'], ['cheese_standard', 'Käse'],
  ['cheese_standard_half', 'Käse'], ['bacon_streifen', 'Bacon'],
  ['crispy_onions', 'Crispy Onions'], ['jalapenos', 'Jalapeños'],
  ['sauce_sandwich', 'Sandwichsauce'], ['sauce_breakfast', 'Breakfast-Sauce'],
  ['sauce_ketchup', 'Ketchup'], ['sauce_senf', 'Senf'],
  ['sauce_big_mac', 'Big-Mac-Sauce'], ['sauce_big_tasty', 'Big-Tasty-Sauce'],
  ['sauce_honig_senf', 'Honig-Senf-Sauce'], ['sauce_tartar', 'Tartarsauce'],
  ['sauce_sweet_chili', 'Sweet-Chili-Sauce'],
  ['sauce_hot_chili_cheese', 'Hot-Chili-Cheese-Sauce'],
]);

const extra = new Map([
  ['cheese_standard', 'Käse'], ['cheese_standard_half', 'Käse'],
  ['salzgurke', 'Gurken'], ['tomate', 'Tomaten'],
  ['bacon_streifen', 'Bacon'],
]);

const extraPattyTypes = new Set([
  'patty_beef_10_1', 'patty_beef_4_1', 'patty_beef_3_1',
  'patty_chicken_tempura', 'patty_chicken_classic', 'patty_mccrispy',
]);

function sampleWeighted(entries, random) {
  const weights = entries.filter(([, weight]) => Number.isFinite(weight) && weight > 0);
  if (!weights.length) throw new Error('No positive weights to sample');
  const total = weights.reduce((sum, [, weight]) => sum + weight, 0);
  let draw = random() * total;
  for (const [value, weight] of weights) {
    if (draw < weight) return value;
    draw -= weight;
  }
  return weights.at(-1)[0];
}

function pick(items, random) {
  if (!items.length) throw new Error('Cannot sample an empty list');
  return items[Math.min(items.length - 1, Math.floor(random() * items.length))];
}

/** Return valid *single* modifications for one existing recipe. */
export function availableModifiers(recipe) {
  const ingredients = new Set(recipe.layers.map(layer => layer.ingredient));
  const choices = { remove: [], extra: [], extraPatty: [] };
  const hasOnion = ingredients.has('zwiebeln_frisch_weiss') || ingredients.has('patty_beef_10_1');
  if (hasOnion) choices.remove.push({ type: 'remove', target: 'onion', label: 'Ohne Zwiebeln' });
  const seenLabels = new Set();
  for (const [target, display] of removable) {
    if (ingredients.has(target) && !seenLabels.has(display)) {
      choices.remove.push({ type: 'remove', target, label: `Ohne ${display}` });
      seenLabels.add(display);
    }
  }
  const seenExtras = new Set();
  for (const [target, display] of extra) {
    if (ingredients.has(target) && !seenExtras.has(display)) {
      choices.extra.push({ type: 'extra', target, label: `Extra ${display}` });
      seenExtras.add(display);
    }
  }
  const patties = recipe.layers.filter(layer => layer.ingredient.startsWith('patty_'));
  if (patties.length === 1 && patties[0].quantity === 1 && extraPattyTypes.has(patties[0].ingredient)) {
    choices.extraPatty.push({ type: 'extraPatty', target: patties[0].ingredient,
      label: 'Extra Fleisch' });
  }
  return choices;
}

/** Apply a choice without ever changing the authoritative base recipe. */
export function applyModification(recipe, modifier) {
  const valid = availableModifiers(recipe)[modifier.type]?.some(choice =>
    choice.target === modifier.target);
  if (!valid) throw new Error(`Invalid modification for ${recipe.id}: ${modifier.type}/${modifier.target}`);
  const layers = recipe.layers.map(layer => ({ ...layer }));
  if (modifier.type === 'remove' && modifier.target === 'onion') {
    return layers.filter(layer => layer.ingredient !== 'zwiebeln_frisch_weiss').map(layer =>
      layer.ingredient === 'patty_beef_10_1'
        ? { ...layer, ingredient: 'patty_beef_10_1_ohne_zwiebeln' } : layer);
  }
  if (modifier.type === 'remove') {
    // A ticket saying "ohne X" removes X from every level of a burger.
    const alsoRemove = modifier.target.startsWith('cheese_standard')
      ? new Set(['cheese_standard', 'cheese_standard_half']) : new Set([modifier.target]);
    return layers.filter(layer => !alsoRemove.has(layer.ingredient));
  }
  const index = layers.findIndex(layer => layer.ingredient === modifier.target);
  if (modifier.type === 'extra') {
    layers[index].quantity += 1;
    return layers;
  }
  if (modifier.type === 'extraPatty') {
    layers.splice(index + 1, 0, { ...layers[index], quantity: 1, customExtra: true });
    return layers;
  }
  throw new Error(`Unknown modifier type: ${modifier.type}`);
}

/** Default pool is burgers. Pass categories to include breakfast or wraps. */
export function generateOrder(recipes, {
  random = Math.random,
  categories = ['burger'],
  config = DEFAULT_ORDER_CONFIG,
} = {}) {
  const pool = recipes.filter(recipe => categories.includes(recipe.category));
  if (!pool.length) throw new Error('No recipes in selected categories');
  const count = Number(sampleWeighted(Object.entries(config.orderSizeWeights), random));
  if (!Number.isInteger(count) || count < 1) throw new Error('Invalid order size');
  if (config.ensureMixedOrder && count < 2) throw new Error('Mixed orders need at least two items');
  const selected = Array.from({ length: count }, () => pick(pool, random));
  const modified = selected.map(recipe =>
    Object.values(availableModifiers(recipe)).some(items => items.length) &&
    random() < config.modifierProbability);
  if (config.ensureMixedOrder) {
    const eligible = selected.flatMap((recipe, index) =>
      Object.values(availableModifiers(recipe)).some(items => items.length) ? [index] : []);
    if (!eligible.length) throw new Error('Selected recipes have no valid modifications');
    if (!modified.some(Boolean)) modified[pick(eligible, random)] = true;
    if (modified.every(Boolean)) modified[pick(selected.map((_, i) => i), random)] = false;
  }
  return {
    items: selected.map((recipe, index) => {
      const choices = availableModifiers(recipe);
      const families = Object.entries(choices)
        .filter(([, items]) => items.length)
        .map(([type]) => [type, config.modifierTypeWeights[type] ?? 0]);
      const modifier = modified[index]
        ? pick(choices[sampleWeighted(families, random)], random) : null;
      return {
        line: index + 1,
        recipeId: recipe.id,
        productName: recipe.name,
        modifier,
        ticketText: modifier ? `${recipe.name} - ${modifier.label}` : recipe.name,
        expectedLayers: modifier ? applyModification(recipe, modifier)
          : recipe.layers.map(layer => ({ ...layer })),
      };
    }),
  };
}
