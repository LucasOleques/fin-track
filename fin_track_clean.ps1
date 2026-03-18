$ProjectRoot = $PSScriptRoot

Write-Host "Diretorio do projeto:" $ProjectRoot -ForegroundColor Yellow

# Limpar __pycache__
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
    Write-Host "Clearing __pycache__ in:" $_.FullName -ForegroundColor Blue
    Remove-Item $_.FullName -Recurse -Force
}

# Limpar migrations (exceto __init__.py)
Get-ChildItem -Recurse -Directory -Filter "migrations" | ForEach-Object {
    Write-Host "Clearing migrations in:" $_.FullName -ForegroundColor Blue
    Get-ChildItem $_.FullName -Exclude "__init__.py" | Remove-Item -Recurse -Force
}

# Remover banco sqlite
Get-ChildItem -Recurse -Path $ProjectRoot -Include "*.sqlite3" | ForEach-Object {
    Write-Host "Removing database file:" $_.FullName -ForegroundColor Blue
    Remove-Item $_.FullName -Force
}

# Executar CMD relativo
$cmdScript = Join-Path $ProjectRoot "scripts\fin_track_create_database.cmd"

Write-Host "Executando script CMD..." -ForegroundColor Green
Start-Process cmd.exe -ArgumentList "/c `"$cmdScript`"" -NoNewWindow -Wait

Write-Host "Limpeza concluida e banco de dados recriado." -ForegroundColor Green