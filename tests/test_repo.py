import json
import os
import re
import unittest

from _load import ROOT

MASTER = "clonar"
SKILLS = ["clonar-explorar", "clonar-arquitecto", "clonar-diseno", "clonar-construir",
          "clonar-backend", "clonar-probar", "clonar-comparar", "clonar-emprendedor",
          "clonar-marca", "clonar-lanzar", "clonar-publicar", "clonar-redes"]
ALL = [MASTER] + SKILLS
ABOUT = ("Doce skills gratis para Claude que clonan cualquier app y la promocionan, más el "
         "comando /clonar que guía todo el proceso: ingeniería inversa, reconstrucción, bugs, "
         "lo que sus usuarios odian, lanzamiento y Reels. Gratis, MIT.")
ALDUSH = "Copyright (c) 2026 Aldush Media (traducción y adaptación al español)"
TEXT_FILES = (".md", ".py", ".json", ".ts", ".csv")


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


def text_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if fn.endswith(TEXT_FILES) or fn in ("LICENSE", ".gitignore"):
                path = os.path.join(dirpath, fn)
                with open(path, encoding="utf-8") as fh:
                    yield os.path.relpath(path, ROOT), fh.read()


class Repo(unittest.TestCase):
    def test_skill_folders_at_the_root(self):
        found = sorted(d for d in os.listdir(ROOT)
                       if os.path.isfile(os.path.join(ROOT, d, "SKILL.md")))
        self.assertEqual(found, sorted(ALL))

    def test_frontmatter_name_and_description(self):
        for s in ALL:
            fm, text = frontmatter(os.path.join(ROOT, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 200, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_plugin_manifest_points_at_the_root_skills(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "clonar")
        self.assertEqual(plugin["skills"], "./")
        self.assertEqual(plugin["description"], ABOUT)
        self.assertEqual(plugin["repository"], "https://github.com/aldushmedia/clonar")
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8") as fh:
            market = json.load(fh)
        self.assertEqual(market["name"], "clonar")
        self.assertEqual(market["plugins"][0]["name"], "clonar")

    def test_readme_carries_the_reel_copy(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# Clonar"))
        for line in (
            "Doce skills para Claude que clonan cualquier app y la promocionan, más el comando "
            "/clonar que te lleva por todo el proceso. Gratis, MIT, sin registro, sin API key, "
            "nada que conectar.",
            "Una hace ingeniería inversa de la app que quieres clonar. Otra la reconstruye. "
            "Otra la prueba en busca de bugs. Y una es la Emprendedora: lee lo que los "
            "usuarios de la app odian y lo arregla en la tuya, para que tengas una app que "
            "puedas vender.",
            "Se adapta a cualquier país hispanohablante",
            "/plugin marketplace add aldushmedia/clonar",
            "/plugin install clonar@clonar",
            "## Letra pequeña",
        ):
            self.assertIn(line, readme)
        for s in ALL:
            self.assertIn("`/%s`" % s, readme)

    def test_master_runs_every_stage_in_order_and_asks_for_approval(self):
        _, text = frontmatter(os.path.join(ROOT, MASTER, "SKILL.md"))
        positions = [text.find("../%s/SKILL.md" % s) for s in SKILLS]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))
        self.assertIn("¿Apruebas para seguir", text)
        self.assertIn("No sigas sin un \"sí\" explícito", text)
        self.assertIn("clonar/progreso.md", text)
        self.assertTrue(os.path.isfile(os.path.join(ROOT, MASTER, "progreso.md")))

    def test_redes_writes_three_reels(self):
        _, text = frontmatter(os.path.join(ROOT, "clonar-redes", "SKILL.md"))
        self.assertIn("3 guiones de Reels", " ".join(text.split()))
        self.assertIn("El nombre de la app original queda fuera", text)
        with open(os.path.join(ROOT, "clonar-redes", "reels.md"), encoding="utf-8") as fh:
            template = fh.read()
        self.assertEqual(len(re.findall(r"^## Reel \d", template, re.M)), 3)
        self.assertEqual(template.count("Caption:"), 3)

    def test_cross_references_point_to_real_skills_and_files(self):
        for rel, text in text_files():
            for name in re.findall(r"\bclonar-[a-z]+\b", text):
                self.assertIn(name, ALL, "%s mentions %s" % (rel, name))
            for folder, fn in re.findall(r"\.\./(clonar(?:-[a-z]+)?)/([\w.-]+\.\w+)", text):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, folder, fn)),
                                "%s points to ../%s/%s" % (rel, folder, fn))

    def test_no_old_names_left(self):
        old_name = "rep" + "lica"  # split so this file does not match itself
        bad = [rel for rel, text in text_files() if old_name in text.lower()]
        self.assertEqual(bad, [])

    def test_license_keeps_the_original_and_adds_aldush_media(self):
        with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as fh:
            lines = fh.read().rstrip("\n").split("\n")
        self.assertEqual(lines[0], "MIT License")
        self.assertTrue(lines[2].startswith("Copyright (c) 2026 "))
        self.assertNotIn("Aldush", lines[2])
        self.assertIn("Permission is hereby granted, free of charge", " ".join(lines))
        self.assertEqual(lines[-1], ALDUSH)

    def test_country_reference_is_shared_by_the_three_skills(self):
        with open(os.path.join(ROOT, "clonar-arquitecto", "paises.md"), encoding="utf-8") as fh:
            ref = fh.read()
        for country in ("México", "Colombia", "Perú", "Chile", "Argentina", "España"):
            self.assertIn("### %s" % country, ref)
        self.assertIn("cambia con el tiempo", ref)
        self.assertIn("contador local", ref)
        for s in ("clonar-arquitecto", "clonar-backend", "clonar-lanzar"):
            _, text = frontmatter(os.path.join(ROOT, s, "SKILL.md"))
            self.assertIn("paises.md", text, s)
            self.assertIn("en qué país o países se va a lanzar", " ".join(text.split()), s)

    def test_no_em_dashes_anywhere(self):
        bad = [rel for rel, text in text_files() if chr(0x2014) in text]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
