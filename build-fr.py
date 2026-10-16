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
    ('content="Scan cards, fill your binders set by set, and see what your collection is worth. Now in beta on Android."',
     'content="Scannez vos cartes, remplissez vos classeurs série par série et découvrez la valeur de votre collection. Désormais en bêta sur Android."'),
    ('content="en_GB"', 'content="fr_FR"'),
    ('<link rel="canonical" href="https://inthebinder.com/">',
     '<link rel="canonical" href="https://inthebinder.com/fr/">'),
    # nav
    ('<a href="#screens">Screens</a>', '<a href="#screens">Aperçu</a>'),
    ('<a href="#features">Features</a>', '<a href="#features">Fonctions</a>'),
    ('<a href="#security">Security</a>', '<a href="#security">Sécurité</a>'),
    ('<a href="/app/">Web version</a>', '<a href="/app/">Version web</a>'),
    ('<a href="/beta/">Join the beta</a>', '<a href="/fr/beta/">Rejoindre la bêta</a>'),
    # hero
    ('<div class="eyebrow">Trading card collection app</div>',
     '<div class="eyebrow">Application de collection de cartes</div>'),
    ('Your whole collection, <span class="holo">in your pocket.</span>',
     'Toute votre collection, <span class="holo">dans votre poche.</span>'),
    ("Point your camera at a card and In the Binder knows which one it is. It files the card into its set's binder and shows what it's worth. Page by page, you watch every set fill up.",
     "Pointez votre caméra sur une carte et In the Binder sait laquelle c'est. Il la classe dans le classeur de sa série et indique sa valeur. Page après page, vous regardez chaque série se remplir."),
    ('<a class="btn primary" href="/beta/">Join the Android beta</a>',
     '<a class="btn primary" href="/fr/beta/">Rejoindre la bêta Android</a>'),
    ('<a class="btn" href="/app/">Open on the web <span class="soon">NEW</span></a>',
     '<a class="btn" href="/app/">Ouvrir sur le web <span class="soon">NOUVEAU</span></a>'),
    ('Android first, App Store to follow. On an iPhone or a computer? <a href="/app/" style="color:inherit;text-decoration:underline">Use the web version</a>, free, no install.',
     "D'abord Android, l'App Store suivra. Sur iPhone ou ordinateur ? <a href=\"/app/\" style=\"color:inherit;text-decoration:underline\">Utilisez la version web</a>, gratuite, sans installation."),
    ('alt="In the Binder home screen showing the collector\'s sets with progress"',
     'alt="Écran d\'accueil d\'In the Binder montrant les séries du collectionneur et leur progression"'),
    # screens
    ("<h2>See it in action</h2>", "<h2>En images</h2>"),
    ('<p class="sub">Real screens from the Android beta. Swipe for more.</p>',
     '<p class="sub">De vraies captures de la bêta Android. Faites défiler pour en voir plus.</p>'),
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
    ("<h3>Is it available on iPhone?</h3>\n    <p>Not yet. In the Binder is in beta on Android through Google Play. An iPhone version is planned.</p>",
     "<h3>Est-il disponible sur iPhone ?</h3>\n    <p>Pas encore. In the Binder est en bêta sur Android via Google Play. Une version iPhone est prévue.</p>"),
    ("<h3>Does it need an internet connection?</h3>\n    <p>No. Your collection is stored on your phone and the app works offline. Prices update when you are online.</p>",
     "<h3>Faut-il une connexion internet ?</h3>\n    <p>Non. Votre collection est stockée sur votre téléphone et l'application fonctionne hors ligne. Les prix se mettent à jour quand vous êtes connecté.</p>"),
    # beta cta band
    ("<h2>Be one of the first testers</h2>", "<h2>Soyez parmi les premiers testeurs</h2>"),
    ("In the Binder is in its final testing on Android. It's free, it takes a minute to join, and your feedback shapes the launch.",
     "In the Binder est en phase finale de test sur Android. C'est gratuit, il suffit d'une minute pour rejoindre, et vos retours façonnent le lancement."),
    ('<a class="btn primary" href="/beta/">Join the beta</a>',
     '<a class="btn primary" href="/fr/beta/">Rejoindre la bêta</a>'),
    # footer
    ('<span>© 2026 In the Binder · <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> · <a href="/privacy.html">Privacy</a></span>',
     '<span>© 2026 In the Binder · <a href="mailto:support@inthebinder.com">support@inthebinder.com</a> · <a href="/fr/privacy.html">Confidentialité</a></span>'),
    ("In the Binder is an independent app and is not affiliated with, endorsed or sponsored by Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami or any other card publisher. All card names, images and trademarks belong to their respective owners. In the Binder may earn a commission from purchases made through its links to marketplaces.",
     "In the Binder est une application indépendante, sans affiliation, approbation ou parrainage de Nintendo, Creatures Inc., GAME FREAK inc., The Pokémon Company, Bandai, Disney, Ravensburger, Wizards of the Coast, Konami ou tout autre éditeur de cartes. Tous les noms de cartes, images et marques appartiennent à leurs propriétaires respectifs. In the Binder peut percevoir une commission sur les achats effectués via ses liens vers des places de marché."),
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
    ('<p class="lead">Thanks for testing. Pick one way to install. You only need one.</p>',
     '<p class="lead">Merci de tester l\'appli. Choisissez une méthode d\'installation. Une seule suffit.</p>'),
    ('<h2>Google Play <span class="tag">Recommended</span></h2>',
     '<h2>Google Play <span class="tag">Recommandé</span></h2>'),
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
    ("<h2>Direct download (APK)</h2>", "<h2>Téléchargement direct (APK)</h2>"),
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

SWITCH = ('<a href="%s" style="color:var(--dim);text-decoration:none;margin-left:18px;'
          'font-size:.95rem">%s</a>')


def build_home():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    fr = apply_pairs(html, HOME, "home")
    fr = fr.replace('<a href="#screens">Aperçu</a>',
                    '<a href="/" style="color:var(--dim);text-decoration:none;margin-left:18px;font-size:.95rem">EN</a><a href="#screens">Aperçu</a>', 1)
    (ROOT / "fr" / "index.html").write_text(fr, encoding="utf-8")

    en = add_hreflang(html, "/", "/fr/")
    if ">EN</a>" not in en and ">FR</a>" not in en:
        en = en.replace('<a href="/beta/">Join the beta</a>',
                        '<a href="/beta/">Join the beta</a>' + SWITCH % ("/fr/", "FR"), 1)
    (ROOT / "index.html").write_text(en, encoding="utf-8")


def build_privacy():
    html = (ROOT / "privacy.html").read_text(encoding="utf-8")
    # Privacy copy is translated separately (see build-fr-privacy appended below).
    fr = translate_privacy(html)
    (ROOT / "fr" / "privacy.html").write_text(fr, encoding="utf-8")
    en = add_hreflang(html, "/privacy.html", "/fr/privacy.html")
    (ROOT / "privacy.html").write_text(en, encoding="utf-8")


def build_beta():
    html = (ROOT / "beta" / "index.html").read_text(encoding="utf-8")
    fr = apply_pairs(html, BETA, "beta")
    (ROOT / "fr" / "beta" / "index.html").write_text(fr, encoding="utf-8")


def build_sitemap():
    today = "2026-10-16"
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
