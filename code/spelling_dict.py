import re 

sd = [(r"[Ww]aare", lambda tok: tok.replace("aa", "a")),  # b:63, k:739
      (r"[Ww]erth", lambda tok: tok.replace("rth", "rt")),  # b:181, k:1418
      (r"[Ss]ocial(is(t(inn)?[ei]n|tisch\w*|mus\w*)|demokrat\w*)", lambda tok: tok.replace("oci", "ozi")),  # b:384, k:0
      (r"[Cc]ommun(is(t(inn)?[ei]n\w*|tisch\w*|mus\w*))", lambda tok: tok.replace("com", "kom").replace("Com", "Kom")),  # b:33, k:0
      (r"[Cc]apital(is(t(inn)?[ei]n\w*|tisch\w*|mus\w*))?", lambda tok: tok.replace("Cap", "Kap").replace("cap", "kap")),  # b:157, k:3
      (r"[Cc]lasse", lambda tok: tok.replace("cla", "kla").replace("Cla", "Kla")) #b:132, k:2
      ]
      
