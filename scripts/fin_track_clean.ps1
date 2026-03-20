[CmdletBinding()]
param(
    [switch]$DeleteDB,
    [switch]$SkipCache,
    [switch]$SkipMigrations,
    [switch]$SkipEnv,
    [switch]$DryRun,
    [switch]$Help
)

# ---------------------------
# HELP
# ---------------------------
if ($Help) {
    Write-Host ""
    Write-Host "Uso do script:" -ForegroundColor Cyan
    Write-Host "  .\fin_track_clean.ps1 [opcoes]" -ForegroundColor White
    Write-Host ""
    Write-Host "Opcoes:" -ForegroundColor Cyan
    Write-Host "  -DeleteDB        Remove banco SQLite"
    Write-Host "  -SkipCache       Nao limpa __pycache__"
    Write-Host "  -SkipMigrations  Nao limpa migrations"
    Write-Host "  -SkipEnv         Nao carrega .env"
    Write-Host "  -DryRun          Apenas simula (nao executa)"
    Write-Host "  -Help            Exibe ajuda"
    Write-Host ""
    exit
}

# ---------------------------
# FUNÇÃO UTIL
# ---------------------------
function Exec($action, $scriptBlock) {
    if ($DryRun) {
        Write-Host "[DRY-RUN] $action" -ForegroundColor Magenta
    } else {
        Write-Host $action -ForegroundColor Green
        & $scriptBlock
    }
}

# ---------------------------
# INIT
# ---------------------------

$ProjectRoot = Split-Path $PSScriptRoot -Parent

Write-Host "Diretorio raiz do projeto: $ProjectRoot" -ForegroundColor Blue

# ---------------------------
# CACHE
# ---------------------------
if (-not $SkipCache) {
    Exec "Limpando __pycache__..." {
        Get-ChildItem -Path $ProjectRoot -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
            Write-Host "Clearing __pycache__ in:" $_.FullName -ForegroundColor Blue
            Remove-Item $_.FullName -Recurse -Force
        }
    }
} else {
    Write-Host "Pulando limpeza de cache..." -ForegroundColor Yellow
}

# ---------------------------
# MIGRATIONS
# ---------------------------
if (-not $SkipMigrations) {
    Exec "Limpando migrations..." {
        Get-ChildItem -Path $ProjectRoot -Recurse -Directory -Filter "migrations" | ForEach-Object {
            Write-Host "Clearing migrations in:" $_.FullName -ForegroundColor Blue
            Get-ChildItem $_.FullName -Exclude "__init__.py" | Remove-Item -Recurse -Force
        }
    }
} else {
    Write-Host "Pulando migrations..." -ForegroundColor Yellow
}

# ---------------------------
# DATABASE
# ---------------------------
if ($DeleteDB) {
    Exec "Removendo banco SQLite..." {
        Get-ChildItem -Recurse -Path $ProjectRoot -Filter "*.sqlite3" | ForEach-Object {
            Write-Host "Removing database file:" $_.FullName -ForegroundColor Blue
            Remove-Item $_.FullName -Force
        }
    }
} else {
    Write-Host "Banco nao sera removido." -ForegroundColor Yellow
}

# ---------------------------
# AMBIENTE
# ---------------------------
Exec "Ativando ambiente virtual..." {
    try {
        conda activate fin-track
    } catch {
        & "$ProjectRoot\.venv\Scripts\Activate.ps1"
    }
}

# ---------------------------
# ENV
# ---------------------------
if (-not $SkipEnv) {
    $envFile = Join-Path $ProjectRoot ".env"

    if (Test-Path $envFile) {
        Exec "Carregando variaveis de ambiente..." {
            Get-Content $envFile | ForEach-Object {
                if ($_ -match "^\s*([^#][^=]*)=(.*)$") {
                    [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
                }
            }
        }
    }
} else {
    Write-Host "Pulando .env..." -ForegroundColor Yellow
}

# ---------------------------
# DJANGO
# ---------------------------
# Navega para o diretório que contém o manage.py
Set-Location (Join-Path $ProjectRoot "fin_track_project")

Exec "Executando makemigrations..." {
    python manage.py makemigrations user transactions categories accounts
}

Exec "Executando migrate..." {
    python manage.py migrate
}

Exec "Criando superusuario..." {
    python manage.py createsuperuser --noinput
}

# ---------------------------
# FINAL
# ---------------------------
Write-Host "Processo concluido." -ForegroundColor Green

Set-Location $PSScriptRoot