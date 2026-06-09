import ee


def get_scaled(image, bands):

    scaled_dict = {}
    for b in bands:
        scaled_dict[b] = image.select(b).divide(10000)
    return scaled_dict


def nvdi(image):
    return image.normalizedDifference(["B8", "B4"]).rename("index")


def gndvi(image):
    return image.normalizedDifference(["B8", "B3"]).rename("index")


def ndre(image):
    return image.normalizedDifference(["B8", "B5"]).rename("index")


def evi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    blue = image.select("B2").divide(10000)
    return image.expression(
        "2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))",
        {"NIR": nir, "RED": red, "BLUE": blue},
    ).rename("index")


def evi2(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    return image.expression(
        "2.5 * ((NIR - RED) / (NIR + RED + 1))",
        {"NIR": nir, "RED": red},
    ).rename("index")


def savi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    L = 0.5
    return image.expression(
        "(1 + L) * ((NIR - RED) / (NIR + RED + L))",
        {"NIR": nir, "RED": red, "L": L},
    ).rename("index")


def msavi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    return image.expression(
        "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
        {"NIR": nir, "RED": red},
    ).rename("index")


def sfdvi(image):
    return image.expression(
        "((NIR + GREEN)/2 - (RED + REDEDGE)/2)",
        {
            "NIR": image.select("B8").divide(10000),  # Near-Infrared
            "GREEN": image.select("B3").divide(10000),  # Green
            "RED": image.select("B4").divide(10000),  # Red
            "REDEDGE": image.select("B5").divide(10000),  # Red Edge
        },
    ).rename("index")


def cigreen(image):
    nir = image.select("B8")
    green = image.select("B3")
    return image.expression("(NIR / GREEN) - 1", {"NIR": nir, "GREEN": green}).rename(
        "index"
    )


def arvi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    blue = image.select("B2").divide(10000)
    return image.expression(
        "(NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))",
        {"NIR": nir, "RED": red, "BLUE": blue},
    ).rename("index")


def ndmi(image):
    return image.normalizedDifference(["B8", "B11"]).rename("index")


def nbr(image):
    return image.normalizedDifference(["B8", "B12"]).rename("index")


def sipi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    blue = image.select("B2").divide(10000)
    return image.expression(
        "(NIR - BLUE) / (NIR - RED)",
        {"NIR": nir, "RED": red, "BLUE": blue},
    ).rename("index")


def ndwi(image):
    return image.normalizedDifference(["B3", "B8"]).rename("index")


def reci(image):
    nir = image.select("B8")
    rededge = image.select("B5")
    return image.expression(
        "(NIR / REDEDGE) - 1",
        {"NIR": nir, "REDEDGE": rededge},
    ).rename("index")


def mtci(image):
    nir = image.select("B8")
    rededge = image.select("B5")
    red = image.select("B4")
    return image.expression(
        "(NIR - REDEDGE) / (REDEDGE - RED)",
        {"NIR": nir, "REDEDGE": rededge, "RED": red},
    ).rename("index")


def mcari(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    green = image.select("B3").divide(10000)
    return image.expression(
        "((REDEDGE - RED) - 0.2 * (REDEDGE - GREEN)) * (REDEDGE / RED)",
        {"REDEDGE": nir, "RED": red, "GREEN": green},
    ).rename("index")


def vari(image):
    red = image.select("B4").divide(10000)
    green = image.select("B3").divide(10000)
    blue = image.select("B2").divide(10000)
    return image.expression(
        "(GREEN - RED) / (GREEN + RED - BLUE)",
        {"GREEN": green, "RED": red, "BLUE": blue},
    ).rename("index")


def tvi(image):
    nir = image.select("B8").divide(10000)
    red = image.select("B4").divide(10000)
    green = image.select("B3").divide(10000)
    return image.expression(
        "0.5 * (120 * (NIR - GREEN) - 200 * (RED - GREEN))",
        {"NIR": nir, "RED": red, "GREEN": green},
    ).rename("index")


def calc_custom(image, expression):
    if not expression:
        raise ValueError("Expressão customizada vazia.")

    all_bands = [
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B8A",
        "B9",
        "B11",
        "B12",
    ]
    b = get_scaled(image, all_bands)

    return image.expression(expression, b).rename("index")


INDEX_REGISTRY = {
    "NDVI": nvdi,
    "EVI": evi,
    "EVI2": evi2,
    "SAVI": savi,
    "GNDVI": gndvi,
    "MSAVI": msavi,
    "SFDVI": sfdvi,
    "CIgreen": cigreen,
    "NDRE": ndre,
    "ARVI": arvi,
    "NDMI": ndmi,
    "NBR": nbr,
    "SIPI": sipi,
    "NDWI": ndwi,
    "ReCI": reci,
    "MTCI": mtci,
    "MCARI": mcari,
    "VARI": vari,
    "TVI": tvi,
}
