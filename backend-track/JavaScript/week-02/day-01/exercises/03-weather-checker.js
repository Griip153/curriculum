// Exercise 3 — Weather checker (Option B of today's task — pick ONE of exercises 02-04)
//
// Fetch the current weather for a city's coordinates from Open-Meteo (free, no API
// key needed) and print a formatted summary — not the raw JSON.
//
// API: https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true
//
// Example output:
//   Weather in Douala:
//     Temperature : 27.4 C
//     Wind speed  : 11.2 km/h
//
// Hint: getWeather() below already builds the URL and handles the fetch/error half —
// you write the part that reads response.current_weather (fields: temperature,
// windspeed) and prints it.
// Run: node exercises/03-weather-checker.js

const CITY = "Douala";
const LATITUDE = 4.05;
const LONGITUDE = 9.7;

async function getWeather(latitude, longitude) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`);
    }

    const data = await response.json();
    return data.current_weather;
  } catch (error) {
    console.error(`Could not fetch weather for ${latitude}, ${longitude}:`, error.message);
    return null;
  }
}

async function printWeather(city, latitude, longitude) {
  // TODO: your code here
}

printWeather(CITY, LATITUDE, LONGITUDE);
