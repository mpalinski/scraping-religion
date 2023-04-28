# Repo
```
├── README.md
├── data
│   ├── arts [scraped articles]
│   │   ├── ... [csv, xlsx]
│   └── links [scraped links to articles]
│       └── ... [csv]
├── requirements.txt [required packages]
└── scripts [scraping articles using Selenium]
    ├── ipynb
    │   └── ... [testing scripts in Jupyter notebooks]
    └── py [working scripts]
        ├── gosc.py
        ├── niedziela.py
        ├── tp.py
        └── jw.py
```

# Quick start
`python scripts/py/gosc.py "kościół wirus"`

# Known issues
- gosc.pl: nie zbieramy "Relacji na żywo", ale zachowujemy linki
- niedziela.pl: nie zbieramy "dat dodania", które są niekonsektwentnie umieszczane; zbieramy za to info o numerze wydania (z rokiem i miesiącem) dla artykułów z e-wydania niedzieli
- tygodnikpowszechny.pl: 
    - wymagane logowanie, rozwiązanie CAPTCHA, zapisanie cookies z identyfikatorem sesji, wgranie cookies do webdrivera
    - pierwszy artykuł z wyszukiwania ma ucięty tekst (cookies issue)
    - API traktuje słowa wyszukiwania jako exact match, czyli wyszukiwanie "wirus" nie znajdzie "wirusa", "wirusem" etc. 
- jw.org/pl: dwa typy artykułów - w domenie i poddomenie (wol.jw.org), pierwsze mają ustrukturyzowaną datę (kolumna added), ale nie zawsze jest podana; drugie nie mają ustrukturyzowanego miejsca na datę, czasem pada ona w tekście lub tytule. Uwaga: zdarzają się tu teksty z lat 90. np. o wirusie AIDS.

