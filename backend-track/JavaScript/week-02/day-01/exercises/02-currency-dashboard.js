// Exercise 2 — Currency dashboard (Option A of today's task — pick ONE of exercises 02-04)
//
// Using getRate() below (same function from exercise 1), fetch the rate from one
// base currency to SEVERAL target currencies, and print a neatly formatted table —
// one aligned row per currency, not a raw object dump.
//
// Example output:
//   USD -> XAF : 605.23
//   USD -> EUR : 0.92
//   USD -> GBP : 0.79
//   USD -> NGN : 1520.11
//
// Hint: loop over TARGET_CURRENCIES with a for...of, await getRate() inside the loop
// (do NOT fire all the requests at once with .map() — keep it sequential and simple),
// and pad the currency code with .padEnd() so the colons line up. Skip any currency
// where getRate() returned null instead of crashing on it.
// Run: node exercises/02-currency-dashboard.js

const BASE_CURRENCY = "USD";
const TARGET_CURRENCIES = ["XAF", "EUR", "GBP", "NGN"];

async function getRate(base, target) {
  const url = `https://open.er-api.com/v6/latest/${base}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`);
    }

    const data = await response.json();
    return data.rates[target];
  } catch (error) {
    console.error(`Could not fetch rate ${base} -> ${target}:`, error.message);
    return null;
  }
}

async function printDashboard(base, targets) {
  // TODO: your code here
}

printDashboard(BASE_CURRENCY, TARGET_CURRENCIES);
