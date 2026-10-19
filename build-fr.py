"""Build the French pages for inthebinder.com.

    python3 build-fr.py

Creates fr/index.html, fr/privacy.html and fr/beta/index.html from the English
originals, adds an EN/FR switcher + hreflang to the English home and privacy
pages, and refreshes sitemap.xml. Asset paths are absolute ("/logo.png"), so
the French pages under /fr/ load the same images and fonts.

Each English string below must appear the expected number of times in its page,
or the build stops and names the one that is wrong.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://inthebinder.com"


def apply_pairs(html, pairs, where):
    for pair in pairs:
        en, fr = pair[0], pair[1]
        want = pair[2] if len(pair) > 2 else 1
        got = html.count(en)
        if got != want:
            sys.exit("STOP [%s]: expected %d of %r, found %d" % (where, want, en[:60], got))
        html = html.replace(en, fr)
    return html


def hreflang(path_en, path_fr):
    return (
        '\n<link rel="alternate" hreflang="en" href="%s%s">'
        '\n<link rel="alternate" hreflang="fr" href="%s%s">'
        '\n<link rel="alternate" hreflang="x-default" href="%s%s">'
        % (BASE, path_en, BASE, path_fr, BASE, path_en)
    )


def add_hreflang(html, path_en, path_fr):
    if "hreflang" in html:
        return html
    return html.replace("</title>", "</title>" + hreflang(path_en, path_fr), 1)


# ── Home page ──────────────────────────────────────────────────────────────
HOME = [
    ('<html lang="en">', '<html lang="fr">'),
    ("<title>In the Binder app: card scanner and collection tracker for Pokémon, One Piece, Lorcana and more</title>",
     "<title>Application In the Binder : scanner de cartes et suivi de collection pour Pokémon, One Piece, Lorcana et plus</title>"),
    ('content="In the Binder is a free trading card collection app for Android: Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering and Yu-Gi-Oh!. Scan cards with your camera, including Japanese, Korean and Chinese Pokémon prints, file them into binders by set, check centring for PSA grading, track slabs and see what your collection is worth. Works offline."',
     'content="In the Binder est une application gratuite de collection de cartes pour Android : Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering et Yu-Gi-Oh!. Scannez vos cartes à la caméra, y compris les éditions japonaises, coréennes et chinoises de Pokémon, classez-les en classeurs par série, vérifiez le centrage pour la gradation PSA, suivez vos slabs et connaissez la valeur de votre collection. Fonctionne hors ligne."'),
    ('content="In the Binder: your card collection, in your pocket"',
     'content="In the Binder : votre collection de cartes, dans votre poche"'),
    ('content="Scan cards, fill your binders set by set, and see what your collection is worth. Free on Android, iPhone beta on TestFlight."',
     'content="Scannez vos cartes, remplissez vos classeurs série par série et découvrez la valeur de votre collection. Gratuit sur Android, bêta iPhone sur TestFlight."'),
    ('content="en_GB"', 'content="fr_FR"'),
    ('<link rel="canonical" href="https://inthebinder.com/">',
     '<link rel="canonical" href="https://inthebinder.com/fr/">'),
    # nav
    ('<a href="#screens">Screens</a>', '<a href="#screens">Aperçu</a>'),
    ('<a href="#features">Features</a>', '<a href="#features">Fonctions</a>'),
    ('<a href="#security">Security</a>', '<a href="#security">Sécurité</a>'),
    ('<a href="/app/">Web version</a>', '<a href="/app/">Version web</a>'),
    ('<a class="nav-get" href="#get">Get the app</a>', '<a class="nav-get" href="#get">Obtenir l\'appli</a>'),
    # mobile dock
    ("<span>Screens</span>", "<span>Aperçu</span>"),
    ("<span>Features</span>", "<span>Fonctions</span>"),
    ("<span>Security</span>", "<span>Sécurité</span>"),
    ("<span>Web app</span>", "<span>Appli web</span>"),
    ('aria-label="Get the app"', 'aria-label="Obtenir l\'appli"'),
    ('aria-label="Quick links"', 'aria-label="Accès rapide"'),
    ('aria-label="Main"', 'aria-label="Menu principal"'),
    # store buttons (hero + get band)
    ("<small>Get it on</small>Google Play", "<small>Disponible sur</small>Google Play", 2),
    ("<small>iPhone beta on</small>TestFlight", "<small>Bêta iPhone sur</small>TestFlight", 2),
    ('href="/beta/#iphone"', 'href="/fr/beta/#iphone"', 2),
    # hero
    ('<div class="eyebrow">Trading card collection app</div>',
     '<div class="eyebrow">Application de collection de cartes</div>'),
    ('Your whole collection, <span class="holo">in your pocket.</span>',
     'Toute votre collection, <span class="holo">dans votre poche.</span>'),
    ("Point your camera at a card and In the Binder knows which one it is. It files the card into its set's binder and shows what it's worth. Page by page, you watch every set fill up.",
     "Pointez votre caméra sur une carte et In the Binder sait laquelle c'est. Il la classe dans le classeur de sa série et indique sa valeur. Page après page, vous regardez chaque série se remplir."),
    ('<a class="btn" href="/app/">Open on the web <span class="soon">NEW</span></a>',
     '<a class="btn" href="/app/">Ouvrir sur le web <span class="soon">NOUVEAU</span></a>'),
    ('On an iPhone or a computer? <a href="/app/" style="color:inherit;text-decoration:underline">Use the web version</a>, free, no install.',
     "Sur iPhone ou ordinateur ? <a href=\"/app/\" style=\"color:inherit;text-decoration:underline\">Utilisez la version web</a>, gratuite, sans installation."),
    ('alt="In the Binder home screen showing the collector\'s sets with progress"',
     'alt="Écran d\'accueil d\'In the Binder montrant les séries du collectionneur et leur progression"'),
    # screens
    ("<h2>See it in action</h2>", "<h2>En images</h2>"),
    ('<p class="sub">Real screens from the Android app. Swipe or tap the arrows.</p>',
     '<p class="sub">De vraies captures de l\'appli Android. Faites glisser ou utilisez les flèches.</p>'),
    ('aria-label="App screens"', 'aria-label="Captures de l\'appli"'),
    ('aria-label="Previous screen"', 'aria-label="Capture précédente"'),
    ('aria-label="Next screen"', 'aria-label="Capture suivante"'),
    ("<figcaption>Every set as a real binder</figcaption>",
     "<figcaption>Chaque série comme un vrai classeur</figcaption>"),
    ('alt="A set shown as binder pages, nine pockets a page"',
     'alt="Une série présentée en pages de classeur, neuf pochettes par page"'),
    ("<figcaption>Scan: your photo next to the match</figcaption>",
     "<figcaption>Scan : votre photo à côté de la correspondance</figcaption>"),
    ('alt="Scanner matching a photographed card to its printing"',
     'alt="Le scanner associe une carte photographiée à son édition"'),
    ("<figcaption>Graded slabs, PSA to CGC</figcaption>",
     "<figcaption>Slabs gradés, de PSA à CGC</figcaption>"),
    ('alt="A PSA graded slab recognised with grader and grade"',
     'alt="Un slab gradé PSA reconnu avec son organisme et sa note"'),
    ("<figcaption>Binders per language</figcaption>",
     "<figcaption>Un classeur par langue</figcaption>"),
    ('alt="Collection shelf of binders with language tabs"',
     'alt="Étagère de classeurs avec onglets par langue"'),
    ("<figcaption>Themes: carbon, underwater, forest…</figcaption>",
     "<figcaption>Thèmes : carbone, sous-marin, forêt…</figcaption>"),
    ('alt="Home screen in the carbon fibre theme"',
     'alt="Écran d\'accueil avec le thème fibre de carbone"'),
    ("<figcaption>Make it yours</figcaption>", "<figcaption>À votre image</figcaption>"),
    ('alt="Theme picker in settings"', 'alt="Choix du thème dans les réglages"'),
    # exclusive
    ("<h2>Things other card apps don't do</h2>",
     "<h2>Ce que les autres applis de cartes ne font pas</h2>"),
    ('<p class="sub">Built by a collector who wanted more than a list.</p>',
     '<p class="sub">Conçue par un collectionneur qui voulait plus qu\'une simple liste.</p>'),
    ('<span class="tag">GRADING</span><h3>AI centring check before you submit</h3><p>Hold a card under the camera and the borders are measured automatically. You see the best grade centring alone allows at PSA, BGS and CGC, before you pay for grading. A manual mode lets you nudge every edge by 0.1 mm.</p>',
     '<span class="tag">GRADATION</span><h3>Vérification du centrage par IA avant l\'envoi</h3><p>Placez une carte sous la caméra et les bords sont mesurés automatiquement. Vous voyez la meilleure note que le centrage seul autorise chez PSA, BGS et CGC, avant de payer la gradation. Un mode manuel permet d\'ajuster chaque bord au 0,1 mm.</p>'),
    ('<span class="tag">SLABS</span><h3>Tap a slab, done</h3><p>Hold an NFC-chipped slab to the back of your phone and the certificate is read instantly, no buttons. No chip? Point the camera at the label and the cert number is read for you.</p>',
     '<span class="tag">SLABS</span><h3>Un slab, un contact, c\'est lu</h3><p>Approchez un slab à puce NFC du dos de votre téléphone et le certificat est lu instantanément, sans bouton. Pas de puce ? Pointez la caméra sur l\'étiquette et le numéro de certificat est lu pour vous.</p>'),
    ('<span class="tag">6 GAMES</span><h3>Six card games, never mixed</h3><p>Pokémon, One Piece, Lorcana, Dragon Ball Super Fusion World, Magic and Yu-Gi-Oh! each get their own binders, slabs and sealed product. Every printing has its own pocket: normal, parallel, foil, alternate art. A game downloads only when you open it, so the app stays small.</p>',
     '<span class="tag">6 JEUX</span><h3>Six jeux de cartes, jamais mélangés</h3><p>Pokémon, One Piece, Lorcana, Dragon Ball Super Fusion World, Magic et Yu-Gi-Oh! ont chacun leurs classeurs, leurs slabs et leurs produits scellés. Chaque édition a sa propre pochette : normale, parallèle, holo, illustration alternative. Un jeu ne se télécharge qu\'à son ouverture, pour garder l\'appli légère.</p>'),
    ('<span class="tag">8 LANGUAGES</span><h3>Japanese, Korean and Chinese Pokémon sets</h3><p>Separate Pokémon binders for English, French, Italian, Spanish, German, Japanese, Korean and Chinese printings, with thousands of Asian cards recognised by the scanner.</p>',
     '<span class="tag">8 LANGUES</span><h3>Séries Pokémon japonaises, coréennes et chinoises</h3><p>Des classeurs Pokémon distincts pour les éditions anglaise, française, italienne, espagnole, allemande, japonaise, coréenne et chinoise, avec des milliers de cartes asiatiques reconnues par le scanner.</p>'),
    ('<span class="tag">WEB</span><h3>Your binder on a big screen</h3><p>Open your collection on a computer or any phone at <a href="/app/" style="color:inherit;text-decoration:underline">inthebinder.com/app</a>: every card of every game, its value over time, grading picks with eBay sold prices for PSA 10, BGS and CGC, and the centring tool for your photos. Your collection stays in your browser, nothing is uploaded.</p>',
     '<span class="tag">WEB</span><h3>Votre classeur sur grand écran</h3><p>Ouvrez votre collection sur un ordinateur ou n\'importe quel téléphone sur <a href="/app/" style="color:inherit;text-decoration:underline">inthebinder.com/app</a> : chaque carte de chaque jeu, sa valeur dans le temps, les choix de gradation avec les prix de vente eBay pour PSA 10, BGS et CGC, et l\'outil de centrage pour vos photos. Votre collection reste dans votre navigateur, rien n\'est envoyé.</p>'),
    ('<span class="tag">SWITCHING</span><h3>Bring your collection with you</h3><p>Import your whole PriceCharting collection in one go, with nothing lost: anything that can\'t be matched is kept with its value. Back up to a single file anytime.</p>',
     '<span class="tag">MIGRATION</span><h3>Emportez votre collection avec vous</h3><p>Importez toute votre collection PriceCharting d\'un coup, sans rien perdre : ce qui ne peut être associé est conservé avec sa valeur. Sauvegardez dans un seul fichier à tout moment.</p>'),
    # features
    ("<h2>Built by a collector, for collectors</h2>",
     "<h2>Conçue par un collectionneur, pour les collectionneurs</h2>"),
    ("Everything you'd do with a real binder, a price guide and a notebook, in one place, and it works offline.",
     "Tout ce que vous feriez avec un vrai classeur, un argus et un carnet, au même endroit, et ça marche hors ligne."),
    ("<h3>Scan by picture</h3><p>Recognition runs on your phone. It reads the artwork, not just the text, so glare, sleeves and whole 9-pocket pages are fine. If it isn't sure, it asks rather than guessing. It reads printed codes like OP01-003 or LOB-EN001 too, and learns the look of your own cards from every scan you confirm.</p>",
     "<h3>Scan par l'image</h3><p>La reconnaissance tourne sur votre téléphone. Elle lit l'illustration, pas seulement le texte : reflets, protections et pages entières de 9 pochettes ne posent aucun problème. En cas de doute, elle demande plutôt que de deviner. Elle lit aussi les codes imprimés comme OP01-003 ou LOB-EN001, et apprend l'aspect de vos propres cartes à chaque scan que vous confirmez.</p>"),
    ("<h3>Binders, set by set</h3><p>Each set is a leather binder with nine cards a page. Empty pockets show what you're still hunting. Normal, reverse holo, holo, parallels and foils are tracked separately.</p>",
     "<h3>Des classeurs, série par série</h3><p>Chaque série est un classeur en cuir de neuf cartes par page. Les pochettes vides montrent ce qu'il vous reste à trouver. Normales, reverse holo, holo, parallèles et foils sont suivies séparément.</p>"),
    ("<h3>Know what it's worth</h3><p>Market prices for each printing, price history over time, and your whole portfolio's value at a glance.</p>",
     "<h3>Connaissez sa valeur</h3><p>Les prix du marché pour chaque édition, l'historique des prix dans le temps et la valeur de tout votre portefeuille en un coup d'œil.</p>"),
    ("<h3>Graded slabs</h3><p>Track PSA, BGS, CGC, ACE, AURA and more. Read the certificate from the label or tap an NFC-chipped slab.</p>",
     "<h3>Slabs gradés</h3><p>Suivez PSA, BGS, CGC, ACE, AURA et d'autres. Lisez le certificat depuis l'étiquette ou par contact sur un slab à puce NFC.</p>"),
    ('<h3>Search like it\'s printed</h3><p>Type "070/084" or a name with a typo, and it still finds the card.</p>',
     '<h3>Cherchez comme c\'est imprimé</h3><p>Tapez « 070/084 » ou un nom avec une faute, il trouve quand même la carte.</p>'),
    ("<h3>Sealed product too</h3><p>Booster boxes, ETBs, decks and tins by barcode or straight from each game's catalogue, alongside your cards and slabs.</p>",
     "<h3>Les produits scellés aussi</h3><p>Displays, ETB, decks et boîtes métal par code-barres ou directement depuis le catalogue de chaque jeu, aux côtés de vos cartes et de vos slabs.</p>"),
    # security
    ("<h2>Secure by design</h2>", "<h2>Sécurisé dès la conception</h2>"),
    ("A collection can be worth thousands. In the Binder never asks you to hand it to a server: there's no account to hack and no cloud database to leak.",
     "Une collection peut valoir des milliers d'euros. In the Binder ne vous demande jamais de la confier à un serveur : aucun compte à pirater, aucune base de données dans le cloud à faire fuiter."),
    ("<li>No sign-up, no login, no password to leak</li>",
     "<li>Aucune inscription, aucune connexion, aucun mot de passe à faire fuiter</li>"),
    ("<li>Your collection is stored only on your phone and works fully offline</li>",
     "<li>Votre collection n'est stockée que sur votre téléphone et fonctionne entièrement hors ligne</li>"),
    ("<li>Card recognition runs on the device; your photos are never uploaded</li>",
     "<li>La reconnaissance des cartes se fait sur l'appareil ; vos photos ne sont jamais envoyées</li>"),
    ("<li>Only the permissions it needs: camera to scan, NFC to read slabs</li>",
     "<li>Seulement les autorisations nécessaires : la caméra pour scanner, le NFC pour lire les slabs</li>"),
    ("<li>Distributed through Google Play, signed and checked by Google</li>",
     "<li>Distribuée via Google Play, signée et vérifiée par Google</li>"),
    ("<li>Everything online is encrypted (HTTPS only, HSTS)</li>",
     "<li>Tout ce qui passe en ligne est chiffré (HTTPS uniquement, HSTS)</li>"),
    ("<li>Your data, your file: export or back up whenever you like</li>",
     "<li>Vos données, votre fichier : exportez ou sauvegardez quand vous voulez</li>"),
    ('<li>Read the full <a href="/privacy.html">privacy policy</a></li>',
     '<li>Lire la <a href="/fr/privacy.html">politique de confidentialité</a> complète</li>'),
    # faq
    ("<h2>Questions</h2>", "<h2>Questions</h2>"),
    ("<h3>What is In the Binder?</h3>\n    <p>In the Binder is a free Android app for trading card collectors. You scan cards with your phone camera, file them into binders set by set, check centring before sending cards for grading, track graded slabs and see what your collection is worth.</p>",
     "<h3>Qu'est-ce qu'In the Binder ?</h3>\n    <p>In the Binder est une application Android gratuite pour les collectionneurs de cartes. Vous scannez vos cartes avec la caméra de votre téléphone, les classez en classeurs série par série, vérifiez le centrage avant de les envoyer à la gradation, suivez vos slabs gradés et découvrez la valeur de votre collection.</p>"),
    ("<h3>Which card games does it support?</h3>\n    <p>Pokémon (including Japanese, Korean and Chinese prints), plus the English editions of One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering and Yu-Gi-Oh!. Each game has its own binders, slabs and sealed product, never mixed. A game's card list downloads the first time you open it.</p>",
     "<h3>Quels jeux de cartes sont pris en charge ?</h3>\n    <p>Pokémon (y compris les éditions japonaise, coréenne et chinoise), ainsi que les éditions anglaises de One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering et Yu-Gi-Oh!. Chaque jeu a ses propres classeurs, slabs et produits scellés, jamais mélangés. La liste des cartes d'un jeu se télécharge à sa première ouverture.</p>"),
    ("<h3>Is In the Binder free?</h3>\n    <p>Yes. The app is free to download and use.</p>",
     "<h3>In the Binder est-il gratuit ?</h3>\n    <p>Oui. L'application est gratuite à télécharger et à utiliser.</p>"),
    ("<h3>Does it work with Japanese, Korean and Chinese cards?</h3>\n    <p>Yes. The scanner and binders support English, French, Italian, Spanish, German, Japanese, Korean and Chinese prints.</p>",
     "<h3>Fonctionne-t-il avec les cartes japonaises, coréennes et chinoises ?</h3>\n    <p>Oui. Le scanner et les classeurs prennent en charge les éditions anglaise, française, italienne, espagnole, allemande, japonaise, coréenne et chinoise.</p>"),
    ("<h3>Can it help me before sending cards to PSA?</h3>\n    <p>The centring check measures the borders of your card from a photo and compares them with the centring limits used by PSA, BGS and CGC. It is a guide only; the final grade is always the grading company's decision.</p>",
     "<h3>Peut-il m'aider avant d'envoyer mes cartes à PSA ?</h3>\n    <p>La vérification du centrage mesure les bords de votre carte à partir d'une photo et les compare aux limites de centrage utilisées par PSA, BGS et CGC. C'est une indication seulement ; la note finale reste toujours la décision de l'organisme de gradation.</p>"),
    ("<h3>Is it available on iPhone?</h3>\n    <p>Yes, as a beta. Anyone can join the iPhone beta through Apple's TestFlight app from inthebinder.com/beta, and the App Store release is coming soon. The web version also works on any iPhone.</p>",
     "<h3>Est-il disponible sur iPhone ?</h3>\n    <p>Oui, en bêta. Tout le monde peut rejoindre la bêta iPhone avec l'appli TestFlight d'Apple depuis inthebinder.com/fr/beta, et la version App Store arrive bientôt. La version web fonctionne aussi sur tous les iPhone.</p>"),
    ("<h3>Does it need an internet connection?</h3>\n    <p>No. Your collection is stored on your phone and the app works offline. Prices update when you are online.</p>",
     "<h3>Faut-il une connexion internet ?</h3>\n    <p>Non. Votre collection est stockée sur votre téléphone et l'application fonctionne hors ligne. Les prix se mettent à jour quand vous êtes connecté.</p>"),
    # beta cta band
    ("<h2>Get In the Binder</h2>", "<h2>Obtenez In the Binder</h2>"),
    ("Free on Android through Google Play, and the iPhone beta is open on TestFlight. The web version works on any device today.",
     "Gratuit sur Android via Google Play, et la bêta iPhone est ouverte sur TestFlight. La version web fonctionne dès aujourd'hui sur tous les appareils."),
    ('<a class="btn" href="/app/">Open on the web</a>', '<a class="btn" href="/app/">Ouvrir sur le web</a>'),
    # feature pictures
    ('alt="A card framed by measurement guides along its four borders"', 'alt="Une carte encadrée de repères de mesure sur ses quatre bords"'),
    ('alt="A graded slab tapped against the back of a phone"', 'alt="Un slab gradé posé contre le dos d\'un téléphone"'),
    ('alt="Six trading cards fanned out, one per game"', 'alt="Six cartes en éventail, une par jeu"'),
    ('alt="A shelf of binders with a coloured tab for each language"', 'alt="Une étagère de classeurs avec un onglet de couleur par langue"'),
    ('alt="A laptop showing a grid of cards and a price chart"', 'alt="Un ordinateur portable affichant une grille de cartes et une courbe de prix"'),
    ('alt="Cards moving from a storage box into a binder"', 'alt="Des cartes passant d\'une boîte de rangement à un classeur"'),
    # footer
    ('<span>© 2026 In the Binder · <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> · <a href="/privacy.html">Privacy</a></span>',
     '<span>© 2026 In the Binder · <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> · <a href="/fr/privacy.html">Confidentialité</a></span>'),
    ("In the Binder is an independent app and is not affiliated with, endorsed or sponsored by Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami or any other card publisher. All card names, images and trademarks belong to their respective owners. In the Binder may earn a commission from purchases made through its links to marketplaces.",
     "In the Binder est une application indépendante, sans affiliation, approbation ou parrainage de Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami ou tout autre éditeur de cartes. Tous les noms de cartes, images et marques appartiennent à leurs propriétaires respectifs. In the Binder peut percevoir une commission sur les achats effectués via ses liens vers des places de marché."),
    # structured data (FAQ + app listing Google reads) — must match the visible French text
    ('"name":"What is In the Binder?","acceptedAnswer":{"@type":"Answer","text":"In the Binder is a free Android app for trading card collectors. You scan cards with your phone camera, file them into binders set by set, check centring before sending cards for grading, track graded slabs and see what your collection is worth."}',
     '"name":"Qu\'est-ce qu\'In the Binder ?","acceptedAnswer":{"@type":"Answer","text":"In the Binder est une application Android gratuite pour les collectionneurs de cartes. Vous scannez vos cartes avec la caméra de votre téléphone, les classez en classeurs série par série, vérifiez le centrage avant de les envoyer à la gradation, suivez vos slabs gradés et découvrez la valeur de votre collection."}'),
    ('"name":"Which card games does it support?","acceptedAnswer":{"@type":"Answer","text":"Pokémon (including Japanese, Korean and Chinese prints), plus the English editions of One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering and Yu-Gi-Oh!. Each game has its own binders, slabs and sealed product, never mixed. A game\'s card list downloads the first time you open it."}',
     '"name":"Quels jeux de cartes sont pris en charge ?","acceptedAnswer":{"@type":"Answer","text":"Pokémon (y compris les éditions japonaise, coréenne et chinoise), ainsi que les éditions anglaises de One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering et Yu-Gi-Oh!. Chaque jeu a ses propres classeurs, slabs et produits scellés, jamais mélangés. La liste des cartes d\'un jeu se télécharge à sa première ouverture."}'),
    ('"name":"Is In the Binder free?","acceptedAnswer":{"@type":"Answer","text":"Yes. The app is free to download and use."}',
     '"name":"In the Binder est-il gratuit ?","acceptedAnswer":{"@type":"Answer","text":"Oui. L\'application est gratuite à télécharger et à utiliser."}'),
    ('"name":"Does it work with Japanese, Korean and Chinese cards?","acceptedAnswer":{"@type":"Answer","text":"Yes. The scanner and binders support English, French, Italian, Spanish, German, Japanese, Korean and Chinese prints."}',
     '"name":"Fonctionne-t-il avec les cartes japonaises, coréennes et chinoises ?","acceptedAnswer":{"@type":"Answer","text":"Oui. Le scanner et les classeurs prennent en charge les éditions anglaise, française, italienne, espagnole, allemande, japonaise, coréenne et chinoise."}'),
    ('"name":"Can it help me before sending cards to PSA?","acceptedAnswer":{"@type":"Answer","text":"The centring check measures the borders of your card from a photo and compares them with the centring limits used by PSA, BGS and CGC. It is a guide only; the final grade is always the grading company\'s decision."}',
     '"name":"Peut-il m\'aider avant d\'envoyer mes cartes à PSA ?","acceptedAnswer":{"@type":"Answer","text":"La vérification du centrage mesure les bords de votre carte à partir d\'une photo et les compare aux limites de centrage utilisées par PSA, BGS et CGC. C\'est une indication seulement ; la note finale reste toujours la décision de l\'organisme de gradation."}'),
    ('"name":"Is it available on iPhone?","acceptedAnswer":{"@type":"Answer","text":"Yes, as a beta. Anyone can join the iPhone beta through Apple\'s TestFlight app from inthebinder.com/beta, and the App Store release is coming soon. The web version also works on any iPhone."}',
     '"name":"Est-il disponible sur iPhone ?","acceptedAnswer":{"@type":"Answer","text":"Oui, en bêta. Tout le monde peut rejoindre la bêta iPhone avec l\'appli TestFlight d\'Apple depuis inthebinder.com/fr/beta, et la version App Store arrive bientôt. La version web fonctionne aussi sur tous les iPhone."}'),
    ('"name":"Does it need an internet connection?","acceptedAnswer":{"@type":"Answer","text":"No. Your collection is stored on your phone and the app works offline. Prices update when you are online."}',
     '"name":"Faut-il une connexion internet ?","acceptedAnswer":{"@type":"Answer","text":"Non. Votre collection est stockée sur votre téléphone et l\'application fonctionne hors ligne. Les prix se mettent à jour quand vous êtes connecté."}'),
    ('"description":"Scan trading cards with your camera (Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering and Yu-Gi-Oh!), file them into binders by set, track graded slabs and see what your collection is worth. Works offline."',
     '"description":"Scannez vos cartes à collectionner avec la caméra (Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering et Yu-Gi-Oh!), classez-les en classeurs par série, suivez vos slabs gradés et découvrez la valeur de votre collection. Fonctionne hors ligne."'),
    ('"featureList":["Camera card scanner","Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering and Yu-Gi-Oh!","English, French, Italian, Spanish, German, Japanese, Korean and Chinese cards","Binders by set with missing-card tracking","Centring check for PSA, BGS and CGC grading","Graded slab and NFC tag reading","Collection value and price tracking","PriceCharting import and CSV backup"]',
     '"featureList":["Scanner de cartes par caméra","Pokémon, One Piece, Disney Lorcana, Dragon Ball Super Fusion World, Magic: The Gathering et Yu-Gi-Oh!","Cartes anglaises, françaises, italiennes, espagnoles, allemandes, japonaises, coréennes et chinoises","Classeurs par série avec suivi des cartes manquantes","Vérification du centrage pour la gradation PSA, BGS et CGC","Lecture des slabs gradés et des tags NFC","Valeur de la collection et suivi des prix","Import PriceCharting et sauvegarde CSV"]'),
    ('"keywords":"pokemon card scanner, one piece card scanner, lorcana collection tracker, mtg collection app, yugioh card scanner, TCG collection tracker, PSA grading centering, card binder app, Japanese pokemon cards"',
     '"keywords":"scanner cartes pokemon, scanner cartes one piece, suivi collection lorcana, appli collection magic, scanner cartes yugioh, gestion collection TCG, centrage gradation PSA, appli classeur cartes, cartes pokemon japonaises, application pokemon carte"'),
    ('"url":"https://inthebinder.com/","author"', '"url":"https://inthebinder.com/fr/","author"'),
    # schema inLanguage (keep simple: flip the two occurrences)
    ('"inLanguage":"en-GB"', '"inLanguage":"fr-FR"', 2),
]

# ── Privacy page ────────────────────────────────────────────────────────────
PRIVACY = [
    ('<html lang="en">', '<html lang="fr">'),
]

# ── Beta page ────────────────────────────────────────────────────────────────
BETA = [
    ('<html lang="en">', '<html lang="fr">'),
    ("<title>In the Binder – Beta</title>", "<title>In the Binder – Bêta</title>"),
    ("<h1>In the Binder beta</h1>", "<h1>Bêta In the Binder</h1>"),
    ('<p class="lead">Thanks for testing. Go to the section for your phone. On Android you only need one of the two ways.</p>',
     '<p class="lead">Merci de tester l\'appli. Allez à la section de votre téléphone. Sur Android, une seule des deux méthodes suffit.</p>'),
    ("<h2>iPhone · TestFlight</h2>", "<h2>iPhone · TestFlight</h2>"),
    ("<p>Apple's own app for testing. Free, no code needed, and new versions arrive by themselves.</p>",
     "<p>L'appli de test d'Apple. Gratuite, sans code, et les nouvelles versions arrivent toutes seules.</p>"),
    (">1 · Get TestFlight from the App Store</a>", ">1 · Installer TestFlight depuis l'App Store</a>"),
    (">2 · Join the In the Binder beta</a>", ">2 · Rejoindre la bêta In the Binder</a>", 0),
    (">2 · Opening soon: Apple is checking the beta</span>", ">2 · Bientôt ouverte : Apple vérifie la bêta</span>", 1),
    ('<p class="wait-note">Apple reviews every new beta, usually within a day. Want a message when it opens? Email <a href="mailto:support@inthebinder.com?subject=iPhone%20beta">support@inthebinder.com</a>.</p>',
     '<p class="wait-note">Apple vérifie chaque nouvelle bêta, généralement en moins d\'un jour. Vous voulez être prévenu à l\'ouverture ? Écrivez à <a href="mailto:support@inthebinder.com?subject=B%C3%AAta%20iPhone">support@inthebinder.com</a>.</p>', 1),
    ("<li>Tap <b>1</b> on your iPhone and install TestFlight. Skip this if you already have it.</li>",
     "<li>Sur votre iPhone, appuyez sur <b>1</b> et installez TestFlight. Passez cette étape si vous l'avez déjà.</li>"),
    ("<li>Come back and tap <b>2</b>, then <b>Accept</b> and <b>Install</b> in TestFlight.</li>",
     "<li>Revenez et appuyez sur <b>2</b>, puis sur <b>Accepter</b> et <b>Installer</b> dans TestFlight.</li>"),
    ("<li>Open In the Binder from your home screen. New test versions show up in TestFlight; turn on <b>Automatic Updates</b> there.</li>",
     "<li>Ouvrez In the Binder depuis votre écran d'accueil. Les nouvelles versions de test apparaissent dans TestFlight ; activez-y les <b>mises à jour automatiques</b>.</li>"),
    ('<p style="margin-top:14px"><b style="color:#f3ecff">Stuck?</b> Open link 2 on the iPhone itself, not on a computer. If TestFlight says the beta is full or not accepting testers, email <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> and we\'ll let you in.</p>',
     '<p style="margin-top:14px"><b style="color:#f3ecff">Bloqué ?</b> Ouvrez le lien 2 sur l\'iPhone lui-même, pas sur un ordinateur. Si TestFlight indique que la bêta est complète ou n\'accepte plus de testeurs, écrivez à <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> et nous vous ajouterons.</p>'),
    ('<h2>Android · Google Play <span class="tag">Recommended</span></h2>',
     '<h2>Android · Google Play <span class="tag">Recommandé</span></h2>'),
    ("<p>Two taps, no email needed. No security warnings, and updates arrive by themselves.</p>",
     "<p>Deux appuis, sans e-mail. Aucun avertissement de sécurité, et les mises à jour arrivent toutes seules.</p>"),
    (">1 · Join the tester group</a>", ">1 · Rejoindre le groupe de testeurs</a>"),
    (">2 · Get the app on Google Play</a>", ">2 · Obtenir l'appli sur Google Play</a>"),
    ("<li>Tap <b>1</b>, sign in with the Google account on your phone, then tap <b>Join group</b>.</li>",
     "<li>Appuyez sur <b>1</b>, connectez-vous avec le compte Google de votre téléphone, puis appuyez sur <b>Rejoindre le groupe</b>.</li>"),
    ("<li>Come back and tap <b>2</b>, then <b>Become a tester</b> and <b>Download it on Google Play</b>.</li>",
     "<li>Revenez et appuyez sur <b>2</b>, puis <b>Devenir testeur</b> et <b>Télécharger sur Google Play</b>.</li>"),
    ("<li>Please keep the app installed for 14 days and open it now and then. That's what gets it into the Play Store for everyone.</li>",
     "<li>Merci de garder l'appli installée pendant 14 jours et de l'ouvrir de temps en temps. C'est ce qui permet sa mise en ligne sur le Play Store pour tout le monde.</li>"),
    ('<p style="margin-top:14px"><b style="color:#f3ecff">Stuck?</b> "App not available" means step 1 wasn\'t finished: open link 1 again and make sure you pressed <b>Join group</b>. "Item not found" means your Play Store app is on a different Google account (tap your photo in the Play Store to switch) or Google needs a few more minutes. Wait 15 minutes and try link 2 again.</p>',
     '<p style="margin-top:14px"><b style="color:#f3ecff">Bloqué ?</b> « Application non disponible » signifie que l\'étape 1 n\'est pas terminée : rouvrez le lien 1 et vérifiez que vous avez bien appuyé sur <b>Rejoindre le groupe</b>. « Élément introuvable » signifie que votre Play Store est sur un autre compte Google (appuyez sur votre photo dans le Play Store pour changer) ou que Google a besoin de quelques minutes de plus. Patientez 15 minutes et réessayez le lien 2.</p>'),
    ("<h2>Android · Direct download (APK)</h2>", "<h2>Android · Téléchargement direct (APK)</h2>"),
    ("<p>For testers without Play access. Enter the personal code you were sent.</p>",
     "<p>Pour les testeurs sans accès au Play Store. Saisissez le code personnel qui vous a été envoyé.</p>"),
    ("That code didn't work. Check it, or ask for a new one.",
     "Ce code n'a pas fonctionné. Vérifiez-le ou demandez-en un nouveau."),
    ('placeholder="Your tester code"', 'placeholder="Votre code testeur"'),
    (">Download for Android</button>", ">Télécharger pour Android</button>"),
    ("<li>When Chrome asks, tap <b>Download anyway</b>. The warning appears for every app outside the Play Store.</li>",
     "<li>Quand Chrome le demande, appuyez sur <b>Télécharger quand même</b>. Cet avertissement apparaît pour toute appli hors du Play Store.</li>"),
    ("<li>Open the file, then allow <b>Install unknown apps</b> for Chrome when asked.</li>",
     "<li>Ouvrez le fichier, puis autorisez <b>Installer des applis inconnues</b> pour Chrome si on vous le demande.</li>"),
    ("<li>Tap <b>Install</b>. If Play Protect asks, tap <b>More details → Install anyway</b>.</li>",
     "<li>Appuyez sur <b>Installer</b>. Si Play Protect le demande, appuyez sur <b>Plus de détails → Installer quand même</b>.</li>"),
    ('<p class="foot"><a href="/">inthebinder.com</a> · <a href="/privacy.html">Privacy</a></p>',
     '<p class="foot"><a href="/fr/">inthebinder.com</a> · <a href="/fr/privacy.html">Confidentialité</a></p>'),
    ('<form action="/beta/apk" method="get">', '<form action="/beta/apk" method="get">'),
    ("In the Binder is an independent app. It is not affiliated with, endorsed or sponsored by Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami or any other card publisher. Card names, images and trademarks belong to their respective owners.",
     "In the Binder est une application indépendante. Elle n'est ni affiliée, ni approuvée, ni parrainée par Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami ou tout autre éditeur de cartes. Les noms de cartes, images et marques appartiennent à leurs propriétaires respectifs."),
]

# English by default; French for French browsers; a switcher click always wins.
# Only pages with a /fr twin get it (not /app/ or /c/, which have no /fr copy).
LANGJS = (
    "<script>(function(){try{var K='h7k_lang',p=location.pathname,onFr=/^\\/fr(\\/|$)/.test(p),s=null;"
    "try{s=localStorage.getItem(K)}catch(e){}"
    "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-lang]');"
    "if(a){try{localStorage.setItem(K,a.getAttribute('data-lang'))}catch(e){}}});"
    "if(onFr||s)return;var L=(navigator.languages||[navigator.language||'']).join(',').toLowerCase();"
    "if(/(^|,)fr(-[a-z]+)?(,|$)/.test(L)){location.replace((p==='/'?'/fr/':'/fr'+p)+location.search+location.hash)}}catch(e){}})();</script>"
)
NAV_SW = '<a href="%s" class="lang-switch" data-lang="%s" aria-label="%s">%s</a>'
ROW_SW = ('<div class="lang-row" style="text-align:right;font-size:.9rem;margin-bottom:-10px">'
          '<a href="%s" class="lang-switch" data-lang="%s" aria-label="%s" style="color:var(--dim)">%s</a></div>')

_CLEAN = [
    re.compile(r'<a href="/fr/" style="color:var\(--dim\);text-decoration:none;margin-left:18px;font-size:\.95rem">FR</a>'),
    re.compile(r'<a [^>]*class="lang-switch"[^>]*>[A-Z]{2}</a>'),
    re.compile(r'\n<div class="lang-row"[^>]*>.*?</div>', re.S),
    re.compile(r"<script>\(function\(\)\{try\{var K='h7k_lang'.*?</script>\n?", re.S),
]


def clean(html):
    """English source without any switcher or language script, so each page is
    rebuilt from the same base and ends up with exactly one switcher."""
    for rx in _CLEAN:
        html = rx.sub("", html)
    return html


def with_js(html):
    return html.replace("</head>", LANGJS + "\n</head>", 1)


def one_switch(name, html):
    n = html.count('class="lang-switch"')
    if n != 1:
        sys.exit("STOP [%s]: %d language switchers" % (name, n))
    return html


def build_home():
    src = clean((ROOT / "index.html").read_text(encoding="utf-8"))
    fr = apply_pairs(src, HOME, "home")
    fr = fr.replace('<a href="/app/">Version web</a>',
                    '<a href="/app/">Version web</a>' + NAV_SW % ("/", "en", "English version", "EN"), 1)
    (ROOT / "fr" / "index.html").write_text(one_switch("fr/index.html", with_js(fr)), encoding="utf-8")

    en = add_hreflang(src, "/", "/fr/")
    en = en.replace('<a href="/app/">Web version</a>',
                    '<a href="/app/">Web version</a>' + NAV_SW % ("/fr/", "fr", "Version française", "FR"), 1)
    (ROOT / "index.html").write_text(one_switch("index.html", with_js(en)), encoding="utf-8")


def build_privacy():
    src = clean((ROOT / "privacy.html").read_text(encoding="utf-8"))
    fr = translate_privacy(src)
    fr = fr.replace("<main>", "<main>\n" + ROW_SW % ("/privacy.html", "en", "English version", "EN"), 1)
    (ROOT / "fr" / "privacy.html").write_text(one_switch("fr/privacy.html", with_js(fr)), encoding="utf-8")

    en = add_hreflang(src, "/privacy.html", "/fr/privacy.html")
    en = en.replace("<main>", "<main>\n" + ROW_SW % ("/fr/privacy.html", "fr", "Version française", "FR"), 1)
    (ROOT / "privacy.html").write_text(one_switch("privacy.html", with_js(en)), encoding="utf-8")


def build_beta():
    src = clean((ROOT / "beta" / "index.html").read_text(encoding="utf-8"))
    fr = apply_pairs(src, BETA, "beta")
    fr = fr.replace("<main>", "<main>\n" + ROW_SW % ("/beta/", "en", "English version", "EN"), 1)
    (ROOT / "fr" / "beta" / "index.html").write_text(one_switch("fr/beta", with_js(fr)), encoding="utf-8")

    en = src.replace("<main>", "<main>\n" + ROW_SW % ("/fr/beta/", "fr", "Version française", "FR"), 1)
    (ROOT / "beta" / "index.html").write_text(one_switch("beta", with_js(en)), encoding="utf-8")


def build_sitemap():
    today = "2026-10-18"
    locs = [
        ("/", today), ("/fr/", today),
        ("/privacy.html", today), ("/fr/privacy.html", today),
        ("/app/", today),
    ]
    rows = "\n".join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (BASE, p, d) for p, d in locs)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n",
        encoding="utf-8")


# translate_privacy is defined in build-fr-privacy.py and imported here.
from build_fr_privacy import translate_privacy  # noqa: E402


if __name__ == "__main__":
    build_home()
    build_beta()
    build_privacy()
    build_sitemap()
    print("Built fr/index.html, fr/beta/index.html, fr/privacy.html, sitemap.xml")
