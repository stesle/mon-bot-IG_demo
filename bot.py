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
    # Utilisation de la bonne URL Dealing API
    url = f"{ig_conf['base_url']}/session"
    
    headers = {
        "X-IG-API-KEY": ig_conf["api_key"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "2"
    }
    
    payload = {
        "identifier": ig_conf["username"],
        "password": ig_conf["password"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        cst = response.headers.get("CST")
        x_security_token = response.headers.get("X-SECURITY-TOKEN")
        print("Connexion réussie à l'API IG (Mode Démo).")
        return cst, x_security_token
    else:
        raise Exception(f"Erreur de connexion : {response.status_code} - {response.text}")

def executer_ordre_knockout(config, cst, x_security_token):
    ig_conf = config["ig"]
    trading_conf = config["trading"]
    
    url = f"{ig_conf['base_url']}/positions/otc"
    
    headers = {
        "X-IG-API-KEY": ig_conf["api_key"],
        "CST": cst,
        "X-SECURITY-TOKEN": x_security_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "2"
    }
    
    payload = {
        "epic": trading_conf["epic"],
        "expiry": trading_conf["DATE"],
        "direction": trading_conf["direction"],
        "size": float(trading_conf["size"]),
        "barrier": float(trading_conf["BARRIER"]),
        "currencyCode": "EUR",
        "orderType": "MARKET",
        "forceOpen": True,
        "guaranteedStop": True,
        "level": "",              # Laissé vide pour un ordre au marché pur sur KO
        "stopDistance": None,     # Géré nativement par la barrière Knock-Out
        "limitLevel": None
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Statut passage d'ordre : {response.status_code}")
    print(f"Réponse ordre : {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Ordre transmis avec succès ! Deal Reference : {data.get('dealReference')}")
    else:
        print(f"Erreur lors du passage d'ordre : {response.text}")
    
    print(f"Statut passage d'ordre : {response.status_code}")
    print(f"Réponse ordre : {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Ordre transmis avec succès ! Deal Reference : {data.get('dealReference')}")
    else:
        print(f"Erreur lors du passage d'ordre : {response.text}")

if __name__ == "__main__":
    config = charger_configuration()
    cst, token = obtenir_tokens(config)
    executer_ordre_knockout(config, cst, token)
