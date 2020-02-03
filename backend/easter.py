ROSA = ['maria',
        'rosamari',
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

AGRAT = ['agrat',
         ]

def message_answer(text):
    text = text.replace("'", " ").split(" ")
    if any(x in text for x in ROSA):
        pass
    elif any(x in text for x in ANIMAL):
        return ['text',
                "Has estàs bloquejat del bot.\n" \
                "Demana perdó si vols tornar a parlar amb mi."]
    # Política
    elif any(x in text for x in VOX):
        return ['photo',
                './backend/files/abascal.jpg',
                'Santiago Abascal quiere limpiar España de Pokémons']
    elif any(x in text for x in CS):
        return ['text',
                'https://play.google.com/store/apps/details?id=es.decesia&hl=en']
    elif any(x in text for x in ERC):
        return ["text",
                "Si encara no teniu programa electoral, " \
                "podeu utilitzar el de Carnaval d’aquest any. De res guapis."]
    elif any(x in text for x in PDCAT):
        return ["text",
                'Ja has provat la crema Ruscus Llorens? '
                'És la millor per les "almorranes"!']
    elif any(x in text for x in HUMOR):
        return ["photo",
                './backend/files/postu.jpg', '']
    elif any(x in text for x in AGRAT):
        return ['text',
                "Encara no ets soci de l’Agrat? Doncs aprofita ara," \
                "que d’aquí dos anys potser..."]
    else:
        return ['text',
                "No tinc respotes a aquesta pregunta...\n"
                "Prova d'utilitzar altres paraules clau.\n"]
