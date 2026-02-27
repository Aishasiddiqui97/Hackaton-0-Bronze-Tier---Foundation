@echo off
echo ========================================
echo Generate and Post LinkedIn Content
echo ========================================
echo.

echo [1/4] Generating new LinkedIn post...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); content = agent.generate_social_post('LinkedIn'); filepath = agent.create_pending_post('LinkedIn', content); print(f'Generated: {filepath}')"

echo.
echo [2/4] Moving to Posted folder...
for %%f in ("02_Pending_Approvals\Social_Posts\LinkedIn_Post_*.md") do (
    set "latest=%%f"
)
move "%latest%" "03_Posted\History\"

echo.
echo [3/4] Getting filename...
for %%f in ("03_Posted\History\LinkedIn_Post_*.md") do (
    set "postfile=%%f"
)

echo.
echo [4/4] Posting to LinkedIn...
python linkedin_auto_poster.py "%postfile%"

echo.
echo ========================================
echo Done!
echo ========================================
pause
