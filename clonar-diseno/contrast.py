#!/usr/bin/env python3
"""Verificación de contraste para los tokens de clonar-diseno. Solo biblioteca estándar.

Cada color de texto de tu archivo de tokens, revisado contra los fondos sobre
los que va, con la proporción de contraste de WCAG 2. Córrelo después de cada
cambio de paleta, incluido el cambio de marca, porque una paleta nueva es donde
se rompe el contraste.

    python3 contrast.py clonar/design/tokens.json
    python3 contrast.py tokens.json --json
    python3 contrast.py "#6b7280" "#ffffff"        # un solo par

Los pares salen de la lista "pairs" del archivo de tokens: [["text", "bg"], ...],
o [["text-muted", "surface", "large"], ...] para texto de 24px o más (o de
18.66px en negrita), que solo necesita 3:1. Sin lista de pares, cada color con
text, fg u on- en el nombre se revisa contra cada color con bg, background o
surface en el nombre.

Umbrales (WCAG 2.2): texto normal AA 4.5, AAA 7. Texto grande AA 3, AAA 4.5.
Las partes de interfaz y los anillos de foco ("ui" como tercer elemento)
necesitan 3. Sale con código 1 si algún par no pasa AA, así puede frenar un
build.
"""

import argparse
import json
import re
import sys

HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
NEEDS = {"normal": (4.5, 7.0), "large": (3.0, 4.5), "ui": (3.0, 3.0)}


def parse_hex(value):
    m = HEX.match(value.strip())
    if not m:
        raise ValueError("no es un color hex: %r" % value)
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    la, lb = luminance(parse_hex(fg)), luminance(parse_hex(bg))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def flatten(obj, prefix=""):
    """{"color": {"text": {"muted": "#..."}}} -> {"text-muted": "#..."}."""
    out = {}
    if isinstance(obj, dict):
        if "value" in obj and isinstance(obj["value"], str):
            out[prefix] = obj["value"]
            return out
        if "$value" in obj and isinstance(obj["$value"], str):
            out[prefix] = obj["$value"]
            return out
        for k, v in obj.items():
            if k.startswith("$") or k.startswith("_"):
                continue
            key = "%s-%s" % (prefix, k) if prefix else k
            out.update(flatten(v, key))
    elif isinstance(obj, str) and HEX.match(obj.strip()):
        out[prefix] = obj.strip()
    return out


def colours(tokens):
    src = tokens.get("color", tokens.get("colors", tokens.get("colour", {})))
    return {k: v for k, v in flatten(src).items() if HEX.match(v)}


def default_pairs(cols):
    fg = [k for k in cols if re.search(r"(^|-)(text|fg|on)(-|$)", k)]
    bg = [k for k in cols if re.search(r"(^|-)(bg|background|surface)(-|$)", k)]
    return [[f, b] for f in fg for b in bg]


def check(cols, pairs):
    rows = []
    for p in pairs:
        if len(p) < 2:
            continue
        fg, bg = p[0], p[1]
        size = p[2] if len(p) > 2 else "normal"
        if size not in NEEDS:
            size = "normal"
        if fg not in cols or bg not in cols:
            rows.append({"fg": fg, "bg": bg, "size": size, "error": "token desconocido"})
            continue
        r = ratio(cols[fg], cols[bg])
        aa, aaa = NEEDS[size]
        rows.append({"fg": fg, "bg": bg, "size": size, "ratio": round(r, 2),
                     "aa": r >= aa, "aaa": r >= aaa,
                     "fg_hex": cols[fg], "bg_hex": cols[bg]})
    return rows


def render(rows):
    out = []
    for r in rows:
        if "error" in r:
            out.append("  ??    %-24s sobre %-20s %s" % (r["fg"], r["bg"], r["error"]))
            continue
        if r["size"] == "ui":
            grade = "PASA" if r["aa"] else "FALLA"
        else:
            grade = "AAA" if r["aaa"] else ("AA" if r["aa"] else "FALLA")
        out.append("  %-5s %5.2f:1  %-24s sobre %-20s %s" % (
            grade, r["ratio"], r["fg"], r["bg"], "" if r["size"] == "normal" else r["size"]))
    fails = sum(1 for r in rows if "error" in r or not r["aa"])
    out.append("")
    out.append("  %d pares, %d no pasan AA" % (len(rows), fails))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("args", nargs="+", help="tokens.json, o dos colores hex")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar de texto")
    a = ap.parse_args(argv)
    try:
        if len(a.args) == 2 and all(HEX.match(x) for x in a.args):
            cols = {"fg": a.args[0], "bg": a.args[1]}
            pairs = [["fg", "bg"]]
        else:
            with open(a.args[0], encoding="utf-8") as fh:
                tokens = json.load(fh)
            cols = colours(tokens)
            pairs = tokens.get("pairs") or default_pairs(cols)
    except (OSError, ValueError) as exc:
        print("contrast: %s" % exc, file=sys.stderr)
        return 2
    if not pairs:
        print("contrast: no hay pares que revisar. Agrega una lista \"pairs\" al archivo de tokens.",
              file=sys.stderr)
        return 2
    rows = check(cols, pairs)
    print(json.dumps(rows, indent=2) if a.json else render(rows))
    return 1 if any("error" in r or not r["aa"] for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
