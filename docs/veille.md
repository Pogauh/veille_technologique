# Veille Java / Architecture hexagonale / C4

> Flux RSS : https://pogauh.github.io/veille_technologique/feed.xml


## 2026-11-25

**Résumé du jour.** Journée calme : un seul élément retenu dans la fenêtre de 24 h. Spring AI 2.1 permet de mettre en pause une boucle d'appels d'outils pour obtenir une validation humaine, puis de la reprendre après un redémarrage. Aucune nouvelle alerte de sécurité Spring publiée depuis le 19 novembre ; inside.java et InfoQ n'étaient pas accessibles depuis cet environnement.


### Java

#### [Spring AI 2.1 : validation humaine des appels d'outils, avec reprise après redémarrage](https://spring.io/blog/2026/11/24/spring-ai-tool-call-confirmation-park-resume)
*spring.io · publié le 2026-11-24 · confiance : élevée · action : lire*

Spring AI 2.1 permet de marquer certains outils comme nécessitant une confirmation : la boucle d'appels s'interrompt uniquement sur ces appels et les renvoie à l'application. L'extension communautaire Spring AI Session Extensions (version 0.11.0, première version) enregistre cette pause dans le journal de session, de sorte qu'une autre instance puisse reprendre avec une décision d'autorisation ou de refus.

**Pourquoi c'est important :** Utile aux équipes qui exposent des actions sensibles à des agents IA et veulent un circuit d'approbation durable.


## 2026-11-23

**Résumé du jour.** Week-end calme côté publications. Spring Security publie deux correctifs à priorité haute (WebAuthn et RSocket) et Spring Data Elasticsearch corrige une injection SpEL. Spring Boot 4.0.10 est disponible. Les dates indiquées sont celles des sources.


### Java

#### [Spring Boot 4.0.10 disponible](https://spring.io/blog/2026/11/20/spring-boot-4-0-10-available-now)
*spring.io · publié le 2026-11-20 · confiance : élevée · action : migrer*

La version corrective 4.0.10 regroupe 97 corrections de bugs, améliorations de documentation et montées de dépendances, et se trouve sur Maven Central. L'annonce ne mentionne aucun CVE ; le détail est dans les notes de version GitHub.

**Pourquoi c'est important :** Permet de rester sur la branche 4.0 à jour, en vérifiant que la version de Spring Security embarquée contient les correctifs de la semaine.


### Sécurité

#### [Spring Data Elasticsearch : injection SpEL dans les requêtes @Query](https://spring.io/security/cve-2026-123886)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

CVE-2026-123886, gravité haute : dans les méthodes @Query en chaîne, les arguments sont insérés avant l'évaluation SpEL, ce qui permet d'exécuter du code avec une entrée non fiable. Versions touchées : 6.1.0 à 6.1.2 et 6.0.0 à 6.0.8. Correctifs : 6.1.3 et 6.0.9. À défaut, rejeter les entrées contenant #{ ou utiliser CriteriaQuery/NativeQuery.

**Pourquoi c'est important :** Exécution de code possible sur les applications qui passent des saisies utilisateur à des @Query Elasticsearch.

#### [Spring Security : le compteur de signature WebAuthn n'est pas contrôlé](https://spring.io/security/cve-2026-59330)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

CVE-2026-59330, gravité haute : un défaut interne empêche de transmettre le compteur stocké à la bibliothèque de vérification, si bien qu'un authentificateur cloné n'est pas détecté. Versions touchées : Spring Security 7.1.0 à 7.1.2 et 7.0.0 à 7.0.8. Correctifs open source : 7.1.3 et 7.0.9.

**Pourquoi c'est important :** Une passkey ou clé clonée pourrait continuer à authentifier un utilisateur sans être rejetée.

#### [Spring Security : déni de service via l'authentification Basic RSocket](https://spring.io/security/cve-2026-59331)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

CVE-2026-59331, gravité haute : BasicAuthenticationPayloadExchangeConverter alloue de la mémoire selon une longueur non validée, et une seule trame forgée peut épuiser la mémoire du serveur. Touche les applications utilisant le support RSocket avec le convertisseur par défaut. Correctifs open source : 7.1.3 et 7.0.9 ; les branches plus anciennes (6.x, 5.x) ne sont corrigées que pour le support entreprise.

**Pourquoi c'est important :** Seules les applications RSocket exposées sont concernées, mais l'attaque ne demande ni privilège ni interaction.


## 2026-11-22

