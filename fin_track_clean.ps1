Get-ChildItem -Recurse -Directory -Filter .\* "__pycache__" | ForEach-Object {
    Write-Host "Clearing __pycache__ in:" $_.FullName
    Get-ChildItem $_ | Remove-Item -Recurse -Force
}

Get-ChildItem -Recurse -Path .\* -Include migrations | ForEach-Object {
    Write-Host "Clearing migrations in:" $_.FullName
    Get-ChildItem $_ -Exclude "__init__.py" | Remove-Item -Recurse -Force
}