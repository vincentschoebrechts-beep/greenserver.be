# Contenu français de la formation « SAP vu de l'atelier ».
# Même structure que content_en.py ; les codes, types de mouvement et statuts restent ceux de SAP.

LANG = {
    "course_title": "SAP vu de l'atelier",
    "course_tag": "Formation gratuite",
    "lesson_word": "Leçon",
    "of": "sur",
    "goals": "Dans cette leçon",
    "example": "En atelier",
    "keys": "À retenir",
    "check": "Testez-vous",
    "check_intro": "Trois questions sur cette leçon. Choisissez une réponse pour savoir si elle est juste.",
    "check_intro_annex": "Six questions sur cette annexe. Choisissez une réponse pour savoir si elle est juste. Elles ne font pas partie du QCM final.",
    "prev": "Précédente",
    "next": "Suivante",
    "contents": "Sommaire de la formation",
    "quiz": "QCM final",
    "switch": "English",
    "right": "Exact.",
    "wrong": "Pas tout à fait.",
    "answer_is": "La bonne réponse :",
}

HOME = {
    "title": "SAP vu de l'atelier, une formation gratuite",
    "description": "Une formation gratuite sur SAP S/4HANA pour ceux qui travaillent avec des automates, de la supervision et un MES : dix leçons et un QCM final.",
    "lead": "SAP S/4HANA expliqué à ceux qui travaillent avec des automates, de la supervision et un MES. Dix leçons courtes, en mots simples, puis un QCM final. Gratuit, sans compte, rien à installer.",
    "disclaimer": "Formation indépendante, sans lien avec SAP SE et non approuvée par SAP SE. SAP, SAP S/4HANA et les autres noms de produits SAP sont des marques de SAP SE. Les écrans et les réglages varient d'une entreprise à l'autre : en cas de doute, votre propre système SAP et votre équipe SAP ont le dernier mot. Les termes SAP sont donnés en français, avec leur nom anglais entre parenthèses quand c'est celui qu'on entend le plus souvent.",
    "who_h": "Pour qui",
    "who": "Automaticiens, techniciens de maintenance et de production, informaticiens industriels : tous ceux qui connaissent l'usine et veulent comprendre ce que SAP en fait, en particulier quand l'entreprise passe à S/4HANA.",
    "how_h": "Comment ça marche",
    "how": [
        "Dix leçons d'environ quinze minutes, à lire dans l'ordre ou non.",
        "Chaque leçon se termine par trois questions pour vous tester.",
        "Le QCM final tire vingt questions d'une banque de cent, deux par leçon. Votre score est calculé dans votre navigateur et n'est envoyé nulle part.",
    ],
    "lessons_h": "Les dix leçons",
    "quiz_h": "QCM final",
    "quiz_p": "Vingt questions tirées au hasard dans la banque, deux par leçon. Vous pouvez le refaire autant de fois que vous voulez : chaque essai tire une nouvelle série.",
    "quiz_btn": "Passer le QCM final",
    "start_btn": "Commencer par la leçon 1",
    "more_h": "Pour aller plus loin",
    "more": [
        ('https://learning.sap.com/', 'learning.sap.com', ' : les parcours gratuits de SAP, à suivre à votre rythme, certains avec un accès à un système d\'entraînement (en anglais).'),
        ('https://community.sap.com/', 'SAP Community', ' : questions et réponses, avec un espace pour les débutants (en anglais).'),
        ('https://api.sap.com/', 'SAP Business Accelerator Hub', ' : le catalogue des API de SAP, avec leur documentation.'),
    ],
    "updated": "Dernière mise à jour : 7 novembre 2026.",
}

QUIZ = {
    "title": "QCM final, SAP vu de l'atelier",
    "h1": "QCM final",
    "lead": "Vingt questions, deux par leçon, tirées d'une banque de cent. Répondez à toutes, puis vérifiez votre score. Rien n'est envoyé : tout se passe dans votre navigateur.",
    "submit": "Vérifier mes réponses",
    "again": "Nouvelle série",
    "answered": "répondues",
    "score": "Votre score",
    "pass": "Bravo : vous connaissez l'essentiel de SAP vu de l'atelier.",
    "fail": "Pas encore. Relisez les leçons où vous avez manqué des questions, puis tentez une nouvelle série.",
    "missing": "Certaines questions n'ont pas encore de réponse.",
    "from_lesson": "Leçon",
}

