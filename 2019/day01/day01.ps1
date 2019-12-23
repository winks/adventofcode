param(
[string]$filename = "nope"
)

function Read-Lines([string]$file)
{
	#Get-Content $args[0] | ForEach-Object {
	$lines = @()
	foreach($line in [System.IO.File]::ReadLines($file)) {
		$lines += $line
	}
	return $lines
}

function Get-Fuel
{
	Param($Mass)
	$r = $Mass / 3.0
	$r = [math]::Floor($r)
	return $r - 2
}

function Main
{
	if ($filename -eq "nope") {
		Write-Output "Usage: day01.ps1 /path/to/file"
		return
	}
	$fn = (Get-Item -Path $filename).FullName
	Write-Output "File: $($fn)"
	$lines = Read-Lines $fn
	Write-Output "Read $($lines.length) lines"
	$fuels = @()
	$total2 = 0
	foreach ($line in $lines) {
		$fuel = Get-Fuel $line
		Write-Output "$($line) => $($fuel)"
		$fuels += $fuel

		$fuel2 = $fuel
		Do {
			$fuel2 = Get-Fuel $fuel2
			if ($fuel2 -gt 0) {
				$total2 += $fuel2
			}
		} While ($fuel2 -gt 0)
	}
	$total = $fuels -join '+'
	Write-Output "Summing up: $($total)"
	$total = Invoke-Expression $total
	Write-Output "Part 1: $($total)"
	Write-Output "Part 2: $($total+$total2)"
}

Main
