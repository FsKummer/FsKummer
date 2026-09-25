# Profile cards

The README uses local animated SVGs. The daily workflow refreshes stats, languages, streaks, and trophies at 09:17 UTC, and can also be run manually from the Actions tab.

`python3 scripts/refresh_profile_cards.py` updates each card only after checking its SVG and expected data labels. If a provider is unavailable or returns an error card, the last successful image remains in the repository. The workflow reports a failure so stale cards are visible in Actions.

The cards display publicly available data. Language and stats cards concern public repositories; the streak card uses publicly displayed contribution activity. The services use different counting windows and methodologies, so their totals may differ.

Sources:

- [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended)
- [GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats)
- [GitHub Profile Trophy](https://github.com/ryo-ma/github-profile-trophy); the selected mirror, `trophy.ryglcloud.net`, is listed by its maintainer.
- [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg), downloaded once because its animation does not depend on changing data.
- Sunglasses emoji: the original README's [Slackmojis GIF](https://emojis.slackmojis.com/emojis/images/1531849430/4246/blob-sunglasses.gif?1531849430).
