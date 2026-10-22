#!/usr/bin/env python3
"""Puntuación de paridad de funciones para clonar-comparar. Solo biblioteca estándar.

Lee la matriz de funciones que escribió clonar-explorar y que fuiste llenando
mientras construías, y te dice cuánto del original hace tu clon, qué falta y en
qué orden construirlo.

    python3 parity.py clonar/features.csv
    python3 parity.py clonar/features.csv --visual diffs/*.json
    python3 parity.py clonar/features.csv --markdown > clonar/parity.md
    python3 parity.py clonar/features.csv --fail-under 80

El CSV tiene estas columnas (las columnas de más se ignoran):

    feature    qué hace, en palabras simples ("reprogramar una reserva")
    area       la pantalla o el flujo al que pertenece ("página de reserva")
    priority   must | should | could   (P0 | P1 | P2 también sirven)
    original   yes | no     si la app original la tiene
    clone      yes | partial | no | skip
    notes      lo que sea. Para skip, di por qué ("contenido con licencia, fuera del alcance")

Pesos: must 3, should 2, could 1. yes cuenta 1, partial 0.5, no 0. Las filas
skip y las filas con original en "no" (funciones que agregaste) quedan fuera de
la puntuación y se listan aparte, así el número solo mide la paridad.

Con --visual, las puntuaciones de layout de imgdiff.py --json se promedian y se
muestran junto a la puntuación de funciones, y la puntuación general es 80%
funciones + 20% layout. Las funciones son lo que pagan los usuarios.
"""

import argparse
import csv
import json
import sys

WEIGHT = {"must": 3, "should": 2, "could": 1, "p0": 3, "p1": 2, "p2": 1}
CREDIT = {"yes": 1.0, "done": 1.0, "partial": 0.5, "no": 0.0, "": 0.0, "todo": 0.0}
PRIORITY_NAME = {3: "must", 2: "should", 1: "could"}


class MatrixError(Exception):
    pass


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise MatrixError("%s está vacío" % path)
        fields = [f.strip().lower() for f in reader.fieldnames]
        for need in ("feature", "priority", "clone"):
            if need not in fields:
                raise MatrixError("%s no tiene la columna '%s'. Columnas necesarias: "
                                  "feature, area, priority, original, clone, notes"
                                  % (path, need))
        rows = []
        for i, raw in enumerate(reader, start=2):
            row = {(k or "").strip().lower(): (v or "").strip() for k, v in raw.items()}
            if not row.get("feature"):
                continue
            row["line"] = i
            rows.append(row)
    return rows


def score(rows):
    counted = []
    skipped = []
    extras = []
    problems = []
    for row in rows:
        original = row.get("original", "yes").lower() or "yes"
        clone = row.get("clone", "").lower()
        prio = row.get("priority", "").lower()
        if original in ("no", "n", "false"):
            extras.append(row)
            continue
        if clone == "skip":
            skipped.append(row)
            continue
        if prio not in WEIGHT:
            problems.append("línea %d: priority '%s' no es must/should/could, se cuenta como could"
                            % (row["line"], row.get("priority", "")))
        if clone not in CREDIT:
            problems.append("línea %d: clone '%s' no es yes/partial/no/skip, se cuenta como no"
                            % (row["line"], row.get("clone", "")))
        w = WEIGHT.get(prio, 1)
        c = CREDIT.get(clone, 0.0)
        counted.append(dict(row, weight=w, credit=c))

    total = sum(r["weight"] for r in counted)
    got = sum(r["weight"] * r["credit"] for r in counted)
    feature_score = 100.0 * got / total if total else 0.0

    areas = {}
    for r in counted:
        a = r.get("area") or "(sin área)"
        t = areas.setdefault(a, [0.0, 0.0, 0])
        t[0] += r["weight"] * r["credit"]
        t[1] += r["weight"]
        t[2] += 1
    by_area = sorted(
        ({"area": a, "score": round(100.0 * g / t, 1) if t else 0.0, "features": n}
         for a, (g, t, n) in areas.items()),
        key=lambda d: d["score"])

    missing = [r for r in counted if r["credit"] < 1.0]
    missing.sort(key=lambda r: (-r["weight"], r["credit"], r.get("area", ""), r["feature"]))

    def brief(r):
        return {"feature": r["feature"], "area": r.get("area", ""),
                "priority": PRIORITY_NAME.get(r.get("weight", WEIGHT.get(
                    r.get("priority", "").lower(), 1)), "could"),
                "clone": r.get("clone", "") or "no", "notes": r.get("notes", "")}

    musts = [r for r in counted if r["weight"] == 3]
    return {
        "feature_score": round(feature_score, 1),
        "counted": len(counted),
        "must_have_done": sum(1 for r in musts if r["credit"] == 1.0),
        "must_have_total": len(musts),
        "by_area": by_area,
        "missing": [brief(r) for r in missing],
        "skipped": [brief(r) for r in skipped],
        "extras": [brief(r) for r in extras],
        "problems": problems,
    }


