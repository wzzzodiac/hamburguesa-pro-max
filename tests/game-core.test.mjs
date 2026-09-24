import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { generateOrder, applyModification } from '../src/order-generator.mjs';
import { ingredientCatalog, checkProduct } from '../src/game-core.mjs';

const recipes = JSON.parse(readFileSync(new URL('../data/recipes.json', import.meta.url))).recipes;
const byId = id => recipes.find(recipe => recipe.id === id);
const copy = layers => layers.map(({ ingredient, quantity, unit, amountPerApplicationMl }) =>
  ({ ingredient, quantity, unit, ...(amountPerApplicationMl === undefined ? {} : { amountPerApplicationMl }) }));

test('catalog includes every recipe ingredient and the onion-free patty', () => {
  const catalog = ingredientCatalog(recipes);
  assert.equal(catalog.size, 52);
  assert.equal(catalog.get('patty_beef_10_1_ohne_zwiebeln'), 'piece');
});

test('normal and double products require every layer in sequence', () => {
  for (const id of ['hamburger', 'double_cheeseburger']) {
    const expected = byId(id).layers;
    assert.deepEqual(checkProduct(copy(expected), expected), []);
    const missing = copy(expected); missing.splice(1, 1);
    assert.ok(checkProduct(missing, expected).length > 0);
  }
});

test('modified products use their own expected layers, including every removed level', () => {
  const mac = byId('big_mac');
  const noSalad = applyModification(mac, { type: 'remove', target: 'eisbergsalat' });
  assert.deepEqual(checkProduct(copy(noSalad), noSalad), []);
  assert.ok(checkProduct(copy(mac.layers), noSalad).length > 0);
  const noOnions = applyModification(byId('double_cheeseburger'), { type: 'remove', target: 'onion' });
  assert.deepEqual(checkProduct(copy(noOnions), noOnions), []);
  assert.ok(checkProduct(copy(byId('double_cheeseburger').layers), noOnions).some(error => error.type === 'ingredient'));
});

test('repeated products are independent ticket lines and quantities or order are checked', () => {
  const order = generateOrder([byId('cheeseburger')], { random: () => 0 });
  assert.equal(order.items.length, 2);
  assert.notEqual(order.items[0].expectedLayers, order.items[1].expectedLayers);
  const expected = byId('cheeseburger').layers;
  const wrongAmount = copy(expected); wrongAmount[2].quantity += 1;
  assert.ok(checkProduct(wrongAmount, expected).some(error => error.type === 'quantity'));
  const wrongOrder = copy(expected); [wrongOrder[1], wrongOrder[2]] = [wrongOrder[2], wrongOrder[1]];
  assert.ok(checkProduct(wrongOrder, expected).some(error => error.type === 'ingredient'));
});

test('sauce applications require the exact milliliters per application', () => {
  const expected = byId('big_mac').layers;
  const correct = copy(expected);
  assert.deepEqual(checkProduct(correct, expected), []);
  const sauce = correct.find(layer => layer.unit === 'application');
  sauce.amountPerApplicationMl += 5;
  assert.ok(checkProduct(correct, expected).some(error => error.type === 'dose'));
});
