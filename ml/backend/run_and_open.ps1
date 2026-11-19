# Start Django dev server and open app in browser (HTTP)
$url = "http://127.0.0.1:8000/"
Write-Host "Starting server... Open this URL in your browser: $url" -ForegroundColor Green
Write-Host "Waiting ~30 seconds for model to load, then opening browser..." -ForegroundColor Yellow
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python manage.py runserver
}
Start-Sleep -Seconds 30
Start-Process $url
Write-Host "Browser opened. Server is running in background (Job ID: $($job.Id))." -ForegroundColor Green
Receive-Job $job