def visual_scores(paths):
    scores = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
        if "score" not in data:
            raise MatrixError("%s no es una salida de imgdiff.py --json" % p)
        name = data.get("files", {}).get("clone", p)
        scores.append({"file": name, "score": float(data["score"]),
                       "mode": data.get("mode", "layout")})
    return scores


def combine(result, visuals):
    if visuals:
        layout = sum(v["score"] for v in visuals) / len(visuals)
        result["visual"] = visuals
        result["layout_score"] = round(layout, 1)
        result["overall"] = round(0.8 * result["feature_score"] + 0.2 * layout, 1)
    else:
        result["overall"] = result["feature_score"]
    return result


def render(result, markdown=False):
    out = []
    h = "## " if markdown else ""
    out.append("%sParidad: %.1f / 100" % (h, result["overall"]))
    out.append("")
    out.append("funciones %.1f  (%d contadas, imprescindibles %d de %d terminadas)" % (
        result["feature_score"], result["counted"], result["must_have_done"],
        result["must_have_total"]))
    if "layout_score" in result:
        out.append("layout    %.1f  (%d pantallas comparadas)" % (
            result["layout_score"], len(result["visual"])))
    if result["must_have_done"] < result["must_have_total"]:
        out.append("")
        out.append("Todavía no se puede publicar: faltan %d funciones imprescindibles."
                   % (result["must_have_total"] - result["must_have_done"]))
    out.append("")
    out.append("%sPor área, de la más débil a la más fuerte" % h)
    for a in result["by_area"]:
        out.append("- %-28s %5.1f  (%d funciones)" % (a["area"], a["score"], a["features"]))
    out.append("")
    out.append("%sLo que falta, en orden de construcción" % h)
    if not result["missing"]:
        out.append("- nada. Todas las funciones contadas están terminadas.")
    for m in result["missing"]:
        note = ("  (%s)" % m["notes"]) if m["notes"] else ""
        out.append("- [%s] %s: %s, %s%s" % (m["priority"], m["area"] or "-",
                                             m["feature"], m["clone"], note))
    if result["skipped"]:
        out.append("")
        out.append("%sFuera a propósito (no puntúan)" % h)
        for m in result["skipped"]:
            out.append("- %s: %s" % (m["feature"], m["notes"] or "sin motivo, agrega uno"))
    if result["extras"]:
        out.append("")
        out.append("%sTuyas, no están en el original (no puntúan)" % h)
        for m in result["extras"]:
            out.append("- %s" % m["feature"])
    if result.get("visual"):
        out.append("")
        out.append("%sPantallas" % h)
        for v in sorted(result["visual"], key=lambda d: d["score"]):
            out.append("- %-40s %5.1f" % (v["file"], v["score"]))
    if result["problems"]:
        out.append("")
        out.append("%sCorrige en la matriz" % h)
        for p in result["problems"]:
            out.append("- %s" % p)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("matrix", help="el CSV de la matriz de funciones")
    ap.add_argument("--visual", nargs="*", default=[],
                    help="salidas de imgdiff.py --json para sumar")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar de texto")
    ap.add_argument("--markdown", action="store_true", help="imprime el reporte en markdown")
    ap.add_argument("--fail-under", type=float,
                    help="sale con código 1 si la puntuación queda debajo de esto")
    args = ap.parse_args(argv)
    try:
        result = combine(score(load(args.matrix)), visual_scores(args.visual))
    except (MatrixError, OSError, ValueError) as exc:
        print("parity: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result, markdown=args.markdown))
    if args.fail_under is not None and result["overall"] < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
