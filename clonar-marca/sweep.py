#!/usr/bin/env python3
"""Barrido de marca para clonar-marca y clonar-publicar. Solo biblioteca estándar.

Busca en el código de tu clon cualquier cosa que todavía sea de la app
original: su nombre, su dominio, sus colores de marca. Córrelo antes de cada
lanzamiento. Sale con código 1 si encuentra algo, así puede bloquear un
despliegue.

    python3 sweep.py . --avoid "Calendly"
    python3 sweep.py . --avoid "Calendly,Calendly LLC" --domains calendly.com \\
        --colors "#006bff,#0ae8f0"
    python3 sweep.py . --config clonar/brand.json --json

--config lee {"avoid": [...], "domains": [...], "colors": [...]}, la misma
lista "avoid" que usa listing.py.

Los nombres se buscan sin distinguir mayúsculas y en cualquier parte, incluso
dentro de identificadores (CalendlyButton, calendly_sync), porque esos también
se publican. Los colores se buscan en mayúsculas o minúsculas y en forma corta
(#06f coincide con #0066ff). Se revisan los nombres de archivos y carpetas,
además del contenido.

Se salta: .git, node_modules, las carpetas de build, los archivos de bloqueo
(lock), los archivos binarios y la carpeta de planeación clonar/ (donde el
nombre del original sí va). Pasa --include-clonar para revisarla también, por
ejemplo si está dentro de public/.
"""

import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".next", ".nuxt", ".svelte-kit", "dist", "build",
             "out", ".vercel", ".turbo", ".cache", "coverage", "__pycache__", ".venv",
             "venv", "Pods", ".expo", "DerivedData", ".gradle"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
              "Podfile.lock", "Cargo.lock", "poetry.lock"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns", ".pdf", ".zip",
              ".gz", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".mov", ".mp3",
              ".wav", ".avif", ".heic", ".psd", ".sketch", ".fig", ".jar", ".so", ".dylib"}
HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z])")
BINARY_ASSET_HINT = re.compile(r"\.(png|jpe?g|svg|webp|gif|ico|woff2?|ttf|otf)$", re.I)


def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def build_patterns(avoid, domains):
    pats = []
    for name in avoid:
        name = name.strip()
        if not name:
            continue
        # "Acuity Scheduling" also matches AcuityScheduling and acuity-scheduling
        parts = [re.escape(p) for p in re.split(r"[\s_-]+", name) if p]
        pats.append(("name", name, re.compile(r"[\s_-]?".join(parts), re.I)))
    for d in domains:
        d = d.strip().lower()
        if d:
            pats.append(("domain", d, re.compile(re.escape(d), re.I)))
    return pats


def is_binary(path):
    if os.path.splitext(path)[1].lower() in BINARY_EXT:
        return True
    try:
        with open(path, "rb") as fh:
            return b"\0" in fh.read(4096)
    except OSError:
        return True


def sweep(root, avoid=(), domains=(), colors=(), include_clonar=False, max_size=2_000_000):
    pats = build_patterns(avoid, domains)
    cols = {norm_hex(c) for c in colors if HEX.fullmatch(c.strip())}
    hits = []
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        keep = []
        for d in dirnames:
            if d in SKIP_DIRS:
                continue
            if d == "clonar" and rel_dir == "." and not include_clonar:
                continue
            keep.append(d)
        dirnames[:] = sorted(keep)
        for d in dirnames:
            for kind, label, rx in pats:
                if kind == "name" and rx.search(d):
                    hits.append({"file": os.path.normpath(os.path.join(rel_dir, d)) + "/",
                                 "line": 0, "kind": "path", "match": label,
                                 "text": "nombre de carpeta"})
        for fn in sorted(filenames):
            if fn in SKIP_FILES:
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.normpath(os.path.join(rel_dir, fn))
            for kind, label, rx in pats:
                if kind == "name" and rx.search(fn):
                    hits.append({"file": rel, "line": 0, "kind": "path", "match": label,
                                 "text": "nombre de archivo"})
            try:
                if os.path.getsize(path) > max_size or is_binary(path):
                    continue
                with open(path, encoding="utf-8", errors="replace") as fh:
                    lines = fh.readlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                for kind, label, rx in pats:
                    if rx.search(line):
                        hits.append({"file": rel, "line": i, "kind": kind, "match": label,
                                     "text": line.strip()[:160]})
                if cols:
                    for m in HEX.finditer(line):
                        if norm_hex(m.group(0)) in cols:
                            hits.append({"file": rel, "line": i, "kind": "color",
                                         "match": norm_hex(m.group(0)),
                                         "text": line.strip()[:160]})
    return hits


KIND = {"path": "ruta", "name": "nombre", "domain": "dominio", "color": "color"}


def render(hits):
    if not hits:
        return "Limpio. No se encontró nada del nombre, el dominio ni los colores del original."
    out = []
    by_kind = {}
    for h in hits:
        by_kind.setdefault(h["kind"], 0)
        by_kind[h["kind"]] += 1
        loc = h["file"] if not h["line"] else "%s:%d" % (h["file"], h["line"])
        out.append("%-7s %-18s %s  %s" % (KIND.get(h["kind"], h["kind"]), h["match"][:18], loc,
                                           h["text"]))
    out.append("")
    out.append("%d coincidencias (%s). Reemplaza cada una antes de lanzar."
               % (len(hits), ", ".join("%s %d" % (KIND.get(k, k), n)
                                       for k, n in sorted(by_kind.items()))))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("root", nargs="?", default=".",
                    help="carpeta del proyecto (por defecto, la actual)")
    ap.add_argument("--avoid", default="", help="nombres separados por comas")
    ap.add_argument("--domains", default="", help="dominios separados por comas")
    ap.add_argument("--colors", default="", help="colores hex separados por comas")
    ap.add_argument("--config", help="JSON con las listas avoid / domains / colors")
    ap.add_argument("--include-clonar", action="store_true",
                    help="revisa también la carpeta clonar/")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar de texto")
    args = ap.parse_args(argv)
    avoid = [x for x in args.avoid.split(",") if x.strip()]
    domains = [x for x in args.domains.split(",") if x.strip()]
    colors = [x for x in args.colors.split(",") if x.strip()]
    if args.config:
        try:
            with open(args.config, encoding="utf-8") as fh:
                cfg = json.load(fh)
        except (OSError, ValueError) as exc:
            print("sweep: %s" % exc, file=sys.stderr)
            return 2
        avoid += cfg.get("avoid", [])
        domains += cfg.get("domains", [])
        colors += cfg.get("colors", [])
    if not (avoid or domains or colors):
        print("sweep: no hay nada que buscar. Pasa --avoid con el nombre de la app original.",
              file=sys.stderr)
        return 2
    hits = sweep(args.root, avoid, domains, colors, args.include_clonar)
    print(json.dumps(hits, indent=2) if args.json else render(hits))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
