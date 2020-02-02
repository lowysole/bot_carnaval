ROSA = ['rosa maria',
        'rosa mari',
        'perelló',
        'perello',
        'rosamaria',
        'rosa'
        ]

PDCAT = ['pdcat',
         'pedecat',
         'junts',
         'juntsxtarrega',
         'juntsxtàrrega',
         'convergencia',
         'convergència']

ANIMAL = ['animal farm',
          'animal',
          'farm'
          ]

FOTOGRAF = ['']

CS = ['ciutadans',
      'ciutadants',
      'ciudadanos',
      'cs',
      "c’s"
      ]

VOX = ['fatxa',
       'fatcha',
       'facha',
       'vox']

ERC = ['esquerra',
       'erc',
       'republicana']

HUMOR = ['humor',
         'monolegs',
         'monòlegs'
         ]


def message_answer(text):
    text = text.split(" ")
    #if text in ROSA:
    #    continue
    #elif text in ANIMAL:
    #    continue
    #    return ['text',
    #            "Has estàs bloquejat del bot.\n" \
    #            "Demana perdó si vols tornar a parlar amb mi."]
    ## Política
    #elif text in VOX:
    #    continue
    #    return ['photo',
    #            './backend/files/abascal.jpg',
    #            'Santiago Abascal quiere limpiar España de Pokémons']
    #elif text in CS:
    #    continue
    #    return ['text',
    #            'https://play.google.com/store/apps/details?id=es.decesia&hl=en']
    #elif text in ERC:
    #    continue
    #    return ["text",
    #            "Si encara no teniu programa electoral, " \
    #            "podeu utilitzar el de Carnaval d’aquest any. De res guapis."]
    #elif text in PDCAT:
    #    continue
    #    return ["text",
    #            'Ja has provat la crema Ruscus Llorens? '
    #            'És la millor per les "almorranes"!']
    #elif any(x in text for x in HUMOR):
    #    continue
    #    return ["photo",
    #            './backend/files/postu.jpg', '']
    #elif text in AGRAT:
    #    continue
    #    return ['text',
    #            "Encara no ets soci de l’Agrat? Doncs aprofita ara," \
    #            "que d’aquí dos anys potser..."]

    return ['text',
            'Estic sent entrenada per poder respondre els teus dubtes.\n'
            'En breus tindràs resposta a totes les teves preguntes.']
