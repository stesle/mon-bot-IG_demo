
import os
import time
import yaml
import requests

from config import (
    BARRIER_EPIC,
    EXPIRY_DATE,
    DEFAULT_BARRIER_LEVEL,
    DEMO_MODE,
    DRY_RUN,
    DIRECTION,
    ORDER_SIZE,
    CURRENCY_CODE,
    GUARANTEED_STOP,
    STOP_DISTANCE,
    LIMIT_DISTANCE
)


class IGBot:

    def __init__(self):

        with open(
            "trading_demo_ig_bot.yml",
            "r",
            encoding="utf-8"
        ) as file:
            config = yaml.safe_load(file)

        ig = config["ig"]

        self.api_key = os.environ.get("IG_API_KEY")
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("IG_PASSWORD")

        if not all([self.api_key, self.username, self.password]):
            raise ValueError("Secrets IG manquants.")

        self.base_url = ig["base_url"].rstrip("/")
        self.session = requests.Session()

        self.cst = None
        self.security_token = None

    def headers(self, version="2"):

        h = {
            "X-IG-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": version
        }

        if self.cst:
            h["CST"] = self.cst
            h["X-SECURITY-TOKEN"] = self.security_token

        return h

    def connecter(self):

        url = f"{self.base_url}/session"

        payload = {
            "identifier": self.username,
            "password": self.password
        }

        r = self.session.post(
            url,
            json=payload,
            headers=self.headers("2"),
            timeout=15
        )

        if r.status_code != 200:
            raise RuntimeError(
                f"Connexion refusée : {r.status_code} {r.text}"
            )

        self.cst = r.headers.get("CST")
        self.security_token = r.headers.get("X-SECURITY-TOKEN")

        if not self.cst or not self.security_token:
            raise RuntimeError("Tokens IG manquants.")

        print("Connexion IG Démo réussie.")

    def verifier_marche(self):

        url = f"{self.base_url}/markets/{BARRIER_EPIC}"

        r = self.session.get(
            url,
            headers=self.headers("3"),
            timeout=15
        )

        if r.status_code != 200:
            raise RuntimeError(
                f"Erreur marché : {r.status_code} {r.text}"
            )

        data = r.json()

        instrument = data.get("instrument", {})
        snapshot = data.get("snapshot", {})

        print("\n--- MARCHÉ ---")
        print("Nom :", instrument.get("name"))
        print("EPIC :", instrument.get("epic"))
        print("Échéance :", instrument.get("expiry"))
        print("Type :", instrument.get("type"))
        print("Statut :", snapshot.get("marketStatus"))

        if instrument.get("epic") != BARRIER_EPIC:
            raise RuntimeError("EPIC incorrect.")

        if instrument.get("expiry") != EXPIRY_DATE:
            raise RuntimeError("Échéance incorrecte.")

        currencies = [
            c.get("code")
            for c in instrument.get("currencies", [])
        ]

        if CURRENCY_CODE not in currencies:
            raise RuntimeError("Devise non autorisée.")

        if snapshot.get("marketStatus") != "TRADEABLE":
            raise RuntimeError("Marché non négociable.")

        return data

    def construire_ordre(self):

        payload = {
            "epic": BARRIER_EPIC,
            "expiry": EXPIRY_DATE,
            "direction": DIRECTION,
            "size": float(ORDER_SIZE),
            "currencyCode": CURRENCY_CODE,
            "orderType": "MARKET",
            "forceOpen": True,
            "guaranteedStop": GUARANTEED_STOP
        }

        if GUARANTEED_STOP:
            if STOP_DISTANCE is None:
                raise ValueError(
                    "Stop Distance obligatoire pour ce réglage."
                )
            payload["stopDistance"] = float(STOP_DISTANCE)

        if LIMIT_DISTANCE is not None:
            payload["limitDistance"] = float(LIMIT_DISTANCE)

        return payload

    def passer_ordre(self):

        if not DEMO_MODE:
            raise RuntimeError("Compte réel interdit.")

        if DIRECTION not in ("BUY", "SELL"):
            raise ValueError("Direction incorrecte.")

        if ORDER_SIZE <= 0:
            raise ValueError("Taille invalide.")

        self.verifier_marche()

        payload = self.construire_ordre()

        print("\n--- ORDRE ---")
        print(payload)
        print("Barrière de référence :", DEFAULT_BARRIER_LEVEL)

        if DRY_RUN:
            print("SIMULATION : aucun ordre envoyé.")
            return None

        url = f"{self.base_url}/positions/otc"

        r = self.session.post(
            url,
            json=payload,
            headers=self.headers("2"),
            timeout=15
        )

        print("HTTP :", r.status_code)
        print("Réponse :", r.text)

        if r.status_code != 200:
            raise RuntimeError("Ordre refusé par IG.")

        reference = r.json().get("dealReference")

        if not reference:
            raise RuntimeError("Deal Reference absent.")

        return reference

    def confirmer_ordre(self, reference):

        url = f"{self.base_url}/confirms/{reference}"
        deadline = time.monotonic() + 15

        while time.monotonic() < deadline:

            r = self.session.get(
                url,
                headers=self.headers("1"),
                timeout=15
            )

            if r.status_code == 200:

                result = r.json()

                print("\n--- CONFIRMATION ---")
                print(result)

                return result

            if r.status_code not in (404, 429):
                raise RuntimeError(r.text)

            time.sleep(1)

        print("Confirmation non reçue.")
        print("Ne pas renvoyer automatiquement l'ordre.")

        return None


if __name__ == "__main__":

    bot = IGBot()

    try:
        bot.connecter()

        reference = bot.passer_ordre()

        if reference:
            bot.confirmer_ordre(reference)

    except Exception as e:
        print("ERREUR :", e)
