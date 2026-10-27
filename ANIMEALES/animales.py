PREDICADOS = {
    "tiene_pelo": "x tiene pelo",
    "da_leche": "x da leche a sus crias",
    "tiene_plumas": "x tiene plumas",
    "vuela": "x vuela",
    "pone_huevos": "x pone huevos",
    "come_carne": "x come carne",
    "tiene_pezunas": "x tiene pezunas",
    "color_leonado": "x es de color leonado",
    "manchas_oscuras": "x tiene manchas oscuras",
    "rayas_negras": "x tiene rayas negras",
    "cuello_largo": "x tiene el cuello largo",
    "nada": "x nada",
    "blanco_y_negro": "x es blanco y negro",
    "vuela_muy_bien": "x vuela muy bien",
    "es_acuatico": "x vive en el agua",
    "aleta_dorsal": "x tiene aleta dorsal",
    "cola_horizontal": "x tiene la cola horizontal",
    "cola_vertical": "x tiene la cola vertical",
    "espiraculo": "x respira por un espiraculo",
    "branquias": "x tiene branquias",
    "sube_a_respirar": "x sube a la superficie a respirar",
    "es_herbivoro": "x es herbivoro",
    "tiene_cascos": "x tiene cascos",
    "es_hembra": "x es hembra",
    "tiene_ubres": "x tiene ubres",
    "leche_comercial": "x da leche de forma comercial",
}

# (premisas, conclusion)
REGLAS = (
    (("tiene_pelo",), "mamifero"),
    (("da_leche",), "mamifero"),
    (("tiene_plumas",), "ave"),
    (("vuela", "pone_huevos"), "ave"),
    (("mamifero", "come_carne"), "carnivoro"),
    (("mamifero", "tiene_pezunas"), "ungulado"),
    (("carnivoro", "color_leonado", "manchas_oscuras"), "guepardo"),
    (("carnivoro", "color_leonado", "rayas_negras"), "tigre"),
    (("ungulado", "cuello_largo", "manchas_oscuras"), "jirafa"),
    (("ungulado", "rayas_negras"), "cebra"),
    (("ave", "nada", "blanco_y_negro"), "pinguino"),
    (("ave", "vuela_muy_bien"), "albatros"),
    # entrevista 1: delfin y tiburon
    (("mamifero", "es_acuatico", "espiraculo", "cola_horizontal"), "delfin"),
    (("branquias", "cola_vertical"), "tiburon"),
    # entrevista 2: vaca
    (("mamifero", "es_herbivoro", "tiene_cascos"), "rumiante"),
    (("rumiante", "es_hembra", "tiene_ubres", "leche_comercial"), "vaca"),
)

# vinculos: (hijo, padre)
VINCULOS = (
    ("mamifero", "animal"),
    ("ave", "animal"),
    ("carnivoro", "mamifero"),
    ("ungulado", "mamifero"),
    ("guepardo", "carnivoro"),
    ("tigre", "carnivoro"),
    ("jirafa", "ungulado"),
    ("cebra", "ungulado"),
    ("pinguino", "ave"),
    ("albatros", "ave"),
    ("delfin", "mamifero"),
    ("rumiante", "mamifero"),
    ("vaca", "rumiante"),
    ("tiburon", "animal"),
)

CASOS = {
    "delfin": {
        "da_leche": True,
        "es_acuatico": True,
        "aleta_dorsal": True,
        "cola_horizontal": True,
        "espiraculo": True,
        "sube_a_respirar": True,
    },
    "tiburon": {
        "es_acuatico": True,
        "aleta_dorsal": True,
        "branquias": True,
        "cola_vertical": True,
    },
    "vaca": {
        "tiene_pelo": True,
        "da_leche": True,
        "es_herbivoro": True,
        "tiene_cascos": True,
        "tiene_pezunas": True,
        "es_hembra": True,
        "tiene_ubres": True,
        "leche_comercial": True,
    },
}


def inferir(hechos):
    conocidos = {k for k, v in hechos.items() if v}
    nuevo = True
    while nuevo:
        nuevo = False
        for premisas, conclusion in REGLAS:
            if conclusion not in conocidos and all(p in conocidos for p in premisas):
                conocidos.add(conclusion)
                nuevo = True
    return conocidos


def ancestros(categoria):
    cadena = []
    actual = categoria
    padres = dict(VINCULOS)
    while actual in padres:
        actual = padres[actual]
        cadena.append(actual)
    return cadena


if __name__ == "__main__":
    for nombre, hechos in CASOS.items():
        derivados = inferir(hechos) - {k for k, v in hechos.items() if v}
        print(nombre, "->", sorted(derivados))
        print("   cadena:", " > ".join([nombre] + ancestros(nombre)))
