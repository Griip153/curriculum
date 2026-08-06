// Exercise 1 — Get exchange rate (SOLVED — worked together in the session, see LESSON.md)
//
// getRate(base, target) fetches live exchange rates from a free public API and
// returns the numeric rate from `base` to `target`, or null (with a logged message)
// if the request fails — network failure or a non-OK HTTP status.
//
// Run: node exercises/01-get-rate.js

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

async function main() {
  const rate = await getRate("USD", "XAF");

  if (rate !== null) {
    console.log(`1 USD = ${rate} XAF`);
  }
}

main();
