import { generateOrder } from './order-generator.mjs';
import { ingredientCatalog, checkProduct } from './game-core.mjs';
import { practiceOrder, retryOrder } from './training-mode.mjs';

const $ = selector => document.querySelector(selector);
const imageUrl = id => new URL(`../assets/ingredients/${id}.png`, import.meta.url).href;
const categoryNames = { burger: 'Burger', breakfast: 'Frühstück', wrap: 'Wraps' };
const categoryPools = { burger: ['burger'], breakfast: ['breakfast', 'breakfast_wrap'], wrap: ['wrap', 'breakfast_wrap'] };
const groupNames = { bread: 'Brot & Wrap', protein: 'Fleisch & Ei', cheese: 'Käse', vegetable: 'Gemüse & Extras', sauce: 'Saucen' };
const names = {
  bacon_streifen: 'Bacon', cheese_standard: 'Käse', cheese_standard_half: 'Halbe Käsescheibe',
  crispy_onions: 'Röstzwiebeln', eisbergsalat: 'Eisbergsalat', jalapenos: 'Jalapeños',
  round_egg: 'Rundes Ei', ruehrei: 'Rührei', salzgurke: 'Salzgurke', tomate: 'Tomate',
  wrap_tortilla: 'Tortilla', zwiebeln_frisch_weiss: 'Weiße Zwiebeln',
  patty_beef_10_1: 'Rindfleisch 10:1 mit Zwiebeln',
  patty_beef_10_1_ohne_zwiebeln: 'Rindfleisch 10:1 ohne Zwiebeln',
  patty_beef_4_1: 'Rindfleisch 4:1', patty_beef_3_1: 'Rindfleisch 3:1',
  patty_chicken_classic: 'Chicken Classic', patty_chicken_classic_half: 'Halbes Chicken Classic',
  patty_chicken_tempura: 'Chicken Tempura', patty_filet_o_fish: 'Fischfilet',
  patty_mccrispy: 'McCrispy Patty', patty_pork_mcrib: 'McRib Patty',
  patty_sausage: 'Sausage Patty', patty_veggie: 'Veggie Patty', patty_veggie_half: 'Halbes Veggie Patty',
};
const breadNames = { big_mac: 'Big Mac', big_tasty: 'Big Tasty', hamburger: 'Hamburger',
  hamburger_royal: 'Royal', koernerbroetchen: 'Körnerbrötchen', mccrispy: 'McCrispy',
  mcmuffin: 'McMuffin', mcrib: 'McRib' };
const sauceNames = { big_mac: 'Big-Mac-Sauce', big_tasty: 'Big-Tasty-Sauce', breakfast: 'Breakfast-Sauce',
  honig_senf: 'Honig-Senf-Sauce', hot_chili_cheese: 'Hot-Chili-Cheese-Sauce', ketchup: 'Ketchup',
  sandwich: 'Sandwichsauce', senf: 'Senf', sweet_chili: 'Sweet-Chili-Sauce', tartar: 'Tartarsauce' };
function ingredientName(id) {
  if (names[id]) return names[id];
  if (id.startsWith('sauce_')) return sauceNames[id.slice(6)] ?? id;
  if (id.startsWith('bun_')) {
    const part = id.endsWith('_oberteil') ? 'Oberteil' : id.endsWith('_unterteil') ? 'Unterteil' : 'Mittelteil';
    const type = id.slice(4).replace(/_(oberteil|unterteil|mittelteil)$/, '');
    return `${breadNames[type] ?? type} ${part}`;
  }
  return id.replaceAll('_', ' ');
}
function groupOf(id) {
  if (id.startsWith('bun_') || id === 'wrap_tortilla') return 'bread';
  if (id.startsWith('patty_') || id === 'round_egg' || id === 'ruehrei' || id === 'bacon_streifen') return 'protein';
  if (id.startsWith('cheese_')) return 'cheese';
  if (id.startsWith('sauce_')) return 'sauce';
  return 'vegetable';
}
const unitNames = { piece: 'Stück', slice: 'Scheiben', half_slice: 'halbe Scheiben',
  strip: 'Streifen', g: 'g', application: 'Aufträge', portion: 'Portionen', half_patty: 'halbe Patties' };
