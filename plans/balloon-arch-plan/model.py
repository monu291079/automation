"""Single source of truth for every number in the plan."""
SETUP_ITEMS = [  # (item, qty text, unit price, total, note/source)
    ("Electric dual-nozzle pump", "2 pcs", "₹800", 1600, "listing ₹666-900 (Kiwiparty, TradeIndia)"),
    ("Arch frame 9 ft (halka)", "1 pc", "₹1,669", 1669, "HASTHIP listing"),
    ("Arch frame 10 ft (majboot)", "1 pc", "₹4,399", 4399, "CRAze listing"),
    ("DIY strip + glue dots kit", "4 kit", "₹499", 1996, "Party Supplies India"),
    ("Latex balloon 12-inch (shuruaati stock)", "1,000 pcs", "₹280/100", 2800, "Party Wholesale Hub"),
    ("Foil, ribbon, tape, fishing line", "allowance", "-", 1500, "apna allowance (local quote lo)"),
    ("Tools: scissor, hooks, extension, repair kit", "1 set", "-", 1200, "apna allowance"),
    ("Sandbag / base weight + carry bag", "1 set", "-", 1500, "apna allowance"),
    ("Basic backdrop + props", "1 set", "-", 2500, "apna allowance (baad mein rent bhi ho sakta)"),
    ("Branding: card, banner, rate-card", "1 set", "-", 1000, "apna allowance"),
    ("Practice + travel buffer", "-", "-", 1500, "apna allowance"),
    ("Starting marketing (photo shoot + boost)", "-", "-", 1500, "apna allowance"),
]
SETUP = sum(x[3] for x in SETUP_ITEMS)  # 23,164
LEAN_ITEMS = [("Pump", 800), ("Frame 9 ft", 1669), ("DIY kit", 499), ("Balloons 1,000", 2800), ("Tape/ribbon/foil", 1000), ("Tools", 800), ("Branding", 500), ("Buffer", 1000)]
LEAN = sum(v for _, v in LEAN_ITEMS)  # 9,068

# ek event (₹3,500 ka arch) ka hisaab
EVENT = [("Latex balloons (~200 pcs)", 560), ("Foil / accent", 240), ("Tape, strip, glue dots, wastage", 250), ("Aana-jaana (petrol/auto)", 400), ("Helper (setup + teardown)", 700), ("Payment fee / extra", 150)]
EVENT_PRICE = 3500
EVENT_COST = sum(v for _, v in EVENT)  # 2,300
EVENT_PROFIT = EVENT_PRICE - EVENT_COST  # 1,200

FIXED = [("Phone + internet", 400), ("Marketing (boost, print)", 1000), ("Repair / purane frame ki maintenance", 300), ("Chhota-mota kharch", 300)]
FIXED_M1 = sum(v for _, v in FIXED)  # 2,000

# month: (events, avg ticket, variable cost per event, fixed monthly)
BASE = [(2, 2500, 1800, 2000), (3, 3000, 2000, 2000), (4, 3000, 2000, 2000), (5, 3500, 2300, 3000), (6, 3500, 2300, 3000), (7, 3500, 2300, 3000),
        (8, 4000, 2500, 3500), (8, 4000, 2500, 3500), (9, 4000, 2500, 3500), (10, 4000, 2500, 3500), (12, 4000, 2500, 3500), (10, 4000, 2500, 3500)]


def scenario(mult):
    rows, cum = [], -SETUP
    for e, p, c, f in BASE:
        ev = max(1, round(e * mult))
        rev = ev * p
        exp = ev * c + f
        prof = rev - exp
        cum += prof
        rows.append(dict(ev=ev, ticket=p, rev=rev, var=ev * c, fixed=f, exp=exp, profit=prof, cum=cum))
    return rows


LOW, BASEROWS, BUSY = scenario(.5), scenario(1), scenario(1.5)


def be_month(rows):
    for i, r in enumerate(rows):
        if r["cum"] >= 0:
            return i + 1
    return None


def tot(rows, a, b, k):
    return sum(r[k] for r in rows[a:b])


def inr(n):
    s = f"{abs(int(round(n))):,}"
    # indian grouping
    d = f"{abs(int(round(n)))}"
    if len(d) > 3:
        h, t = d[:-3], d[-3:]
        g = []
        while len(h) > 2:
            g.insert(0, h[-2:]); h = h[:-2]
        if h:
            g.insert(0, h)
        s = ",".join(g + [t])
    return ("-₹" if n < 0 else "₹") + s


if __name__ == "__main__":
    print("setup", SETUP, "lean", LEAN, "event", EVENT_COST, EVENT_PROFIT, "fixed", FIXED_M1)
    for nm, r in (("low", LOW), ("base", BASEROWS), ("busy", BUSY)):
        print(nm, "BE month", be_month(r), "6m rev", tot(r, 0, 6, "rev"), "6m profit", tot(r, 0, 6, "profit"), "12m rev", tot(r, 0, 12, "rev"), "exp", tot(r, 0, 12, "exp"), "profit", tot(r, 0, 12, "profit"), "cum", r[-1]["cum"])
    for i, r in enumerate(BASEROWS):
        print(i + 1, r)
