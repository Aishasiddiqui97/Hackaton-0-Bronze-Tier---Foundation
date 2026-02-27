@echo off
echo ========================================
echo Test Autonomous Agent (Single Run)
echo ========================================
echo.
echo This will run ONE iteration to test:
echo - Folder creation
echo - Post generation
echo - WhatsApp processing
echo.
pause

echo.
echo Creating test WhatsApp message...
echo # Test WhatsApp Message > "00_Inbox/WhatsApp/test_message.md"
echo. >> "00_Inbox/WhatsApp/test_message.md"
echo Hello, I need information about your services. >> "00_Inbox/WhatsApp/test_message.md"

echo.
echo Running single iteration...
python -c "from autonomous_social_agent import AutonomousSocialAgent; agent = AutonomousSocialAgent(); agent.check_approved_posts(); agent.process_whatsapp_messages(); print('\n✅ Test complete! Check folders for results.')"

echo.
echo ========================================
echo Test Results
echo ========================================
echo.
echo Check these folders:
echo - 02_Pending_Approvals\Social_Posts\  (Generated posts)
echo - 00_Inbox\WhatsApp\                  (Processed messages)
echo - logs\autonomous_agent.log           (Activity log)
echo.
pause
