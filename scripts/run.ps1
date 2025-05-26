param (
    [string]$port = "8000"
)

flask --app src/sentry/ run --debug --port $port
