# Prompt à coller dans la tâche planifiée Claude

Chaque exécution démarre une session vierge : ce texte doit donc être autonome.

```
Tu exécutes la veille technologique quotidienne du dépôt GitHub Pogauh/veille_technologique.

1. Rattache le dépôt à la session avec un accès en écriture (push), puis clone-le
   (git clone --depth 1 https://github.com/Pogauh/veille_technologique).
2. Lis prompts/veille.md dans le dépôt et applique-le à la lettre : recherche,
   écriture de data/nouveautes.json, contrôle, fusion avec scripts/fusion.py,
   commit "Veille du AAAA-MM-JJ" et push sur main.
3. Si la validation ou la fusion échoue, ne pousse rien et explique l'erreur.
4. Réponds en 3 lignes maximum : éléments ajoutés, alerte sécurité éventuelle,
   succès du push.
```

Paramètres conseillés :
- **Fréquence** : du lundi au vendredi, vers 7h15 heure de Paris (`CRON_TZ=Europe/Paris 15 7 * * 1-5`).
- **Approbation** : automatique, sinon la tâche s'arrête au premier push.
- **Notification** : activée à la fin d'exécution pour repérer les échecs.
