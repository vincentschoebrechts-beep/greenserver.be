# greenserver.be

Site statique en anglais, publié par GitHub Pages depuis le dossier `docs/` de la branche `main`. Aucune étape de construction : ce qui est dans `docs/` est ce qui est en ligne. Le reste du dépôt (ce fichier, `outils/`) n'est pas publié.

## Contenu de `docs/`

| Adresse | Fichier | Rôle |
|---|---|---|
| `/` | `index.html` | Accueil : les outils |
| `/pc-time/` | `pc-time/index.html` | Présentation de PC Time |
| `/update/` | `update/` | **Utilisée par le bouton « Mise à jour » de PC Time.** Téléchargement de la dernière version |
| `/velo-train/` | `velo-train/index.html` | Présentation de Bike + Train |
| `/smtp/` | `smtp/index.html` + `assets/smtp.js` | Testeur SMTP (DNS du domaine expéditeur, commandes de test) |
| `/ewon/` | `ewon/index.html` + `assets/ewon.js` | eWon Backup Cleaner : remplace les mots de passe chiffrés `#_6_` d'un backup eWon par un mot de passe en clair (tout se fait dans le navigateur) |
| `/files/` | `files/` | Documents chiffrés, accessibles par mot de passe |
| `/sap/`, `/sap/fr/` | `sap/` | Formation gratuite « SAP from the shop floor / SAP vu de l'atelier » : 10 leçons, annexe, QCM final |
| `/share/` | `share/index.html` + `assets/share.js` | Panier commun (EN/FR) : dépôt et téléchargement de fichiers avec un mot de passe commun. Les fichiers sont chez Cloudflare, voir plus bas |
| toute adresse inconnue | `404.html` | Page d'erreur |

`assets/` contient la feuille de style, l'icône et les polices (Barlow, IBM Plex Mono, licence SIL OFL), sans appel à Google Fonts. `CNAME` contient le domaine, `.nojekyll` dit à GitHub de servir les fichiers tels quels.

## Publier des documents protégés

Les documents ne sont jamais poussés en clair : le dépôt est public.

```
pip install cryptography
python outils/chiffrer_documents.py "C:\chemin\vers\dossier_hors_depot"
git add docs/files
git commit -m "Documents"
git push
```

Les sous-dossiers du dossier donné (un niveau) deviennent des rubriques sur la page. Le script demande le mot de passe et reconstruit `docs/files/data/` à partir du dossier donné : pour ajouter ou retirer un document, ou changer le mot de passe, on le relance avec le dossier complet.

## DNS

Le domaine est chez EasyHost. Les enregistrements A, AAAA et `www` pointent vers GitHub Pages. **Ne pas toucher aux enregistrements SMTP2GO** (CNAME `em…`, `s…._domainkey`, DMARC) : ils servent aux mails de l'automate.

## Formation SAP

Les pages de `docs/sap/` et la banque de questions `docs/assets/sap-questions.js` sont générées : ne les modifiez pas à la main. Le contenu se trouve dans `outils/sap_course/` (`content_en.py`, `content_fr.py`, `questions.py`). Après une modification :

```
python outils/sap_course/build.py
git add docs outils
git commit -m "Formation SAP : …"
git push
```

## Panier commun (`/share/`)

La page est statique, mais les fichiers ne peuvent pas être stockés sur GitHub Pages. Ils vont dans un Worker Cloudflare gratuit avec un espace KV : 25 Mo par fichier, 1 Go au total, environ 1000 dépôts par jour. Le code du Worker est dans `outils/panier-commun/worker.js`. Le mot de passe est un secret Cloudflare : il n'est jamais dans le dépôt, et on le change sans toucher au code.

Mise en place, une seule fois, depuis le tableau de bord Cloudflare (compte gratuit, pas de carte bancaire) :

1. **Storage & Databases > KV > Create** : un espace nommé `panier-commun`.
2. **Compute (Workers) > Create > Start with Hello World** : nommer le Worker `panier-commun`, **Deploy**, puis **Edit code** : remplacer tout le code par le contenu de `outils/panier-commun/worker.js`, **Deploy**.
3. Dans le Worker, **Settings > Bindings > Add > KV namespace** : nom de variable `FILES`, espace `panier-commun`.
4. **Settings > Variables and Secrets > Add**, type **Secret** :
   - `PASSWORD` = le mot de passe commun (`1234`) ;
   - `ADMIN_PASSWORD` = un autre mot de passe, pour supprimer des fichiers depuis la page (« Gérer »). Sans lui, la suppression est désactivée.
5. Copier l'adresse du Worker (`https://panier-commun.<votre-sous-domaine>.workers.dev`) dans `docs/share/index.html`, attribut `data-api` de `<section id="sh">`, puis commit et push.

Les fichiers n'expirent pas : on les supprime depuis la page (« Gérer », avec `ADMIN_PASSWORD`) ou dans Cloudflare (**KV > panier-commun > KV Pairs**). Pour changer le mot de passe commun : modifier le secret `PASSWORD` dans Cloudflare, rien à changer ici.

