Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Drawing

$inputPath = Join-Path $PSScriptRoot '..\archive\iterations\self-evolution-history-bucket-v9.png'
$outputPath = Join-Path $PSScriptRoot '..\self-evolution-history-bucket-v11.png'
$image = [System.Drawing.Image]::FromFile($inputPath)
$bitmap = New-Object System.Drawing.Bitmap $image
$image.Dispose()

$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$graphics.FillRectangle([System.Drawing.Brushes]::White, 598, 678, 195, 42)

$font = New-Object System.Drawing.Font 'Microsoft YaHei UI', 20, ([System.Drawing.FontStyle]::Bold), ([System.Drawing.GraphicsUnit]::Pixel)
$brush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(0, 128, 32))
$graphics.DrawString('ACCEPT | 显著改善', $font, $brush, 599, 682)

$brush.Dispose()
$font.Dispose()
$graphics.Dispose()
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$bitmap.Dispose()
