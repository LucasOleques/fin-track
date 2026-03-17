$Path = "C:\Users\lucas\IdeaProjects VSCode\fin-track\*"

Get-ChildItem -Recurse -Directory -Filter .\* "__pycache__" | ForEach-Object {
    Write-Host "Clearing __pycache__ in:" $_.FullName -ForegroundColor Blue
    Get-ChildItem $_ | Remove-Item -Recurse -Force
}

Get-ChildItem -Recurse -Path $Path -Include migrations | ForEach-Object {
    Write-Host "Clearing migrations in:" $_.FullName -ForegroundColor Blue
    Get-ChildItem $_ -Exclude "__init__.py" | Remove-Item -Recurse -Force
}

Get-ChildItem -Recurse -Path $Path -Include "*.sqlite3" | ForEach-Object {
    Write-Host "Removing database file:" $_.FullName -ForegroundColor Blue
    Remove-Item $_ -Force
}

$cmdScript = "C:\Users\lucas\IdeaProjects VSCode\fin-track\scripts\fin_track_create_database.cmd"
Write-Host "Executando script CMD..." -ForegroundColor Green

Start-Process cmd.exe -ArgumentList "/c `"$cmdScript`"" -NoNewWindow -Wait

Write-Host "Limpeza concluida e banco de dados recriado." -ForegroundColor Green