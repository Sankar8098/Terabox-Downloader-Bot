import os

API_ID = 24444928  # api id
API_HASH = "0a278a515cd13ec8802b7dabed73dede"

BOT_TOKEN = "7394038228:AAFLad15p6m5hvO8AcIlPTqMxa5xSoJgSao"


## REDIS
HOST = "redis-16448.c73.us-east-1-2.ec2.cloud.redislabs.com"  # redis host uri
PORT = 16448  # redis port
PASSWORD = "o5BMtARZTkrMHP7xvxkOEx6XrXS583NN"  # redis password

PRIVATE_CHAT_ID = -1002189431069
ADMINS = [6695586027]
'''
#Database 
#Database [https://youtu.be/qFB0cFqiyOM?si=fVicsCcRSmpuja1A]
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "ultroidxTeam")

#Shortner (token system) 
# check my discription to help by using my refer link of shareus.io


SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "api.shareus.io")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "PUIAQBIFrydvLhIzAOeGV8yZppu2")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 86400)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/Ultroid_Official/18") # shareus ka tut_vid he 
'''
        
COOKIE = """csrfToken=xOP11j7onKx_cELYY_x2bnwM; browserid=4z1XCJy2wski9a4955nT9LNe_XhSFTALjRye3sC9ggZ1tkwuwwvd0opwssA=; lang=en; TSID=8ifhqzTGTQPakDH9L7crjhGvP2MC5nmx; __bid_n=18eef166c5bf0afa4f4207; _ga=GA1.1.1651334296.1715623398; ndus=Y48dhKyteHuiixsjZKwAv2HvNOUCith3i87C3R8G; ndut_fmt=04B36097FEFACABD1CF54F6C34EA07923739EEC667AA2C9BE0A0370C1C65701F; ab_sr=1.0.1_ZTg4MDFjOWE5YTFlYzI1YjY0OTliMjAyZmQ3Mzc2ODk5ZmUyOTgzNzA3MmEwZmJmOTRkODAwY2U3MzAzODE2ZDBjNjJjMDI1NjE3NTk5ODczOTMxMTM3ZjQ0MDQ2Nzg3NDFmOTk1OGQ4YmRjYjQzMjdiMzk5ZmVlYzFlMGUyYjNjOTc5MWIwMDdjNmFkMDhkNTc0OGZmZDA2ODI4ZmMyZQ==; ab_ymg_result={"data":"8b0482c84aac99214162666d7e1afaa0d1dc4f2ceb93d9c2d79f6988326f3e9fa72d8b2523832a2be820da543f5063b02ae4d4dfe77dc237073db1ebaa5e5a3ee0510545dbf1856a101f9f89d1f7ed355e8776708b1fcf6b73d335f1332fcf88663c2fd3769cdc0846450007cf7ed195f22fc9bc2daa1fb07c9d6ae1b66e783c","key_id":"66","sign":"868c72da"}; _ga_06ZNKL8C2E=GS1.1.1715623398.1.1.1715625259.50.0.0"""