const singularUnits = { slice: 'Scheibe', half_slice: 'halbe Scheibe', application: 'Auftrag', portion: 'Portion', half_patty: 'halbes Patty' };
const quantityText = (quantity, unit) => `${new Intl.NumberFormat('de-DE', { maximumFractionDigits: 2 }).format(quantity)} ${quantity === 1 ? singularUnits[unit] ?? unitNames[unit] : unitNames[unit]}`;

let recipes = [];
let catalog = new Map();
let order = null;
let lineStates = [];
let currentLine = 0;
let currentCategory = 'burger';
let currentMode = 'order';
let currentRecipeId = null;
let currentGroup = 'bread';
let selectedIngredient = null;
let lastErrors = null;

function showScreen(id) {
  for (const screen of ['start-screen', 'game-screen', 'summary-screen']) {
    $(`#${screen}`).classList.toggle('hidden', screen !== id);
  }
}

function renderTicket() {
  const list = $('#ticket-list');
  list.replaceChildren();
  order.items.forEach((item, index) => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `ticket-line${index === currentLine ? ' active' : ''}`;
    button.disabled = lineStates[index].result !== null;
    button.setAttribute('aria-current', index === currentLine ? 'step' : 'false');
    const number = document.createElement('span'); number.className = 'ticket-number'; number.textContent = String(index + 1).padStart(2, '0');
    const text = document.createElement('span'); text.className = 'ticket-text';
    const title = document.createElement('strong'); title.textContent = item.productName;
    const detail = document.createElement('span'); detail.textContent = item.modifier?.label ?? 'Ohne Änderung';
    text.append(title, detail);
    const status = document.createElement('span'); status.className = `ticket-status ${lineStates[index].result ?? ''}`;
    status.textContent = lineStates[index].result === 'correct' ? '✓' : lineStates[index].result === 'incorrect' ? '!' : '→';
    button.append(number, text, status);
    button.addEventListener('click', () => selectLine(index));
    li.append(button); list.append(li);
  });
  const done = lineStates.filter(state => state.result !== null).length;
  $('#ticket-progress').textContent = `${done} von ${order.items.length} Produkten abgegeben`;
}

function renderStack() {
  const stack = $('#stack'); stack.replaceChildren();
  const layers = lineStates[currentLine].layers;
  for (const layer of layers) {
    const band = document.createElement('div'); band.className = 'stack-layer';
    const img = document.createElement('img'); img.src = imageUrl(layer.ingredient); img.alt = '';
    const badge = document.createElement('span'); badge.className = 'stack-quantity'; badge.textContent = `${quantityText(layer.quantity, layer.unit)}${layer.unit === 'application' ? ` × ${layer.amountPerApplicationMl} ml` : ''}`;
    band.append(img, badge); stack.append(band);
  }
  $('#empty-stack').classList.toggle('hidden', layers.length > 0);
  $('#layer-count').textContent = `${layers.length} ${layers.length === 1 ? 'Schicht' : 'Schichten'}`;
  $('#undo-button').disabled = !layers.length;
  $('#reset-button').disabled = !layers.length;
}

function renderGroupTabs() {
  const tabs = $('#group-tabs'); tabs.replaceChildren();
  for (const [key, label] of Object.entries(groupNames)) {
    const button = document.createElement('button'); button.type = 'button';
    button.textContent = label; button.className = key === currentGroup ? 'active' : '';
    button.setAttribute('aria-pressed', String(key === currentGroup));
    button.addEventListener('click', () => { currentGroup = key; renderGroupTabs(); renderIngredients(); });
    tabs.append(button);
  }
}

function renderIngredients() {
  const grid = $('#ingredient-grid'); grid.replaceChildren();
  for (const [id] of catalog) {
    if (groupOf(id) !== currentGroup) continue;
    const button = document.createElement('button'); button.type = 'button';
    button.className = `ingredient-card${id === selectedIngredient ? ' selected' : ''}`;
    button.setAttribute('aria-pressed', String(id === selectedIngredient));
    const img = document.createElement('img'); img.src = imageUrl(id); img.alt = '';
    const name = document.createElement('span'); name.textContent = ingredientName(id);
    button.append(img, name);
    button.addEventListener('click', () => selectIngredient(id));
    grid.append(button);
  }
}

