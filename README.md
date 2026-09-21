# Game Edge Tracker

An NBA-first, GitHub Pages dashboard for organizing daily game information and testing whether signals add predictive value beyond the betting market.

## What it does

- Displays the current slate from `data/daily_game_inputs.csv`.
- Calculates a transparent, editable signal score from injuries, rest, travel, and team-strength inputs.
- Separates confirmed player news from unconfirmed reporting.
- Stores historic results in `data/historical_games.csv` so you can compare our numbers against the DraftKings market after each game.
- Includes an optional daily GitHub Action that retrieves odds and news metadata through APIs. No API key is ever placed in the public website.

This project is a research tracker, not a prediction guarantee. A signal is worth keeping only if it improves a back-test against the closing market line.

## Upload to GitHub Pages

1. Create a new GitHub repository, e.g. `game-edge-tracker`.
2. Upload the contents of this folder (not the folder itself) to the repository root.
3. In GitHub, open **Settings → Pages** and select **Deploy from a branch**, then choose `main` and `/ (root)`.
4. Your dashboard will be available at `https://YOUR-USERNAME.github.io/game-edge-tracker/`.

## Daily workflow without APIs

Open `data/daily_game_inputs.csv` in Excel or Google Sheets. Add one row per game, save as CSV, and commit/upload it. Refresh the page.

The calculated score is a triage signal, not a bet recommendation:

- `Watch`: information may deserve a closer look.
- `No signal`: no material divergence from the market baseline.

## DraftKings and post-game review

Use DraftKings as the market reference by recording the DK opening and closing moneylines in `data/historical_games.csv`. Do not scrape DraftKings' website. If an odds-data provider offers DraftKings as a bookmaker, use that permitted feed; otherwise, enter the values manually from the odds screen.

Open `analysis.html` after results are entered. It reports market and tracker Brier scores, completed-game detail, and closing-line movement. Lower Brier scores are better. Do not change a pre-game row after the game starts; add final results only after the game ends.

## Optional daily updater

The workflow in `.github/workflows/daily-update.yml` runs every morning and can be triggered manually from the Actions tab.

Add these repository secrets under **Settings → Secrets and variables → Actions**:

- `ODDS_API_KEY` — optional key from The Odds API.
- `NEWS_API_KEY` — optional key from NewsAPI.

The updater writes raw, timestamped source metadata to `data/source_log.csv`. It intentionally does not treat an article headline as confirmed player availability. Confirmed statuses should be entered from the relevant league/team report before relying on them.

## The fields that matter most

`market_implied_home_win_prob` is the benchmark. The dashboard adjusts it only with factors you can later evaluate:

- confirmed availability impact;
- rest and compressed schedules;
- travel distance and time-zone direction;
- team net rating;
- home-court and matchup information;
- news confidence and timing; and
- closing-line value (in the historic file).

Saturday is recorded as a variable, but it should not be treated as a universal advantage. Its apparent effect can be caused by schedule composition, travel, and which teams play that day.

## Important data rule

Keep the original market snapshot and every source URL/timestamp. Do not overwrite them with later information. That is what makes a future back-test honest.
