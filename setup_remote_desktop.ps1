# 远程桌面设置脚本
# 需要以管理员身份运行！

Write-Host "=== 远程桌面设置脚本 ===" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ 请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击脚本，选择'以管理员身份运行'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ 管理员权限确认" -ForegroundColor Green
Write-Host ""

# 1. 启用远程桌面
Write-Host "正在启用远程桌面..." -ForegroundColor Yellow
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Write-Host "✅ 远程桌面已启用" -ForegroundColor Green

# 2. 启用网络级身份验证（NLA）
Write-Host "正在启用网络级身份验证（更安全）..." -ForegroundColor Yellow
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1
Write-Host "✅ 网络级身份验证已启用" -ForegroundColor Green

# 3. 配置防火墙允许远程桌面
Write-Host "正在配置防火墙..." -ForegroundColor Yellow
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Write-Host "✅ 防火墙已配置" -ForegroundColor Green

# 4. 设置RDP端口（默认3389）
Write-Host "RDP端口设置为: 3389" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== 远程桌面设置完成！===" -ForegroundColor Green
Write-Host ""
Write-Host "📝 使用说明：" -ForegroundColor Yellow
Write-Host "1. 局域网内访问：使用电脑IP地址 + :3389" -ForegroundColor White
Write-Host "2. 外网访问需要配置端口转发（路由器设置）" -ForegroundColor White
Write-Host "3. 用户名: $env:USERNAME" -ForegroundColor White
Write-Host "4. 密码: lianggangwei123" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  安全警告：从外网访问有风险！" -ForegroundColor Red
Write-Host ""

pause