function selectIngredient(id) {
  selectedIngredient = id;
  const unit = catalog.get(id);
  $('#selected-image').src = imageUrl(id);
  $('#selected-name').textContent = ingredientName(id);
  $('#selected-unit').textContent = unit === 'g' ? 'Gewicht eingeben' : `Einheit: ${unitNames[unit]}`;
  $('#quantity-suffix').textContent = unitNames[unit];
  const input = $('#quantity-input');
  input.value = unit === 'g' ? '' : '1';
  input.min = unit === 'g' ? '0.01' : '1';
  input.step = unit === 'g' ? 'any' : '1';
  input.placeholder = unit === 'g' ? 'z. B. 12,5' : '1';
  $('#quantity-error').textContent = '';
  $('#dose-panel').classList.toggle('hidden', unit !== 'application');
  $('#dose-input').value = '';
  $('#quantity-panel').classList.remove('hidden');
  renderIngredients();
  $('#quantity-panel').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function changeQuantity(direction) {
  if (!selectedIngredient) return;
  const input = $('#quantity-input');
  const step = catalog.get(selectedIngredient) === 'g' ? 1 : 1;
  input.value = String(Math.max(step, (Number(input.value) || 0) + direction * step));
}

function addLayer() {
  if (!selectedIngredient || lineStates[currentLine].result !== null) return;
  const unit = catalog.get(selectedIngredient);
  const input = $('#quantity-input');
  const quantity = Number(input.value);
  if (!Number.isFinite(quantity) || quantity <= 0 || (unit !== 'g' && !Number.isInteger(quantity))) {
    $('#quantity-error').textContent = unit === 'g' ? 'Bitte eine Grammzahl über 0 eingeben.' : 'Bitte eine ganze Menge über 0 eingeben.';
    input.focus(); return;
  }
  const amountPerApplicationMl = Number($('#dose-input').value);
  if (unit === 'application' && !amountPerApplicationMl) {
    $('#quantity-error').textContent = 'Bitte die Milliliter pro Auftrag wählen.';
    $('#dose-input').focus(); return;
  }
  lineStates[currentLine].layers.push({ ingredient: selectedIngredient, quantity, unit,
    ...(unit === 'application' ? { amountPerApplicationMl } : {}) });
  lastErrors = null; $('#feedback').classList.add('hidden');
  renderStack();
  $('#quantity-error').textContent = '';
}

function selectLine(index) {
  if (lineStates[index].result !== null) return;
  currentLine = index;
  selectedIngredient = null;
  lastErrors = null;
  $('#quantity-panel').classList.add('hidden');
  $('#feedback').classList.add('hidden');
  $('#submit-button').disabled = false;
  $('#add-button').disabled = false;
  const item = order.items[index];
  $('#product-title').textContent = item.productName;
  $('#product-subtitle').textContent = item.modifier?.label ?? 'Ohne Änderung';
  renderTicket(); renderStack(); renderIngredients();
}

function errorText(error) {
  const level = `Schicht ${error.index + 1}`;
  if (error.type === 'missing') return `${level} fehlt: ${ingredientName(error.wanted.ingredient)} (${quantityText(error.wanted.quantity, error.wanted.unit)}).`;
  if (error.type === 'extra') return `${level} ist zu viel: ${ingredientName(error.placed.ingredient)}.`;
  if (error.type === 'ingredient') return `${level}: Hier gehört ${ingredientName(error.wanted.ingredient)} hin, statt ${ingredientName(error.placed.ingredient)}. Prüfe auch die Reihenfolge.`;
  if (error.type === 'dose') return `${level}: ${ingredientName(error.wanted.ingredient)} braucht ${error.wanted.amountPerApplicationMl} ml pro Auftrag; gewählt sind ${error.placed.amountPerApplicationMl} ml.`;
  return `${level}: ${ingredientName(error.wanted.ingredient)} braucht ${quantityText(error.wanted.quantity, error.wanted.unit)}; gelegt sind ${quantityText(error.placed.quantity, error.placed.unit)}.`;
}

function renderComparison(placed, expected, errors) {
  const comparison = document.createElement('div'); comparison.className = 'recipe-comparison';
  const heading = document.createElement('h4'); heading.textContent = 'Aufbau vergleichen · von unten nach oben';
  comparison.append(heading);
  const columns = document.createElement('div'); columns.className = 'comparison-columns';
  const wrongIndexes = new Set(errors.map(error => error.index));
  for (const [title, layers] of [['Dein Aufbau', placed], ['Richtiger Aufbau', expected]]) {
    const column = document.createElement('div'); column.className = 'comparison-column';
    const label = document.createElement('h5'); label.textContent = title; column.append(label);
    if (!layers.length) {
      const empty = document.createElement('p'); empty.textContent = 'Keine Zutaten aufgelegt.'; column.append(empty);
    } else {
      const list = document.createElement('ol');
      layers.forEach((layer, index) => {
        const row = document.createElement('li');
        if (wrongIndexes.has(index)) row.classList.add('mismatch');
        const img = document.createElement('img'); img.src = imageUrl(layer.ingredient); img.alt = '';
        const detail = document.createElement('span');
        detail.textContent = `${ingredientName(layer.ingredient)} · ${quantityText(layer.quantity, layer.unit)}${layer.unit === 'application' ? ` × ${layer.amountPerApplicationMl} ml` : ''}`;
        row.append(img, detail); list.append(row);
      });
      column.append(list);
    }
    columns.append(column);
  }
  comparison.append(columns);
  return comparison;
}

function submitProduct() {
  const state = lineStates[currentLine];
  state.attempts++;
  lastErrors = checkProduct(state.layers, order.items[currentLine].expectedLayers);
  const feedback = $('#feedback'); feedback.replaceChildren(); feedback.classList.remove('hidden');
  const title = document.createElement('h3');
  title.textContent = lastErrors.length ? `${lastErrors.length} ${lastErrors.length === 1 ? 'Fehler' : 'Fehler'} gefunden` : 'Alles richtig aufgebaut!';
  feedback.append(title);
  if (lastErrors.length) {
    const list = document.createElement('ol');
    for (const error of lastErrors) { const li = document.createElement('li'); li.textContent = errorText(error); list.append(li); }
    feedback.append(list);
  } else {
    const p = document.createElement('p'); p.textContent = 'Zutaten, Mengen und Reihenfolge stimmen.'; feedback.append(p);
  }
  const actions = document.createElement('div'); actions.className = 'feedback-actions';
  if (lastErrors.length) {
    const correct = document.createElement('button'); correct.type = 'button'; correct.className = 'button secondary'; correct.textContent = 'Korrigieren';
    correct.addEventListener('click', () => { feedback.classList.add('hidden'); }); actions.append(correct);
  }
  const next = document.createElement('button'); next.type = 'button'; next.className = 'button dark';
  next.textContent = lastErrors.length ? 'Abgeben & Aufbau vergleichen'
    : lineStates.filter((entry, i) => i !== currentLine && entry.result === null).length ? 'Weiter zum nächsten Produkt' : 'Zusammenfassung ansehen';
  next.addEventListener('click', finishLine); actions.append(next); feedback.append(actions);
  feedback.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function finishLine() {
  const state = lineStates[currentLine];
  if (state.result !== null || !lastErrors) return;
  state.result = lastErrors.length ? 'incorrect' : 'correct';
  if (lastErrors.length) {
    const feedback = $('#feedback');
    feedback.append(renderComparison(state.layers, order.items[currentLine].expectedLayers, lastErrors));
    feedback.querySelector('.feedback-actions').replaceChildren();
    const next = document.createElement('button'); next.type = 'button'; next.className = 'button dark';
    next.textContent = lineStates.some(entry => entry.result === null) ? 'Weiter zum nächsten Produkt' : 'Zusammenfassung ansehen';
    next.addEventListener('click', advanceLine);
    feedback.querySelector('.feedback-actions').append(next);
    $('#submit-button').disabled = true;
    $('#add-button').disabled = true;
    $('#undo-button').disabled = true;
    $('#reset-button').disabled = true;
    renderTicket();
    feedback.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    return;
  }
  advanceLine();
}

function advanceLine() {
  const next = lineStates.findIndex(state => state.result === null);
  if (next >= 0) selectLine(next);
  else showSummary();
}

function showSummary() {
  showScreen('summary-screen');
  const right = lineStates.filter(state => state.result === 'correct').length;
  $('#summary-intro').textContent = `${right} von ${order.items.length} Produkten richtig aufgebaut.`;
  const list = $('#summary-list'); list.replaceChildren();
  order.items.forEach((item, index) => {
    const li = document.createElement('li');
    const title = document.createElement('strong'); title.textContent = `${index + 1}. ${item.ticketText}`;
    const status = document.createElement('span');
    status.textContent = `${lineStates[index].result === 'correct' ? 'Richtig' : 'Mit Fehlern abgegeben'} · ${lineStates[index].attempts} ${lineStates[index].attempts === 1 ? 'Versuch' : 'Versuche'}`;
    li.append(title, status); list.append(li);
  });
  $('#retry-button').classList.toggle('hidden', !lineStates.some(state => state.result === 'incorrect'));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function startSession(nextOrder, category, mode, recipeId = null) {
  currentCategory = category;
  currentMode = mode;
  currentRecipeId = recipeId;
  order = nextOrder;
  lineStates = order.items.map(() => ({ layers: [], result: null, attempts: 0 }));
  currentGroup = 'bread'; selectedIngredient = null;
  $('#game-title').textContent = mode === 'single' ? 'Einzelübung' : mode === 'retry' ? 'Fehler erneut üben' : `${categoryNames[category]}-Bestellung`;
  $('#new-order-button').textContent = mode === 'single' ? 'Produkt neu üben' : 'Neue Bestellung';
  renderGroupTabs(); showScreen('game-screen'); selectLine(0);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function startOrder(category, mode, recipeId) {
  const selected = recipes.find(recipe => recipe.id === recipeId && categoryPools[category].includes(recipe.category));
  if (mode === 'single' && !selected) return;
  startSession(mode === 'single' ? practiceOrder(selected)
    : generateOrder(recipes, { categories: categoryPools[category] }), category, mode, selected?.id ?? null);
}

function populateRecipePicker() {
  const category = $('input[name="category"]:checked').value;
  const select = $('#recipe-select');
  const previous = select.value;
  select.replaceChildren();
  recipes.filter(recipe => categoryPools[category].includes(recipe.category))
    .sort((a, b) => a.name.localeCompare(b.name, 'de'))
    .forEach(recipe => {
      const option = document.createElement('option'); option.value = recipe.id; option.textContent = recipe.name;
      select.append(option);
    });
  if ([...select.options].some(option => option.value === previous)) select.value = previous;
}

async function init() {
  try {
    const response = await fetch(new URL('../data/recipes.json', import.meta.url));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    recipes = (await response.json()).recipes;
    catalog = ingredientCatalog(recipes);
  } catch (error) {
    $('#start-button').disabled = true;
    $('.small-note').textContent = `Die Rezeptdaten konnten nicht geladen werden (${error.message}). Bitte die Seite neu laden.`;
    return;
  }
  populateRecipePicker();
  document.querySelectorAll('input[name="category"]').forEach(input => input.addEventListener('change', populateRecipePicker));
  document.querySelectorAll('input[name="practice-mode"]').forEach(input => input.addEventListener('change', () => {
    $('#recipe-picker').classList.toggle('hidden', $('input[name="practice-mode"]:checked').value !== 'single');
    $('#start-button').firstChild.textContent = input.value === 'single' ? 'Produkt üben ' : 'Bestellung starten ';
  }));
  $('#start-button').addEventListener('click', () => startOrder($('input[name="category"]:checked').value,
    $('input[name="practice-mode"]:checked').value, $('#recipe-select').value));
  $('#new-order-button').addEventListener('click', () => startOrder(currentCategory, currentMode === 'retry' ? 'order' : currentMode, currentRecipeId));
  $('#summary-new-button').addEventListener('click', () => startOrder(currentCategory, currentMode === 'retry' ? 'order' : currentMode, currentRecipeId));
  $('#retry-button').addEventListener('click', () => {
    const next = retryOrder(order, lineStates);
    if (next.items.length) startSession(next, currentCategory, 'retry');
  });
  $('#undo-button').addEventListener('click', () => { lineStates[currentLine].layers.pop(); $('#feedback').classList.add('hidden'); renderStack(); });
  $('#reset-button').addEventListener('click', () => { lineStates[currentLine].layers = []; $('#feedback').classList.add('hidden'); renderStack(); });
  $('#quantity-minus').addEventListener('click', () => changeQuantity(-1));
  $('#quantity-plus').addEventListener('click', () => changeQuantity(1));
  $('#add-button').addEventListener('click', addLayer);
  $('#submit-button').addEventListener('click', submitProduct);
}
init();
