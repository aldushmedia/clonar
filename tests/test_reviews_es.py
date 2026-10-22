import csv
import datetime
import os
import tempfile
import unittest

from _load import load
from test_reviews import ROWS as EN_ROWS

reviews = load("clonar-emprendedor", "reviews")

# (theme, where it is said, review text). "general" means any Spanish-speaking country.
SPANISH = [
    ("pricing", "general", "Está carísima para lo que ofrece."),
    ("pricing", "general", "ESTÁ CARÍSIMA y encima subió."),
    ("pricing", "AR", "Es un afano lo que cobran por mes."),
    ("pricing", "ES", "Ahora es de pago y antes no."),
    ("pricing", "general", "Cobran en dólares y no en pesos."),
    ("pricing", "general", "Muy cara la suscripción."),
    ("billing", "general", "Me cobraron dos veces este mes."),
    ("billing", "ES", "No pude darme de baja y me siguen cobrando."),
    ("billing", "AR", "Pedí el reintegro y nada."),
    ("billing", "ES", "Es un timo."),
    ("billing", "general", "Me descontaron de la tarjeta sin avisar."),
    ("bugs", "MX", "Se traba cada vez que abro el calendario."),
    ("bugs", "AR", "Se tilda todo el tiempo."),
    ("bugs", "ES", "Se cuelga al pagar."),
    ("bugs", "CO", "Se queda pegada en la pantalla de inicio."),
    ("bugs", "CL", "Se pega cuando subo una foto."),
    ("bugs", "general", "Se congela y se cierra sola."),
    ("bugs", "AR", "No anda desde ayer."),
    ("bugs", "general", "No sirve, la app no responde."),
    ("performance", "general", "Se demora mucho en cargar."),
    ("performance", "general", "Tarda una eternidad en abrir."),
    ("performance", "general", "Consume mucha batería."),
    ("performance", "general", "Lentísima."),
    ("data", "general", "Se borraron todas mis citas."),
    ("data", "general", "Perdí todos mis datos."),
    ("data", "general", "No sincroniza con el calendario."),
    ("ux", "MX", "Es muy enredada."),
    ("ux", "ES", "Es un lío encontrar el botón."),
    ("ux", "general", "Nada intuitiva."),
    ("ux", "general", "Demasiados pasos para reservar."),
    ("support", "general", "Nunca contesta nadie los correos."),
    ("support", "general", "El soporte no responde."),
    ("support", "general", "Solo te atiende un bot."),
    ("support", "general", "Pésima atención al cliente."),
    ("account", "general", "No me deja iniciar sesión."),
    ("account", "AR", "Olvidé mi clave y no llega el correo."),
    ("account", "general", "No puedo recuperar mi contraseña."),
    ("account", "general", "No puedo entrar a mi cuenta."),
    ("notifications", "general", "Demasiadas notificaciones."),
    ("notifications", "general", "Me llenan de correos."),
    ("notifications", "ES", "Demasiados mails."),
    ("ads", "general", "Está llena de anuncios."),
    ("ads", "general", "Mucha publicidad."),
    ("ads", "MX", "Demasiada propaganda."),
    ("updates", "general", "Desde la última actualización no funciona."),
    ("updates", "general", "Antes era mejor."),
    ("updates", "general", "Devuelvan la versión anterior."),
    ("privacy", "general", "Pide permisos de más."),
    ("privacy", "general", "Venden tus datos."),
    ("privacy", "general", "Nos están espiando."),
    ("integrations", "general", "No se integra con Google Calendar."),
    ("integrations", "general", "Ojalá pudiera exportar a Excel."),
    ("integrations", "general", "No manda recordatorios por WhatsApp."),
    ("integrations", "general", "No emite factura electrónica."),
    ("platforms", "MX", "No hay versión para computadora."),
    ("platforms", "ES", "Falta la app para ordenador."),
    ("platforms", "CO", "Necesito la versión para celular."),
    ("platforms", "ES", "No hay versión móvil."),
    ("platforms", "general", "No funciona sin conexión."),
    ("customisation", "general", "Ojalá tuviera modo oscuro."),
    ("customisation", "general", "No se puede personalizar el correo."),
    ("collaboration", "general", "No sirve para trabajar en equipo."),
    ("collaboration", "general", "No permite varios usuarios."),
    ("collaboration", "general", "Tengo varias sucursales y no me sirve."),
    ("payment_methods", "general", "No acepta Mercado Pago."),
    ("payment_methods", "MX", "No se puede pagar en efectivo en OXXO."),
    ("payment_methods", "CO", "Solo acepta tarjeta, no PSE."),
    ("payment_methods", "PE", "Deberían aceptar Yape y Plin."),
    ("payment_methods", "ES", "Que acepten Bizum."),
    ("payment_methods", "AR", "Medios de pago muy limitados."),
]

