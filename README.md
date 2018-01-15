# The Story of Jigsolve
## Web Research: Proof of Concept

### Ergens in november/december
Dit idee is geboren toen ik met mijn vriendin een puzzel aan het maken was. Het vlotte niet zo goed en na even paste geen enkel stukje meer. Toen kwam het in me op: zou er een app bestaan die me kan helpen met deze puzzel? Na eens snel te kijken op de Play Store vond ik niet direct iets dat er legitiem uitzag, dus dacht ik dat het misschien zelf kon maken.

![](puzzles/preview.JPG)
> De puzzel van die bewuste avond
>
> Status: Niet af, ligt op de kast

Mijn idee was dus geboren:
> Kan ik een app/programmaatje maken dat mij kan helpen puzzels op te lossen?

Een beetje later die week begon ik op te zoeken over puzzels en het oplossen ervan door computers. Ik ontdekte dat er veel verschillende manier waren om dit probleem aan te pakken. Ze waren dan ook allemaal (meerdere keren) getest door mijn (wat slimmere) collega's, medepuzzelaars.

![](Verslag/puzzle_solving_attempts.JPG)

> Boom die de verdeling in het domein toont.
>
> Bron: _F. Andalo et al. [PSQP – Puzzle Solving by Quadratic Programming] p.3_

Een hele tijd gaat voorbij en ik vergeet er aan te werken. De feestdagen en kerstvakantie vliegen voorbij en plots is het 9 januari: tijd voor onderzoek!

Het idee was dus om te proberen iets te maken dat het dagelijkse leven van een puzzelaar makkelijker kan maken. Dus ging ik kijken naar oplossingen voor pictoriële stukken. Dit zijn stukken met een afbeelding/grafiek er op. Voor gewoon gevormde puzzelstukken staat op bovenstaande afbeelding maar 1 paper gegeven. Er staat ook bij wat voor algoritme ze gebruiken om de puzzel op te lossen: greedy.

### Greedy algoritmen
Ik begon de paper te lezen en probeerde het te snappen, maar het lukte niet. Toen besefte ik dat ik niet eens wist wat een greedy algoritme was. Een paar uur later had ik gelezen over wat voor algoritmen het juist zijn, graph coloring en MST's (minimum spanning trees).

Met die informatie las ik de paper nog een keer en het ging al vlotter, maar ik kon het niet volledig vatten: er werd wiskunde in gebruikt die ik ofwel niet kende ofwel te ver weg zat dat het te veel moeite zou zijn om het terug op te frissen.

Zo keek ik verder op het lijstje en zag ik _genetic-based greedy_ staan. Dit bleek een combinatie van een greedy algoritme en een genetisch algoritme. Weer iets dat ik nog nooit gezien had!

### Genetische algoritmen
Door geleerd te hebben van mijn fouten, begon ik eerst met research naar deze soort van algoritmen. Kort gezegd zijn het algoritme die beginnen met een willekeurige start-set, waarop ze verschillende functies op toe gaan passen (fitness, crossover, mutatie,...) om een nieuwe, hopelijk betere generatie te genereren. Het is dus gebaseerd op de biologische genetica van alle leven op Aarde. Door telkens de beste oplossingen uit die generatie te bevoordelen en te gebruiken voor 'voortplanting' creeert men telkens betere en betere oplossingen die meer en meer de oplossing van de puzzel zullen benaderen.

![](Verslag/genetic_algorithms.JPG)

> Voorbeeld van hoe een genetisch algoritme een puzzel oplost generatie op generatie
>
> Bron: _Sholomon et al. [A Genetic Algorithm-Based Solver for Very Large Jigsaw Puzzles] p.7_

Net zoals bij de vorige paper was dit te ver boven mijn pet en had ik de tijd niet om dit te gaan bestuderen en uit te dokteren. Op zoek naar een iets makkelijkere oplossing dus!

