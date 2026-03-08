
@echo off
echo ========================================
echo 推送到 Gitee
echo ========================================
echo.

REM 设置Git路径
set PATH=%PATH%;C:\Program Files\Git\bin

echo [1/2] 准备推送...
echo.
echo 请确保：
echo 1. 你已经在Gitee上创建了仓库：https://gitee.com/lianggangwei/lianggangwei
echo 2. 你的网络连接正常
echo.
pause

echo.
echo [2/2] 开始推送...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 可能的解决方案：
    echo 1. 检查网络连接
    echo 2. 在Gitee上检查仓库是否存在
    echo 3. 尝试使用SSH方式推送
    echo.
    echo 或者手动运行以下命令：
    echo git push https://6e40e4d7bef4d36d99bf1924001e8698@gitee.com/lianggangwei/lianggangwei.git main
    echo.
) else (
    echo.
    echo ✅ 推送成功！
    echo.
    echo 访问你的仓库：https://gitee.com/lianggangwei/lianggangwei
    echo.
)

pause

