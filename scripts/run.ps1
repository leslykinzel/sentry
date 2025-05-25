param (
    [string]$port = "8000"
)

flask --app src/server run --debug --port $port