WITHOUT_ACCENTS = [
    ("account", "No me deja iniciar sesion."),
    ("account", "Olvide mi contrasena."),
    ("updates", "Desde la ultima actualizacion no abre."),
    ("performance", "Lentisima."),
    ("pricing", "Muy cara la suscripcion."),
]

SPANISH_REQUESTS = [
    ("general", "Ojalá tuviera recordatorios por WhatsApp."),
    ("MX", "Estaría padre poder elegir barbero."),
    ("CO", "Sería chévere un modo oscuro."),
    ("CL", "Sería bacán poder pagar en cuotas."),
    ("ES", "Sería guay poder exportar."),
    ("AR", "Estaría copado que tenga lista de espera."),
    ("general", "Le falta una opción para repetir la cita."),
    ("general", "Deberían agregar pagos con Yape."),
    ("general", "No se puede cambiar la hora de la cita."),
    ("general", "No hay forma de ver el historial."),
]

HAPPY = [
    "Me encanta, la uso todos los días y funciona perfecto.",
    "Excelente app, muy fácil de usar.",
    "La recomiendo, el equipo de la barbería es muy amable.",
    "Súper práctica, reservé en dos minutos.",
    "Muy buena, la uso en mi celular todos los días.",
    "Todo bien, llegó rápido mi pedido.",
    "Funciona de maravilla.",
]

# What each English row in test_reviews matched before the Spanish patterns were added.
EN_BASELINE = {
    "https://apps.apple.com/r/1": {"pricing", "notifications"},
    "https://play.google.com/r/2": {"pricing", "support"},
    "https://www.g2.com/r/3": {"pricing"},
    "https://www.reddit.com/r/x/comments/4": {"pricing", "collaboration"},
    "https://apps.apple.com/r/5": set(),
    "https://www.capterra.com/r/6": {"bugs"},
    "https://apps.apple.com/r/7": set(),
    "https://play.google.com/r/9": {"pricing", "support"},
}

EN_PHRASES = [
    ("pricing", "Way too expensive."),
    ("billing", "They charged me twice and refused a refund."),
    ("bugs", "It crashes all the time."),
    ("performance", "So slow and laggy."),
    ("data", "Sync failed and I lost all my notes."),
    ("ux", "Very confusing and clunky."),
    ("support", "Customer support never replied."),
    ("account", "I got locked out of my account."),
    ("notifications", "Way too many notifications."),
    ("ads", "Full of ads."),
    ("updates", "Since the update it is broken."),
    ("privacy", "Creepy tracking everywhere."),
    ("integrations", "Needs a Zapier integration."),
    ("platforms", "No offline mode."),
    ("customisation", "Please add dark mode."),
    ("collaboration", "Not built for teams."),
    ("payment_methods", "I wish they had more payment options."),
]

ROWS_ES = [
    ("app-store", "https://apps.apple.com/mx/r/1", "2026-08-01", "1",
     "Carísima para lo que ofrece. Ojalá tuviera recordatorios por WhatsApp."),
    ("google-play", "https://play.google.com/co/r/2", "2026-07-15", "2",
     "Subieron el precio dos veces este año y el soporte nunca contesta."),
    ("reddit", "https://www.reddit.com/r/argentina/comments/3", "2026-06-01", "",
     "Es un afano lo que cobran por cada barbero."),
    ("trustpilot", "https://es.trustpilot.com/r/4", "2026-05-20", "1",
     "Me cobraron dos veces y no me dejan cancelar la suscripción."),
    ("app-store", "https://apps.apple.com/es/r/5", "2026-08-10", "5",
     "Me encanta, la uso todos los días."),
    ("google-play", "https://play.google.com/cl/r/6", "2026-07-01", "1",
     "Se queda pegada cada vez que abro la agenda."),
    ("app-store", "https://apps.apple.com/pe/r/7", "2026-08-02", "2",
     "Deberían aceptar Yape, solo acepta tarjeta."),
    ("google-play", "https://play.google.com/ar/r/8", "2026-07-20", "1",
     "Se tilda todo el tiempo desde la última actualización."),
    ("app-store", "https://apps.apple.com/mx/r/9", "2026-08-05", "1",
     "El cliente llegó y la cita no aparecía."),
]


