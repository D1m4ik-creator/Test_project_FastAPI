[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("up", "down", "info", "logs", "help")]
    [string]$Action = "help"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Show-Usage {
    Write-Host "Usage: .\scripts.ps1 <up|down|info|logs>"
}

switch ($Action) {
    "up" {
        docker compose up -d --build
    }
    "down" {
        docker compose down
    }
    "info" {
        docker compose ps
    }
    "logs" {
        docker compose logs -f
    }
    "help" {
        Show-Usage
    }
}
