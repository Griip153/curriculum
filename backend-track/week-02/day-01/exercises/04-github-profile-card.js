// Exercise 4 — GitHub profile card (Option C of today's task — pick ONE of exercises 02-04)
//
// Fetch a GitHub user's public profile and print a formatted card. This one
// deliberately tests the response.ok gotcha from LESSON.md section 6: a made-up
// username does NOT fail the network call — GitHub answers with a normal 404, and
// your code has to notice that itself instead of crashing on undefined fields.
//
// API: https://api.github.com/users/<username>
//
// Example output (real username):
//   The Octocat (@octocat)
//   Bio          : (none)
//   Followers    : 18000
//   Public repos : 8
//
// Example output (username that doesn't exist):
//   No GitHub user found with the username "this-user-does-not-exist-12345"
//
// Hint: getGithubUser() below does the fetch and already handles the 404 case for
// you (same pattern as getRate()/getWeather() above, just checking response.status
// instead of only response.ok). You write the part that prints the fields.
// Run: node exercises/04-github-profile-card.js

const USERNAME = "octocat";

async function getGithubUser(username) {
  const url = `https://api.github.com/users/${username}`;

  try {
    const response = await fetch(url);

    if (response.status === 404) {
      console.log(`No GitHub user found with the username "${username}"`);
      return null;
    }

    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Could not fetch GitHub user "${username}":`, error.message);
    return null;
  }
}

async function printProfileCard(username) {
  // TODO: your code here
}

printProfileCard(USERNAME);
