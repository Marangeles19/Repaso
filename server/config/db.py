from pymongo import MongoClient

MONGO_URI = "mongodb+srv://marangeles1306:M2c1AFlptCJprvAk@cluster0.jqgjd18.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
NOMBRE_DB = "library"

client = MongoClient(MONGO_URI)
db = client[NOMBRE_DB]

# Colecciones
book_collection = db["books"]
cedulas_collection = db["cedulas"]
rucs_collection = db["rucs"]

try:
    for col in ["books", "cedulas", "rucs"]:
        if col not in db.list_collection_names():
            db[col].insert_one({"_init": f"{col} creada automáticamente --"})
            print(f"✅ Colección '{col}' creada.")
    print(f"✅ Conectado a la base de datos '{NOMBRE_DB}' correctamente.")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
