$(document).ready(async function() {
    live = await getLiveGames();
    $("#live-game-container").html(live);

    // replace any missing hero icons (update manually)
    $("#live-game-container").find("img.hero-icon").on("error", function() {
        this.onerror = null;
        this.src = 'data:image/svg+xml;utf8,' +
            encodeURIComponent(`
                <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 -960 960 960" width="32px" fill="#e3e3e3">
                    <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm40-337 160-160 160 160 160-160 40 40v-183H200v263l40 40Zm-40 257h560v-264l-40-40-160 160-160-160-160 160-40-40v184Zm0 0v-264 80-376 560Z"/>
                </svg>
            `);
    });

    $(document).on("click", "#copy-match-id", function() {
        const match_id = $(this).attr("data");
        if (match_id) {
            navigator.clipboard.writeText(match_id)
        }
    });
});

async function getLiveGames() {
    return $.ajax({
        type: "GET",
        url:  "/api/live-games"
    });
}
