import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { practiceOrder, retryOrder } from '../src/training-mode.mjs';

const recipes = JSON.parse(readFileSync(new URL('../data/recipes.json', import.meta.url))).recipes;

test('focused practice offers one original recipe with independent layers', () => {
  const recipe = recipes.find(item => item.id === 'big_mac');
  const order = practiceOrder(recipe);
  assert.equal(order.items.length, 1);
  assert.equal(order.items[0].recipeId, recipe.id);
  assert.deepEqual(order.items[0].expectedLayers, recipe.layers);
  order.items[0].expectedLayers[0].quantity++;
  assert.notEqual(order.items[0].expectedLayers[0].quantity, recipe.layers[0].quantity);
});

test('retry keeps failed variants and repetitions in ticket order', () => {
  const original = { items: [
    { line: 1, recipeId: 'a', modifier: null, expectedLayers: [{ ingredient: 'a', quantity: 1 }] },
    { line: 2, recipeId: 'b', modifier: { type: 'remove', target: 'onion' }, expectedLayers: [{ ingredient: 'b', quantity: 2 }] },
    { line: 3, recipeId: 'b', modifier: null, expectedLayers: [{ ingredient: 'b', quantity: 1 }] },
    { line: 4, recipeId: 'b', modifier: { type: 'remove', target: 'onion' }, expectedLayers: [{ ingredient: 'b', quantity: 2 }] },
  ] };
  const retry = retryOrder(original, [
    { result: 'correct' }, { result: 'incorrect' }, { result: 'correct' }, { result: 'incorrect' },
  ]);
  assert.deepEqual(retry.items.map(item => item.line), [1, 2]);
  assert.equal(retry.items[0].modifier.target, 'onion');
  assert.deepEqual(retry.items[0].expectedLayers, original.items[1].expectedLayers);
  retry.items[0].expectedLayers[0].quantity++;
  assert.equal(original.items[1].expectedLayers[0].quantity, 2);
  assert.equal(retryOrder(original, original.items.map(() => ({ result: 'correct' }))).items.length, 0);
});
