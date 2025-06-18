import json
from markupsafe import escape
import opendota


class LiveGames:
    """
        self.data   = json
        self.games  = list[LiveDotaGame]
        self.html   = str
    """

    def __init__(self, data):
        self.data = json
        self.games = self.validate(data)
        self.html = self.as_html()

    def validate(self, data):
        live_games = []
        response = json.loads(data)

        for game in response:
            try:
                if game.get("is_watch_eligible", False) == True:
                    live_games.append(
                        LiveDotaGame(
                            avg_mmr=game.get("average_mmr", 0),
                            r_score=game.get("radiant_score", 0),
                            d_score=game.get("dire_score", 0),
                            game_time=game.get("game_time", 0),
                            players=game.get("players", None)
                        )
                    )
            except Exception:
                continue

        return live_games

    def as_html(self):
        if self.games is None:
            return "<p>No live games available</p>"

        top_games = sorted(self.games, reverse=True)[:9]

        return "".join(str(game) for game in top_games)


class LiveDotaGame:

    def __init__(self, avg_mmr, r_score, d_score, game_time, players):
        self.avg_mmr = avg_mmr
        self.r_score = r_score
        self.d_score = d_score
        self.game_time = game_time
        self.players = self.get_players_summary(players)

    def __lt__(self, other: "LiveDotaGame"):
        return self.avg_mmr < other.avg_mmr

    def __str__(self):
        mins = self.game_time // 60
        secs = self.game_time % 60
        time = f"{mins}:{secs:02d}"

        player_rows = ""
        for i in range(5):
            radiant = self.players[i]
            dire = self.players[i + 5]
            player_rows += f"""
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <!-- Radiant -->
                    <div class="d-flex align-items-center">
                        <img src="{escape(radiant["static_hero_icon_path"])}" alt="hero icon">
                        <span class="ms-2">{escape(radiant["account_id"])}</span>
                    </div>
                    <!-- Dire -->
                    <div class="d-flex align-items-center flex-row-reverse">
                        <img src="{escape(dire["static_hero_icon_path"])}" alt="hero icon">
                        <span class="me-2">{escape(dire["account_id"])}</span>
                    </div>
                </div>
            """

        return f"""
        <div class="col-sm-4">
            <div class="card mb-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>MMR: {self.avg_mmr}</span>
                            <div class="d-flex align-items-center" style="gap: 4px;">
                            <span class="text-success">{self.r_score}</span>
                            <span>-</span>
                            <span class="text-danger">{self.d_score}</span>
                        </div>
                    </div>
                    <br>
                    <div class="col-12 mb-2">
                        {player_rows}
                    </div>
                    <pre>{escape(self.players)}</pre>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="btn-group">
                            <button type="button" class="btn btn-sm btn-outline-secondary">Copy Match ID</button>
                        </div>
                        <small class="text-muted">{time}</small>
                    </div>
                </div>
            </div>
        </div>
        """

    def get_players_summary(self, players_response):
        dota = opendota.OpenDota()
        player_summary = [{} for _ in range(10)]

        for player in players_response:
            try:
                slot = player.get("team_slot")
                if slot not in range(0, 10):
                    continue

                summary = {
                    "account_id":       player.get("account_id", None),
                    "account_metadata": {},
                    "hero_id":          player.get("hero_id", None)
                }

                if summary["hero_id"] is not None:
                    summary["static_hero_icon_path"] = f"static/images/dota2/hero/icon/{summary["hero_id"]}.png"
                else:
                    summary["static_hero_icon_path"] = "static/images/dota2/hero/icon/unknown/png"

                player_summary[slot] = summary
            except Exception:
                continue

        # defaults
        for i in range(10):
            if not player_summary[i]:
                player_summary[i] = {
                    "account_id":            "???",
                    "account_metadata":      {},
                    "hero_id":               "unknown",
                    "static_hero_icon_path": "static/images/dota2/hero/icon/unknown.png"
                }

        return player_summary
