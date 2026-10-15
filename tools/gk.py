"""socio-arena 레벨2·3 가이드 공용 도구 (tech-arena·math-arena·sci-arena와 같은 공통 단원 템플릿).

과목: overview(분야 개요), prereq(선수지식 점검 + 레벨1 연결), units(로드맵), next(다음 과목)
단원: objectives(학습 목표), checklist(핵심 개념), advice(학습 조언 1~2문단),
      resources(추천 자료), hours(예상 학습 시간), after(먼저 볼 단원), selfcheck(자가점검 문항)
자가점검 문항은 레벨1 문항 스키마를 그대로 써서 같은 채점 코드로 동작한다.
트랙 항목 [id, 제목, 다른 트랙 id]는 다른 트랙의 과목을 공유한다(예: 심리학의 사회통계 → 사회학 트랙).

바뀔 수 있는 값(법령 조문·연령 기준·제도 금액·통계)은 tools/facts.py에 두고 F(키)·V(키)로 쓴다.
그런 값이나 제도를 다루는 단원에는 review(근거, 확인 시점, 다음 점검, 무엇을 볼지, 쓰는 facts 키)를 붙인다.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from facts import FACTS, F, V  # noqa: F401  (가이드 스크립트에서 함께 쓴다)

CONTENT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

TRACKS = [
    {"id": "korean-history", "title": "한국사", "note": "레벨1 한국사Ⅰ·Ⅱ의 흐름 위에 제도·사회·문화사와 사료 읽기를 더합니다. 한국사능력검정시험 심화 수준입니다.",
     "l2": [["korean-premodern", "전근대 한국사 심화"], ["korean-modern", "근현대 한국사 심화"]],
     "l3": [["korean-historiography", "한국사학사·사료 읽기"], ["korean-thematic", "분야사(사상·경제·사회)"]]},
    {"id": "world-history", "title": "세계사", "note": "동양사와 서양사를 개설서 수준으로 정리합니다. 레벨1 세계사Ⅰ·Ⅱ에서 이어집니다.",
     "l2": [["east-asian-history", "동양사개설"], ["western-history", "서양사개설"]],
     "l3": [["regional-history", "지역사(중국·일본·유럽·이슬람)"], ["historiography", "사학사"]]},
    {"id": "sociology", "title": "사회학", "note": "사회를 설명하는 이론과 그것을 확인하는 조사·통계의 방법. 조사방법론과 사회통계는 사회복지·심리학 트랙과 공유합니다.",
     "l2": [["sociology-intro", "사회학개론"], ["research-methods", "사회조사방법론"], ["social-statistics", "사회통계"]],
     "l3": [["sociological-theory", "사회학 이론사"], ["urban-family-labor", "도시·가족·노동 사회학"], ["qualitative-research", "질적 연구"]]},
    {"id": "anthropology", "title": "문화인류학·미디어", "note": "낯선 문화를 이해하는 인류학의 눈과, 오늘의 문화를 만드는 미디어를 함께 봅니다.",
     "l2": [["anthropology-intro", "문화인류학개론"], ["media-society", "미디어와 사회"]],
     "l3": [["ethnography", "민족지"], ["cultural-theory", "문화이론"], ["digital-culture", "디지털 문화"]]},
    {"id": "social-welfare", "title": "사회복지", "note": "복지 제도의 원리와 사람을 이해하는 이론. 사회복지사 1급 과목 구성을 바탕으로 하며, 조사방법은 사회학 트랙과 공유합니다.",
     "l2": [["welfare-intro", "사회복지개론"], ["hbse", "인간행동과 사회환경"], ["research-methods", "사회조사방법론", "sociology"]],
     "l3": [["welfare-policy-law", "사회복지정책·법제"], ["welfare-practice", "사회복지실천론"]]},
    {"id": "psychology", "title": "심리학", "note": "고교 과목이 없어 레벨2에서 시작합니다. 통계는 사회학 트랙과 공유하며, 뇌와 신경은 sci-arena 생물Ⅰ을 함께 보면 좋습니다.",
     "l2": [["psychology-intro", "심리학개론"], ["dev-social-psych", "발달·사회심리학"], ["social-statistics", "사회통계", "sociology"]],
     "l3": [["cognitive-psych", "인지심리학"], ["clinical-counseling", "임상·상담심리학"], ["psychometrics", "심리측정·연구방법"]]},
    {"id": "geography", "title": "지리학", "note": "땅과 기후의 자연지리, 사람과 공간의 인문지리, 그리고 그것을 그리는 지도학. 레벨1 지리Ⅰ·Ⅱ에서 이어집니다.",
     "l2": [["physical-geography", "자연지리학 개론"], ["human-geography", "인문지리학 개론"], ["cartography", "지도학"]],
     "l3": [["urban-economic-geo", "도시·경제지리"], ["gis-remote-sensing", "GIS·원격탐사"], ["regional-planning", "지역계획"]]},
    {"id": "politics", "title": "정치학·국제관계", "note": "권력과 제도, 그리고 나라 사이의 관계. 레벨1 정치와 법Ⅰ에서 이어집니다.",
     "l2": [["politics-intro", "정치학개론"], ["korean-politics", "한국정치"]],
     "l3": [["comparative-politics", "비교정치"], ["political-thought", "정치사상"], ["international-relations", "국제관계론·외교사"]]},
    {"id": "public-admin", "title": "행정학", "note": "정부가 일하는 방식. 공무원 시험 행정학 과목 구성을 바탕으로 하며, 헌법은 법학 트랙과 공유합니다.",
     "l2": [["public-admin-intro", "행정학개론"], ["constitutional-law", "헌법", "law"]],
     "l3": [["org-hr-finance", "조직·인사·재무행정"], ["policy-studies", "정책학"]]},
    {"id": "law", "title": "법학", "note": "법의 체계와 해석, 국가의 기본법인 헌법, 사적 생활의 기본인 민법총칙. 레벨1 정치와 법Ⅰ·Ⅱ에서 이어집니다.",
     "l2": [["law-intro", "법학개론"], ["constitutional-law", "헌법"], ["civil-law-general", "민법총칙"]],
     "l3": [["criminal-law", "형법"], ["administrative-law", "행정법"], ["commercial-labor-law", "상법·노동법"], ["procedure-law", "소송법"]]},
    {"id": "philosophy", "title": "철학·윤리학", "note": "생각하는 법과 생각의 역사. 레벨1 윤리Ⅰ·Ⅱ에서 이어집니다.",
     "l2": [["philosophy-intro", "철학개론"], ["logic", "논리학"], ["history-of-philosophy", "동서양 철학사"]],
     "l3": [["ethics-applied", "윤리학·응용윤리"], ["epistemology-metaphysics", "인식론·형이상학"], ["social-philosophy", "정치·사회철학"]]},
]
LEVELS = {"2": "전문대 수준 (학문 입문·개론)", "3": "대학 수준 (전공 심화)"}
VALIDATION = {"2": "학과별 개론 교재의 목차와 관련 시험(한국사능력검정시험 심화, 사회조사분석사 2급, 임상심리사 2급·청소년상담사 3급, 공무원 시험 행정학·헌법, 관광통역안내사 국사 등)의 출제 범위",
              "3": "학부 전공 교재의 목차와 관련 자격·시험(사회조사분석사 1급, 사회복지사 1급, 준학예사, 중등교사 임용 도덕·윤리 등)의 과목 구성. 시험 대비가 아니라 누락 방지용입니다"}

# ---------------------------------------------------------------- 자주 쓰는 자료와 링크
OPENSTAX = lambda title, slug: {"kind": "book", "provider": "OpenStax (무료 공개 교재)", "title": title,
                                "url": f"https://openstax.org/details/books/{slug}", "lang": "영어"}
SEP = lambda title, slug: {"kind": "web", "provider": "Stanford Encyclopedia of Philosophy", "title": title,
                           "url": f"https://plato.stanford.edu/entries/{slug}/", "lang": "영어"}
WEB = lambda provider, title, url, lang="한국어": {"kind": "web", "provider": provider, "title": title, "url": url, "lang": lang}
KMOOC = {"kind": "lecture", "provider": "K-MOOC", "title": "K-MOOC 강좌 검색 (과목명으로 검색)", "url": "https://www.kmooc.kr/", "lang": "한국어"}
KOCW = {"kind": "lecture", "provider": "KOCW (대학 공개 강의)", "title": "KOCW 강의 검색 (과목명으로 검색)", "url": "http://www.kocw.net/", "lang": "한국어"}
LAW = {"kind": "web", "provider": "국가법령정보센터", "title": "법령 원문 검색", "url": "https://www.law.go.kr/", "lang": "한국어"}
HISTNET = {"kind": "web", "provider": "국사편찬위원회", "title": "우리역사넷", "url": "https://contents.history.go.kr/", "lang": "한국어"}
HISTDB = {"kind": "web", "provider": "국사편찬위원회", "title": "한국사데이터베이스 (사료 원문·번역)", "url": "https://db.history.go.kr/", "lang": "한국어"}
L1 = lambda c, n, title: {"title": f"레벨1 · {title}", "href": f"browse.html?c={c}#ch{n:02d}"}
L1R = lambda c, n, title: {"kind": "web", "provider": "socio-arena 레벨1", "title": f"챕터 {n} {title}", "url": f"browse.html?c={c}#ch{n:02d}", "part": "레벨1 복습"}
SCI = lambda c, title: {"title": f"sci-arena 레벨1 · {title}", "href": f"https://sci-arena.org/browse.html?c={c}"}
MATH = lambda c, title: {"title": f"math-arena 레벨1 · {title}", "href": f"https://math-arena.org/browse.html?c={c}"}
G2R = lambda t, s, u, title: {"kind": "web", "provider": "socio-arena 레벨2", "title": title, "url": f"guide.html?lv=2&t={t}&s={s}" + (f"&u={u}" if u else ""), "part": "함께 볼 단원"}
G3R = lambda t, s, u, title: {"kind": "web", "provider": "socio-arena 레벨3", "title": title, "url": f"guide.html?lv=3&t={t}&s={s}" + (f"&u={u}" if u else ""), "part": "함께 볼 단원"}
G2 = lambda t, s, title: {"title": f"레벨2 · {title}", "href": f"guide.html?lv=2&t={t}&s={s}"}
G3 = lambda t, s, title: {"title": f"레벨3 · {title}", "href": f"guide.html?lv=3&t={t}&s={s}"}


def book(provider, title):
    return {"kind": "book", "provider": provider, "title": title}


def R(base, part):
    d = dict(base); d["part"] = part; return d


L2NOTE = "레벨 2 (전문대 수준, 학문 입문·개론). 목차 검증 기준: {}."
L3NOTE = "레벨 3 (대학 수준, 전공 심화). 목차 검증 기준: {}. 레벨3은 단원당 학습 조언 1문단, 자가점검 3문항의 가벼운 형식이며 원전과 전공서를 직접 읽는 것을 전제로 합니다."


# ---------------------------------------------------------------- 점검 정보(review)
# 법령·제도·통계처럼 바뀔 수 있는 내용이 있는 단원(또는 과목)에 붙인다.
#   basis: 근거, checked: 마지막 확인 "YYYY-MM", next: 다음 점검 "YYYY-MM", watch: 무엇이 바뀌면 고칠지,
#   facts: 이 단원이 쓰는 tools/facts.py 키 목록(값을 고치고 다시 빌드하면 함께 바뀐다)
def review(basis, checked, next_, watch, facts=()):
    return {"basis": basis, "checked": checked, "next": next_, "watch": watch, "facts": list(facts)}


def _check_review(r, where):
    for k in ("basis", "checked", "next", "watch"):
        assert r.get(k), f"{where}: review.{k}"
    assert re.fullmatch(r"\d{4}-\d{2}", r["checked"]) and re.fullmatch(r"\d{4}-\d{2}", r["next"]), f"{where}: review 날짜 형식 YYYY-MM"
    assert r["next"] > r["checked"], f"{where}: 다음 점검은 확인일 뒤"
    for k in r.get("facts", []): assert k in FACTS, f"{where}: facts 키 {k} 없음"


# ---------------------------------------------------------------- 문항
def num(i, prompt, answer, expl, hint=None, fmt="integer", tol=0):
    q = {"type": "question", "id": f"q{i}", "qtype": "numeric", "prompt": prompt, "answer": str(answer),
         "answer_format": fmt, "tolerance": tol, "explanation": expl}
    if hint: q["hint"] = hint
    return q


def fill(i, prompt, blanks, expl, hint=None):
    q = {"type": "question", "id": f"q{i}", "qtype": "fill_blank", "prompt": prompt,
         "blanks": [{"id": k + 1, "answers": a if isinstance(a, list) else [a]} for k, a in enumerate(blanks)],
         "explanation": expl}
    if hint: q["hint"] = hint
    return q


def order(i, prompt, correct, disp, expl, hint=None):
    """correct: 정답 순서의 항목, disp: 화면 표시 순서(correct의 인덱스, 정답 순서와 달라야 함)."""
    ids = "abcdefgh"
    q = {"type": "question", "id": f"q{i}", "qtype": "ordering", "prompt": prompt,
         "items": [{"id": ids[k], "text": correct[j]} for k, j in enumerate(disp)],
         "answer_order": [ids[disp.index(j)] for j in range(len(correct))], "explanation": expl}
    if hint: q["hint"] = hint
    return q


def written(i, prompt, groups, need, model):
    return {"type": "question", "id": f"q{i}", "qtype": "written", "prompt": prompt,
            "rubric": {"visibility": "hidden", "keyword_groups": groups, "min_groups_matched": need},
            "model_answer": model}


def unit(no, title, hours, after, objectives, checklist, advice, resources, selfcheck, review=None):
    u = {"no": no, "title": title, "hours": hours, "after": after, "objectives": objectives,
         "checklist": checklist, "advice": advice, "resources": resources, "selfcheck": selfcheck}
    if review: u["review"] = review
    return u


# ---------------------------------------------------------------- 검사와 저장
def _norm(s):
    return re.sub(r"\s+", "", str(s)).lower()


_EXPOSED = []


def _check_q(q, where):
    if q["qtype"] == "written":
        m = q["model_answer"]
        hit = sum(any(k in m for k in g) for g in q["rubric"]["keyword_groups"])
        assert hit >= q["rubric"]["min_groups_matched"], f"{where}: 모범 답안이 채점 기준 미달"
        return
    assert len(q.get("explanation", "")) >= 10, f"{where}: 풀이"
    if q["qtype"] == "fill_blank":
        n = q["prompt"].count("{{")
        assert n == len(q["blanks"]), f"{where}: 빈칸 수"
        shown = _norm(re.sub(r"\{\{\d+\}\}", "", q["prompt"]))
        for b in q["blanks"]:
            for a in b["answers"]:
                if len(_norm(a)) >= 2 and _norm(a) in shown: _EXPOSED.append(f"{where}: 지문에 정답 노출({a})")
    if q["qtype"] == "ordering":
        assert len(q["items"]) >= 3, f"{where}: 순서 항목 3개 이상"
        assert q["answer_order"] != [it["id"] for it in q["items"]], f"{where}: 표시 순서가 정답 순서와 같음"


def check(subject, units):
    """최소 품질 검사"""
    nos = [u["no"] for u in units]
    assert nos == list(range(1, len(units) + 1)), "단원 번호"
    for u in units:
        where = f"{subject['id']} u{u['no']}"
        assert all(a < u["no"] for a in u["after"]), f"{where}: 선수 단원은 앞 단원이어야 함"
        assert len(u["objectives"]) >= 2 and len(u["checklist"]) >= 4, f"{where}: 목표·체크리스트"
        assert len(u["advice"]) >= 1 and all(len(a) >= 80 for a in u["advice"]), f"{where}: 조언 분량"
        assert u["resources"], f"{where}: 자료"
        for r in u["resources"]:
            assert r.get("kind") in ("lecture", "video", "book", "web") and r.get("provider") and r.get("title"), f"{where}: 자료 형식 {r}"
        assert 3 <= len(u["selfcheck"]) <= 6, f"{where}: 자가점검 3~6문항"
        if u.get("review"): _check_review(u["review"], where)
        for q in u["selfcheck"]: _check_q(q, where)
    if subject.get("review"): _check_review(subject["review"], subject["id"])
    p = subject["prereq"]
    assert p["links"] and len(p["questions"]) >= 3, f"{subject['id']}: 선수 점검"
    for q in p["questions"]: _check_q(q, f"{subject['id']} 선수")
    assert len(subject["overview"]) == 3, f"{subject['id']}: 개요 3문단"
    assert not _EXPOSED, "\n".join(_EXPOSED)


def write_subject(subject, units):
    check(subject, units)
    lv, tr, sid = subject["level"], subject["track"], subject["id"]
    base = os.path.join(CONTENT, f"level{lv}", tr, sid)
    os.makedirs(base, exist_ok=True)
    subj = dict(subject, schema_version="1.0", type="guide_subject")
    for k, q in enumerate(subj["prereq"]["questions"]):
        q["id"] = f"p{k + 1}"; q["stage"] = "prereq"
    subj["units"] = [dict({"no": u["no"], "title": u["title"], "hours": u["hours"], "after": u["after"],
                      "file": f"u{u['no']:02d}.json"}, **({"review": True} if u.get("review") else {})) for u in units]
    subj["total_hours"] = sum(u["hours"] for u in units)
    json.dump(subj, open(os.path.join(base, "subject.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for u in units:
        d = dict(u, schema_version="1.0", type="guide_unit", level=lv, track=tr, subject=sid,
                 id=f"l{lv}-{tr}-{sid}-u{u['no']:02d}")
        for k, q in enumerate(d["selfcheck"]):
            q["id"] = f"q{k + 1}"; q["stage"] = "selfcheck"
        json.dump(d, open(os.path.join(base, f"u{u['no']:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_tracks()
    n = sum(len(u["selfcheck"]) for u in units)
    print(f"{subject['title']}: {len(units)}단원, 약 {subj['total_hours']}시간, 자가점검 {n}문항, 선수 점검 {len(subject['prereq']['questions'])}문항")
    return subj


def write_tracks():
    out = {"schema_version": "1.0", "levels": LEVELS, "validation": VALIDATION, "tracks": []}
    for t in TRACKS:
        subs = []
        for lv, key in ((2, "l2"), (3, "l3")):
            for e in t[key]:
                sid, title = e[0], e[1]
                home = e[2] if len(e) > 2 and e[2] else t["id"]
                ok = os.path.exists(os.path.join(CONTENT, f"level{lv}", home, sid, "subject.json"))
                d = {"level": lv, "id": sid, "title": title, "available": ok}
                if home != t["id"]: d["t"] = home
                subs.append(d)
        out["tracks"].append({"id": t["id"], "title": t["title"], "note": t["note"], "subjects": subs})
    json.dump(out, open(os.path.join(CONTENT, "guides.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    write_tracks(); print("guides.json 갱신")
