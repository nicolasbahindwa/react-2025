# from fastapi import FastAPI, APIRouter, Depends
# from pydantic import EmailStr
# from app.services.email import EmailService, EmailContent, EmailTemplate

# app = FastAPI()

# router = APIRouter()

# @router.post("/test-email")
# async def test_send_email(email: EmailStr):
#     email_service = EmailService()
#     content = EmailContent(
#         subject="Test Email",
#         template_name=EmailTemplate.WELCOME,  # Ensure you have a 'welcome' template
#         template_data={"username": "Test User"},
#         to_email=email
#     )
    
#     print(content)
    
#     result = await email_service.send_email(content)
#     return {"email_sent": result}

# app.include_router(router)
