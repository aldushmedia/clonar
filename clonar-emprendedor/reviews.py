#!/usr/bin/env python3
"""Ordenador de reseñas para clonar-emprendedor. Solo biblioteca estándar.

Toma las reseñas reales que juntaste de la app que estás clonando y ordena lo
que sus usuarios odian y lo que piden una y otra vez, con las palabras exactas y
un enlace para cada afirmación.

    python3 reviews.py clonar/reviews.csv
    python3 reviews.py clonar/reviews.csv --out clonar/feedback.md
    python3 reviews.py clonar/reviews.csv --json
    python3 reviews.py clonar/reviews.csv --themes mis-temas.json

El CSV necesita estas columnas (las columnas de más se ignoran):

    source   de dónde salió: app-store, google-play, g2, capterra,
             trustpilot, reddit, hacker-news, product-hunt, ...
    url      el enlace a la reseña o al hilo. Obligatorio.
    date     AAAA-MM-DD si la tienes (AAAA-MM también sirve)
    rating   de 1 a 5 estrellas si la fuente tiene estrellas, si no, vacío
    text     la reseña, copiada exactamente. Obligatorio.

Una fila sin url o sin texto se descarta y se cuenta, nunca se adivina. Esta
herramienta solo reorganiza lo que le das. No escribe reseñas, no las
parafrasea, y cada cita que imprime es un fragmento de una fila que tú le diste,
con el enlace de esa fila.

Cómo se ordena un tema: cada reseña que coincide con él suma un peso. Una
reseña de 1 estrella suma 1.0, una de 5 estrellas suma 0.2 y una sin
calificación suma 0.6. Las reseñas más antiguas que --months (por defecto 18)
cuentan la mitad. Los temas con menos de 3 reseñas, o todas de una sola fuente,
se marcan como débiles.
"""

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_THEMES = os.path.join(HERE, "themes.json")
SENTENCE = re.compile(r"(?<=[.!?])\s+|\n+")


class FeedbackError(Exception):
    pass


def load_themes(path=DEFAULT_THEMES):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    themes = []
    for t in data.get("themes", []):
        themes.append({
            "id": t["id"], "label": t.get("label", t["id"]),
            "kind": t.get("kind", "complaint"),
            "patterns": [re.compile(p, re.I) for p in t.get("patterns", [])],
        })
    requests = [re.compile(p, re.I) for p in data.get("request_patterns", [])]
    return themes, requests


def parse_date(text):
    text = (text or "").strip()
    for fmt, n in (("%Y-%m-%d", 10), ("%Y-%m", 7)):
        try:
            return _dt.datetime.strptime(text[:n], fmt).date()
        except ValueError:
            continue
    return None


def parse_rating(text):
    text = (text or "").strip()
    if not text:
        return None
    m = re.match(r"^\s*(\d+(?:\.\d+)?)", text)
    if not m:
        return None
    value = float(m.group(1))
    if value < 1 or value > 5:
        return None
    return value


