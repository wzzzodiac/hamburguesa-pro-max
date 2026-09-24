import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { availableModifiers, applyModification, generateOrder, DEFAULT_ORDER_CONFIG } from '../src/order-generator.mjs';

const recipes = JSON.parse(readFileSync(new URL('../data/recipes.json', import.meta.url))).recipes;
const byId = id => recipes.find(recipe => recipe.id === id);
function seededRandom(seed) {
  let state = seed >>> 0;
  return () => ((state = (1664525 * state + 1013904223) >>> 0) / 2 ** 32);
}

test('random orders have 2-5 burgers and mix ordinary and changed products', () => {
  const random = seededRandom(2026);
  for (let i = 0; i < 500; i++) {
    const order = generateOrder(recipes, { random });
    assert.ok(order.items.length >= 2 && order.items.length <= 5);
    assert.ok(order.items.some(item => item.modifier));
    assert.ok(order.items.some(item => !item.modifier));
    for (const item of order.items) {
      assert.equal(byId(item.recipeId).category, 'burger');
      for (const layer of item.expectedLayers) {
        assert.ok(existsSync(new URL(`../assets/ingredients/${layer.ingredient}.png`, import.meta.url)));
      }
    }
  }
});

test('without onions handles pre-onioned beef and fresh onions without touching original data', () => {
  const burger = byId('double_cheeseburger');
  const original = JSON.stringify(burger.layers);
  const changed = applyModification(burger, { type: 'remove', target: 'onion' });
  assert.equal(changed.filter(layer => layer.ingredient === 'patty_beef_10_1_ohne_zwiebeln').length, 2);
  assert.equal(JSON.stringify(burger.layers), original);
  const royal = applyModification(byId('hamburger_royal_cheese'), { type: 'remove', target: 'onion' });
  assert.ok(!royal.some(layer => layer.ingredient === 'zwiebeln_frisch_weiss'));
});

test('omission removes every matching level; extra patty is only offered on single-patty recipes', () => {
  const mac = byId('big_mac');
  const noLettuce = applyModification(mac, { type: 'remove', target: 'eisbergsalat' });
  assert.equal(noLettuce.filter(layer => layer.ingredient === 'eisbergsalat').length, 0);
  assert.equal(mac.layers.filter(layer => layer.ingredient === 'eisbergsalat').length, 2);
  assert.equal(availableModifiers(byId('double_cheeseburger')).extraPatty.length, 0);
  const extra = applyModification(byId('cheeseburger'), {
    type: 'extraPatty', target: 'patty_beef_10_1',
  });
  assert.equal(extra.filter(layer => layer.ingredient === 'patty_beef_10_1').length, 2);
  assert.throws(() => applyModification(byId('hamburger'), {
    type: 'remove', target: 'eisbergsalat',
  }), /Invalid modification/);
});

test('size and modifier draws follow configured weights before mixed-order adjustment', () => {
  const random = seededRandom(861);
  const sizes = new Map([[2,0],[3,0],[4,0],[5,0]]);
  let modified = 0, total = 0;
  const config = { ...DEFAULT_ORDER_CONFIG, ensureMixedOrder: false };
  for (let i = 0; i < 3000; i++) {
    const order = generateOrder(recipes, { random, config });
    sizes.set(order.items.length, sizes.get(order.items.length) + 1);
    for (const item of order.items) { total++; if (item.modifier) modified++; }
  }
  for (const [size, expected] of [[2,.35],[3,.35],[4,.20],[5,.10]]) {
    assert.ok(Math.abs(sizes.get(size)/3000 - expected) < .04);
  }
  assert.ok(Math.abs(modified/total - .35) < .035);
});

test('every offered customization resolves to available graphic assets', () => {
  for (const recipe of recipes) {
    for (const choices of Object.values(availableModifiers(recipe))) {
      for (const choice of choices) {
        const changed = applyModification(recipe, choice);
        assert.ok(changed.length > 0);
        for (const layer of changed) {
          assert.ok(existsSync(new URL(`../assets/ingredients/${layer.ingredient}.png`, import.meta.url)),
            `${recipe.id}: ${choice.label} needs ${layer.ingredient}`);
        }
      }
    }
  }
});