**Résumé du jour.** Alerte critique : une faille d'exécution de code à distance (CVE-2026-59273) touche Spring Security via ELRequestMatcher ; mettre à jour vers 7.1.3 ou 7.0.9. Rien d'autre de vérifié aujourd'hui (dimanche).


### Sécurité

#### [Spring Security : exécution de code à distance via ELRequestMatcher (CVE-2026-59273)](https://spring.io/security/cve-2026-59273/)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

Faille critique (vecteur réseau, sans authentification) dans ELRequestMatcher de Spring Security : si une application lie une entrée externe à une propriété de ce type, elle est évaluée comme expression SpEL. Versions touchées : 7.1.0 à 7.1.2, 7.0.0 à 7.0.8, 6.5.0 à 6.5.12, 6.4.0 à 6.4.19, 5.8.0 à 5.8.28, 5.7.26 et antérieures. Correctifs open source : 7.1.3 et 7.0.9 ; les branches plus anciennes ne sont corrigées que via le support Enterprise.

**Pourquoi c'est important :** Risque d'exécution de code à distance : vérifier l'usage d'ELRequestMatcher et mettre à jour les projets Spring Security.


## 2026-11-21

**Résumé du jour.** Le 20 novembre, Spring publie Spring Cloud 2026.0.0 (base Spring Boot 4.2.0) et Spring AI 2.1.0, deux versions qui embarquent des correctifs de sécurité modifiant des comportements par défaut. Spring Boot 4.1.3 et 4.0.10 sont aussi disponibles. Rien de notable détecté côté architecture hexagonale ou C4 sur la fenêtre.


### Java

#### [Spring Boot 4.1.3 et 4.0.10 disponibles](https://spring.io/blog/2026/11/20/spring-boot-4-1-3-available-now)
*spring.io · publié le 2026-11-20 · confiance : élevée · action : migrer*

Spring Boot 4.1.3 regroupe 112 corrections de bugs, améliorations de documentation et mises à jour de dépendances. L'annonce ne mentionne ni CVE ni correctif de sécurité, et ne précise pas de notes de migration.

**Pourquoi c'est important :** Mise à jour de maintenance à intégrer dans le cycle normal de patch des branches 4.1 et 4.0.


### Sécurité

#### [Spring Cloud 2026.0.0 (Paddington) : correctifs de sécurité aux effets sur les comportements par défaut](https://spring.io/blog/2026/11/20/spring-cloud-2026-0-0-has-been-released)
*spring.io · publié le 2026-11-20 · confiance : élevée · action : tester*

La release train s'appuie sur Spring Boot 4.2.0 et intègre plusieurs correctifs de CVE qui changent les valeurs par défaut : le filtre WebSocket de Gateway impose désormais la même origine, et Config Server valide les clés d'hôte SSH des dépôts Git. Les numéros de CVE ne sont pas détaillés dans l'annonce : consulter les avis individuels.

**Pourquoi c'est important :** Ces changements de comportement peuvent casser des routes WebSocket ou des dépôts Git de configuration lors de la montée de version.

#### [Spring AI 2.1.0 : 13 CVE corrigées, MCP sans état, nouvelle API de sessions](https://spring.io/blog/2026/11/20/spring-ai-2-1-0-GA-available-now)
*spring.io · publié le 2026-11-20 · confiance : élevée · action : corriger*

La version 2.1.0 (sur Spring Boot 4.2) corrige 13 CVE, reprises dans la 2.0.3 pour la branche 2.0. Certains correctifs changent le comportement depuis 2.0.2 ou antérieur : SemanticCacheScopeResolver requis, limite de 10 millions de caractères pour l'extraction Tika, échappement plus strict des filtres Typesense. Gravité et détail des CVE non précisés dans l'annonce.

**Pourquoi c'est important :** Les projets Spring AI doivent monter en 2.0.3 ou 2.1.0 et vérifier les changements de comportement.


## 2026-11-20

**Résumé du jour.** Journée dominée par la vague de releases Spring du 19 novembre. Spring Integration livre 12 correctifs de sécurité (7.0.8, 7.1.3, 7.2.0), dont plusieurs désérialisations non sûres : mise à jour prioritaire si vous utilisez FTP/SFTP, JDBC, MongoDB, Redis ou AMQP. Spring Batch 6.1 et Spring AMQP 4.2 sont aussi disponibles. Rien de notable détecté côté architecture hexagonale ou C4 sur la fenêtre.


### Java

