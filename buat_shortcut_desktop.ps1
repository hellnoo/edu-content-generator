$WshShell   = New-Object -ComObject WScript.Shell
$Desktop    = [System.Environment]::GetFolderPath("Desktop")
$Shortcut   = $WshShell.CreateShortcut("$Desktop\EduGen.lnk")

$Shortcut.TargetPath       = "pythonw.exe"
$Shortcut.Arguments        = "`"C:\Users\User\edu-content-generator\app.py`""
$Shortcut.WorkingDirectory = "C:\Users\User\edu-content-generator"
$Shortcut.IconLocation     = "C:\Users\User\edu-content-generator\icon.ico"
$Shortcut.Description      = "EduGen - AI Content Generator"
$Shortcut.WindowStyle      = 1

$Shortcut.Save()
Write-Host "Shortcut EduGen berhasil dibuat di Desktop!" -ForegroundColor Green
