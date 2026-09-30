# Veille technologique : Java, architecture hexagonale, C4

Veille quotidienne automatisée, lue dans **Inoreader** via un flux RSS.

```
Tâche planifiée Claude ──► data/nouveautes.json ──► scripts/fusion.py ──► data/veille.json (base cumulée)
   (recherche web)          (écrit par l'agent)     (valide + dédoublonne)  docs/feed.xml   → Inoreader
                                                                            docs/index.html → page web
                                                                            docs/veille.md  → lecture Markdown
```

| Fichier | Écrit par | Rôle |
|---|---|---|
| `prompts/veille.md` | vous | Consignes de l'agent |
| `prompts/tache_planifiee.md` | vous | Texte à coller dans la tâche planifiée |
| `schema/nouveautes.schema.json` | vous | Contrat du fichier produit par l'agent |
| `data/nouveautes.json` | l'agent | Nouveautés du jour |
| `data/veille.json` | le script | Base cumulée |
| `docs/*` | le script | Flux RSS, page web, Markdown |

## Mise en place (une seule fois)

### 1. Publier le flux avec GitHub Pages
1. Dans GitHub : **Settings → Pages**.
2. Source : *Deploy from a branch*, branche `main`, dossier `/docs`.
3. Le flux sera disponible à `https://pogauh.github.io/veille_technologique/feed.xml`.

> Inoreader doit pouvoir lire le flux sans authentification : le dépôt (ou au minimum Pages) doit donc être **public**. Le contenu ne contient que des liens et résumés d'articles publics. Si le dépôt doit rester privé, Pages privé exige un plan GitHub payant.

### 2. Ajouter le flux dans Inoreader
1. **Ajouter un contenu → Flux / URL** et coller l'URL du flux ci-dessus.
2. Placer le flux dans un dossier « Veille Java » et activer, si souhaité, les notifications ou une règle sur le tag `Sécurité`.
3. Astuce : chaque article porte des catégories (`Java`, `Hexagonal`, `C4`, `Sécurité`, nom de la source) utilisables dans les filtres et règles Inoreader. Une entrée « Synthèse du jour » est publiée chaque matin en tête.

### 3. Créer la tâche planifiée Claude
Suivre `prompts/tache_planifiee.md` (du lundi au vendredi, vers 7h15 Paris, approbation automatique).

## Utilisation manuelle

```bash
python3 scripts/fusion.py --check   # valider data/nouveautes.json sans rien écrire
python3 scripts/fusion.py           # fusionner et régénérer docs/
python3 scripts/fusion.py --urls    # URLs déjà publiées (60 derniers jours)
```

Codes de sortie : `0` OK, `2` fichier invalide (rien n'est modifié). Bibliothèque standard uniquement (Python 3.9+).

## Personnalisation
- URL publique du flux : constante `SITE_URL` de `scripts/fusion.py` (ou variable d'environnement `FEED_BASE_URL`).
- Nombre d'éléments dans le flux : `FEED_MAX_ITEMS` (100 par défaut).
- Thèmes et sources : `prompts/veille.md` (si vous ajoutez un thème, ajoutez-le aussi dans `schema/` et dans `THEMES` de `fusion.py`).

## Dépannage
| Symptôme | Cause probable |
|---|---|
| Aucun commit un jour de semaine | Tâche en échec ou en attente d'approbation : vérifier son historique |
| Push refusé | Dépôt rattaché en lecture seule à la session : redonner l'accès en écriture |
| Inoreader n'affiche rien de nouveau | Pages pas encore redéployé (quelques minutes) ou flux non rafraîchi : forcer la mise à jour du flux |
| `ERREUR : nouveautes.json invalide` | L'agent a produit un JSON hors schéma : le message liste les champs fautifs |
