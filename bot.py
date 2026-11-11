import os
import yaml
import requests

def charger_configuration():
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(dossier_script, "trading_demo_ig_bot.yml")
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def obtenir_tokens(config):
    ig_conf = config["ig"]
    url = f"{ig_conf['base_url']}/session"
    
    headers = {
        "X-IG-API-KEY": ig_conf["api_key"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "2"  # <-- La virgule manquante était ici
    }
    
    payload = {
        "identifier": ig_conf["username"],
        "password": ig_conf["password"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Statut HTTP reçu : {response.status_code}")
    print(f"Réponse brute : {response.text}")
    
    if response.status_code == 200:
        cst = response.headers.get("CST")
        x_security_token = response.headers.get("X-SECURITY-TOKEN")
        print("Connexion réussie à l'API IG (Mode Démo).")
        return cst, x_security_token
    else:
        raise Exception(f"Erreur de connexion : {response.status_code} - {response.text}")

if __name__ == "__main__":
    config = charger_configuration()
    cst, token = obtenir_tokens(config)
