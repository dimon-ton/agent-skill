param(
    [Parameter(Mandatory)][string] $Machine,
    [Parameter(Mandatory)][string] $Status,
    [string] $DownloadMbps = '',
    [string] $UploadMbps = '',
    [string] $LatencyMs = '',
    [string] $JitterMs = '',
    [string] $Server = '',
    [string] $Screenshot = '',
    [string] $Folder = (Join-Path ([Environment]::GetFolderPath('MyDocuments')) ('nPerf-' + (Get-Date -Format 'yyyy-MM-dd')))
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($Machine)) { throw 'Machine cannot be empty.' }
if ($Status -ne 'Completed' -and -not $Status.StartsWith('Unavailable - ')) {
    throw 'Status must be Completed or begin with Unavailable - .'
}
if ($Status -eq 'Completed' -and -not (Test-Path -LiteralPath $Screenshot -PathType Leaf)) {
    throw 'A completed result requires an existing screenshot.'
}
if ($Status -ne 'Completed' -and @(@($DownloadMbps, $UploadMbps, $LatencyMs, $JitterMs) | Where-Object { $_ -ne '' }).Count -gt 0) {
    throw 'Unavailable results must have blank measurements.'
}

New-Item -ItemType Directory -Path $Folder -Force | Out-Null
$date = Get-Date -Format 'yyyy-MM-dd'
$csv = Join-Path $Folder "nperf-results-$date.csv"
if (Test-Path -LiteralPath $csv) {
    $existing = @(Import-Csv -LiteralPath $csv)
    if ($Machine -in $existing.Machine) { throw "A result for $Machine already exists in $csv" }
}

if ($Status -eq 'Completed') {
    $safeName = $Machine -replace '[^A-Za-z0-9._-]', '_'
    $destination = Join-Path $Folder "Machine-$safeName.png"
    if (Test-Path -LiteralPath $destination) { throw "Screenshot already exists: $destination" }
    Copy-Item -LiteralPath $Screenshot -Destination $destination
}

[pscustomobject]@{
    Machine       = $Machine
    Download_Mbps = $DownloadMbps
    Upload_Mbps   = $UploadMbps
    Latency_ms    = $LatencyMs
    Jitter_ms     = $JitterMs
    Server        = $Server
    Status        = $Status
} | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8 -Append

Write-Output $csv
