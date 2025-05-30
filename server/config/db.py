
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://marangeles1306:M2c1AFlptCJprvAk@cluster0.jqgjd18.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

NOMBRE_DB = "library"
NOMBRE_COLECCION = "books"

client = MongoClient(MONGO_URI)
db = client[NOMBRE_DB]
book_collection = db[NOMBRE_COLECCION]

try:
    if NOMBRE_COLECCION not in db.list_collection_names():
        db[NOMBRE_COLECCION].insert_one({"_init": "colección creada automáticamente"})
        print(f"✅ Colección '{NOMBRE_COLECCION}' creada.")
    print(f"✅ Conectado a la base de datos '{NOMBRE_DB}' correctamente.")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
