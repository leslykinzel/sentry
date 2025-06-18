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
                players = game.get("players")
                if ( 
                    # if a game is not full, ignore it
                    game.get("is_watch_eligible", False)
                    and players
                    and len(players) == 10
                ):
                    live_games.append(
                        LiveDotaGame(
                            match_id=game.get("match_id", 0),
                            avg_mmr=game.get("average_mmr", 0),
                            r_score=game.get("radiant_score", 0),
                            d_score=game.get("dire_score", 0),
                            game_time=game.get("game_time", 0),
                            gold_lead=game.get("radiant_lead", 0),
                            players=players
                        )
                    )
            except Exception:
                continue

        return live_games

    def as_html(self):
        if self.games is None:
            return "<p>No games available, try again later.</p>"

        top_games = sorted(self.games, reverse=True)[:6]

        return "".join(str(game) for game in top_games)


class LiveDotaGame:

    def __init__(self, match_id, avg_mmr, r_score, d_score, game_time, gold_lead, players):
        self.match_id = match_id
        self.avg_mmr = avg_mmr
        self.r_score = r_score
        self.d_score = d_score
        self.game_time = game_time
        self.gold_lead = gold_lead
        self.players = self.get_players_summary(players)

    def __lt__(self, other: "LiveDotaGame"):
        return self.avg_mmr < other.avg_mmr

    def __str__(self):
        mins = self.game_time // 60
        secs = self.game_time % 60
        time = f"{mins}:{secs:02d}"

        radiant_players = self.players["radiant"]
        dire_players = self.players["dire"]

        player_rows = ""
        for radiant, dire in zip(radiant_players, dire_players):
            player_rows += f"""
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <!-- Radiant -->
                    <div class="d-flex align-items-center">
                        <img 
                            class="hero-icon"
                            src="{escape(radiant["static_hero_icon_path"])}" 
                            alt="hero icon {escape(radiant["hero_id"])}"
                        >
                        <span class="ms-2">{escape(radiant["account_id"])}</span>
                    </div>
                    <!-- Dire -->
                    <div class="d-flex align-items-center flex-row-reverse">
                        <img
                            class="hero-icon"
                            src="{escape(dire["static_hero_icon_path"])}"
                            alt="hero icon {dire["hero_id"]}"
                        >
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
                    <br>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="btn-group">
                            <button
                                id="copy-match-id"
                                type="button" 
                                class="btn btn-sm btn-outline-secondary"
                                data="{self.match_id}"
                            >
                                Copy Match ID
                            </button>
                        </div>
                        {self.get_gold_display()}
                        <small class="text-muted">{time}</small>
                    </div>
                </div>
            </div>
        </div>
        """

    def get_players_summary(self, players_response):
        if not players_response:
            print(f"WARNING: No players in match {self.match_id}")
            return {"radiant": [], "dire": []}

        radiant_players = []
        dire_players = []

        for player in players_response:
            summary = {
                "account_id": player.get("account_id", None),
                "account_metadata": {}, # todo: player names
                "hero_id": player.get("hero_id", None)
            }

            hero_id = summary["hero_id"]
            if hero_id == None:
                summary["static_hero_icon_path"] = f"static/images/dota2/hero/icon/unknown.png"
            else:
                summary["static_hero_icon_path"] = f"static/images/dota2/hero/icon/{hero_id}.png"

            team = player.get("team")
            slot = player.get("team_slot")

            if team == 0:
                radiant_players.append((slot, summary))
            elif team == 1:
                dire_players.append((slot, summary))
            
        radiant_sorted = [s for _, s in sorted(radiant_players, key=lambda x: x[0])]
        dire_sorted = [s for _, s in sorted(dire_players, key=lambda x: x[0])]

        return {
            "radiant": radiant_sorted,
            "dire": dire_sorted
        }

    def get_gold_display(self):
        if self.gold_lead >= 0:
            return f"""
                <span class='text-success'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor">
                        <path d="m280-400 200-200 200 200H280Z"/>
                    </svg>
                    {self.gold_lead}
                </span>
                """
        else:
            return f"""
                <span class='text-danger'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor">
                        <path d="M480-360 280-560h400L480-360Z"/>
                    </svg>
                    {abs(self.gold_lead)}
                </span>
                """
