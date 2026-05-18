$in = 'assets/brand/logo-240.png'
$out = 'assets/brand/logo-240.dataurl.txt'
$b = [System.Convert]::ToBase64String([IO.File]::ReadAllBytes($in))
$d = 'data:image/png;base64,' + $b
Set-Content -Path $out -Value $d -Encoding UTF8
Write-Output "WROTE $out"
