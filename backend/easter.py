import re
from random import randint
from backend.database import query as q
from backend.settings import DB_FILE

ROSA = ['maria',
        'rosamari',
        'perelló',
        'perello',
        'rosamaria',
        'rosa',
        'festuc'
        ]

PDCAT = ['pdcat',
         'pedecat',
         'junts',
         'juntsxtarrega',
         'juntsxtàrrega',
         'convergencia',
         'convergència']

ANIMAL = ['animal',
          'farm'
          ]

FOTOGRAF = ['fotograf',
            'fotògraf',
            'raul',
            'raül',
            'palacios']

CS = ['ciutadans',
      'ciutadants',
      'ciudadanos',
      'cs',
      "c’s"
      ]

CUP = ['cup']

VOX = ['fatxa',
       'fatcha',
       'facha',
       'vox']

ERC = ['esquerra',
       'erc',
       'republicana']

HUMOR = ['humor',
         'monolegs',
         'monòlegs',
         'meme',
         'memefest'
         ]

AGRAT = ['agrat',
         ]

SILVERI = ['silveri',
           'caro',
           'psc']

LOWY = ['lowy',
        'llorenç']

GENT = ['jaume',
        'vilalta',
        'lluis',
        'lluís',
        'nadal',
        'ramon']

REINA = ['rei',
         'reina']

FOLGUERA = ['folgui',
            'folguera']

def message_answer(text):
    db = q.Query(DB_FILE)
    text = re.findall(r"[\w']+", text)
    if any(x in text for x in ANIMAL):
        db.get_or_create_msg('animal')
        return ['text',
                "Has estàs bloquejat del bot.\n" \
                "Demana perdó si vols tornar a parlar amb mi."]
    elif any(x in text for x in AGRAT):
        db.get_or_create_msg('agrat')
        return ['text',
                "Encara no ets soci de l’agrat? doncs aprofita ara," \
                "que d’aquí dos anys potser..."]
    elif any(x in text for x in ROSA):
        db.get_or_create_msg('rosa')
        return ['photo',
                './backend/files/rosa.jpeg', '']
    elif any(x in text for x in VOX):
        db.get_or_create_msg('vox')
        return ['text',
                'De debò? Ni aigua.']
    elif any(x in text for x in CS):
        db.get_or_create_msg('cs')
        return ['text',
                'https://play.google.com/store/apps/details?id=es.decesia&hl=en']
    elif any(x in text for x in ERC):
        db.get_or_create_msg('erc')
        return ["text",
                "Si encara no teniu programa electoral, " \
                "podeu utilitzar el de Carnaval d’aquest any. De res guapis."]
    elif any(x in text for x in PDCAT):
        db.get_or_create_msg('pdcat')
        return ["text",
                'Ja has provat la crema Ruscus Llorens? '
                'És la millor per les "almorranes"!']
    elif any(x in text for x in HUMOR):
        db.get_or_create_msg('humor')
        return ["photo",
                './backend/files/postu.jpg', '']
    elif any(x in text for x in SILVERI):
        db.get_or_create_msg('silveri')
        return ['text',
                'https://bit.ly/31Gs6px']
    elif any(x in text for x in CUP):
        db.get_or_create_msg('cup')
        return ['text',
                "Pobres, estant patint una època amb alguns 'batches'"]
    elif any(x in text for x in GENT):
        db.get_or_create_msg('gent')
        return ['text',
                'Si ets tu, et pensaves que et dedicaríem un lloc aquí? ' \
                'Si no ets tu, bon intent.']
    elif any(x in text for x in LOWY):
        db.get_or_create_msg('lowy')
        return ['text',
                'És el creador de tot això. @lowysole']
    elif any(x in text for x in REINA):
        db.get_or_create_msg('reina')
        return ['text',
                'No flipes ni res.']
    elif any(x in text for x in FOTOGRAF):
        db.get_or_create_msg('fotograf')
        return ['audio',
                './backend/files/fotograf.mp3']
    elif any(x in text for x in FOLGUERA):
        db.get_or_create_msg('folguera')
        return ['text',
                'Ja li hem donat massa protagonsime. Millor parar '
                'sinó es creix massa.']
    else:
        num = randint(1,20)
        if num == 1 and num == 2:
            return['text',
                   "No tinc respostes a aquesta pregunta però " \
                   "potser et poden interessar els horaris de " \
                   "la Tagiatella:\n" \
                   "Cada dia de 13 a 16 i de 20:30 a 00"]
        elif num == 3 and num == 4:
            return ['text',
                    'Enhorabona! Has sigut el missatge 1000! ' \
                    'Escriu reina si vols saber qui és.']
        elif num in (5,6,7,8,9):
            return ['text',
                    'Sigue intentando...']
        else:
            return ['text',
                    "No tinc respotes a aquesta pregunta...\n"
                    "Prova d'utilitzar altres paraules clau.\n"]
