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
        └── tp.py
```

# Quick start
`python scripts/py/gosc.py "kościół wirus"`

# Known issues
- gosc.pl: nie zbieramy "Relacji na żywo", ale zachowujemy linki
- niedziela.pl: nie zbieramy "dat dodania", które są niekonsektwentnie umieszczane; zbieramy za to info o numerze wydania (z rokiem i miesiącem) dla artykułów z e-wydania niedzieli
- tygodnikpowszechny.pl: wymagane logowanie, rozwiązanie CAPTCHA, zapisanie cookies z identyfikatorem sesji, wgranie cookies do webdrivera
