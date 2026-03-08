
@echo off
echo ========================================
echo 推送到 GitHub (SSH方式)
echo ========================================
echo.

REM 设置Git路径
set PATH=%PATH%;C:\Program Files\Git\bin

REM 添加GitHub到已知主机
echo [1/3] 添加GitHub主机密钥...
ssh-keyscan github.com &gt;&gt; "%USERPROFILE%\.ssh\known_hosts" 2&gt;nul
echo ✅ GitHub主机已添加
echo.

echo [2/3] 开始推送...
echo.
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 请检查：
    echo 1. SSH密钥是否已添加到GitHub
    echo 2. GitHub仓库是否存在
    echo 3. 网络连接是否正常
    echo.
    echo 访问: https://github.com/lianggangwei/lianggangwei
    echo.
) else (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 访问你的仓库:
    echo https://github.com/lianggangwei/lianggangwei
    echo.
)

pause

