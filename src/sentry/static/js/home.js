$(document).ready(async function() {
    live = await getLiveGames();
    // console.log(live);
    $("#live-game-container").html(live)
});

async function getLiveGames() {
    return $.ajax({
        type: "GET",
        url:  "/api/live-games"
    });
}
