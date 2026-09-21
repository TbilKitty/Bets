Can we create a data set that scraps the interenet for news articles on high performing athetes that will be out of game, etc. I want to create a betting daily updater to use for betting strategy. But first lets consider if there are any trends about what makes a sport team lose/win. Best player out on personal issues? Lose? Travelings across country? Tired factors? Are games on a Saturday more likey to win ? IDK. Lets consider every factor and make a sheet that supports a winner/loser so I can use it to bet. 

Yes. Start with one league—NBA is ideal for a daily model because there are many games, frequent injury updates, and clear rest/travel effects.

The model should predict whether a team beats the market’s implied probability, not merely whether it wins. The betting line already reflects obvious information, so the question is: “Is the line underreacting?”

Factor group	Capture	How to use it
Market baseline	Opening/closing moneyline, spread, implied probability	The benchmark; do not try to replace it
Player availability	Confirmed out, doubtful, questionable, return from injury, expected minutes limit	Weight by player value and position; distinguish confirmed report from rumor
Team strength	Adjusted offensive/defensive rating, recent form, lineup strength	Use multi-season/recent-game measures, not raw win streaks
Rest and workload	Days’ rest, back-to-back, 3 games in 4 nights, overtime minutes	Usually stronger than “Saturday” as a standalone idea
Travel/body-clock	Miles traveled, time zones crossed, direction of travel, home stand/road trip length	Test by league and direction; do not assume every trip matters equally
Matchup	Pace, shooting profile, rebounding, turnovers, defensive scheme	Especially useful once you have enough historical games
Venue/context	Home court, altitude, weather for outdoor sports, playoff/season incentives	Home advantage and altitude are real candidates; weather is sport-specific
Schedule	Day of week, start time, early game, holiday, international travel	Include Saturday, but treat it as a testable variable—not a rule
News signal	Personal absence, suspension, coaching change, locker-room issue	Use only reputable sources, timestamped, and label confidence
Outcome/evaluation	Win/loss, cover, line movement, closing-line value, ROI	Lets us find what actually added value rather than memorable anecdotes

A star being out is not automatically a “bet against” signal. The line often moves immediately, and a team can outperform expectations if the replacement matchup is favorable or the opponent is also shorthanded. For example, current injury reporting regularly contains multiple important absences and late designations, which is exactly why the sheet needs timestamps and “confirmed versus uncertain” status rather than a simple yes/no injury flag. Reuters injury-report example

I would build the workbook around these outputs:

Daily slate: each game, market baseline, injury/news flags, rest/travel factors, and a “review only” edge estimate.
Raw news log: article URL, publication time, team/player, claim, source quality, confirmation status, and expected return/game impact.
Historical games: one row per team-game, so each factor can be tested against both win probability and against-the-spread results.
Backtest dashboard: hit rate, ROI, and—most importantly—closing-line value by factor combination.
Model rules: only surface a wager candidate when the estimated edge is materially greater than the uncertainty; otherwise mark “No bet.”

For data collection, I would avoid indiscriminate site scraping. We can use official league injury reports, permitted RSS/news feeds, and a licensed odds/sports-stat API; retain the source link and timestamp for every record. That will be sturdier and less likely to break than scraping article pages.

The first decision is the league. I recommend starting with NBA, then expanding after we see which factors actually survive backtesting.

Can you create files that I will upload to Githu
I aim to use it for DraftKings. But Id also like updates post game about accuracy rating for our numbers. And we can adjust long term. 

Built the upload-ready GitHub Pages project.

It includes:

Daily NBA dashboard with DraftKings market probability and tracker probability
Editable factor weights for availability, rest, travel, and net rating
Scheduled daily updater using an odds API key stored in GitHub Secrets
DraftKings opening/closing-line fields
Post-game accuracy page comparing our Brier score to the market’s
Historical data template that preserves original pre-game values

Unzip it, then upload the contents of the sports-betting-updater folder to a new GitHub repository.

Game_Edge_Tracker_GitHub_Pages.zip

ok I think everything is in its correct place

Yes—your main files are in the repository root, which is correct.

Two quick checks:

Open .github/workflows and confirm it contains daily-update.yml (not only the deleted main.yml).
The file named download is not part of the project; you can delete it.

Then go to Settings → Pages and set deployment to:

Branch: main
Folder: / (root)

After it deploys, your site should be at:

https://tbilkitty.github.io/[repository-name]/

Choose Static HTML → Configure.

GitHub will open a workflow file. Leave its default contents and click Commit changes. That creates the separate Pages deployment workflow; it will not interfere with your daily-update.yml updater.

Then wait a minute or two, refresh this Pages screen, and GitHub will show the published site URL.

Perfect—the two workflows are present.

Click Deploy static content to Pages in the left sidebar. Then click Run workflow on the right and confirm Run workflow again.

That will publish the website immediately. Once it finishes with a green checkmark, return to Settings → Pages for the live URL.

Can we put the daily sports games? Can we do NFL? Like a page that auto updates based on the games happening this day

Yes—use this NFL update to replace the project files in your repository.

It auto-refreshes that day’s NFL slate and DraftKings-implied probability when you add ODDS_API_KEY under Settings → Secrets and variables → Actions. Then manually run Update daily NFL research data once to test it.

NFL_Game_Edge_Tracker_GitHub_Pages.zip

Just give the updates files. I have uploaded the other files

Upload these over the matching existing files:

index.html → repository root

update_daily_data.py → scripts

daily-update.yml → .github/workflows

README.md → repository root

index.html
HTML
update_daily_data.py
Code
daily-update.yml
Code
README.md
Document
Show less
Can we make it prettier? 

Absolutely. Replace just your existing 
styles.css with this one—it gives the site a polished dark sports-dashboard design with a stronger header, richer cards, cleaner table, and mobile-friendly layout.

styles.css

styles.css
Code
