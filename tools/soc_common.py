"""사회학·문화인류학·사회복지·심리학 트랙 가이드 공용 자료."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gk import *  # noqa: F401,F403

SOC3 = OPENSTAX("Introduction to Sociology 3e", "introduction-sociology-3e")
STAT2 = OPENSTAX("Introductory Statistics 2e", "introductory-statistics-2e")
PSY2 = OPENSTAX("Psychology 2e", "psychology-2e")
LIFESPAN = OPENSTAX("Lifespan Development", "lifespan-development")
ANTH = OPENSTAX("Introduction to Anthropology", "introduction-anthropology")
GIDDENS = book("을유문화사", "Giddens · Sutton, Sociology (번역본 『현대 사회학』, 장 제목으로 표기)")
BABBIE = book("센게이지러닝", "Babbie, The Practice of Social Research (번역본 『사회조사방법론』, 장 제목으로 표기)")
BHATT = {"kind": "book", "provider": "University of South Florida (무료 공개 교재)", "title": "Bhattacherjee, Social Science Research: Principles, Methods, and Practices",
         "url": "https://digitalcommons.usf.edu/oa_textbooks/3/", "lang": "영어"}
KHAN_STAT = {"kind": "video", "provider": "Khan Academy", "title": "Statistics and probability", "url": "https://www.khanacademy.org/math/statistics-probability", "lang": "영어(일부 한국어)"}
KOSIS = {"kind": "web", "provider": "국가데이터처", "title": "국가통계포털 KOSIS", "url": "https://kosis.kr/", "lang": "한국어"}
QNET = {"kind": "web", "provider": "한국산업인력공단", "title": "큐넷 Q-Net (자격 시험 출제 기준)", "url": "https://www.q-net.or.kr/", "lang": "한국어"}
KOSSDA = {"kind": "web", "provider": "한국사회과학자료원", "title": "KOSSDA (조사 자료·설문지 공개)", "url": "https://kossda.snu.ac.kr/", "lang": "한국어"}
HAVILAND = book("Cengage", "Haviland 외, Cultural Anthropology: The Human Challenge (장 제목으로 표기)")
NATSEON = book("일조각", "한국문화인류학회 엮음, 『낯선 곳에서 나를 만나다』 (현지 조사 이야기)")
MCQUAIL = book("나남", "McQuail, Mass Communication Theory (번역본 『맥퀘일의 매스 커뮤니케이션 이론』, 장 제목으로 표기)")
KPF = {"kind": "web", "provider": "한국언론진흥재단", "title": "미디어 교육·언론 통계 자료", "url": "https://www.kpf.or.kr/", "lang": "한국어"}
PAC = {"kind": "web", "provider": "언론중재위원회", "title": "언론 피해 구제 제도 안내", "url": "https://www.pac.or.kr/", "lang": "한국어"}
BOKJIRO = {"kind": "web", "provider": "보건복지부", "title": "복지로 (복지 서비스·급여 기준 안내)", "url": "https://www.bokjiro.go.kr/", "lang": "한국어"}
MOHW = {"kind": "web", "provider": "보건복지부", "title": "보건복지부 정책 자료", "url": "https://www.mohw.go.kr/", "lang": "한국어"}
KASW = {"kind": "web", "provider": "한국사회복지사협회", "title": "사회복지사 윤리 강령·자격 안내", "url": "https://www.welfare.net/", "lang": "한국어"}
WELFARE_BOOK = book("여러 출판사", "대학 사회복지개론 교재 (사회복지사 1급 표준 교과목 기준, 장 제목으로 표기)")
ZASTROW = book("Cengage", "Zastrow · Kirst-Ashman, Understanding Human Behavior and the Social Environment (장 제목으로 표기)")
MYERS = book("시그마프레스", "Myers · DeWall, Psychology (번역본 『마이어스의 심리학』, 장 제목으로 표기)")
ARONSON = book("탐구당 등", "Aronson, The Social Animal (번역본 『사회적 동물』)")
KPA = {"kind": "web", "provider": "한국심리학회", "title": "한국심리학회 (심리학 분야·자격 안내)", "url": "https://www.koreanpsychology.or.kr/", "lang": "한국어"}
CRESWELL = book("학지사 등", "Creswell · Poth, Qualitative Inquiry and Research Design (번역본 『질적 연구 방법론』, 장 제목으로 표기)")
EMERSON = book("한울 등", "Emerson 외, Writing Ethnographic Fieldnotes (번역본 『민족지 현장 연구 노트 쓰기』)")
IRB = {"kind": "web", "provider": "국가생명윤리정책원", "title": "국가생명윤리정책원 (기관생명윤리위원회·IRB 안내)", "url": "https://www.nibp.kr/", "lang": "한국어"}