#### [Spring Batch 6.1 GA : @JobParameter, PageableItemReader et gains de performance](https://spring.io/blog/2026/11/19/spring-batch-6-1-0-available-now)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : migrer*

Spring Batch 6.1 s'appuie sur Spring Framework 7.1.0 et Spring Data 2026.1.0. Il introduit l'annotation @JobParameter, un PageableItemReader typé, la prise en charge de JSON Lines et des DAO JDBC migrés vers JdbcClient. Il apporte aussi des changements incompatibles (types de retour des builders, constructeurs DAO supprimés) et déprécie Derby.

**Pourquoi c'est important :** Une migration depuis 6.0 nécessite de revoir les builders et DAO personnalisés.

#### [Spring AMQP 4.2.0 : messages différés natifs RabbitMQ 4.4 et correctifs de 3 CVE](https://spring.io/blog/2026/11/19/spring-amqp-4-2-0-available)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

La version 4.2.0 prend en charge la livraison différée native des quorum queues RabbitMQ 4.4+ via setDeliveryTime, et déclare plusieurs exchanges, queues et bindings en un appel. Elle apporte aussi un batching par listener et une vérification de nom d'hôte TLS automatique. Les patchs 4.1.3 et 4.0.7 corrigent CVE-2026-59395, CVE-2026-59403 et CVE-2026-59404 (détails non précisés dans l'annonce).

**Pourquoi c'est important :** Les correctifs de sécurité justifient la mise à jour des projets utilisant Spring AMQP.


### Sécurité

#### [Spring Integration : 12 CVE corrigées dans les versions 7.0.8, 7.1.3 et 7.2.0](https://spring.io/blog/2026/11/19/spring-integration-7-2-0-available)
*spring.io · publié le 2026-11-19 · confiance : élevée · action : corriger*

Les correctifs touchent les adaptateurs SFTP/FTP/FTPS, MQTT, AMQP, XMPP et les message stores JDBC, MongoDB et Redis. On y trouve des contournements de liste d'autorisation de désérialisation (CVE-2026-59383, CVE-2026-59438), une désérialisation Java non sûre côté Redis (CVE-2026-59444), une injection de commande FTP (CVE-2026-59416) et un défaut de vérification de certificat FTPS (CVE-2026-59364). Les versions affectées et la gravité par CVE ne sont pas détaillées dans l'annonce : consulter les avis individuels. Correctifs : 7.0.8, 7.1.3 ou 7.2.0.

**Pourquoi c'est important :** Toute application utilisant Spring Integration avec ces adaptateurs ou message stores est potentiellement exposée.


## 2026-11-19

**Résumé du jour.** Oracle a publié le 17 novembre son Critical Patch Update pour Java SE (11 failles annoncées, builds corrigés dont 27.0.1.1, 25.0.5.1, 21.0.13.1, 17.0.21.1). Une faille baptisée « Java4Shell » circule et est jugée sérieuse par l'équipe Spring, mais ses détails ne sont pas confirmés par une source primaire accessible : à surveiller.


### Sécurité

#### [« Java4Shell » : faille Java jugée sérieuse, détails à confirmer](https://research.jfrog.com/post/java4shell-vulnerability/)
*research.jfrog.com · publié le 2026-11-18 · confiance : faible · action : surveiller*

Le billet hebdomadaire de Spring du 18 novembre appelle à mettre à jour les JVM et qualifie le CVE « Java4Shell » de préoccupant, en renvoyant vers une analyse de JFrog. Des médias secondaires évoquent une exécution de code à distance dans OpenJDK 17 avec un identifiant CVE et un score non recoupés. Aucun identifiant, version ni correctif n'a pu être vérifié : information à confirmer.

**Pourquoi c'est important :** Possible RCE côté JDK : il faut suivre les avis des éditeurs de JDK et appliquer le CPU en attendant.

#### [Oracle CPU de novembre 2026 : 11 failles Java SE et nouveaux builds corrigés](https://www.oracle.com/security-alerts/cspunov2026.html)
*oracle.com · publié le 2026-11-17 · confiance : moyenne · action : corriger*

Oracle annonce pour le 17 novembre 2026 des correctifs pour 11 vulnérabilités de Java SE, selon les relais secondaires toutes exploitables à distance sans authentification (score max rapporté : 8.1 en CVSS 3.1). Builds corrigés rapportés : 8u513, 11.0.33.1, 17.0.21.1, 21.0.13.1, 25.0.5.1 et 27.0.1.1. La page Oracle n'a pas pu être lue directement (403) : détails à confirmer.

