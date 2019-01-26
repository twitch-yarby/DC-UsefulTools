import winrm

ps_script = """Clear
$systeminfo = systeminfo /FO CSV | ConvertFrom-CSV
$CPU = Get-WmiObject Win32_Processor

New-Object -TypeName PSObject -Property @{Time=(Get-Date -Format 'dd-MM-yyyy HH:mm'); "Host Name" = $env:computername; "System Boot Time" = $systeminfo."System Boot Time"; "System Up Time" = $systeminfo."System Up Time"; "Total Physical Memory" = $systeminfo."Total Physical Memory"; "Available Physical Memory" = $systeminfo."Available Physical Memory" ; "Available Memory Percent" = ("{0:F0} %" -f ([int32]($systeminfo."Available Physical Memory".Replace('MB','')) / [int32]($systeminfo."Total Physical Memory".Replace('MB','')) * 100)); "CPU Load Percentage" = ("{0:F0} %" -f ($CPU.LoadPercentage))} | Format-List "Host Name",Time,"System Up Time","System Boot Time","Total Physical Memory","Available Physical Memory","Available Memory Percent","CPU Load Percentage"
Get-WmiObject win32_logicaldisk | Where-Object {$_.DriveType -eq 3} | Select-Object @{ n = 'Drive'; e = {$_.DeviceID.Replace(":","")}}, @{ n = 'Size'; e = { "{0:F2} GB" -f ($_.Size / 1gb)}}, @{ n = 'Size Remaining'; e = { "{0:F2} GB" -f ($_.FreeSpace / 1gb) } }, @{n='Free Space'; e={ "{0:F0} %" -f ($_.FreeSpace / $_.Size * 100)}} | Format-List
Get-WmiObject -namespace root\wmi -Class MSStorageDriver_FailurePredictStatus -ErrorAction Silentlycontinue | Select-Object InstanceName, PredictFailure, Reason | Format-List
"""

s = winrm.Session('windows-host.example.com', auth=('john.smith', 'secret'))
r = s.run_ps(ps_script)
r.std_out