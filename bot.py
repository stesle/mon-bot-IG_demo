import os
import sys
from trading_ig import IGService
from trading_ig.rest import IGException

def main():
    # 1. Récupération sécurisée des identifiants (Variables d'environnement / Secrets GitHub)
    username = os.environ.get("IG_USERNAME")
    password = os.environ.get("IG_PASSWORD")
    api_key = os.environ.get("IG_API_KEY")

    # Vérification que les secrets sont bien présents
    if not username or not password or not api_key:
        print("Erreur : Les identifiants IG (Username, Password, API Key) sont manquants dans les variables d'environnement.")
        sys.exit(1)

    print("Tentative de connexion à l'API IG (Compte DEMO)...")

    # 2. Initialisation de la session IG
    ig_service = IGService(
        username=username,
        password=password,
        api_key=api_key,
        acc_type="DEMO"  # Forcé en DEMO pour vos tests
    )

    try:
        # Création de la session active
        ig_service.create_session()
        print("Connexion réussie avec succès !")

        # 3. Exemple de logique pour les Produits Barrières
        # Remplacer cet EPIC par l'EPIC réel du produit barrière souhaité trouvé sur la plateforme IG
        epic_barriere = "IX.D.DAX.DAILY.IP"  
        
        print(f"Analyse / Recherche de l'actif ou passage d'ordre sur l'EPIC : {epic_barriere}")

        # Exemple de passage d'ordre (décommentez et adaptez selon vos paramètres de test)
        # order = ig_service.create_working_order(
        #     currency_code="EUR",
        #     direction="BUY",
        #     epic=epic_barriere,
        #     expiry="DF",
        #     force_open=True,
        #     guaranteed_stop=True,
        #     level=None,  # Ordre au marché
        #     limit_level=None,
        #     order_type="MARKET",
        #     size=1.0,    # Taille de position minimale pour tester
        #     stop_level=None,
        #     time_in_force="FILL_OR_KILL"
        # )
        # print(f"Ordre passé avec succès ! Référence : {order}")

    except IGException as e:
        print(f"Erreur lors de la communication avec l'API IG : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
