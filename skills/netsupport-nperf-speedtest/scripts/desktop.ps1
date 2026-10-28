param(
    [Parameter(Mandatory)]
    [ValidateSet('capture', 'click', 'doubleclick', 'wheel', 'keys')]
    [string] $Action,
    [int] $X = 0,
    [int] $Y = 0,
    [int] $Delta = 0,
    [string] $Keys = '',
    [string] $Out = (Join-Path $env:TEMP 'netsupport-nperf-current.png')
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class NperfMouse {
    [DllImport("user32.dll")]
    public static extern void mouse_event(int flags, int dx, int dy, int data, IntPtr extraInfo);
}
'@

$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bounds = $screen.Bounds
if ($Action -in @('click', 'doubleclick', 'wheel')) {
    if (-not $bounds.Contains((New-Object System.Drawing.Point($X, $Y)))) {
        throw "Point ($X, $Y) is outside the primary screen $bounds"
    }
    [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($X, $Y)
}

switch ($Action) {
    'click' {
        [NperfMouse]::mouse_event(2, 0, 0, 0, [IntPtr]::Zero)
        [NperfMouse]::mouse_event(4, 0, 0, 0, [IntPtr]::Zero)
    }
    'doubleclick' {
        1..2 | ForEach-Object {
            [NperfMouse]::mouse_event(2, 0, 0, 0, [IntPtr]::Zero)
            [NperfMouse]::mouse_event(4, 0, 0, 0, [IntPtr]::Zero)
            Start-Sleep -Milliseconds 100
        }
    }
    'wheel' { [NperfMouse]::mouse_event(0x0800, 0, 0, $Delta, [IntPtr]::Zero) }
    'keys' {
        if ([string]::IsNullOrWhiteSpace($Keys)) { throw 'Keys cannot be empty.' }
        [System.Windows.Forms.SendKeys]::SendWait($Keys)
    }
}

Start-Sleep -Milliseconds 350
$destination = [System.IO.Path]::GetFullPath($Out)
$parent = [System.IO.Path]::GetDirectoryName($destination)
if (-not [System.IO.Directory]::Exists($parent)) {
    [System.IO.Directory]::CreateDirectory($parent) | Out-Null
}
$bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($destination, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose()
    $bitmap.Dispose()
}
Write-Output $destination
