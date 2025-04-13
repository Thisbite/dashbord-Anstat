from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Créer toutes les tables définies dans models.py
    db.create_all()
    
    # Vérifier les tables créées
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if tables:
        print("✅ Tables créées avec succès :")
        for table in tables:
            print(f"- {table}")
    else:
        print("⚠️ Aucune table créée ou trouvée dans la base de données.")