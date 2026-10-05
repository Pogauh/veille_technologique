# Veille Java / Architecture hexagonale / C4

> Flux RSS : https://pogauh.github.io/veille_technologique/feed.xml


## 2026-10-05

**Résumé du jour.** Veille réduite : plusieurs sources primaires (openjdk.org, quarkus.io, inside.java) étaient inaccessibles depuis l'environnement. À retenir : Quarkus 4.0.0.Beta1 (Java 21 minimum) et deux JEP ciblant JDK 28 signalés par Baeldung, à confirmer. Aucune alerte de sécurité nouvelle vérifiée.


### Java

#### [JEP 540 : API JSON simple (incubation) ciblée pour JDK 28](https://www.baeldung.com/java-weekly-666)
*baeldung.com · publié le 2026-10-02 · confiance : faible · action : surveiller*

La newsletter Java Weekly n°666 signale que le JEP 540, une API JSON simple en incubation, a été ciblé pour JDK 28 le 2 octobre. Elle mentionne aussi le JEP 541, qui déprécie le port macOS/x64 en vue de sa suppression. Informations relayées par une source secondaire, non recoupées avec openjdk.org (inaccessible).

**Pourquoi c'est important :** Une API JSON dans le JDK pourrait à terme réduire la dépendance à Jackson ou Gson pour les cas simples.

#### [Quarkus 4.0.0.Beta1 : première bêta de la prochaine version majeure](https://github.com/quarkusio/quarkus/releases)
*github.com/quarkusio/quarkus · publié le 2026-10-01 · confiance : élevée · action : surveiller*

La page des releases GitHub de Quarkus liste une préversion 4.0.0.Beta1 publiée le 1er octobre. Elle fixerait Java 21 comme version minimale et intégrerait Hibernate 8 ainsi que Jakarta REST 4. Publication juste en dehors de la fenêtre de 72 h ; le détail des changements cassants n'a pas pu être lu sur le blog officiel.

**Pourquoi c'est important :** Une majeure avec baseline Java 21 impose de planifier dès maintenant la migration des applications Quarkus.


## 2026-10-02

**Résumé du jour.** Journée calme côté Java, hexagonal et C4 : aucune release majeure vérifiée dans la fenêtre. Deux avis de sécurité à sévérité élevée touchent jackson-core (DoS) ; les correctifs sont disponibles dans les branches 2.18, 2.21, 2.22 et 3.x.


### Sécurité

#### [jackson-core : consommation mémoire non bornée dans UTF8DataInputJsonParser (DoS)](https://github.com/advisories/GHSA-7hhh-6rmp-j9qf)
*GitHub Security Advisories · publié le 2026-10-01 · confiance : élevée · action : corriger*

CVE-2026-89425, gravité haute (CVSS 7.5). Le parseur DataInput construit le message d'erreur d'un jeton invalide sans respecter maxErrorTokenLength, d'où un risque d'OutOfMemoryError. Concerne jackson-core 2.8.0 à 2.18.10, 2.19.0 à 2.21.6, 2.22.0 à 2.22.2 et tools.jackson.core 3.x ; corrigé en 2.18.11, 2.21.7, 2.22.3, 3.1.7 et 3.2.3. L'avis a été publié upstream le 22/09 et référencé par GitHub le 01/10.

**Pourquoi c'est important :** Jackson est présent dans presque toutes les applications Spring : le risque de déni de service justifie une montée de version.

#### [jackson-core : ReDoS quadratique dans NumberInput.PATTERN_FLOAT](https://github.com/advisories/GHSA-p6pp-m3f8-5c89)
*GitHub Security Advisories · publié le 2026-10-01 · confiance : élevée · action : corriger*

CVE-2026-89407, gravité haute (CVSS 7.5). L'expression régulière de lecture des flottants a un comportement quadratique sur certaines entrées, et la limite appliquée est maxStringLength (20 M de caractères) plutôt que maxNumberLength. Concerne jackson-core 2.17.0 à 2.18.10, 2.19.0 à 2.21.6, 2.22.0 à 2.22.2 et 3.0.0 à 3.2.1 ; corrigé en 2.18.11, 2.21.7, 2.22.3, 3.1.7 et 3.2.2. Avis publié upstream le 22/09.

**Pourquoi c'est important :** Quelques requêtes JSON forgées peuvent saturer les threads d'un service exposé ; à traiter avec le correctif précédent.


## 2026-09-30

**Résumé du jour.** Journée calme. Le point hebdomadaire Spring recense une vague de jalons (Boot 4.2.0 M2, Security 7.2.0-M2, Data, Batch) et aucune correction de sécurité. Rien de nouveau n'a pu être vérifié en source primaire sur les thèmes hexagonal et C4 dans la fenêtre.


### Java

#### [Point hebdomadaire Spring : jalons Boot 4.2.0 M2, Security 7.2.0-M2 et Batch 6.1.0-M2](https://spring.io/blog/2026/09/29/this-week-in-spring-september-29th-2026)
*spring.io · publié le 2026-09-29 · confiance : élevée · action : surveiller*

La lettre hebdomadaire de Josh Long liste les jalons publiés les 24 et 25 septembre : Spring Boot 4.2.0 M2 (bundles SSL pour LDAP/LDAPS, conventions sémantiques OpenTelemetry, configuration de l'endpoint OTLP), Spring Security 7.2.0-M2, Spring Data 2026.1.0-M2, Spring Batch 6.1.0-M2 et Spring Cloud 2026.0.0-M1. Aucune correction de sécurité n'y est mentionnée.

**Pourquoi c'est important :** Permet d'anticiper la prochaine version mineure de Boot et de Security avant sa sortie finale.

