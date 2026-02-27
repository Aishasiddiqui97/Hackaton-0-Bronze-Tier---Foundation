@echo off
echo ========================================
echo Generate Posts for All Platforms
echo ========================================
echo.

echo Generating posts for:
echo - LinkedIn (will auto-post)
echo - Twitter (manual posting)
echo - Facebook (manual posting)
echo - Instagram (manual posting)
echo.
pause

echo.
echo [1/4] Generating LinkedIn post...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); content = agent.generate_social_post('LinkedIn'); agent.create_pending_post('LinkedIn', content)"

echo.
echo [2/4] Generating Twitter post...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); content = agent.generate_social_post('Twitter'); agent.create_pending_post('Twitter', content)"

echo.
echo [3/4] Generating Facebook post...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); content = agent.generate_social_post('Facebook'); agent.create_pending_post('Facebook', content)"

echo.
echo [4/4] Generating Instagram post...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); content = agent.generate_social_post('Instagram'); agent.create_pending_post('Instagram', content)"

echo.
echo ========================================
echo Posts Generated!
echo ========================================
echo.
echo Check: 02_Pending_Approvals\Social_Posts\
echo.
echo Next steps:
echo 1. Review posts
echo 2. Move to 03_Posted\History\ to approve
echo 3. LinkedIn will auto-post
echo 4. Run quick_post_all.bat for others
echo.
pause
