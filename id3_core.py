import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# ====== URUTAN NILAI (biar rules tampil rapi seperti Excel ) ======
VALUE_ORDER: Dict[str, List[str]] = {
    "Penghasilan": ["Rendah", "Sedang", "Tinggi"],
    "Usia": ["Dewasa", "Lansia"],
    "Kredit": ["Buruk", "Bagus"],
    "Pekerjaan": ["Karyawan", "Pensiunan", "Wiraswasta"],
    # kalau ada fitur lain, bisa ditambah
}


def _ordered_values(feature: str, values: List[str]) -> List[str]:
    """Urutkan nilai cabang sesuai VALUE_ORDER kalau ada, sisanya alfabet."""
    custom = VALUE_ORDER.get(feature)
    if not custom:
        return sorted(values)

    rank = {v: i for i, v in enumerate(custom)}
    # nilai yang tidak ada di custom akan ditaruh di belakang (urut alfabet)
    return sorted(values, key=lambda v: (rank.get(v, 10**9), str(v)))


@dataclass
class Node:
    label: Optional[str] = None
    feature: Optional[str] = None
    children: Optional[Dict[str, "Node"]] = None
    majority_label: Optional[str] = None

    def is_leaf(self) -> bool:
        return self.label is not None


def entropy(labels: List[str]) -> float:
    total = len(labels)
    if total == 0:
        return 0.0
    counts = Counter(labels)
    ent = 0.0
    for c in counts.values():
        p = c / total
        if p <= 0.0:
            continue
        ent -= p * math.log2(p)
    return ent


def info_gain(rows: List[Dict[str, str]], feature: str, target_key: str) -> float:
    base = entropy([r.get(target_key, "") for r in rows])

    groups = defaultdict(list)
    for r in rows:
        groups[r.get(feature, "")].append(r)

    n = len(rows)
    if n == 0:
        return 0.0

    weighted = 0.0
    for g in groups.values():
        weighted += (len(g) / n) * entropy([x.get(target_key, "") for x in g])

    return base - weighted


def majority_label(rows: List[Dict[str, str]], target_key: str) -> Optional[str]:
    labels = [r.get(target_key, "") for r in rows]
    labels = [x for x in labels if x != ""]
    return Counter(labels).most_common(1)[0][0] if labels else None


def build_id3(rows: List[Dict[str, str]], features: List[str], target_key: str) -> Node:
    if not rows:
        return Node(label="", majority_label="")

    labels = [r.get(target_key, "") for r in rows]
    labels = [x for x in labels if x != ""]
    if not labels:
        return Node(label="", majority_label="")

    # kalau semua label sama → leaf
    if len(set(labels)) == 1:
        return Node(label=labels[0], majority_label=labels[0])

    maj = majority_label(rows, target_key)
    if not features:
        return Node(label=maj, majority_label=maj)

    # ====== pilih feature dengan gain terbesar
    # FIX: tie-break ikut urutan "features" (bukan alfabet) supaya konsisten
    gains = [(info_gain(rows, f, target_key), f) for f in features]
    best_gain = max(g for g, _ in gains)

    # semua feature yang gain-nya sama (atau sangat dekat)
    eps = 1e-12
    best_candidates = [f for g, f in gains if abs(g - best_gain) <= eps]

    # pilih kandidat yang posisinya paling awal di list features
    best_feature = min(best_candidates, key=lambda f: features.index(f))

    if best_gain <= 1e-12:
        return Node(label=maj, majority_label=maj)

    node = Node(feature=best_feature, majority_label=maj, children={})

    values = list(set(r.get(best_feature, "") for r in rows))
    values = _ordered_values(best_feature, values)

    remaining = [f for f in features if f != best_feature]
    for v in values:
        subset = [r for r in rows if r.get(best_feature, "") == v]
        node.children[v] = build_id3(subset, remaining, target_key)

    return node


def predict(tree: Node, sample: Dict[str, str]) -> str:
    node = tree
    while not node.is_leaf():
        f = node.feature
        if not f:
            return node.majority_label or ""
        v = sample.get(f, "")
        if node.children and v in node.children:
            node = node.children[v]
        else:
            return node.majority_label or ""
    return node.label or ""


def tree_to_text(node: Node, indent: str = "") -> str:
    if node.is_leaf():
        return indent + f"-> {node.label}\n"

    s = indent + f"[{node.feature}] (fallback={node.majority_label})\n"

    # FIX: urutkan cabang sesuai VALUE_ORDER
    if node.children:
        vals = _ordered_values(node.feature or "", list(node.children.keys()))
        for val in vals:
            child = node.children[val]
            s += indent + f"  - {node.feature} = {val}:\n"
            s += tree_to_text(child, indent + "    ")
    return s


def rules_from_tree(node: Node, path: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    path = path or []
    if node.is_leaf():
        cond = " AND ".join(path) if path else "(ROOT)"
        return [(cond, node.label or "")]

    out: List[Tuple[str, str]] = []

    # FIX: urutkan cabang sesuai VALUE_ORDER
    if node.children:
        vals = _ordered_values(node.feature or "", list(node.children.keys()))
        for val in vals:
            child = node.children[val]
            out.extend(rules_from_tree(child, path + [f"{node.feature}={val}"]))

    return out
