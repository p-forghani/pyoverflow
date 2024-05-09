import pymongo
from loguru import logger


conn = pymongo.MongoClient("localhost", port=27017)
database = conn.pyoverflow

database.users.drop()
database.questions.drop()
logger.info("Database created succesfully.")