LESSONS = [
# ------------------------------------------------------------------ 1
dict(
 slug="lecon-1",
 title="SAP dans l'usine",
 lead="Ce qu'est un ERP, où se place SAP S/4HANA parmi les systèmes d'une usine, et comment SAP décrit une entreprise.",
 goals=["Situer SAP parmi les niveaux d'une usine.", "Savoir ce que SAP fait, et ce qu'il ne fait pas.", "Reconnaître les principales unités organisationnelles : mandant, société, division, magasin."],
 body="""
<h2>Un ERP, en une phrase</h2>
<p>Un ERP (progiciel de gestion intégré) rassemble toute l'entreprise dans une seule base de données : ventes, achats, production, stocks, maintenance, qualité et comptabilité. Quand le magasin sort une pièce, le stock change, le coût de l'ordre change et la comptabilité change, tout en même temps. SAP S/4HANA est l'ERP actuel de SAP. Il succède à SAP ECC, la génération précédente, et ne tourne que sur SAP HANA, la base de données en mémoire de SAP. Il peut être installé sur les serveurs de l'entreprise ou utilisé comme service dans le cloud.</p>

<h2>Où se place SAP</h2>
<p>On décrit souvent une usine en niveaux, des capteurs en bas jusqu'aux systèmes de gestion en haut : c'est le modèle ISA-95. SAP se trouve tout en haut.</p>
{DIAGRAM_LEVELS}
<p>SAP sait ce qu'il faut fabriquer, avec quelles pièces, pour quand, et ce que ça coûte. Il ne pilote pas les machines : il ne lit pas un capteur toutes les 10 ms, et il ne doit jamais écrire dans un automate. Entre SAP et les machines, il y a en général un MES (niveau 3), ou au moins une passerelle.</p>

<h2>Comment SAP décrit une entreprise</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Unité</th><th scope="col">Ce que c'est</th><th scope="col">Exemple</th></tr></thead>
<tbody>
<tr><td>Mandant (client)</td><td>Un environnement autonome dans le système SAP, avec ses propres données.</td><td>Mandant 100 : production</td></tr>
<tr><td>Société (company code)</td><td>Une entité juridique avec sa propre comptabilité.</td><td>La société belge</td></tr>
<tr><td>Division (plant)</td><td>Une usine ou un site : l'unité de la production, de la planification et du stock.</td><td>Division 1100</td></tr>
<tr><td>Magasin (storage location)</td><td>Un endroit où le stock est rangé dans une division.</td><td>0001 matières premières, 0002 produits finis</td></tr>
</tbody></table></div>

<h2>Les modules dont vous entendrez parler</h2>
<p>On décrit toujours SAP par ses modules historiques : <strong>PP</strong> (planification de la production), <strong>MM</strong> (gestion des articles : achats et stocks), <strong>QM</strong> (qualité), <strong>PM</strong> (maintenance), <strong>SD</strong> (ventes et distribution) et <strong>FI/CO</strong> (finance et contrôle de gestion). Dans S/4HANA, ils forment un seul système qui partage les mêmes données, mais les abréviations sont partout.</p>
""",
 example="Une usine avec deux lignes de fabrication de pompes est la division 1100 dans SAP. Les matières premières sont dans le magasin 0001, les racks en bord de ligne dans le 0003, les pompes finies dans le 0002. Les automates et la supervision ne connaissent aucun de ces numéros : c'est le MES, ou les personnes, qui font le lien.",
 keys=["SAP S/4HANA est un ERP : niveau 4, des heures et des jours, pas des millisecondes.", "Il ne pilote jamais les machines ; un MES ou une passerelle se place entre les deux.", "Mandant, société, division et magasin décrivent l'entreprise.", "PP, MM, QM, PM, SD et FI/CO sont les noms de modules encore utilisés tous les jours."],
),
# ------------------------------------------------------------------ 2
dict(
 slug="lecon-2",
 title="Se repérer dans SAP",
 lead="Les deux façons de travailler dans SAP, les codes de transaction que tout le monde utilise, et la différence entre données de base et données de mouvement.",
 goals=["Distinguer SAP Fiori et SAP GUI.", "Utiliser les codes de transaction et les principaux raccourcis clavier.", "Distinguer données de base et données de mouvement."],
 body="""
<h2>Deux interfaces</h2>
<p><strong>SAP Fiori</strong> est l'interface web. On ouvre le launchpad Fiori dans un navigateur et on voit des tuiles : chaque tuile est une application faite pour une tâche, par exemple confirmer une opération de fabrication. Les applications dépendent du rôle : un magasinier et un planificateur ne voient pas les mêmes tuiles. Fiori fonctionne sur PC comme sur tablette.</p>
<p><strong>SAP GUI</strong> est le client Windows classique. On y travaille avec des <strong>codes de transaction</strong> : des codes courts tapés dans le champ de commande, en haut à gauche. Les deux interfaces travaillent sur les mêmes données, et beaucoup de gens utilisent les deux.</p>

<h2>Les codes de transaction</h2>
<ul>
<li>Depuis le menu principal, tapez le code puis Entrée, par exemple <code>MM03</code> pour afficher un article.</li>
<li><code>/n</code> devant le code quitte d'abord la transaction en cours : <code>/nMM03</code>.</li>
<li><code>/o</code> ouvre la transaction dans une nouvelle session (fenêtre) : <code>/oMD04</code>.</li>
<li>Beaucoup de codes suivent le schéma créer, modifier, afficher : <code>MM01</code>, <code>MM02</code>, <code>MM03</code> pour les articles, <code>CO01</code>, <code>CO02</code>, <code>CO03</code> pour les ordres de fabrication. Quand vous voulez seulement regarder, utilisez le code d'affichage : vous ne pouvez rien casser.</li>
</ul>
<p>Deux touches aident partout dans SAP GUI : <strong>F1</strong> explique le champ où se trouve le curseur, <strong>F4</strong> liste ses valeurs possibles.</p>

<h2>Données de base et données de mouvement</h2>
<p>Les <strong>données de base</strong> décrivent ce qui dure : articles, nomenclatures, gammes, postes de travail, fournisseurs, équipements. On les crée une fois et on les modifie rarement.</p>
<p>Les <strong>données de mouvement</strong> enregistrent des événements : un ordre de fabrication, une confirmation, un mouvement de stock. Chaque événement crée un <strong>document</strong> avec un numéro, une date et un utilisateur. Un mouvement de stock, par exemple, crée un document article. On ne supprime pas les documents : une erreur se corrige par une annulation, et l'historique reste complet.</p>

<h2>Rôles et autorisations</h2>
<p>Ce que vous pouvez voir et faire dépend de vos rôles. S'il manque une application ou une transaction, votre rôle ne la contient probablement pas. Pour apprendre sans risque, demandez des rôles en affichage seul dans un système de test ou de formation.</p>
""",
 example="Un opérateur scanne un ordre de fabrication à la fin d'une opération ; le MES envoie la confirmation à SAP. L'ordre de fabrication est une donnée de mouvement, l'article et la gamme qu'il utilise sont des données de base, et la confirmation crée un nouveau document que toute personne ayant le bon rôle peut afficher.",
 keys=["Fiori : applications web selon le rôle. SAP GUI : client classique avec des codes de transaction.", "/n ouvre un code dans la même fenêtre, /o dans une nouvelle ; 01, 02, 03 signifient souvent créer, modifier, afficher.", "F1 explique un champ, F4 liste ses valeurs.", "Les données de base durent ; les données de mouvement enregistrent des événements dans des documents numérotés."],
),
# ------------------------------------------------------------------ 3
dict(
 slug="lecon-3",
 title="Les données de base de la production",
 lead="La fiche article, la nomenclature, le poste de travail, la gamme et la version de fabrication : les cinq fiches sur lesquelles repose la production.",
 goals=["Lire une fiche article et connaître ses principales vues.", "Comprendre comment nomenclature, gamme et poste de travail s'articulent.", "Savoir pourquoi la version de fabrication compte dans S/4HANA."],
 body="""
<h2>La fiche article</h2>
<p>Chaque article a une seule fiche : matière première, pièce semi-finie, produit fini, pièce de rechange. Elle est organisée en <strong>vues</strong> que chaque service remplit : données de base, achats, MRP, préparation du travail, qualité, comptabilité, calcul des coûts. La plupart des vues sont tenues par division, car une même pièce peut être planifiée différemment dans deux usines.</p>
<p>Le <strong>type d'article</strong> fixe les vues autorisées et la façon de valoriser le stock. Les types standard sont ROH (matière première), HALB (semi-fini), FERT (produit fini), HAWA (marchandise) et ERSA (pièce de rechange) ; les entreprises ajoutent souvent les leurs.</p>

<h2>Nomenclature, poste de travail, gamme</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Fiche</th><th scope="col">Répond à la question</th><th scope="col">Contient</th></tr></thead>
<tbody>
<tr><td>Nomenclature (BOM)</td><td>De quoi est-il fait ?</td><td>Les composants et leurs quantités pour une quantité de base du produit</td></tr>
<tr><td>Poste de travail (work center)</td><td>Où le travail est-il fait ?</td><td>Une machine, une ligne ou une équipe, avec sa capacité, ses horaires et ses taux de coût</td></tr>
<tr><td>Gamme (routing)</td><td>Comment est-il fait ?</td><td>La suite des opérations, chacune sur un poste de travail, avec des temps standard de réglage, machine et main-d'œuvre</td></tr>
</tbody></table></div>
<p>Chaque opération a une <strong>clé de commande</strong> (control key), qui indique par exemple si elle est ordonnancée, valorisée et doit être confirmée, ou si elle est sous-traitée.</p>

<h2>La version de fabrication</h2>
<p>Un produit peut avoir deux nomenclatures (deux conceptions) ou deux gammes (deux lignes). La <strong>version de fabrication</strong> (production version) indique quelle nomenclature et quelle gamme vont ensemble, pour quelle période et quelles quantités. Dans S/4HANA, elle est obligatoire pour les articles fabriqués en interne : c'est par elle que le MRP trouve la nomenclature. Un article sans version de fabrication valide ne sera pas planifié correctement.</p>
""",
 example="La pompe finie P-200 (type FERT) a une nomenclature avec un moteur, un corps de pompe et huit vis. Sa gamme comporte l'opération 10, montage sur le poste ASSY1, et l'opération 20, test sur le poste TEST1. La version de fabrication 0001 relie cette nomenclature et cette gamme. Le banc de test du poste TEST1 est ce que voient l'automate et la supervision ; dans SAP, c'est un poste de travail avec une capacité.",
 keys=["Une fiche article par article, en vues, surtout par division.", "Nomenclature : de quoi il est fait. Gamme : comment. Poste de travail : où.", "La clé de commande décide du traitement de chaque opération.", "Dans S/4HANA, sans version de fabrication, pas de planification correcte."],
),
# ------------------------------------------------------------------ 4
dict(
 slug="lecon-4",
 title="Planifier avec le MRP",
 lead="Comment SAP transforme la demande en propositions : ce que calcule le MRP, les réglages qui le pilotent et l'écran où vivent les planificateurs.",
 goals=["Comprendre le calcul des besoins nets.", "Connaître les résultats du MRP : ordres planifiés et demandes d'achat.", "Lire la liste des besoins et des stocks."],
 body="""
<h2>Ce que calcule le MRP</h2>
<p>Le MRP (calcul des besoins) compare la <strong>demande</strong> et l'<strong>offre</strong>. La demande, ce sont les commandes clients et les prévisions (besoins indépendants planifiés). L'offre, c'est le stock et tout ce qui est déjà en route : ordres de fabrication, commandes d'achat. Ce qui manque est le <strong>besoin net</strong>.</p>
<p>Pour chaque quantité manquante, le MRP crée une proposition à la bonne date. Pour un produit fabriqué en interne, il crée un <strong>ordre planifié</strong> et éclate la nomenclature : les composants reçoivent des <strong>besoins dépendants</strong>, que le MRP planifie à leur tour, niveau après niveau. Pour une pièce achetée, il crée une <strong>demande d'achat</strong>, que les acheteurs transforment en commande.</p>

<h2>Les réglages qui le pilotent</h2>
<p>Ils se trouvent dans les vues MRP de la fiche article :</p>
<ul>
<li><strong>Type de planification</strong> (MRP type) : si et comment l'article est planifié (PD pour le MRP, VB pour un point de commande manuel, ND pour aucune planification).</li>
<li><strong>Type d'approvisionnement</strong> : E pour la fabrication interne, F pour l'approvisionnement externe, X pour les deux.</li>
<li><strong>Taille de lot</strong> : EX commande exactement ce qui manque (lot pour lot), FX une quantité fixe, HB jusqu'à un stock maximum.</li>
<li><strong>Délais</strong> : durée de fabrication interne, délai de livraison prévu, délai de traitement à l'entrée. Le MRP planifie à rebours depuis la date du besoin.</li>
</ul>

<h2>MRP Live et MD04</h2>
<p>Dans S/4HANA, le calcul s'appelle <strong>MRP Live</strong> (<code>MD01N</code>) : il tourne dans la base SAP HANA et va beaucoup plus vite que le calcul classique. Les planificateurs travaillent ensuite dans la <strong>liste des besoins et des stocks</strong> (<code>MD04</code>, ou les applications MRP de Fiori) : stock, besoins et entrées par date, avec des messages d'exception quand quelque chose est en retard ou en trop.</p>
<p>Quand la date approche, l'ordre planifié est <strong>converti</strong> en ordre de fabrication : la proposition devient un ordre réel, prêt à être lancé.</p>
""",
 example="Les clients ont besoin de 100 pompes vendredi prochain. Il y en a 20 en stock et rien en commande ; la taille de lot est lot pour lot. Le MRP propose un ordre planifié de 80 pompes, positionné à rebours depuis vendredi selon la durée de fabrication. Il éclate la nomenclature : 80 moteurs, 80 corps de pompe, 640 vis. Les moteurs sont achetés et reçoivent une demande d'achat ; les corps sont fabriqués en interne et reçoivent leur propre ordre planifié.",
 keys=["Besoin net = demande − stock − entrées déjà prévues.", "Fabrication interne : ordres planifiés, avec des besoins dépendants pour les composants. Achats : demandes d'achat.", "Type de planification, type d'approvisionnement, taille de lot et délais déterminent le résultat.", "MD01N lance MRP Live ; MD04 montre la situation en direct pour un article."],
),
# ------------------------------------------------------------------ 5
dict(
 slug="lecon-5",
 title="L'ordre de fabrication",
 lead="La vie d'un ordre de fabrication de sa création à sa clôture, ses statuts, et les mouvements de stock et confirmations que l'atelier alimente.",
 goals=["Suivre un ordre de fabrication à travers ses statuts.", "Savoir quand les composants sortent et quand les produits finis entrent en stock.", "Comprendre ce que rapporte une confirmation."],
 body="""
<h2>Création et lancement</h2>
<p>Un ordre de fabrication est créé en convertissant un ordre planifié, ou à la main (<code>CO01</code>). SAP copie les <strong>opérations</strong> de la gamme et les <strong>composants</strong> de la nomenclature, via la version de fabrication, et réserve les composants. Un contrôle de disponibilité indique si les pièces sont là.</p>
<p>Le <strong>lancement</strong> (release) est le moment où l'ordre peut être exécuté : on peut imprimer les documents d'atelier, envoyer l'ordre au MES, et SAP accepte les mouvements de stock et les confirmations.</p>

<h2>Les statuts</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Statut</th><th scope="col">Signification</th></tr></thead>
<tbody>
<tr><td><code>CRTD</code></td><td>Créé : planifié, pas encore exécutable</td></tr>
<tr><td><code>REL</code></td><td>Lancé : peut être exécuté</td></tr>
<tr><td><code>PCNF</code> / <code>CNF</code></td><td>Partiellement confirmé / confirmé</td></tr>
<tr><td><code>PDLV</code> / <code>DLV</code></td><td>Partiellement livré / livré en stock</td></tr>
<tr><td><code>TECO</code></td><td>Techniquement terminé : plus aucune production attendue</td></tr>
<tr><td><code>CLSD</code></td><td>Clôturé : coûts imputés, plus rien ne peut être saisi</td></tr>
</tbody></table></div>

<h2>Sortie, confirmation, entrée</h2>
<ol class="steps">
<li><strong>Sortie de marchandises</strong> (type de mouvement 261) : les composants quittent le stock et sont imputés à l'ordre. Avec le <strong>prélèvement rétroactif</strong> (backflush), cela se fait automatiquement à la confirmation de l'opération.</li>
<li><strong>Confirmation</strong> (<code>CO11N</code>) : pour chaque opération, la quantité bonne (yield), le rebut, les retouches et les temps réellement passés. Une confirmation peut être partielle ou finale. <code>CO13</code> en annule une.</li>
<li><strong>Entrée de marchandises</strong> (type de mouvement 101) : les produits finis entrent en stock. Elle peut être comptabilisée automatiquement avec la confirmation de la dernière opération.</li>
<li><strong>Clôture</strong> : l'ordre passe en TECO, puis ses coûts sont imputés au contrôle de gestion, qui montre l'écart entre coût prévu et coût réel.</li>
</ol>
<p>Pour suivre beaucoup d'ordres à la fois, <code>COOIS</code> liste les ordres, les opérations et les composants avec leurs statuts.</p>
""",
 example="Un compteur sur la ligne de montage compte 82 pompes pour l'ordre 1000123, et le banc de test en refuse 2. En fin d'équipe, le MES envoie la confirmation de l'opération 20 : quantité bonne 80, rebut 2, temps machine 7,5 heures. SAP prélève rétroactivement les vis et les moteurs, et comptabilise automatiquement l'entrée de 80 pompes. Personne n'a rien tapé dans SAP.",
 keys=["Les opérations viennent de la gamme, les composants de la nomenclature.", "Le lancement ouvre l'ordre aux confirmations et aux mouvements de stock.", "261 sort les composants, 101 fait entrer les produits finis ; le prélèvement rétroactif automatise la sortie.", "Une confirmation rapporte quantité bonne, rebut et temps ; TECO termine la production, l'imputation clôt les coûts."],
),
# ------------------------------------------------------------------ 6
dict(
 slug="lecon-6",
 title="Stocks et mouvements",
 lead="Comment SAP enregistre chaque changement de stock : types de mouvement, types de stock, documents, et les transactions que le magasin utilise tous les jours.",
 goals=["Connaître les types de mouvement les plus courants.", "Comprendre les trois types de stock.", "Trouver le stock d'un article et ses mouvements."],
 body="""
<h2>Les types de mouvement</h2>
<p>Chaque changement de stock est un <strong>mouvement de stock</strong>, et chaque mouvement a un <strong>type de mouvement</strong> à trois chiffres qui indique à SAP ce qui se passe et comment le comptabiliser.</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Type</th><th scope="col">Mouvement</th></tr></thead>
<tbody>
<tr><td><code>101</code></td><td>Entrée de marchandises sur commande d'achat ou ordre de fabrication</td></tr>
<tr><td><code>261</code></td><td>Sortie de marchandises vers un ordre</td></tr>
<tr><td><code>201</code></td><td>Sortie vers un centre de coûts (consommation sans ordre)</td></tr>
<tr><td><code>311</code></td><td>Transfert entre magasins, en une étape</td></tr>
<tr><td><code>321</code></td><td>Libération du contrôle qualité vers la libre utilisation</td></tr>
<tr><td><code>551</code></td><td>Sortie pour mise au rebut</td></tr>
</tbody></table></div>
<p>Un mouvement s'annule avec le type d'annulation correspondant, en général le numéro suivant : <code>102</code> annule <code>101</code>, <code>262</code> annule <code>261</code>.</p>

<h2>Les types de stock</h2>
<p>Dans un magasin, un même article peut se trouver dans trois types de stock :</p>
<ul>
<li><strong>Libre utilisation</strong> : peut être consommé ou expédié librement.</li>
<li><strong>Contrôle qualité</strong> : attend une décision de la qualité.</li>
<li><strong>Bloqué</strong> : ne doit pas être utilisé.</li>
</ul>

<h2>Documents et valeur</h2>
<p>Chaque mouvement de stock crée un <strong>document article</strong>. Le stock a une valeur : un mouvement valorisé crée donc aussi un <strong>document comptable</strong>, et logistique et finance avancent ensemble. Dans S/4HANA, les quantités en stock sont calculées à partir des documents articles eux-mêmes, rangés dans une seule table.</p>

<h2>Les transactions de tous les jours</h2>
<ul>
<li><code>MIGO</code> : saisir et afficher la plupart des mouvements de stock.</li>
<li><code>MMBE</code> : vue du stock d'un article par division, magasin et type de stock.</li>
<li>L'inventaire : on compte le stock et on comptabilise les écarts, pour que SAP corresponde aux étagères.</li>
</ul>
""",
 example="Le magasinier déplace 50 corps de pompe du magasin principal (0001) vers le rack en bord de ligne (0003) : type de mouvement 311. Deux corps sont cabossés : type de mouvement 551, mise au rebut. Si le rack en bord de ligne n'est pas un magasin à part dans SAP, la supervision peut montrer un rack plein alors que SAP n'y voit rien : se mettre d'accord tôt sur les magasins évite beaucoup de confusion.",
 keys=["Le type de mouvement dit ce qui se passe : 101 entrée, 261 sortie vers un ordre, 311 transfert, 551 rebut.", "Les erreurs s'annulent, elles ne se suppriment pas (102 pour 101, 262 pour 261).", "Libre utilisation, contrôle qualité, bloqué : seul le premier est utilisable librement.", "MIGO saisit les mouvements, MMBE montre le stock ; chaque mouvement laisse un document article."],
),
# ------------------------------------------------------------------ 7
dict(
 slug="lecon-7",
 title="La gestion de la qualité",
 lead="Lots de contrôle, résultats et décisions d'emploi : comment SAP QM vérifie ce qui entre, ce qui est fabriqué et ce qui part en stock.",
 goals=["Savoir ce qui crée un lot de contrôle.", "Suivre un contrôle depuis les résultats jusqu'à la décision d'emploi.", "Savoir où se placent les mesures de l'atelier."],
 body="""
<h2>Le lot de contrôle</h2>
<p>Un <strong>lot de contrôle</strong> (inspection lot) est une demande de contrôle d'une quantité d'article. SAP le crée automatiquement quand un événement se produit, et son <strong>origine</strong> indique lequel :</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Origine</th><th scope="col">Créé par</th></tr></thead>
<tbody>
<tr><td><code>01</code></td><td>Entrée de marchandises sur commande d'achat : contrôle à réception</td></tr>
<tr><td><code>03</code></td><td>Lancement d'un ordre de fabrication : contrôle en cours de fabrication, au fil des opérations</td></tr>
<tr><td><code>04</code></td><td>Entrée de marchandises depuis la production : contrôle final ; les produits attendent en général en stock de contrôle qualité</td></tr>
</tbody></table></div>

<h2>Que contrôler</h2>
<p>Le plan de contrôle (ou la gamme, pour le contrôle en cours de fabrication) liste les <strong>caractéristiques</strong> à vérifier : un diamètre, une pression, un aspect visuel. Les caractéristiques utilisées dans de nombreux plans sont définies une fois comme <strong>caractéristiques de contrôle de référence</strong>. Une procédure d'échantillonnage indique combien de pièces contrôler.</p>

<h2>Des résultats à la décision</h2>
<ol class="steps">
<li><strong>Saisie des résultats</strong> (<code>QE51N</code>) : valeurs mesurées ou conforme / non conforme pour chaque caractéristique.</li>
<li><strong>Décision d'emploi</strong> (depuis la liste de travail <code>QA32</code>) : le lot est accepté ou refusé. La décision peut transférer le stock en libre utilisation, en bloqué ou au rebut.</li>
</ol>

<h2>Quand quelque chose ne va pas</h2>
<p>Les problèmes sont enregistrés dans des <strong>avis qualité</strong>. Dans le standard SAP, Q1 est une réclamation client, Q2 une réclamation contre un fournisseur et Q3 un problème interne. L'avis rassemble les défauts, les causes et les actions.</p>

<h2>Les mesures de l'atelier</h2>
<p>Les bancs de test et les machines mesurent déjà. Leurs valeurs peuvent arriver dans SAP par le MES ou par une interface qui enregistre les résultats dans le lot de contrôle. Elles ne doivent jamais être écrites directement dans la base de données de SAP.</p>
""",
 example="Les pompes sortent du banc de test avec un débit et une pression mesurés. Le MES regroupe les valeurs par ordre et les enregistre dans le lot de contrôle d'origine 04. Le technicien qualité ne regarde que les lots hors tolérance, puis prend la décision d'emploi : les pompes bonnes passent en libre utilisation avec le type de mouvement 321, comptabilisé automatiquement.",
 keys=["Origine 01 : livraisons fournisseurs. 03 : pendant la fabrication. 04 : entrée depuis la production.", "Les caractéristiques disent quoi contrôler ; les caractéristiques de référence se réutilisent d'un plan à l'autre.", "Saisie des résultats, puis décision d'emploi, qui déplace le stock.", "Q1, Q2, Q3 : problèmes client, fournisseur et interne."],
),
# ------------------------------------------------------------------ 8
dict(
 slug="lecon-8",
 title="La maintenance",
 lead="Comment SAP PM décrit les installations, enregistre les pannes, planifie les réparations et déclenche la maintenance préventive, y compris à partir des compteurs des machines.",
 goals=["Distinguer postes techniques et équipements.", "Suivre une panne depuis l'avis jusqu'à l'ordre.", "Comprendre la maintenance préventive selon compteur."],
 body="""
<h2>Les objets techniques</h2>
<p>Un <strong>poste technique</strong> (functional location) est un emplacement de la structure technique de l'usine, organisé en arborescence : site, ligne, station. Un <strong>équipement</strong> est un objet physique individuel, comme une pompe ou un moteur, avec son propre numéro de série et son historique. Il est installé sur un poste technique et peut être déplacé vers un autre, en emportant son historique.</p>

<h2>Avis et ordre</h2>
<ol class="steps">
<li><strong>Avis</strong> (<code>IW21</code>) : quelqu'un signale un besoin. Dans le standard SAP, M1 est une demande d'entretien, M2 un avis de panne, M3 un compte rendu d'activité.</li>
<li><strong>Ordre d'entretien</strong> (<code>IW31</code>) : le travail est planifié, avec les opérations, les pièces de rechange et les prestations externes. L'ordre rassemble les confirmations de temps et les coûts réels.</li>
<li><strong>Clôture</strong> : le technicien confirme le travail, note le dommage et la cause, et l'ordre est clôturé.</li>
</ol>

<h2>La maintenance préventive</h2>
<p>Les <strong>plans d'entretien</strong> créent automatiquement des ordres ou des avis :</p>
<ul>
<li><strong>Périodiques</strong> : tous les trois mois, tous les ans.</li>
<li><strong>Selon compteur</strong> : tous les 10 000 cycles, toutes les 500 heures de marche.</li>
</ul>
<p>Les compteurs sont des <strong>points de mesure</strong> sur l'équipement. Chaque relevé crée un <strong>document de mesure</strong> ; quand le compteur atteint la prochaine échéance, le plan génère le travail.</p>

<h2>Un travail tout trouvé pour l'informatique industrielle</h2>
<p>Les automates et la supervision comptent déjà les cycles et les heures de marche. Envoyer ces compteurs à SAP sous forme de documents de mesure, par le MES ou une interface, remplace les relevés manuels et permet à la maintenance de suivre l'usage réel de chaque machine.</p>
""",
 example="La presse de la ligne 1 est le poste technique 1100-L1-PRESSE ; sa pompe hydraulique est un équipement avec un compteur d'heures de marche. Chaque nuit, une interface lit le compteur d'heures dans la supervision et crée un document de mesure. À 2 000 heures, le plan d'entretien crée un ordre de remplacement du filtre, avec le filtre déjà prévu comme pièce de rechange.",
 keys=["Poste technique : un emplacement. Équipement : un objet qui peut passer d'un emplacement à l'autre.", "Avis (IW21) pour signaler, ordre (IW31) pour planifier, exécuter et rassembler les coûts.", "Les plans d'entretien sont périodiques ou selon compteur.", "Points de mesure et documents de mesure peuvent être alimentés par les compteurs des automates."],
),
# ------------------------------------------------------------------ 9
dict(
 slug="lecon-9",
 title="Lots et traçabilité",
 lead="Lots, numéros de série et utilisations : comment SAP répond à la question par laquelle commence chaque rappel de produits.",
 goals=["Savoir ce qu'apporte la gestion par lots.", "Distinguer traçabilité ascendante et descendante.", "Comprendre pourquoi l'atelier fait ou défait la traçabilité."],
 body="""
<h2>Les lots</h2>
<p>Un <strong>lot</strong> (batch) est une quantité d'article fabriquée ou reçue dans les mêmes conditions et suivie sous un même numéro. La gestion par lots s'active <strong>par article</strong> : seuls les articles qui ont besoin de traçabilité en ont.</p>
<p>Les lots sont décrits par des <strong>caractéristiques</strong> dans leur classification : viscosité, couleur, lot fournisseur, et les dates qui comptent, comme la date de fabrication et la <strong>date limite de conservation</strong> (SLED), que SAP peut calculer à partir de la durée de conservation de l'article.</p>

<h2>Choisir les lots</h2>
<p>À la sortie de stock, la <strong>détermination des lots</strong> propose les lots à prendre, selon une stratégie : FIFO (premier entré, premier sorti) ou FEFO (premier périmé, premier sorti), et des valeurs de caractéristiques qui doivent correspondre.</p>

<h2>La traçabilité</h2>
<ul>
<li><strong>Ascendante</strong> : d'un lot de produit vers les lots de composants, et de là vers les fournisseurs.</li>
<li><strong>Descendante</strong> : d'un lot de composant vers tous les lots de produits qui l'ont utilisé, et vers tous les clients qui les ont reçus. C'est ce dont un rappel a besoin.</li>
</ul>
<p>La liste des utilisations des lots et le <strong>cockpit d'information sur les lots</strong> (<code>BMBC</code>) montrent ces liens.</p>

<h2>Les numéros de série</h2>
<p>Un lot suit un groupe d'unités. Quand chaque unité doit être suivie individuellement, comme chaque pompe avec son propre relevé de test, SAP utilise des <strong>numéros de série</strong>. Lots et numéros de série peuvent être utilisés ensemble.</p>

<h2>Le maillon faible est en atelier</h2>
<p>SAP ne connaît que les lots qui ont été saisis. Si la ligne consomme le lot B alors que SAP enregistre le lot A, la traçabilité est fausse, et personne ne s'en apercevra avant le jour où on en aura besoin. Scanner les étiquettes de lot en ligne, et laisser le MES saisir les sorties de stock par lot, c'est ce qui rend la traçabilité fiable.</p>
""",
 example="Un fournisseur prévient qu'un lot de joints est défectueux. La traçabilité descendante depuis ce lot de joints liste les trois lots de pompes qui l'ont utilisé, et les livraisons qui les ont expédiés. Comme la ligne scanne chaque boîte de joints, la réponse prend quelques minutes et ne concerne que les pompes réellement touchées.",
 keys=["La gestion par lots s'active par article ; les lots sont décrits par des caractéristiques.", "FIFO prend le lot le plus ancien, FEFO celui qui périme le premier.", "Ascendante : ce qui est entré dedans. Descendante : où il est allé.", "La traçabilité ne vaut que ce que valent les lots scannés et saisis en ligne."],
),
# ------------------------------------------------------------------ 10
dict(
 slug="lecon-10",
 title="Connecter et sécuriser l'atelier",
 lead="Comment les données circulent vraiment entre SAP et les machines, quels canaux existent, et comment éviter que ce lien devienne une porte d'entrée dans l'usine.",
 goals=["Connaître les canaux entre SAP et l'usine.", "Suivre un compteur de ligne jusqu'à une confirmation dans SAP.", "Appliquer les règles de sécurité de base au lien SAP."],
 body="""
<h2>Traduire entre deux mondes</h2>
<p>Un automate connaît des variables, des compteurs et des événements. SAP connaît des ordres, des confirmations et des mouvements de stock. Entre les deux, quelque chose traduit : un <strong>MES</strong>, une passerelle ou un logiciel intermédiaire.</p>
{DIAGRAM_FLOW}

<h2>Les canaux</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Canal</th><th scope="col">En quelques mots</th></tr></thead>
<tbody>
<tr><td>IDoc</td><td>Le format de SAP pour les messages asynchrones : envoyés, mis en file, traités plus tard. <code>LOIPRO</code> sert couramment à envoyer les ordres de fabrication à un MES.</td></tr>
<tr><td>BAPI par RFC</td><td>Des fonctions de SAP que des programmes externes appellent et qui répondent immédiatement, par exemple pour saisir une confirmation.</td></tr>
<tr><td>API OData</td><td>Des services web en HTTPS, documentés sur le SAP Business Accelerator Hub, comme les API des ordres de fabrication et de leurs confirmations.</td></tr>
<tr><td>Connecteurs SAP</td><td>SAP Plant Connectivity (PCo) tourne comme service Windows dans le réseau de l'usine et lit notamment les serveurs OPC UA. Avec SAP Digital Manufacturing, le MES de SAP dans le cloud, c'est le Production Connector qui joue ce rôle.</td></tr>
</tbody></table></div>

<h2>Du compteur à la confirmation</h2>
<ol class="steps">
<li>SAP lance l'ordre et l'envoie au MES (par exemple en IDoc <code>LOIPRO</code>).</li>
<li>L'automate compte les pièces bonnes et rejetées ; le MES lit les compteurs en OPC UA.</li>
<li>À la fin de l'opération, le MES saisit une confirmation avec quantité bonne et rebut (BAPI ou OData).</li>
<li>SAP prélève rétroactivement les composants et comptabilise l'entrée de marchandises.</li>
<li>Les messages en échec sont surveillés : <code>BD87</code> affiche les IDocs par statut et les retraite une fois la cause corrigée.</li>
</ol>

<h2>Sécuriser le lien</h2>
<ul>
<li><strong>Zones et conduits.</strong> Au sens de l'IEC 62443, le réseau bureautique et le réseau de l'usine sont des zones distinctes, et le lien SAP est un conduit entre elles : il passe par une DMZ, il est filtré et il est documenté.</li>
<li><strong>SAP ne parle jamais aux automates.</strong> Il parle au MES ou à la passerelle ; seuls ceux-ci parlent aux automates.</li>
<li><strong>Un utilisateur technique par interface.</strong> Utilisez un utilisateur système ou de communication, qui ne peut pas ouvrir de session interactive, avec les seuls droits dont l'interface a besoin.</li>
<li><strong>Chiffrer.</strong> SNC pour le RFC, HTTPS pour l'OData.</li>
<li><strong>Surveiller.</strong> Les IDocs en échec et les appels refusés sont souvent le premier signe d'un problème, d'un côté comme de l'autre.</li>
</ul>
""",
 example="Une usine connecte ses lignes de montage à S/4HANA. Le MES tourne dans le réseau de l'usine et lit les automates en OPC UA. Il échange avec SAP uniquement via un serveur de la DMZ, avec un utilisateur de communication dédié et un chiffrement SNC. Quand l'équipe réseau voit un nouveau flux du réseau bureautique directement vers un automate, elle sait que ce n'est pas le lien SAP : celui-là ne va jamais là.",
 keys=["Un MES ou une passerelle traduit les signaux machine en événements de gestion.", "IDoc : asynchrone. BAPI/RFC : immédiat. OData : API en HTTPS. PCo et le Production Connector lisent l'OPC UA.", "Compteur, MES, confirmation, prélèvement rétroactif, entrée en stock : rien à taper.", "Zones et conduits, DMZ, utilisateurs techniques dédiés, chiffrement et surveillance."],
),
]

