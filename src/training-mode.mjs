/** Build focused practice tickets without mutating the reference recipe or old attempt. */
export function practiceOrder(recipe) {
  return { items: [{
    line: 1,
    recipeId: recipe.id,
    productName: recipe.name,
    modifier: null,
    ticketText: recipe.name,
    expectedLayers: recipe.layers.map(layer => ({ ...layer })),
  }] };
}

/** Retry exactly the failed ticket lines, including their original modifications. */
export function retryOrder(order, lineStates) {
  return { items: order.items.flatMap((item, index) =>
    lineStates[index]?.result === 'incorrect'
      ? [{ ...item, line: 0, expectedLayers: item.expectedLayers.map(layer => ({ ...layer })) }]
      : []).map((item, index) => ({ ...item, line: index + 1 })) };
}
