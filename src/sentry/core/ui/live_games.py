from markupsafe import escape
import json


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
                            game_time=game.get("game_time", 0)
                        )
                    )
            except Exception:
                continue

        return live_games

    def as_html(self):
        if self.games is None:
            return "<p>No live games available</p>"

        top_games = sorted(self.games, reverse=True)[:6]

        return "\n".join(game.as_html() for game in top_games)


class LiveDotaGame:

    def __init__(self, avg_mmr, r_score, d_score, game_time):
        self.avg_mmr = avg_mmr
        self.r_score = r_score
        self.d_score = d_score
        self.game_time = game_time

    def __lt__(self, other: "LiveDotaGame"):
        return self.avg_mmr < other.avg_mmr

    def as_html(self):
        mins = self.game_time // 60
        secs = self.game_time % 60
        time = f"{mins}:{secs:02d}"

        return f"""
        <div class="col-sm-4">
            <div class="card mb-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>MMR: {escape(self.avg_mmr)}</span>
                            <div class="d-flex align-items-center" style="gap: 4px;">
                            <span class="text-success">{escape(self.r_score)}</span>
                            <span>-</span>
                            <span class="text-danger">{escape(self.d_score)}</span>
                        </div>
                    </div>
                    <br>
                    <div class="col-12 mb-2 d-flex justify-content-between align-items-center">
                        <!-- Radiant -->
                        <div class="d-flex align-items-center">
                            <img src="static/images/dota2/hero/icon/70.png" alt="Hero A1">
                            <span class="ms-2">RadiantPlayer1</span>
                        </div>
                        <!-- Dire -->
                        <div class="d-flex align-items-center flex-row-reverse">
                            <img src="static/images/dota2/hero/icon/2.png" alt="Hero B1">
                            <span class="me-2">DirePlayer1</span>
                        </div>
                    </div>
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