HOME_ANNEX = {
    "h": "Annexe : passer de son ERP à SAP S/4HANA",
    "p": "Facultative. Pourquoi les entreprises passent à S/4HANA, les trois façons d'y aller, le déroulement du projet et une liste de contrôle pour l'informatique industrielle. Ne fait pas partie du QCM final.",
    "label": "Annexe",
}

ANNEX = dict(
 slug="annexe",
 title="Passer de son ERP à SAP S/4HANA",
 lead="Annexe facultative : pourquoi les entreprises passent à S/4HANA maintenant, les trois façons d'y aller, le déroulement d'un tel projet et ce que l'informatique industrielle doit préparer côté atelier.",
 goals=["Savoir pourquoi tant d'entreprises passent à S/4HANA maintenant.", "Distinguer nouvelle implémentation, conversion de système et transition sélective des données.", "Préparer le côté atelier du projet : interfaces, identifiants, bascule."],
 body="""
<h2>Pourquoi maintenant</h2>
<ul>
<li><strong>La fin de SAP ECC.</strong> La maintenance standard de SAP ECC se termine fin 2027. Une maintenance étendue optionnelle, plus chère, court jusqu'à fin 2030. Les investissements de SAP vont à S/4HANA, que SAP s'est engagé à faire évoluer au moins jusqu'en 2040.</li>
<li><strong>Un seul système pour le groupe.</strong> Les groupes remplacent souvent les ERP locaux, SAP ou non, par un modèle S/4HANA unique, pour que tous les sites travaillent et rapportent de la même façon.</li>
</ul>

<h2>Trois façons d'y aller</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Approche</th><th scope="col">Ce que ça veut dire</th><th scope="col">Cas typique</th></tr></thead>
<tbody>
<tr><td>Nouvelle implémentation (greenfield)</td><td>Un nouveau système S/4HANA construit sur les processus standard ; seule une sélection de données est migrée.</td><td>La seule voie depuis un ERP qui n'est pas SAP ; choisie aussi pour repartir propre.</td></tr>
<tr><td>Conversion de système (brownfield)</td><td>Un système SAP ECC existant est converti en S/4HANA, avec ses données et ses réglages.</td><td>Un système ECC en bonne santé, quand l'historique doit être gardé.</td></tr>
<tr><td>Transition sélective des données</td><td>Un nouveau système vide, dans lequel on reprend les données, sociétés ou périodes choisies.</td><td>Groupes qui fusionnent des systèmes ou séparent une activité.</td></tr>
</tbody></table></div>

<h2>Le modèle du groupe</h2>
<p>Dans un groupe, une équipe centrale conçoit en général un <strong>modèle global</strong> (template) : processus, réglages et règles de données de base communs à tous les sites, puis déployés site après site. Chaque site adapte ses habitudes au standard plutôt que l'inverse : c'est le <strong>fit-to-standard</strong>. SAP parle aussi de <strong>clean core</strong> : garder le système SAP aussi standard que possible et placer à côté les développements propres à l'entreprise, pour que les mises à jour futures restent simples.</p>

<h2>Le déroulement du projet</h2>
<p>La plupart des projets suivent <strong>SAP Activate</strong>, la méthode de SAP, en six phases :</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Phase</th><th scope="col">Ce qui se passe</th></tr></thead>
<tbody>
<tr><td>Discover</td><td>Comprendre ce qu'apporte S/4HANA et bâtir le dossier de décision.</td></tr>
<tr><td>Prepare</td><td>Mettre en place l'équipe, le planning, les systèmes et la gouvernance.</td></tr>
<tr><td>Explore</td><td>Ateliers fit-to-standard : les utilisateurs clés découvrent les processus standard dans un bac à sable et listent les vrais écarts.</td></tr>
<tr><td>Realize</td><td>Paramétrer, construire les interfaces et les extensions, faire des chargements de données de test, tout tester ensemble.</td></tr>
<tr><td>Deploy</td><td>Former les utilisateurs, répéter puis réaliser la bascule, démarrer.</td></tr>
<tr><td>Run</td><td>Hypercare juste après le démarrage, puis support normal et améliorations.</td></tr>
</tbody></table></div>

<h2>La migration des données</h2>
<ol class="steps">
<li><strong>Nettoyer</strong> les anciennes données : doublons, articles obsolètes, fournisseurs que plus personne n'utilise.</li>
<li><strong>Faire la correspondance</strong> entre anciens et nouveaux codes : numéros d'article, postes de travail, magasins, unités de mesure.</li>
<li><strong>Charger</strong> avec les outils du projet, souvent le SAP S/4HANA Migration Cockpit, qui fonctionne avec un modèle par type de données.</li>
<li><strong>Contrôler et valider</strong> : les responsables métier confirment que les données chargées sont justes. Plusieurs chargements de test précèdent le vrai.</li>
</ol>
<p>À la bascule, les éléments en cours suivent aussi : ordres ouverts, commandes d'achat ouvertes, et le stock, en général compté juste avant.</p>

<h2>Liste de contrôle pour l'informatique industrielle</h2>
<ul class="checklist">
<li><strong>Lister tous les flux</strong> entre l'ancien ERP et l'usine : ordres envoyés au MES, confirmations, impression d'étiquettes, scanners, balances, résultats qualité, compteurs de maintenance. Pour chacun : sens, protocole, fréquence, responsable.</li>
<li><strong>Vérifier les identifiants et la longueur des champs.</strong> Les numéros d'ordre de fabrication ont 12 caractères dans SAP ; les numéros d'article peuvent en avoir jusqu'à 40 dans S/4HANA. Les tables du MES, les champs des IHM, les chaînes des automates et les codes-barres taillés pour l'ancien ERP peuvent les tronquer.</li>
<li><strong>Se mettre d'accord sur les magasins et les postes de travail</strong> avec le projet, pour que ce que voit l'atelier corresponde à ce que sait SAP.</li>
<li><strong>Reconstruire les interfaces</strong> avec les canaux de SAP (IDoc, BAPI, OData) et les tester de bout en bout dans le système de test, avec les vrais scanners et imprimantes.</li>
<li><strong>Sécuriser les nouveaux conduits</strong> : règles de pare-feu, utilisateurs techniques, chiffrement, documentation (leçon 10).</li>
<li><strong>Planifier la bascule avec la production</strong> : production réduite ou arrêt, inventaire, gel des données de base, et un plan de repli si le démarrage est reporté.</li>
<li><strong>Préparer l'hypercare</strong> : qui appeler, comment les erreurs d'interface sont surveillées, en combien de temps elles sont corrigées.</li>
<li><strong>Former les utilisateurs clés et les opérateurs</strong> : écrans, étiquettes et gestes de scan changent tous.</li>
</ul>
""",
 example="Un groupe décide de remplacer l'ERP local d'un site par son modèle S/4HANA. L'informatique industrielle liste quatorze flux avec l'usine. Les tests montrent que le MES attend des numéros d'ordre à 8 chiffres alors que SAP en envoie 12 : la table du MES et les mises en page des étiquettes sont modifiées avant le démarrage. Après deux chargements de test, le site démarre sur un long week-end, juste après un inventaire. La première semaine, trente IDocs échouent sur une correspondance d'unités de mesure ; l'hypercare corrige la correspondance et les retraite.",
 keys=["La maintenance standard d'ECC se termine fin 2027 ; la maintenance étendue court jusqu'en 2030.", "Depuis un ERP non SAP : nouvelle implémentation. Depuis ECC : conversion, nouvelle implémentation ou transition sélective.", "SAP Activate : Discover, Prepare, Explore (fit-to-standard), Realize, Deploy, Run.", "Pour l'informatique industrielle : lister les flux, vérifier la longueur des champs, reconstruire et tester les interfaces, planifier la bascule et l'hypercare."],
)
