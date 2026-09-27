# Portale ordini — applicazione dimostrativa per Cerbercode

**Volutamente vulnerabile.** Serve a mostrare dal vivo una scansione di
[Cerbercode](https://objlab.it/cerbercode): ogni difetto è voluto. Non usare
in produzione e non esporre in rete. Nomi, dati e credenziali sono di fantasia.

Che cosa trova Cerbercode, in circa un minuto:

| Difetto | Dove | Chi lo trova |
|---|---|---|
| Rotte senza autenticazione (export clienti con IBAN, dettaglio ordine) | `app/main.py` | web-authz |
| SQL costruito per concatenazione | `app/main.py` | Bandit, Semgrep |
| Comando di shell con input dell'utente | `app/main.py` | Bandit, Semgrep |
| `yaml.load` non sicuro, MD5 per le password | `app/main.py` | Bandit |
| Token e password nel codice | `config/settings.py` | gitleaks, detect-secrets |
| Dipendenze con CVE note (PyYAML, requests, Jinja2, urllib3) | `requirements.txt` | pip-audit, osv-scanner, Grype |
| Container eseguito come root, immagine non fissata | `Dockerfile` | Checkov |

Licenza: MIT. © Objlab S.r.l.
