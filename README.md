# Repo
```
├── README.md
├── data
│   ├── arts
│   │   ├── ... [csv, xlsx]
│   └── links 
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
