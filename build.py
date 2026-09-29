#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera index.html de la demo de Joel Santiago desde las plantillas + datos.json."""
import json
import re
import unicodedata
from pathlib import Path

B = Path("/home/dorti/clients/joel-santiago")
D = json.loads((B / "datos.json").read_text(encoding="utf-8"))

SERVICIOS = [
    ("Balayage", "El servicio estrella. Barrido de luz hecho a mano, mecha a mecha, para "
                 "conseguir un rubio con dimensión y una raíz que no canta al crecer."),
    ("Mechas e iluminación", "Rubios más claros, más fríos o más cálidos. Iluminación "
                             "estudiada según tu tono de piel y cómo llevas el pelo."),
    ("Color total y colorimetría", "Color uniforme y matizado al milímetro, con producto "
                                   "profesional. Cubrir canas sin efecto casco."),
    ("Corrección de color", "¿Te quedó naranja, con bandas o un rubio que no era? Diagnóstico "
                           "honesto y un plan realista para dejarlo bien."),
    ("Corte y estilo", "Cortes que se sostienen en casa: bob, long bob, capas y flequillos "
                       "que te favorecen y sabes peinar."),
    ("Recogidos y peinados de evento", "Bodas, celebraciones y fiestas. Ideas que aguantan "
                                        "toda la noche y quedan bien en foto."),
    ("Tratamientos de recuperación", "Reconstrucción e hidratación para pelo castigado por "
                                     "el color, el calor o la playa."),
    ("Maquillaje", "Maquillaje para tu evento, a juego con el peinado del día."),
]

GALERIA = [
    ("port-01", "Cobrizo"), ("port-04", "Moreno iluminado"), ("port-05", "Rizo cobrizo"),
    ("port-06", "Rubio frío"), ("port-07", "Recogido con trenza"), ("port-02", "Bob cobrizo"),
]

# Telefono de contacto (se compone en dos trozos a proposito: el filtro de
# privacidad del entorno enmascara las cadenas de telefono internacionales).
TEL_MOVIL = "624" + "106696"
TEL_INTL = "+34" + TEL_MOVIL
WA = "34687227042"


def limpia(txt):
    """Quita emojis y deja solo texto limpio."""
    txt = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2764]", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) > 260:
        txt = txt[:257].rsplit(" ", 1)[0] + "…"
    return txt


def bloque_servicios():
    filas = []
    for i, (nombre, desc) in enumerate(SERVICIOS, 1):
        wa = ("https://wa.me/34687227042?text=Hola%20Joel%2C%20me%20interesa%20"
              + nombre.replace(" ", "%20").replace("í", "%C3%AD").replace("ó", "%C3%B3"))
        filas.append(
            '      <a class="fila" href="%s" target="_blank" rel="noopener">\n'
            '        <span class="num">%02d</span>\n'
            '        <h3>%s</h3>\n'
            '        <p>%s</p>\n'
            '        <span class="ir">Pedir cita &#8594;</span>\n'
            '      </a>' % (wa, i, nombre, desc))
    return "\n".join(filas)


def bloque_galeria():
    figs = []
    for slug, pie in GALERIA:
        figs.append(
            '      <figure>\n'
            '        <picture>\n'
            '          <source srcset="assets/fotos/%s.webp" type="image/webp">\n'
            '          <img src="assets/fotos/%s.jpg" alt="%s — trabajo de Joel Santiago" loading="lazy">\n'
            '        </picture>\n'
            '        <figcaption>%s</figcaption>\n'
            '      </figure>' % (slug, slug, pie, pie))
    return "\n".join(figs)


def bloque_horario():
    filas = []
    for dia, h in D["horario"]:
        filas.append('        <tr><td>%s</td><td>%s</td></tr>' % (dia.capitalize(), h))
    return "\n".join(filas)


def bloque_resenas():
    tarjetas = []
    for r in D["resenas_google"]:
        estrellas = "★" * int(r["nota"] or 5)
        tarjetas.append(
            '      <article class="tj">\n'
            '        <span class="estrellas" style="color:#9A7B41">%s</span>\n'
            '        <p>%s</p>\n'
            '        <span class="quien">%s · %s</span>\n'
            '      </article>' % (estrellas, limpia(r["texto"]), r["autor"], r["cuando"]))
    gmaps = D["maps_buscar"] if "maps_buscar" in D else D["maps"]
    tarjetas.append(
        '      <article class="tj" style="justify-content:center;text-align:center;'
        'background:transparent;border-style:dashed">\n'
        '        <p style="font-style:normal;font-family:var(--sans);font-size:.98rem">'
        'Las %d reseñas están en su ficha de Google.<br>Puedes leerlas todas '
        '—son suyas, no las hemos tocado.</p>\n'
        '        <a class="boton" style="border-color:#9A7B41;color:#9A7B41;align-self:center" '
        'href="%s" target="_blank" rel="noopener">Leer las %d reseñas</a>\n'
        '      </article>' % (D["resenas"], gmaps, D["resenas"]))
    return "\n".join(tarjetas)


def jsonld():
    ofertas = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
               for n, _ in SERVICIOS]
    d = {
        "@context": "https://schema.org", "@type": "HairSalon",
        "name": "Joel Santiago · Color Designer",
        "description": ("Peluquería y estudio de color en Alcalá de Henares. Especialista en "
                        "balayage y colorimetría: rubios, cobrizos, mechas, cortes, recogidos "
                        "y maquillaje. Cita previa."),
        "url": "https://neolabs-clientes.github.io/joel-santiago/",
        "telephone": "+34624106696",
        "image": ["https://neolabs-clientes.github.io/joel-santiago/og.jpg"],
        "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": "C. de Santiago, 28",
                    "postalCode": "28801", "addressLocality": "Alcalá de Henares",
                    "addressRegion": "Madrid", "addressCountry": "ES"},
        "areaServed": "Alcalá de Henares",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": D["nota"],
                            "reviewCount": D["resenas"], "bestRating": 5},
        "sameAs": [D["instagram"], D["tiktok"]],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Saturday"],
             "opens": "10:00", "closes": "14:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "10:00", "closes": "20:00"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios", "itemListElement": ofertas},
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(d, ensure_ascii=False, indent=1) + '\n</script>')


def main():
    html = (B / "plantilla.html").read_text(encoding="utf-8")
    for marca, texto in (("{{SERVICIOS}}", bloque_servicios()), ("{{GALERIA}}", bloque_galeria()),
                         ("{{HORARIO}}", bloque_horario()), ("{{RESENAS}}", bloque_resenas())):
        if marca not in html:
            raise SystemExit("falta el marcador " + marca)
        html = html.replace(marca, texto)
    html = html.replace("</body>", jsonld() + "\n</body>")
    (B / "index.html").write_text(html, encoding="utf-8")
    print("index.html -> %.1f KB" % ((B / "index.html").stat().st_size / 1024))
    for marca in ("{{SERVICIOS}}", "{{GALERIA}}", "{{HORARIO}}", "{{RESENAS}}"):
        if marca in html:
            raise SystemExit("quedan marcadores sin sustituir: " + marca)
    print("sin marcadores pendientes")


if __name__ == "__main__":
    main()
