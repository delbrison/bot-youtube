$exclude = @(".venv", "log_canais_youtube.txt", "BotYoutube.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotYoutube.zip" -Force