def load_reviews(path):
    """Return (kept rows, dropped count, duplicate count)."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise FeedbackError("%s está vacío" % path)
        cols = [c.strip().lower() for c in reader.fieldnames]
        for need in ("url", "text"):
            if need not in cols:
                raise FeedbackError(
                    "%s no tiene la columna '%s'. Cada reseña necesita el enlace de "
                    "donde salió y su texto exacto: source,url,date,rating,text" % (path, need))
        kept, dropped, dupes = [], 0, 0
        seen = set()
        for i, raw in enumerate(reader, start=2):
            row = {(k or "").strip().lower(): (v or "").strip() for k, v in raw.items()}
            url, text = row.get("url", ""), row.get("text", "")
            if not url or not text or not re.match(r"^https?://", url):
                dropped += 1
                continue
            key = re.sub(r"\W+", " ", text.lower()).strip()
            if key in seen:
                dupes += 1
                continue
            seen.add(key)
            kept.append({
                "line": i,
                "source": row.get("source", "") or _host(url),
                "url": url,
                "date": parse_date(row.get("date", "")),
                "rating": parse_rating(row.get("rating", "")),
                "text": text,
            })
    return kept, dropped, dupes


def _host(url):
    m = re.match(r"^https?://(?:www\.)?([^/]+)", url)
    return m.group(1) if m else "unknown"


def weight(review, today, months):
    r = review["rating"]
    w = 0.6 if r is None else (6.0 - r) / 5.0
    if review["date"] is not None and today is not None:
        age_days = (today - review["date"]).days
        if age_days > months * 30.4:
            w *= 0.5
    return w


def snippet(text, pattern, limit=220):
    """The first sentence of text that matches pattern, verbatim."""
    for sent in SENTENCE.split(text):
        if pattern.search(sent):
            s = sent.strip()
            if len(s) > limit:
                m = pattern.search(s)
                start = max(0, m.start() - limit // 2)
                s = s[start:start + limit].strip()
                s = ("..." if start > 0 else "") + s + "..."
            return s
    s = text.strip()
    return s if len(s) <= limit else s[:limit].rstrip() + "..."


def analyse(reviews, themes, request_patterns, today=None, months=18):
    if today is None:
        today = _dt.date.today()
    results = {t["id"]: {"id": t["id"], "label": t["label"], "kind": t["kind"],
                         "reviews": [], "score": 0.0} for t in themes}
    requests = []
    unthemed_negative = []
    for rv in reviews:
        w = weight(rv, today, months)
        matched = False
        for t in themes:
            hit = next((p for p in t["patterns"] if p.search(rv["text"])), None)
            if hit is None:
                continue
            matched = True
            res = results[t["id"]]
            res["score"] += w
            res["reviews"].append({"rv": rv, "quote": snippet(rv["text"], hit)})
        req = next((p for p in request_patterns if p.search(rv["text"])), None)
        if req is not None:
            requests.append({"quote": snippet(rv["text"], req), "url": rv["url"],
                             "source": rv["source"], "rating": rv["rating"]})
        if not matched and rv["rating"] is not None and rv["rating"] <= 2:
            unthemed_negative.append(rv)

    total = len(reviews) or 1
    ranked = []
    for res in results.values():
        items = res["reviews"]
        if not items:
            continue
        rated = [x["rv"]["rating"] for x in items if x["rv"]["rating"] is not None]
        sources = sorted({x["rv"]["source"] for x in items})
        # Lowest rated first, then shortest, so the quotes shown are the sharpest.
        items.sort(key=lambda x: (x["rv"]["rating"] if x["rv"]["rating"] is not None else 3,
                                  len(x["quote"])))
        ranked.append({
            "id": res["id"], "label": res["label"], "kind": res["kind"],
            "score": round(res["score"], 2),
            "count": len(items),
            "share_pct": round(100.0 * len(items) / total, 1),
            "avg_rating": round(sum(rated) / len(rated), 2) if rated else None,
            "sources": sources,
            "thin": len(items) < 3 or len(sources) < 2,
            "quotes": [{"quote": x["quote"], "url": x["rv"]["url"],
                        "source": x["rv"]["source"], "rating": x["rv"]["rating"]}
                       for x in items[:3]],
        })
    ranked.sort(key=lambda d: (-d["score"], -d["count"], d["id"]))
    return {
        "reviews": len(reviews),
        "sources": sorted({r["source"] for r in reviews}),
        "rated": sum(1 for r in reviews if r["rating"] is not None),
        "themes": ranked,
        "requests": requests,
        "unthemed_negative": [{"url": r["url"], "source": r["source"],
                               "rating": r["rating"], "text": r["text"][:220]}
                              for r in unthemed_negative],
    }


def _stars(r):
    return "-" if r is None else ("%g*" % r)


def render(result, dropped=0, dupes=0):
    out = ["# Lo que los usuarios del original odian y quieren", ""]
    out.append("%d reseñas de %d fuentes (%s). %d tenían calificación con estrellas." % (
        result["reviews"], len(result["sources"]), ", ".join(result["sources"]) or "ninguna",
        result["rated"]))
    if dropped:
        out.append("%d filas descartadas: sin enlace o sin texto. Nada se cuenta sin "
                   "su fuente." % dropped)
    if dupes:
        out.append("%d reseñas duplicadas eliminadas." % dupes)
    if result["reviews"] < 30:
        out.append("")
        out.append("Muestra pequeña. Menos de 30 reseñas sirven para marcar una "
                   "dirección, no un ranking. Reúne más antes de apostar la hoja de ruta a esto.")
    for kind, title in (("complaint", "Lo que odian"), ("request", "Lo que piden")):
        rows = [t for t in result["themes"] if t["kind"] == kind]
        out.append("")
        out.append("## %s" % title)
        out.append("")
        if not rows:
            out.append("Nada coincidió. Lee las reseñas a mano.")
            continue
        out.append("| puesto | tema | puntuación | reseñas | porcentaje | estrellas promedio | fuentes |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for i, t in enumerate(rows, 1):
            out.append("| %d | %s%s | %.1f | %d | %.0f%% | %s | %d |" % (
                i, t["label"], " (débil)" if t["thin"] else "", t["score"], t["count"],
                t["share_pct"], "-" if t["avg_rating"] is None else "%.1f" % t["avg_rating"],
                len(t["sources"])))
        for t in rows[:6]:
            out.append("")
            out.append("**%s**" % t["label"])
            for q in t["quotes"]:
                out.append('- "%s" (%s, %s) %s' % (q["quote"], q["source"],
                                                   _stars(q["rating"]), q["url"]))
    if result["requests"]:
        out.append("")
        out.append("## Lo que piden, en sus propias palabras")
        out.append("")
        for q in result["requests"][:25]:
            out.append('- "%s" (%s, %s) %s' % (q["quote"], q["source"],
                                               _stars(q["rating"]), q["url"]))
    if result["unthemed_negative"]:
        out.append("")
        out.append("## Lee estas a mano")
        out.append("")
        out.append("Calificaciones bajas que no coincidieron con ningún tema. O es ruido, "
                   "o es un tema que themes.json todavía no tiene. Muchas veces es la "
                   "parte más útil.")
        out.append("")
        for r in result["unthemed_negative"][:15]:
            out.append('- (%s, %s) %s: "%s"' % (r["source"], _stars(r["rating"]),
                                               r["url"], r["text"]))
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("reviews", help="CSV con source,url,date,rating,text")
    ap.add_argument("--themes", default=DEFAULT_THEMES,
                    help="JSON de temas (por defecto, themes.json de esta carpeta)")
    ap.add_argument("--months", type=int, default=18,
                    help="las reseñas con más meses que esto cuentan la mitad (por defecto 18)")
    ap.add_argument("--today", help="AAAA-MM-DD, para resultados reproducibles")
    ap.add_argument("--out", help="escribe aquí el reporte en markdown")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar de texto")
    args = ap.parse_args(argv)
    try:
        themes, req = load_themes(args.themes)
        reviews, dropped, dupes = load_reviews(args.reviews)
    except (FeedbackError, OSError, ValueError, KeyError, re.error) as exc:
        print("reviews: %s" % exc, file=sys.stderr)
        return 2
    if not reviews:
        print("reviews: no hay filas utilizables. Cada fila necesita una url (http...) "
              "y el texto de la reseña.", file=sys.stderr)
        return 2
    today = parse_date(args.today) if args.today else None
    result = analyse(reviews, themes, req, today=today, months=args.months)
    result["dropped"] = dropped
    result["duplicates"] = dupes
    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0
    text = render(result, dropped, dupes)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("listo: %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
