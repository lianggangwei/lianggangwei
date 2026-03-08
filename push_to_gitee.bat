
@echo off
echo ========================================
echo 推送到 Gitee
echo ========================================
echo.

REM 刷新环境变量
set PATH=%PATH%;C:\Program Files\Git\bin

REM 设置Git远程仓库
echo [1/3] 设置Gitee远程仓库...
git remote remove origin 2&gt;nul
git remote add origin https://gitee.com/lianggangwei/lianggangwei.git
if %errorlevel% neq 0 (
    echo ❌ 设置远程仓库失败
    pause
    exit /b 1
)
echo ✅ 远程仓库设置成功
echo.

REM 推送到Gitee
echo [2/3] 推送到Gitee...
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 可能需要身份验证，请尝试：
    echo 1. 在浏览器中访问 https://gitee.com/profile/personal_access_tokens
    echo 2. 创建Personal Access Token，选择projects权限
    echo 3. 使用以下格式推送：
    echo    git push https://你的token@gitee.com/lianggangwei/lianggangwei.git main
    echo.
    pause
    exit /b 1
)
echo ✅ 推送成功！
echo.

echo [3/3] 完成！
echo ========================================
echo 🎉 代码已成功推送到Gitee！
echo 仓库地址: https://gitee.com/lianggangwei/lianggangwei
echo ========================================
echo.
pause

