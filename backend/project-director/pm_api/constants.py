from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

#.env passwords
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
TEST_USERS_PASSWORD = os.getenv("TEST_USERS_PASSWORD")

PROJECT_MANAGER_GROUP = "Project_Manager"
SUPER_INTENDENT_GROUP = "Superintendent"

TOKEN_MAX_LENGTH = 10


#RFI model field names
RFI_FROM = "f_user"
RFI_JOB = 'job_key'
RFI_TO = "t_user"
RFI_SUBJECT = "subject"
RFI_BODY = "body"
RFI_ATTACHMENTS = "attachments"
RFI_DATE = "date_created"
RFI_STATUS = "closed"

RFI_DETAIL_FIELDS = ("id", RFI_FROM, RFI_TO, RFI_SUBJECT, RFI_BODY, RFI_DATE, RFI_STATUS)
RFI_LIST_FIELDS = ("id", RFI_FROM, RFI_TO, RFI_SUBJECT, RFI_DATE, RFI_STATUS)   
#RFI_LIST_FIELDS = ("id", RFI_SUBJECT, RFI_DATE, RFI_STATUS)   

#Job model field names
JOB_NAME = "name"
USERS = "user_key"
DATE_START = "date_start"

#Response model field names
RESPONSE_FROM = "_from_user_key"
RESPONSE_RFI_KEY = "rfi_key"
RESPONSE_TEXT_BODY = "text_body"
RESPONSE_DATE_SENT = "date_sent"