**Pourquoi c'est important :** Tous les JDK Oracle en production (8 à 27) sont concernés ; les versions précédentes ne doivent plus être utilisées.


## 2026-11-18

**Résumé du jour.** Une seule information notable dans la fenêtre : la newsletter Spring du 18 novembre signale une nouvelle faille Java surnommée « Java4Shell » et appelle à mettre à jour les JVM. Aucun identifiant CVE ni version affectée n'a pu être vérifié (le write-up JFrog est inaccessible depuis cet environnement). Spring Boot 4.2 et Framework 7.1 sont annoncés pour le 19 novembre mais pas encore publiés.


### Sécurité

#### [Alerte « Java4Shell » : la newsletter Spring appelle à mettre à jour les JVM](https://spring.io/blog/2026/11/18/this-week-in-spring-november-18th-2026)
*spring.io · publié le 2026-11-18 · confiance : faible · action : surveiller*

La newsletter hebdomadaire de Spring mentionne une nouvelle vulnérabilité Java surnommée « Java4Shell », jugée sérieuse, et recommande de mettre à jour les JVM. Elle renvoie vers une analyse de JFrog. Information à confirmer : ni CVE, ni versions touchées, ni correctif n'ont pu être vérifiés dans une source primaire.

**Pourquoi c'est important :** Une faille de type exécution de code sur la JVM concernerait tous nos services ; il faut suivre les avis Oracle/OpenJDK et préparer une mise à jour.


## 2026-11-11

**Résumé du jour.** Journée calme. Spring annonce le transfert du projet Spring for Apache Pulsar vers la fondation Apache : les équipes qui l'utilisent devront changer de coordonnées Maven et de packages pour recevoir les futures évolutions. Aucun nouvel avis de sécurité Spring publié depuis le 20 août 2026.


### Java

#### [Spring for Apache Pulsar déménage chez Apache Pulsar](https://spring.io/blog/2026/11/10/spring-pulsar-new-home-asf)
*spring.io · publié le 2026-11-10 · confiance : élevée · action : surveiller*

Le projet Spring for Apache Pulsar devient un sous-projet d'Apache Pulsar, sous le nom Apache Pulsar support for Spring. Spring ne publiera plus de mises à jour après la version 2.0.8 (starter Boot) et après le binder Spring Cloud Stream 5.1.0. Les applications existantes continuent de fonctionner avec ces versions.

**Pourquoi c'est important :** Les équipes utilisant Pulsar avec Spring doivent prévoir le changement de dépendances et d'imports pour continuer à recevoir correctifs et nouveautés.


## 2026-11-10

**Résumé du jour.** Journée calme. Seule nouveauté notable dans la fenêtre : Spring AI 2.1.0-RC2 (9 novembre), construite sur Spring Boot 4.2.0-RC2, avec plusieurs ruptures à anticiper pour les équipes qui utilisent Anthropic ou Bedrock. Aucune alerte de sécurité nouvelle repérée.


### Java

#### [Spring AI 2.1.0-RC2 : nouvelle API DecisionModel et points de migration](https://spring.io/blog/2026/11/09/spring-ai-2-1-0-RC2-available-now)
*spring.io · publié le 2026-11-09 · confiance : élevée · action : tester*

Deuxième release candidate de Spring AI 2.1 avant la GA, alignée sur Spring Boot 4.2.0-RC2. Elle ajoute l'API DecisionModel (réponses typées oui/non, choix, score), le streaming des arguments d'appels d'outils et un serveur MCP « modern ». Les notes de migration signalent des ruptures côté Anthropic (paramètres temperature/topP/topK rejetés, clé API en en-tête Bearer) et Typesense.

**Pourquoi c'est important :** Les équipes utilisant Spring AI avec Anthropic, Bedrock ou Typesense doivent tester cette RC avant la GA pour anticiper les changements incompatibles.


## 2026-11-07

**Résumé du jour.** Journée calme. Spring Boot 4.2.0-RC2 est disponible, dernière étape avant la version finale attendue en novembre. Aucune alerte de sécurité nouvelle repérée sur les sources accessibles.


### Java

#### [Spring Boot 4.2.0-RC2 disponible sur Maven Central](https://spring.io/blog/2026/11/06/spring-boot-4-2-0-RC2-available-now)
*spring.io · publié le 2026-11-06 · confiance : élevée · action : tester*

