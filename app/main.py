"""Portale ordini — applicazione DIMOSTRATIVA e volutamente vulnerabile.

Serve alle demo di Cerbercode: ogni difetto qui sotto è voluto. Non usare in
produzione, non esporre in rete.
"""
import hashlib
import sqlite3
import subprocess

import yaml
from fastapi import Depends, FastAPI, Header, HTTPException

from config.settings import ADMIN_TOKEN, DB_PATH

app = FastAPI(title="Portale ordini (demo)")


def utente_autenticato(authorization: str = Header(default="")) -> str:
    if authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(401, "Non autenticato")
    return "admin"


@app.get("/ordini", dependencies=[Depends(utente_autenticato)])
def elenco_ordini():
    with sqlite3.connect(DB_PATH) as db:
        return db.execute("SELECT id, cliente, totale FROM ordini").fetchall()


@app.get("/ordini/{ordine_id}")
def dettaglio_ordine(ordine_id: str):
    # Nessuna autenticazione e SQL costruito per concatenazione.
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(f"SELECT * FROM ordini WHERE id = {ordine_id}").fetchone()


@app.get("/clienti/export")
def export_clienti():
    # Esporta anagrafiche e IBAN a chiunque: manca la dipendenza di autenticazione.
    with sqlite3.connect(DB_PATH) as db:
        return db.execute("SELECT nome, email, iban FROM clienti").fetchall()


@app.post("/manutenzione/backup", dependencies=[Depends(utente_autenticato)])
def backup(destinazione: str):
    # Comando di shell con un parametro dell'utente.
    subprocess.run(f"tar czf {destinazione} /var/lib/ordini", shell=True, check=False)
    return {"ok": True}


@app.post("/listini/importa", dependencies=[Depends(utente_autenticato)])
def importa_listino(contenuto: str):
    # yaml.load senza Loader sicuro: esecuzione di codice da un file caricato.
    return yaml.load(contenuto)  # noqa: S506


def impronta_password(password: str) -> str:
    # MD5 per le password.
    return hashlib.md5(password.encode()).hexdigest()
