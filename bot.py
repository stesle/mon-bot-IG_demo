# bot.py
import requests
from config import (
    IG_API_KEY,
    IG_USERNAME,
    IG_PASSWORD,
    IG_BASE_URL,
    BARRIER_EPIC,
    EXPIRY_DATE,
    DEFAULT_BARRIER_LEVEL,
)

def obtenir_tokens():
    """Authentification auprès de l'API IG pour récupérer les jetons de session."""
    url = f"{IG_BASE_URL}/session"
    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "identifier": IG_USERNAME,
        "password": IG_PASSWORD
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        # Les tokens d'authentification sont renvoyés dans les en-têtes (headers)
        cst = response.headers.get("CST")
        x_security_token = response.headers.get("X-SECURITY-TOKEN")
        print("Connexion réussie à l'API IG (Mode Démo).")
        return cst, x_security_token
    else:
        raise Exception(f"Erreur de connexion : {response.status_code} - {response.text}")

def executer_ordre_knockout(cst, x_security_token):
    """Passe un ordre d'achat sur l'option Knock-Out cible."""
    url = f"{IG_BASE_URL}/positions/v2"
    
    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": x_security_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Corps de la requête adapté aux options Knock-Out
    order_payload = {
        "epic": BARRIER_EPIC,
        "expiry": EXPIRY_DATE,
        "direction": "BUY",              # "BUY" pour un Call/Bull, "SELL" pour un Put/Bear
        "size": 1.0,                     # Taille du contrat
        "orderType": "MARKET",           # Ordre au marché
        "guaranteedStop": True,          # Risque limité inhérent aux barrières
        "barrier": DEFAULT_BARRIER_LEVEL, # Niveau de Knock-Out cible
        "currencyCode": "EUR"
    }
    
    print(f"Envoi de l'ordre sur l'EPIC : {BARRIER_EPIC} (Barrière : {DEFAULT_BARRIER_LEVEL})")
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
        # 1. Connexion et récupération des tokens
        cst_token, security_token = obtenir_tokens()
        
        # 2. Exécution de l'ordre sur le produit barrière
        executer_ordre_knockout(cst_token, security_token)
        
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
