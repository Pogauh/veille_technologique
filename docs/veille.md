# Veille Java / Architecture hexagonale / C4

> Flux RSS : https://pogauh.github.io/veille_technologique/feed.xml


## 2026-10-26

**Résumé du jour.** Week-end calme : l'actualité se limite aux publications Spring du 23 octobre. Spring AI 2.1.0-RC1 apporte la mémoire de session et la confirmation des appels d'outils, avec des dépréciations à anticiper. Spring Boot 4.0.9 et Spring Cloud 2025.1.4 sont des versions de maintenance. Aucune alerte de sécurité vérifiée dans la fenêtre.


### Java

#### [Spring AI 2.1.0-RC1 : mémoire de session, confirmation des outils et dépréciations](https://spring.io/blog/2026/10/23/spring-ai-2-1-0-RC1-available-now)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : tester*

La première release candidate de Spring AI 2.1.0 introduit une API de session stockant les conversations sous forme de journal d'événements, avec un dépôt JDBC, ainsi qu'une confirmation avant exécution des outils. L'API ChatMemory est dépréciée pour suppression en 3.0.0, et BedrockChatOptions.requestParameters change de type. La version corrective 2.0.2 est publiée en parallèle.

**Pourquoi c'est important :** Les équipes utilisant ChatMemory ou Bedrock doivent planifier la migration et tester la RC avant la version finale.

#### [Spring Boot 4.0.9 : version corrective avec 99 corrections de bugs](https://spring.io/blog/2026/10/23/spring-boot-4-0-9-available-now)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : migrer*

Spring Boot 4.0.9 est disponible sur Maven Central avec 99 corrections de bugs, des améliorations de documentation et des montées de version de dépendances. L'annonce ne mentionne aucun CVE.

**Pourquoi c'est important :** Mise à jour de routine à appliquer sur les projets en branche 4.0, dont le support open source se termine fin 2026 selon les sources secondaires.

#### [Spring Cloud 2025.1.4 (Northfields) publiée, basée sur Spring Boot 4.0.9](https://spring.io/blog/2026/10/23/spring-cloud-2025-1-4-has-been-released)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : migrer*

La release train Spring Cloud 2025.1.4 est disponible, construite sur Spring Boot 4.0.9 et compatible avec Boot 4.1.2. Elle corrige des bugs dans l'ensemble des projets, avec par exemple Config 5.0.6 et Function 5.0.5, la plupart des autres modules passant en 5.0.4.

**Pourquoi c'est important :** À aligner avec la mise à jour de Spring Boot 4.0.9 pour garder des versions cohérentes dans le BOM.


## 2026-10-24

**Résumé du jour.** Journée calme côté Java : la publication du 23 octobre de Spring Boot 4.2.0-RC1 et de la correction 4.1.2 est l'essentiel à retenir. Aucune alerte de sécurité nouvelle vérifiée. Rien de notable sur l'architecture hexagonale ni sur C4 dans la fenêtre.


### Java

#### [Spring Boot 4.2.0-RC1 : builder Buildpacks Ubuntu 26.04 et démarrage accéléré](https://spring.io/blog/2026/10/23/spring-boot-4-2-0-RC1-available-now)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : tester*

Première release candidate de Spring Boot 4.2 avec 113 améliorations. Le builder Buildpacks par défaut passe sur Ubuntu 26.04, le migrateur de propriétés peut faire échouer l'application en cas d'erreur ou d'avertissement, et la recherche de classes et ressources dans les jars exécutables est plus rapide.

**Pourquoi c'est important :** Permet d'anticiper la migration vers 4.2 et de tester l'impact sur les images conteneur et le démarrage.

#### [Spring Boot 4.1.2 et 4.0.9 : versions correctives publiées](https://spring.io/blog/2026/10/23/spring-boot-4-1-2-available-now)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : migrer*

Spring Boot 4.1.2 apporte 126 corrections de bogues, mises à jour de documentation et de dépendances ; 4.0.9 est publiée le même jour. L'annonce ne mentionne aucun correctif de sécurité ni CVE ; le détail se trouve dans les notes de version GitHub.

**Pourquoi c'est important :** Mise à jour de routine à intégrer dans les branches 4.1 et 4.0 en production.

#### [Spring Cloud 2026.0.0-RC1 (Paddington) et 2025.1.4 disponibles](https://spring.io/blog/2026/10/23/spring-cloud-2026-0-0-RC1-has-been-released)
*spring.io · publié le 2026-10-23 · confiance : moyenne · action : surveiller*

Le train de versions Spring Cloud 2026.0.0 atteint sa première release candidate, en parallèle de la version corrective 2025.1.4 (Northfields). Le contenu détaillé n'a pas été relu en profondeur : se référer à l'annonce.

