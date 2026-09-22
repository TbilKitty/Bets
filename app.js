const DATA_FILE = "data/daily_game_inputs.csv";

function parseCsv(text) {
  const rows = text.trim().split(/\r?\n/).map(row => row.split(","));
  const headers = rows.shift();
  return rows.filter(row => row.length === headers.length && row.some(Boolean)).map(row =>
    Object.fromEntries(headers.map((header, index) => [header, row[index].trim()]))
  );
}

function number(value) { return Number.parseFloat(value) || 0; }

function weights() {
  return {
    availability: number(document.querySelector("#availability-weight").value),
    rest: number(document.querySelector("#rest-weight").value),
    travel: number(document.querySelector("#travel-weight").value),
    rating: number(document.querySelector("#rating-weight").value),
  };
}

function score(game) {
  const w = weights();
  return (number(game.availability_edge) * w.availability) +
    (number(game.rest_edge) * w.rest) +
    (number(game.travel_edge) * w.travel) +
    (number(game.net_rating_edge) * w.rating);
}

function trackerProbability(game) {
  if (game.market_implied_home_win_prob === "") return null;
  return Math.max(0.02, Math.min(0.98, number(game.market_implied_home_win_prob) + score(game) / 100));
}

function formatFactor(value) { return `${number(value) >= 0 ? "+" : ""}${number(value).toFixed(1)}`; }

function render(games) {
  const rows = games.map(game => {
    const signal = score(game);
    const marketAvailable = game.market_implied_home_win_prob !== "";
    const tracker = trackerProbability(game);
    const watch = Math.abs(signal) >= 2.5;
    const availability = game.availability_note || "No material item logged";
    const sourceClass = game.news_confirmed === "yes" ? "confirm" : "unconfirmed";
    return `<tr>
      <td><strong>${game.away_team}</strong> @ <strong>${game.home_team}</strong><br><small>${game.game_date}</small></td>
      <td>${game.start_time_et}</td>
      <td>${marketAvailable ? `${(number(game.market_implied_home_win_prob) * 100).toFixed(0)}%` : "—"}</td>
      <td>${tracker === null ? "—" : `${(tracker * 100).toFixed(0)}%`}</td>
      <td>${availability}</td>
      <td>${formatFactor(game.rest_edge)}</td>
      <td>${formatFactor(game.travel_edge)}</td>
      <td>${formatFactor(game.net_rating_edge)}</td>
      <td><span class="tag ${watch ? "watch" : "neutral"}">${watch ? `Watch ${formatFactor(signal)}` : "No signal"}</span></td>
      <td class="${sourceClass}">${game.news_confirmed === "yes" ? "Confirmed" : "Verify"}</td>
    </tr>`;
  }).join("");
  document.querySelector("#slate-body").innerHTML = rows || "<tr><td colspan='10'>No games in the daily file.</td></tr>";
  document.querySelector("#game-count").textContent = games.length;
  document.querySelector("#watch-count").textContent = games.filter(game => Math.abs(score(game)) >= 2.5).length;
  document.querySelector("#absence-count").textContent = games.filter(game => game.news_confirmed === "yes" && number(game.availability_edge) !== 0).length;
}

async function load() {
  try {
    const response = await fetch(`${DATA_FILE}?v=${Date.now()}`);
    if (!response.ok) throw new Error("Daily CSV could not be loaded");
    const games = parseCsv(await response.text());
    render(games);
    document.querySelector("#data-status").textContent = `Loaded ${games[0]?.game_date || "daily"} slate`;
    document.querySelector("#recalculate").addEventListener("click", () => render(games));
  } catch (error) {
    document.querySelector("#data-status").textContent = error.message;
    document.querySelector("#slate-body").innerHTML = "<tr><td colspan='10'>Add data/daily_game_inputs.csv, then refresh.</td></tr>";
  }
}
load();
