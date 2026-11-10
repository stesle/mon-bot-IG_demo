import yaml
import requests

def charger_configuration(chemin_fichier="trading_demo_ig_bot.yml"):
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def obtenir_tokens(config):
    ig_conf = config["ig"]
    url = f"{ig_conf['base_url']}/session"
    headers = {
        "X-IG-API-KEY": ig_conf["208c91fdac17ebce7fcd019f89ff1e465864b6c3"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "identifier": ig_conf["steveL76"],
        "password": ig_conf["steveL76**"]
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

def executer_ordre_knockout(config, cst, x_security_token):
    ig_conf = config["ig"]
    trading_conf = config["trading"]
    
    url = f"{ig_conf['base_url']}/positions/v2"
    
    headers = {
        "X-IG-API-KEY": ig_conf["208c91fdac17ebce7fcd019f89ff1e465864b6c3"],
        "CST": cst,
        "X-SECURITY-TOKEN": x_security_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    order_payload = {
        "epic": trading_conf["IX.D.DAX.OPTCALL.IP"],
        "expiry": trading_conf["FEB-27"],
        "direction": trading_conf["BUY"],
        "size": trading_conf["1.2"],
        "orderType": "MARKET",
        "guaranteedStop": True,
        "barrier": trading_conf["25750"],
        "currencyCode": "EUR"
    }
    
    print(f"Envoi de l'ordre sur l'EPIC : {trading_conf['epic']} (Barrière : {trading_conf['25750']})")
    response = requests.post(url, json=order_payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Ordre transmis avec succès ! Deal Reference : {data.get('dealReference')}")
        return data
    else:
        print(f"Erreur lors du passage d'ordre : {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        config_data = charger_configuration("trading_demo_ig_bot.yml")
        cst_token, security_token = obtenir_tokens(config_data)
        executer_ordre_knockout(config_data, cst_token, security_token)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