### Hopelijk makkelijkere oplossingen
Ik ging eens kijken op github om te zien of er mensen waren die dit eerder geprobeerd hebben. Ik vond deze [repo](https://github.com/guansanghai/CVX-Jigsaw) en daar stonden twee oplossingsmogelijkheden. Met lineair programmeren of met quadratisch programmeren. Na dit weer allebei kort op te zoeken en over te leren, begreep ik de basisprincipes wel, maar de paper die ik vond van quadratisch puzzels oplossen _(F. Andalo et al. [PSQP])_ was weer te wiskundig en liet deze oplossingen dus weer links liggen.

Een trend in het puzzel-oplossen is dat er steeds grotere puzzels worden opgelost door de verbeteringen die ze maken in hun algoritmen. Nu worden er puzzels van 22 000+ stukken opgelost, terwijl het eerste algoritme een puzzel van 9 stukken kon oplossen (1964).
Dat deed me denken dat ik misschien helemaal naar het begin kon gaan, naar de allereerste algoritmen, omdat deze veel minder stukken aanpakten en dan toch zeker makkelijker zouden zijn? Het vroegste algoritme waaraan ik kon geraken was 1 uit 1989 en dat was voor 24 stuks.
Spijtig genoeg was het hier weer mis. Weer werd er gebruik gemaakt van hoge wiskunde en snapte ik er niets van.

### Back to the Roots
Al deze tegenslagen lieten me nog eens nadenken over het probleem en wat ik ging doen voor de oplossing. _'Falen is hip'_, maar ik kon toch niet met alleen een paar papers binnenwandelen op de dag van het examen?

Na even na te denken en met puzzels te spelen, kwam ik op het idee dat ik helemaal geen puzzel uit het niets moet oplossen. Ik was het punt van mijn onderzoeksvraag vergeten: *Kan ik een app/programmaatje maken dat mij kan **helpen** puzzels op te lossen?*

Als mens maak je ook geen puzzel met alleen de stukjes, je maakt ook gebruik van de afbeelding op de doos, de referentie afbeelding.
Daar draait heel de komende oplossing rond. Het matchen en lokaliseren van puzzelstukjes op de referentie afbeelding.

### OpenCV

Voor een ander project was ik al eens in contact gekomen met OpenCV en ik wist dat het een heel goeie library is om beeldverwerking te doen. De naam zeg het zelf: Open Computer Vision. Plus, het kon in Python en dat moest ik nog opfrissen voor mijn stage.

![](Verslag/opencv.jpg)

Al snel vond ik de functie cv::matchTemplate() en ik was er van overtuigd dat ik hiermee verder kon. Deze functie neemt een patroon (vb. deel van afbeelding) en begint deze vervolgens vanaf linksboven over de bron afbeelding te schuiven. Op het einde van de rit checkt de functie waar de grootste overeenkomst was en geeft die terug als locatie van de match.
Al snel had ik hiervoor een klein scriptje geschreven en kon ik afbeeldingen in afbeeldingen terugvinden. (searchPiece.py)

### Intermezzo: Faaldroid
Als intermezzo, waarschijnlijk onder invloed van slaaptekort, besloot ik dat het tof zou zijn om mijn app ook echt in een app te gieten voor Android. Zoals de titel van dit stuk laat uitwijzen, lukte dit niet echt.

Om pythons scripts te builden tot Android-apps waarbij je ook gebruik kan maken van het toestel en het besturingssysteem, gebruikte ik Kivy:
> Open source Python framework for rapid development of applications that make use of innovative user interfaces, such as multi-touch apps.

_Rapid development_ was toch niet waar bij mij en ik besloot (jammer genoeg iets te laat) na eindelijk 'Hello World!' op mijn gsm te krijgen dat deze route het niet waard zou zijn. Zeker omdat ik nog niet alles had.

### Puzzelstukken extracten
Een volgend deel van mijn uitwerking was het extracten van puzzelstukken uit een foto. De gebruiker trekt een foto van 1 of meerdere puzzelstukken op een vlakke achtergrond en deze worden dan gezocht in de voorafgegeven referentie afbeelding.

![](puzzles/lot.jpg)

Door gebruik te maken van OpenCV's functie cv::findContours() zou ik alle objecten die op de ingevoerde afbeelding staan, kunnen markeren met een omlijning. Door dan te kijken naar de langste contouren die de functie teruggeeft, zou ik de contouren van de puzzelstukken er uit kunnen filteren.

![](Verslag/contours.jpg)
> Links: de originele afbeelding met de gefilterde contouren van de puzzelstukken
> Rechts/midden: Alle contouren die herkent zijn door cv::findContours()

Met de gefilterde contouren zou ik dan voor elk puzzelstuk op de afbeelding een mask kunnen maken om het puzzelstuk achteraf uit de afbeelding te halen en over te blijven met het puzzelstuk met zwarte achtergrond.

Het vinden van de contouren en het filteren lukte vrij snel. Dan dacht ik dat het maskeren ook vrij makkelijk ging gaan, maar niets was minder waar. Door een gebrek aan goede documentatie voor OpenCV voor Python omtrent maskering heb ik een lange tijd met de handen in het haar gezeten omdat alles wat ik probeerde niet vond. Mogelijke oplossingen in C++ die ik dan vertaalde naar Python werkten niet omdat de versie voor Python niet identiek is aan die van C++.

Laat in de nacht lukte het me dan toch en het bleek een vrij makkelijke oplossing te zijn...

Dit stukje code was de boosdoener:
```python
roi = img[y:y2, x:x2]
```

Ik had een paar uur vroeger dit al geprobeerd:
```python
roi = img[x:x2, y:y2]
```
Maar blijkbaar werkt OpenCV met een omgekeerd coördinatenstelsel...

Uiteindelijk kon ik de puzzelstukken dus wel uit hun afbeelding halen. Uit bovenstaande afbeelding haalde ik volgende puzzelstukken:

![](Verslag/puzzlepiece3.jpg)
![](Verslag/puzzlepiece13.jpg)
![](Verslag/puzzlepiece14.jpg)
![](Verslag/puzzlepiece15.jpg)

### Alles samenvoegen
Nu dat ik afbeeldingen kan zoeken in een andere afbeelding en ik puzzelstukken uit andere afbeeldingen kan halen, is het tijd om deze twee functionaliteiten met elkaar te laten samenwerken.

Ik dacht door alle puzzelstukken die ik verzamel uit de extractie in de zoek functie te gooien dat het opgelost zou zijn, maar helaas. Heel soms was het raak, maar hoe algemener het puzzelstuk hoe meer kans op een willekeurige, foute plek het programma aangaf op de referentie afbeelding.

![](Verslag/21matches_skewed.JPG)

>Het resultaat van het zoeken van 21 bovenstaande puzzelstukken in de Afrikaanse puzzel
>
> Conclusie: niet zo goed

Afgezien van de foute matching, is het ook niet zo duidelijk met zoveel puzzelstukken.

Toen dacht ik weer even na en schoot me te binnen dat er geen rekening wordt gehouden met de grootte van de puzzelstukken ten opzichte van de referentie afbeelding. In het echt zouden de puzzelstukken een veel grotere afbeelding vormen en via de camera is het onmogelijk te zien of ze juiste schaal t.o.v. elkaar hebben. Ook zie je dat de referentie afbeelding nog scheef getrokken staat door het perspectief waarmee de foto getrokken is.

### Matchfunctie mk.2: SIFT
Door wat te bladeren op de documentatiepagina's van OpenCV kwam ik het SIFT algoritme tegen. SIFT is een algoritme om objecten te detecteren/matchen en zoals de naam (Scale-invariant feature transform) het al zegt, hoeft er hierbij geen rekening te houden worden met schaal en eventuele rotatie.

Het algoritme gaat over het te zoeken puzzelstuk en probeert hieruit een aantal merkwaardige punten te halen. Dit doet het ook met de referentie afbeelding en vervolgens wordt er gekeken of de punten van het puzzelstuk overeenkomen met (een deel van) de punten van de referentie afbeelding.

![](Verslag/SIFT.jpg)

> Hoe SIFT zou moeten werken

Door iets te weinig tijd en verstaanbaarheid nam ik de uitwerking die op de [documentatiepagina](https://docs.opencv.org/3.4.0/d1/de0/tutorial_py_feature_homography.html) stond en paste het aan aan mijn situatie. Voor gewone afbeeldingen (geen puzzelstukken) werkte het perfect. Het kon bijvoorbeeld heel makkelijk de aap in de linker onderhoek terugvinden.
Wanneer ik het met puzzelstukken probeerde was het ook mogelijk, maar in veel gevallen waren er geen gematchte punten tussen de twee afbeeldingen.

Ik kon nog 1 ding proberen dat het misschien zou oplossen, of toch op z'n minst zou verbeteren: het rechttrekken van de referentie afbeelding.

### Rechttrekken referentie
Dit was op zich niet zo'n moeilijke opgave, maar wegens tijdsdruk hebben een aantal blogposts op het web me toch moeten helpen.

Eerst ga je met een canny edge filter over de afbeeldingen om alle randen in de afbeelding te zoeken.

![](Verslag/close_up_canny.jpg)
> Close-up van het resultaat van de canny edge filter

Vervolgens neem je de randen van de canny edge filter en zoek je hierop de contouren met de eerder gebruikte cv::findContours() functie.
Vervolgens filteren we weer de allergrootsten er uit. Maar hoe zouden we nu de grote rechthoek er uit kunnen halen?

Een rechthoek bestaat altijd uit 4 hoeken, dus gaat de contour die deze rechthoek beschrijft ook slecht 4 punten hebben. Als we daarop nog eens filteren hebben we de uiteindelijke contour voor de afbeelding:

![](Verslag/contour_ex.JPG)

> De contour is te zien in het geel

Nu moeten we deze scheve rechthoek alleen nog maar rechttrekken naar de hoeken van de afbeelding en dan hebben de referentie afbeelding recht getrokken!

Hiervoor gebruikte ik de functies van onderstaande blogposts die specifiek over het maken van document scanner gaat.
- https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
- https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

Het resultaat hiervan is dit, een mooie vlakke referentie afbeelding:

![](Verslag/flatten.JPG)

Hoe mooi dit allemaal mag zijn uitgedraaid voor de referentie afbeelding, het vinden van puzzelstukken in de afbeelding werd niet beter.

### Conclusie
Ik ben tot op heden nog geen betere oplossing tegengekomen, maar mijn vermoeden is dat het ligt aan de lage resolutie van de foto's, de slechte belichting en de vorm van de puzzelstukken.
Wanneer het gedaan wordt met digitaal uitgesneden stukken afbeelding en de bron afbeelding is er een groter succes percentage dan wanneer er handgemaakte foto's worden gebruikt.

Ik vond het zeer tof om eens dieper in iets te gaan en me helemaal toe te wijden aan de wereld van het puzzelen.

Eén quote die me bijgebleven is uit het lezen van de papers is de deze van Goldberg uit _A global approach to automatic solution of jigsaw puzzles_:
> The real
interest in jigsaw puzzle solving is simply that it is a natural and challenging problem that
catches people’s imaginations.

De quote zegt perfect wat ik vond van het opzoeken en onderzoeken over dit probleem. Het is uiteindelijk niet gelukt, maar ik heb er veel uit geleerd en het was interessant!
