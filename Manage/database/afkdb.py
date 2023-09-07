import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["your_database_name"]  # Replace with your database name
afk_collection = db["afk_users"]

class AFK:
    def __init__(self, user_id, reason="", is_afk=True):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "reason": self.reason,
            "is_afk": self.is_afk,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["user_id"],
            reason=data["reason"],
            is_afk=data["is_afk"],
        )

    def __repr__(self):
        return f"afk_status for {self.user_id}"



def is_afk(user_id):
    return afk_collection.find_one({"user_id": user_id, "is_afk": True}) is not None

def check_afk_status(user_id):
    return afk_collection.find_one({"user_id": user_id})

def set_afk(user_id, reason=""):
    afk_data = AFK(user_id, reason, is_afk=True)
    afk_collection.replace_one({"user_id": user_id}, afk_data.to_dict(), upsert=True)

def rm_afk(user_id):
    result = afk_collection.delete_one({"user_id": user_id})
    return result.deleted_count > 0

def toggle_afk(user_id, reason=""):
    current_status = check_afk_status(user_id)
    if not current_status:
        afk_data = AFK(user_id, reason, is_afk=True)
        afk_collection.insert_one(afk_data.to_dict())
    else:
        afk_collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_afk": not current_status["is_afk"]}},
        )

def __load_afk_users():
    global AFK_USERS
    afk_users = afk_collection.find({"is_afk": True})
    AFK_USERS = {user["user_id"]: user["reason"] for user in afk_users}

__load_afk_users()