Le deuxième release candidate de Spring Boot 4.2 regroupe 99 améliorations, mises à jour de dépendances et corrections. Parmi les changements cités : prise en charge de l'en-tête X-Forwarded-Prefix avec Reactor Netty et application de spring.data.redis.database aux connexions Redis maître/réplica.

**Pourquoi c'est important :** Permet de tester dès maintenant la compatibilité de nos applications avant la sortie finale de la 4.2.


## 2026-11-06

**Résumé du jour.** Journée calme. Seule nouveauté notable dans la fenêtre : la deuxième release candidate de Spring Cloud 2026.0.0, alignée sur Spring Boot 4.2.0-RC2. Aucune alerte de sécurité critique repérée sur le JDK, Spring, Log4j ou Jackson.


### Java

#### [Spring Cloud 2026.0.0-RC2 (Paddington) disponible](https://spring.io/blog/2026/11/05/spring-cloud-2026-0-0-RC2-has-been-released)
*spring.io · publié le 2026-11-05 · confiance : élevée · action : tester*

La deuxième release candidate du train Spring Cloud 2026.0.0 est publiée. La plupart des modules (Gateway, Config, OpenFeign, Stream, Circuitbreaker, Kubernetes…) passent en 5.1.0-RC2, et le train repose sur Spring Boot 4.2.0-RC2.

**Pourquoi c'est important :** Permet de tester dès maintenant la compatibilité des applications Spring Cloud avec Spring Boot 4.2 avant la version finale.


## 2026-10-30

**Résumé du jour.** Journée calme : aucune annonce Java, C4 ou sécurité vérifiable dans la fenêtre de 24 h. Seule retenue, un article de fond récent : Spring Modulith 2.2 RC1, utile pour les équipes qui appliquent une architecture modulaire ou hexagonale.


### Hexagonal

#### [Spring Modulith 2.2 RC1 : dépendances de modules, événements et tests](https://spring.io/blog/2026/10/23/spring-modulith-2-2-rc1-2-1-2-2-0-9-and-1-4-14-released)
*spring.io · publié le 2026-10-23 · confiance : élevée · action : lire*

La première release candidate de Spring Modulith 2.2 assouplit la déclaration des dépendances autorisées entre modules, ajoute l'état « abandonné » pour les publications d'événements et exécute la complétion dans la transaction du listener. Elle vise Spring Boot 4.2 et ArchUnit 1.5.1. Les versions 2.1.2, 2.0.9 et 1.4.14 corrigent le registre de publications ; la 1.4.14 est la dernière de la branche 1.x.

**Pourquoi c'est important :** Utile pour vérifier les frontières de modules ; les équipes encore en 1.x doivent planifier la migration vers la 2.x.


## 2026-10-29

**Résumé du jour.** Journée calme. Spring AI 2.1 (candidate à la release RC1) se précise avec deux articles du 28 octobre : un modèle de messages en parties ordonnées pour conserver le raisonnement des modèles, et la possibilité d'enregistrer ses propres embeddings. Aucune alerte de sécurité Spring nouvelle sur la période.


### Java

#### [Spring AI 2.1 : des messages en parties pour préserver le raisonnement des modèles](https://spring.io/blog/2026/10/28/spring-ai-message-parts-reasoning-replay)
*spring.io · publié le 2026-10-28 · confiance : élevée · action : surveiller*

Spring AI 2.1 remplace le modèle chaîne de texte plus listes annexes par une liste ordonnée de parties de message, afin de renvoyer à l'identique les blocs de raisonnement et les signatures des fournisseurs. Cela concerne les principaux modèles de chat, et une mémoire de session persiste ces parties, tandis que ChatMemory devient obsolète. La version 2.1.0-RC1 était disponible à la publication.

**Pourquoi c'est important :** Les équipes qui utilisent ChatMemory devront prévoir une migration vers la mémoire de session.

#### [Spring AI 2.1 : stocker ses propres embeddings avec upsert](https://spring.io/blog/2026/10/28/spring-ai-upsert-own-embeddings)
*spring.io · publié le 2026-10-28 · confiance : élevée · action : tester*

Spring AI 2.1 ajoute une méthode upsert pour enregistrer des documents avec des vecteurs déjà calculés (image, audio, vidéo) sans passer par le modèle d'embedding du store. Une surcharge de similaritySearch accepte aussi un vecteur de requête précalculé. Disponible en 2.1.0-RC1 pour PGvector, Redis, Elasticsearch, Qdrant et OpenSearch.

**Pourquoi c'est important :** Permet des cas d'usage multimodaux ou de réutiliser des embeddings existants sans recalcul.


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

