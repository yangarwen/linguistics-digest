param(
    [string]$TaskName = "LinguisticsDigestDailySlang",
    [string]$PythonPath = "C:\Users\acer\AppData\Local\Programs\Python\Python313\python.exe",
    [string]$ScriptPath = "C:\Users\acer\linguistics-digest\main.py",
    [string]$Time = "08:00"
)

$action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At $Time
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel LeastPrivilege

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Description "Send daily youth slang digest email" -Force

Write-Host "Scheduled task '$TaskName' created to run at $Time daily."
Write-Host "If you want a different time, re-run this script with -Time 'HH:mm'."