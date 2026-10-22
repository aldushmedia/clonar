#!/usr/bin/env python3
"""Revisor de fichas de tienda para clonar-lanzar. Solo biblioteca estándar.

Revisa una ficha de App Store y de Google Play contra los límites de cada campo
de las tiendas y contra los errores que hacen que rechacen un clon: el nombre
de la app original en tus metadatos, afirmaciones de ranking en el título y
caracteres desperdiciados en las palabras clave.

    python3 listing.py clonar/launch/listing.json
    python3 listing.py listing.json --avoid "Calendly,Acuity Scheduling"
    python3 listing.py listing.json --json

listing.json (ver listing.example.json):

    {
      "avoid": ["Nombre De La App Original", "Su Empresa"],
      "app_store":   {"name", "subtitle", "promotional_text", "description",
                      "keywords", "whats_new"},
      "google_play": {"title", "short_description", "full_description"}
    }

Deja fuera la tienda en la que no vas a publicar. Sale con código 1 si hay
algún error, y con 0 si solo hay avisos.
"""

import argparse
import json
import re
import sys
import unicodedata

LIMITS = {
    "app_store": {"name": 30, "subtitle": 30, "promotional_text": 170,
                  "description": 4000, "keywords": 100, "whats_new": 4000},
    "google_play": {"title": 30, "short_description": 80, "full_description": 4000},
}
SHORT_FIELDS = {"name", "subtitle", "title", "short_description"}
CLAIMS = re.compile(
    r"(#\s?1\b|\bnumber one\b|\bno\.? ?1\b|\bbest\b|\btop[- ]rated\b|\b(app|game) of the year\b"
    r"|\bfree\b|\bdiscount\b|\bsale\b|\b\d+% off\b|\bnew!?$)", re.I)
STOP = {"a", "an", "and", "app", "for", "the", "to", "of", "with", "your", "you", "in", "on", "&"}


def length(text):
    """Characters as a person counts them (an emoji built from parts is one)."""
    text = unicodedata.normalize("NFC", text or "")
    count = 0
    prev_joiner = False
    for ch in text:
        cat = unicodedata.category(ch)
        if ch == "‍":
            prev_joiner = True
            continue
        if cat in ("Mn", "Me") or ch in ("️", "︎") or 0x1F3FB <= ord(ch) <= 0x1F3FF:
            continue
        if prev_joiner:
            prev_joiner = False
            continue
        count += 1
    return count


def has_emoji(text):
    return any(unicodedata.category(ch) == "So" or ord(ch) >= 0x1F000 for ch in text or "")


def words(text):
    return [w for w in re.findall(r"[a-z0-9']+", (text or "").lower()) if w not in STOP]


def lint(listing, avoid=None):
    issues = []
    avoid = [a.strip() for a in (avoid or listing.get("avoid") or []) if a.strip()]

    def add(level, store, field, msg):
        issues.append({"level": level, "store": store, "field": field, "message": msg})

    found_store = False
    for store, limits in LIMITS.items():
        data = listing.get(store)
        if not data:
            continue
        found_store = True
        for field, limit in limits.items():
            value = data.get(field, "")
            n = length(value)
            if not value:
                level = "error" if field in ("name", "title", "description",
                                             "full_description") else "warn"
                add(level, store, field, "vacío")
                continue
            if n > limit:
                add("error", store, field, "%d caracteres, el límite es %d (%d de más)"
                    % (n, limit, n - limit))
            for name in avoid:
                if re.search(r"(?<!\w)%s(?!\w)" % re.escape(name), value, re.I):
                    add("error", store, field,
                        "menciona '%s'. El nombre o la marca de otra app en tus "
                        "metadatos hace que rechacen la ficha y es una invitación a que "
                        "te den de baja. Describe lo que hace la tuya." % name)
            if field in SHORT_FIELDS:
                m = CLAIMS.search(value)
                if m:
                    add("warn", store, field,
                        "'%s' se lee como una afirmación de ranking o de precio. "
                        "Google Play las prohíbe en el título y la descripción corta, "
                        "y Apple rechaza las que no puedes respaldar." % m.group(0).strip())
                if has_emoji(value):
                    add("warn", store, field, "emoji en un campo corto. Play los rechaza "
                        "en los títulos, y los revisores de App Store muchas veces también.")
                caps = re.findall(r"\b[A-Z]{4,}\b", value)
                if caps:
                    add("warn", store, field, "palabra(s) en mayúsculas: %s" % ", ".join(caps))
        if store == "app_store" and data.get("keywords"):
            kw_raw = data["keywords"]
            parts = [k.strip().lower() for k in kw_raw.split(",")]
            if re.search(r",\s", kw_raw):
                add("warn", store, "keywords", "los espacios después de las comas desperdician "
                    "caracteres. Usa palabra1,palabra2,palabra3")
            dupes = sorted({k for k in parts if k and parts.count(k) > 1})
            if dupes:
                add("warn", store, "keywords", "repetidas: %s" % ", ".join(dupes))
            in_name = set(words(data.get("name", "")) + words(data.get("subtitle", "")))
            wasted = sorted({w for k in parts for w in words(k) if w in in_name})
            if wasted:
                add("warn", store, "keywords", "ya están en el nombre o el subtítulo, así "
                    "que estos caracteres se desperdician: %s" % ", ".join(wasted))
            if any(not k for k in parts):
                add("warn", store, "keywords", "entrada vacía (coma doble o coma al final)")
    if not found_store:
        add("error", "-", "-", "no se encontró ninguna sección app_store ni google_play")
    return issues


LEVEL = {"error": "ERROR", "warn": "AVISO"}


def render(listing, issues):
    out = []
    for store, limits in LIMITS.items():
        data = listing.get(store)
        if not data:
            continue
        out.append(store.replace("_", " ").title())
        for field, limit in limits.items():
            n = length(data.get(field, ""))
            mark = "EXCEDE" if n > limit else ("ok" if n else "--")
            out.append("  %-18s %5d / %-5d %s" % (field, n, limit, mark))
        out.append("")
    if not issues:
        out.append("Sin problemas.")
    for i in issues:
        out.append("%-5s %s.%s: %s" % (LEVEL.get(i["level"], i["level"]), i["store"], i["field"],
                                       i["message"]))
    errs = sum(1 for i in issues if i["level"] == "error")
    warns = len(issues) - errs
    out.append("")
    out.append("%d errores, %d avisos" % (errs, warns))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("listing", help="el archivo listing.json")
    ap.add_argument("--avoid", help="nombres separados por comas que no deben aparecer "
                                    "(la app original, su empresa)")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar de texto")
    args = ap.parse_args(argv)
    try:
        with open(args.listing, encoding="utf-8") as fh:
            listing = json.load(fh)
    except (OSError, ValueError) as exc:
        print("listing: %s" % exc, file=sys.stderr)
        return 2
    avoid = args.avoid.split(",") if args.avoid else None
    issues = lint(listing, avoid)
    if args.json:
        print(json.dumps(issues, indent=2))
    else:
        print(render(listing, issues))
    return 1 if any(i["level"] == "error" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
