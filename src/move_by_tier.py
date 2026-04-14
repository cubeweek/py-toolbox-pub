import os
import re
import json
import time
import ssl
import urllib.request
import urllib.parse
from pathlib import Path

import requests

# =======================
# Paths (수정 가능)
# =======================
BASE_DIR = Path("/Users/carrie/DEV/project/Coding-Test")

BOJ_ROOT = BASE_DIR / "src/problem/baekjoon"
LC_ROOT = BASE_DIR / "src/problem/leetcode"

ALLOWED_SUFFIX = {".java", ".kt"}

# =======================
# BOJ: solved.ac API
# =======================
SOLVEDAC_API_URL = "https://solved.ac/api/v3/problem/lookup"
SOLVEDAC_HEADERS = {"Accept": "application/json"}

BJ_RE = re.compile(r"\b(?:BJ|BOJ)\s*0*([0-9]{1,6})\b", re.IGNORECASE)

def extract_boj_problem_id(filename: str):
    m = BJ_RE.search(filename)
    return int(m.group(1)) if m else None

def level_to_subdir(level: int | None) -> Path:
    # level: 1~30 (Bronze~Ruby), 0/None은 unrated
    if level is None or level == 0:
        return Path("unrated")

    if 1 <= level <= 5:
        return Path("bronze") / f"b{6 - level}"   # 1->b5, 5->b1
    if 6 <= level <= 10:
        return Path("silver") / f"s{11 - level}"  # 6->s5, 10->s1
    if 11 <= level <= 15:
        return Path("gold") / f"g{16 - level}"    # 11->g5, 15->g1
    if 16 <= level <= 20:
        return Path("platinum") / f"p{21 - level}"# 16->p5, 20->p1
    if 21 <= level <= 25:
        return Path("diamond") / f"d{26 - level}" # 21->d5, 25->d1
    if 26 <= level <= 30:
        return Path("ruby") / f"r{31 - level}"    # 26->r5, 30->r1

    return Path("unrated")

def solvedac_http_get_json(url: str):
    req = urllib.request.Request(url, headers=SOLVEDAC_HEADERS, method="GET")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

def lookup_boj_levels(problem_ids):
    # problem/lookup?problemIds=1000,1001,...
    if not problem_ids:
        return {}

    BATCH = 100
    result = {}
    ids = list(problem_ids)

    for i in range(0, len(ids), BATCH):
        batch = ids[i:i + BATCH]
        qs = urllib.parse.urlencode({"problemIds": ",".join(map(str, batch))})
        url = f"{SOLVEDAC_API_URL}?{qs}"

        data = solvedac_http_get_json(url)  # 배열 응답
        for item in data:
            pid = int(item.get("problemId"))
            lvl = item.get("level")
            result[pid] = lvl

        time.sleep(0.2)

    return result

# =======================
# Common: move with overwrite
# =======================
def safe_move(src: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        dst.unlink()
    src.replace(dst)

# =======================
# Leaf checks
# =======================
BOJ_TIER_SET = {"bronze", "silver", "gold", "platinum", "diamond", "ruby", "unrated"}
BOJ_GROUP_RE = re.compile(r"^[bsgpdr][1-5]$", re.IGNORECASE)

def is_in_boj_leaf(path: Path) -> bool:
    # backjoon/{tier}/{group}/file
    try:
        rel = path.relative_to(BOJ_ROOT).parts
    except ValueError:
        return False
    if len(rel) < 3:
        return False
    tier = rel[0].lower()
    group = rel[1].lower()
    return (tier in BOJ_TIER_SET) and (BOJ_GROUP_RE.match(group) is not None)

LC_DIFF_SET = {"easy", "medium", "hard"}

def is_in_lc_leaf(path: Path) -> bool:
    # leetcode/{difficulty}/file
    try:
        rel = path.relative_to(LC_ROOT).parts
    except ValueError:
        return False
    if len(rel) < 2:
        return False
    diff = rel[0].lower()
    return diff in LC_DIFF_SET

# =======================
# LeetCode: GraphQL difficulty
# =======================
LC_GRAPHQL_URL = "https://leetcode.com/graphql/"
LC_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

def load_lc_cookies_from_env():
    # 로컬에서만 쓰는 용도: 환경변수로 쿠키를 넣으면 성공률이 올라갈 수 있음
    cookies = {}
    if os.getenv("LEETCODE_SESSION"):
        cookies["LEETCODE_SESSION"] = os.getenv("LEETCODE_SESSION")
    if os.getenv("csrftoken"):
        cookies["csrftoken"] = os.getenv("csrftoken")
    return cookies

def pascal_to_kebab(name: str) -> str:
    # TwoSum -> two-sum
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).lower()