class Patterns(unittest.TestCase):
    def setUp(self):
        self.themes, self.requests = reviews.load_themes()

    def matched(self, text):
        return {t["id"] for t in self.themes if any(p.search(text) for p in t["patterns"])}

    def is_request(self, text):
        return any(p.search(text) for p in self.requests)

    def test_every_theme_has_spanish_examples(self):
        self.assertEqual({theme for theme, _, _ in SPANISH}, {t["id"] for t in self.themes})

    def test_spanish_complaints_land_in_their_theme(self):
        for theme, where, text in SPANISH:
            with self.subTest(text=text, where=where):
                self.assertIn(theme, self.matched(text))

    def test_regional_variants_come_from_several_countries(self):
        freezes = {where for theme, where, _ in SPANISH if theme == "bugs" and where != "general"}
        self.assertGreaterEqual(len(freezes), 4, freezes)
        countries = {where for _, where, _ in SPANISH + [(None,) + r for r in SPANISH_REQUESTS]
                     if where != "general"}
        self.assertGreaterEqual(len(countries), 6, countries)

    def test_accents_are_optional(self):
        for theme, text in WITHOUT_ACCENTS:
            with self.subTest(text=text):
                self.assertIn(theme, self.matched(text))

    def test_spanish_requests_are_found(self):
        for where, text in SPANISH_REQUESTS:
            with self.subTest(text=text, where=where):
                self.assertTrue(self.is_request(text))

    def test_happy_spanish_reviews_match_nothing(self):
        for text in HAPPY:
            with self.subTest(text=text):
                self.assertEqual(self.matched(text), set())
                self.assertFalse(self.is_request(text))

    def test_english_rows_keep_their_themes(self):
        for row in EN_ROWS:
            if row[1] in EN_BASELINE:
                with self.subTest(url=row[1]):
                    self.assertEqual(self.matched(row[4]), EN_BASELINE[row[1]])

    def test_english_phrases_still_match(self):
        for theme, text in EN_PHRASES:
            with self.subTest(text=text):
                self.assertIn(theme, self.matched(text))


class SpanishReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "reviews.csv")
        with open(self.path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(("source", "url", "date", "rating", "text"))
            w.writerows(ROWS_ES)
        themes, req = reviews.load_themes()
        self.kept, self.dropped, self.dupes = reviews.load_reviews(self.path)
        self.result = reviews.analyse(self.kept, themes, req, today=datetime.date(2026, 10, 1))

    def tearDown(self):
        self.tmp.cleanup()

    def theme(self, theme_id):
        return next(t for t in self.result["themes"] if t["id"] == theme_id)

    def test_price_is_the_top_complaint_across_countries(self):
        top = [t for t in self.result["themes"] if t["kind"] == "complaint"][0]
        self.assertEqual(top["id"], "pricing")
        self.assertEqual(top["count"], 4)
        self.assertFalse(top["thin"])

    def test_two_freezes_from_two_countries_are_still_thin(self):
        bugs = self.theme("bugs")
        self.assertEqual(bugs["count"], 2)
        self.assertTrue(bugs["thin"])

    def test_payment_methods_are_a_request(self):
        pay = self.theme("payment_methods")
        self.assertEqual(pay["kind"], "request")
        self.assertEqual([q["url"] for q in pay["quotes"]], ["https://apps.apple.com/pe/r/7"])

    def test_every_quote_is_verbatim_and_linked(self):
        by_url = {r["url"]: r["text"] for r in self.kept}
        quotes = [q for t in self.result["themes"] for q in t["quotes"]]
        quotes += self.result["requests"]
        self.assertTrue(quotes)
        for q in quotes:
            self.assertIn(q["url"], by_url)
            self.assertIn(q["quote"].strip(".").strip(), by_url[q["url"]])

    def test_requests_in_spanish_are_listed(self):
        texts = [q["quote"] for q in self.result["requests"]]
        self.assertTrue(any("Ojalá tuviera recordatorios por WhatsApp" in t for t in texts))
        self.assertTrue(any("Deberían aceptar Yape" in t for t in texts))

    def test_unthemed_low_rating_is_surfaced(self):
        urls = [r["url"] for r in self.result["unthemed_negative"]]
        self.assertEqual(urls, ["https://apps.apple.com/mx/r/9"])

    def test_render_uses_the_spanish_labels(self):
        text = reviews.render(self.result, self.dropped, self.dupes)
        self.assertIn("Precio y muros de pago", text)
        self.assertIn("https://es.trustpilot.com/r/4", text)
        self.assertNotIn(chr(0x2014), text)


if __name__ == "__main__":
    unittest.main()
