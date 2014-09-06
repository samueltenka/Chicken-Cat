Chicken-Cat
===========

Translates voices in input audio:

                                      Sam's voice   Darth Vader's voice  
                                           |            |
                                           v            v
    (Sam saying "Mary had a little Lamb") ------------------> (Darth Vader saying "Mary had a little lamb")

How?

             CHUNKING           CLASSIFICATION                 TRANSLATION                      JOINING
    input audio --> list of phonemes --> list of labeled phonemes --> list of translated phonemes --> output audio