**Pourquoi c'est important :** À suivre pour les équipes utilisant Spring Cloud, en lien avec Spring Boot 4.2.


## 2026-10-23

**Résumé du jour.** Journée calme : seule nouveauté vérifiée en source primaire, la sortie de Spring Batch 6.1.0-RC1 et du correctif 6.0.6. Le CPU Oracle d'octobre (Java SE) a déjà été publié dans une édition précédente.


### Java

#### [Spring Batch 6.1.0-RC1 et 6.0.6 disponibles sur Maven Central](https://spring.io/blog/2026/10/22/spring-batch-6)
*spring.io · publié le 2026-10-22 · confiance : élevée · action : tester*

La RC1 de Spring Batch 6.1 apporte l'annotation @JobParameter, un PageableItemReader basé sur Pageable de Spring Data, un support JSON indépendant de la bibliothèque (JsonLineAggregator) et des DAO JDBC passés à JdbcClient, dont les constructeurs sans argument disparaissent. Moins de requêtes SQL au redémarrage de jobs ; une partie de ces gains figure aussi dans le correctif 6.0.6.

**Pourquoi c'est important :** Les projets batch peuvent tester la RC1 et anticiper la rupture sur les constructeurs des DAO JDBC.


## 2026-10-21

**Résumé du jour.** Oracle a publié le 20 octobre 2026 sa mise à jour critique trimestrielle, avec 55 correctifs pour Java SE. Aucune autre nouveauté notable n'a pu être vérifiée dans la fenêtre de veille.


### Sécurité

#### [Oracle Critical Patch Update d'octobre 2026 : 55 correctifs pour Java SE](https://www.oracle.com/security-alerts/cpuoct2026.html)
*oracle.com · publié le 2026-10-20 · confiance : moyenne · action : corriger*

Le CPU d'octobre 2026 corrige 55 vulnérabilités dans Java SE, dont 49 exploitables à distance sans authentification, avec un score CVSS v3.1 maximal de 7.5 (aucune faille critique). Les branches 8, 11, 17, 21, 25 et 27 sont concernées. Les numéros de build exacts diffèrent selon les sources consultées (l'advisory et les notes de version cloud) : page non ouverte directement, chiffres à confirmer.

**Pourquoi c'est important :** Les JDK en production doivent être mis à jour vers les builds d'octobre ; les chiffres sont à confirmer sur la page Oracle.


## 2026-10-06

**Résumé du jour.** Veille réduite : openjdk.org, inside.java et blogs.oracle.com sont inaccessibles depuis l'environnement. À retenir : Spring passe à un rythme de correctifs mensuel unique (« Patch Thursday », premier jalon le 22 octobre) face à la hausse des CVE. Oracle annoncerait aussi un changement de licence pour les mises à jour d'Oracle JDK 21 dès le CPU d'octobre, à confirmer. Aucune alerte de sécurité nouvelle vérifiée.


### Java

#### [Oracle JDK 21 : mises à jour sous licence OTN dès le CPU d'octobre 2026](https://blogs.oracle.com/java/jdk-21-approaches-end-of-permissive-license)
*blogs.oracle.com · publié le 2026-10-05 · confiance : faible · action : surveiller*

Selon un article du blog Java d'Oracle relevé via un moteur de recherche (page non lisible directement), les mises à jour d'Oracle JDK 21 publiées à partir du CPU d'octobre 2026 passeraient sous licence Java SE OTN, comme Java 8, 11 et 17. Oracle recommanderait JDK 25 ou ultérieur pour rester sous licence permissive. Date de publication et détails non vérifiés ; les distributions OpenJDK (Temurin, Corretto) ne sont pas concernées par cette annonce.

**Pourquoi c'est important :** Les équipes qui utilisent Oracle JDK 21 doivent vérifier leur licence ou migrer vers JDK 25 ou une distribution OpenJDK.


### Sécurité

#### [Spring adopte un « Patch Thursday » mensuel face à l'afflux de CVE](https://spring.io/blog/2026/09/21/releasing-spring-for-modern-challenges/)
*spring.io · publié le 2026-09-21 · confiance : élevée · action : surveiller*

L'équipe Spring regroupe désormais ses correctifs sur un seul jour par mois, le jeudi suivant le troisième lundi. Elle explique avoir reçu près de 80 signalements de sécurité par mois depuis mars et corrigé plus de 160 CVE ; la page des avis de sécurité est refondue avec filtres par gravité et projet. Le premier lot de correctifs est annoncé pour le 22 octobre 2026. Publication hors fenêtre de 72 h, retenue comme article de fond récent.

**Pourquoi c'est important :** Les équipes doivent caler leurs montées de version Spring sur ce rythme mensuel et s'attendre à un volume élevé de correctifs de sécurité.


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