def lc_fetch_difficulty(title_slug: str, cookies: dict | None = None) -> str | None:
    # title_slug: "two-sum"
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
      }
    }
    """
    payload = {
        "operationName": "getQuestionDetail",
        "query": query,
        "variables": {"titleSlug": title_slug},
    }

    try:
        r = requests.post(
            LC_GRAPHQL_URL,
            headers=LC_HEADERS,
            json=payload,
            cookies=cookies or {},
            timeout=15,
        )
        if r.status_code != 200:
            return None

        data = r.json()
        q = (data.get("data") or {}).get("question") or {}
        diff = q.get("difficulty")  # "Easy"/"Medium"/"Hard"
        if not isinstance(diff, str):
            return None
        return diff.lower()
    except Exception:
        return None

def lc_target_dir(diff: str) -> Path | None:
    if diff in LC_DIFF_SET:
        return LC_ROOT / diff
    return None

# =======================
# Main routines
# =======================
def organize_boj():
    if not BOJ_ROOT.exists():
        raise FileNotFoundError(f"BOJ_ROOT not found: {BOJ_ROOT}")

    files = [p for p in BOJ_ROOT.rglob("*") if p.is_file() and p.suffix in ALLOWED_SUFFIX]

    # leaf 아닌 파일만 대상
    targets = {}
    for f in files:
        if is_in_boj_leaf(f):
            continue
        pid = extract_boj_problem_id(f.name)
        if pid is not None:
            targets[f] = pid

    if not targets:
        print("[BOJ] nothing to move (no non-leaf BJ files found).")
        return 0, 0

    levels = lookup_boj_levels(sorted(set(targets.values())))

    moved, skipped = 0, 0
    for path, pid in targets.items():
        lvl = levels.get(pid)
        subdir = level_to_subdir(lvl)
        dst_dir = BOJ_ROOT / subdir
        safe_move(path, dst_dir)
        moved += 1

    return moved, skipped

def organize_leetcode():
    if not LC_ROOT.exists():
        print(f"[LC] LC_ROOT not found: {LC_ROOT} (skip).")
        return 0, 0

    cookies = load_lc_cookies_from_env()

    files = [p for p in LC_ROOT.rglob("*") if p.is_file() and p.suffix in ALLOWED_SUFFIX]

    moved, skipped = 0, 0
    for f in files:
        if is_in_lc_leaf(f):
            continue  # 이미 easy/medium/hard 안이면 스킵

        name = f.stem  # PascalCase
        slug = pascal_to_kebab(name)

        diff = lc_fetch_difficulty(slug, cookies=cookies)
        if diff is None:
            print(f"[LC][skip] cannot fetch difficulty: {name} (slug={slug}) -> keep: {f}")
            skipped += 1
            continue

        dst_dir = lc_target_dir(diff)
        if dst_dir is None:
            print(f"[LC][skip] unknown difficulty '{diff}': {name} -> keep: {f}")
            skipped += 1
            continue

        safe_move(f, dst_dir)
        print(f"[LC][moved] {name} -> {dst_dir}")
        moved += 1

    return moved, skipped

def main():
    boj_moved, _ = organize_boj()
    lc_moved, lc_skipped = organize_leetcode()
    print(f"Done. boj_moved={boj_moved}, lc_moved={lc_moved}, lc_skipped={lc_skipped}")

if __name__ == "__main__":
    main()
