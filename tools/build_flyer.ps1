# Erzeugt industrietaucher-flyer.pdf und img/flyer-vorschau.png aus tools/flyer.html.
# Voraussetzung: lokaler Server auf Port 8765 im Repo-Root (python -m http.server 8765)
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$profile = Join-Path $env:TEMP "flyer-edge-$(Get-Random)"
$url = "http://localhost:8765/tools/flyer.html"
& $edge --headless=new --disable-gpu "--user-data-dir=$profile" --no-pdf-header-footer "--print-to-pdf=$root\industrietaucher-flyer.pdf" $url 2>&1 | Out-Null
& $edge --headless=new --disable-gpu --hide-scrollbars "--user-data-dir=$profile" "--window-size=794,1123" "--screenshot=$root\img\flyer-vorschau.png" $url 2>&1 | Out-Null
Write-Output "Flyer erzeugt."
