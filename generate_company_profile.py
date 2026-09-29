# -*- coding: utf-8 -*-
"""Generate TourMaker company introduction PDF (black text, 2026 data)."""
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, ListFlowable, ListItem
)

pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", r"C:\Windows\Fonts\malgunbd.ttf"))

BRAND = HexColor("#1e40af")
BRAND_DARK = HexColor("#0f172a")
ACCENT = HexColor("#0ea5e9")
LINE = HexColor("#e2e8f0")
SOFT = HexColor("#f8fafc")
# 본문·제목 모두 검정에 가깝게 (가독성)
TEXT = HexColor("#000000")
MUTED = HexColor("#000000")  # 본문·푸터 모두 검정 (가독성)

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm

OUT = Path(__file__).with_name("투어메이커_회사소개서.pdf")


def styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title", fontName="MalgunBold", fontSize=22, textColor=white,
            leading=30, alignment=1, spaceAfter=4,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontName="Malgun", fontSize=10, textColor=HexColor("#dbeafe"),
            leading=15, alignment=1,
        ),
        "h1": ParagraphStyle(
            "h1", fontName="MalgunBold", fontSize=13, textColor=BRAND,
            leading=18, spaceBefore=10, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="MalgunBold", fontSize=11, textColor=TEXT,
            leading=15, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", fontName="Malgun", fontSize=9, textColor=TEXT,
            leading=14, spaceAfter=3,
        ),
        "body_b": ParagraphStyle(
            "body_b", fontName="MalgunBold", fontSize=9, textColor=TEXT,
            leading=14, spaceAfter=2,
        ),
        "small": ParagraphStyle(
            "small", fontName="Malgun", fontSize=8, textColor=MUTED,
            leading=12, spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Malgun", fontSize=8.5, textColor=TEXT,
            leading=13, leftIndent=8,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Malgun", fontSize=7.5, textColor=MUTED,
            alignment=1, leading=10,
        ),
        "chip": ParagraphStyle(
            "chip", fontName="MalgunBold", fontSize=8, textColor=BRAND,
            leading=11, alignment=1,
        ),
        "card_t": ParagraphStyle(
            "card_t", fontName="MalgunBold", fontSize=9, textColor=TEXT,
            leading=12, spaceAfter=2,
        ),
        "card_d": ParagraphStyle(
            "card_d", fontName="Malgun", fontSize=8, textColor=TEXT,
            leading=11,
        ),
    }


def header_band(canvas, doc):
    canvas.saveState()
    # top brand bar
    canvas.setFillColor(BRAND)
    canvas.rect(0, PAGE_H - 14 * mm, PAGE_W, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("MalgunBold", 9)
    canvas.drawString(MARGIN, PAGE_H - 9 * mm, "(주)투어메이커  회사소개서")
    canvas.setFont("Malgun", 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 9 * mm, "tourmaker.kr  ·  2026")
    # footer
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Malgun", 7)
    canvas.drawString(MARGIN, 7 * mm, "Copyright © 2024–2026 Tourmaker Corp. All rights reserved.")
    canvas.drawRightString(PAGE_W - MARGIN, 7 * mm, f"{doc.page}")
    canvas.restoreState()


def cover_first(canvas, doc):
    """First page: cover hero + standard header/footer after content starts."""
    canvas.saveState()
    # hero band
    canvas.setFillColor(BRAND_DARK)
    canvas.rect(0, PAGE_H - 52 * mm, PAGE_W, 52 * mm, fill=1, stroke=0)
    canvas.setFillColor(BRAND)
    canvas.rect(0, PAGE_H - 52 * mm, PAGE_W, 3 * mm, fill=1, stroke=0)

    canvas.setFillColor(ACCENT)
    canvas.setFont("MalgunBold", 8)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 18 * mm, "종합여행업  ·  국내·해외  ·  S2B / G2B  ·  스마트 가이드북")

    canvas.setFillColor(white)
    canvas.setFont("MalgunBold", 20)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 30 * mm, "(주)투어메이커  회사소개서")
    canvas.setFont("Malgun", 10)
    canvas.setFillColor(HexColor("#bfdbfe"))
    canvas.drawCentredString(
        PAGE_W / 2, PAGE_H - 39 * mm,
        "학교·관공서·단체 여행을 디지털로 운영합니다"
    )
    canvas.setFont("Malgun", 8)
    canvas.drawCentredString(
        PAGE_W / 2, PAGE_H - 46 * mm,
        "스마트 가이드 · 단계별 행정 · 정산 증빙  |  tourmaker.kr"
    )

    # footer
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Malgun", 7)
    canvas.drawString(MARGIN, 7 * mm, "Copyright © 2024–2026 Tourmaker Corp. All rights reserved.")
    canvas.drawRightString(PAGE_W - MARGIN, 7 * mm, f"{doc.page}")
    canvas.restoreState()


def section_title(s, n, title):
    return Paragraph(f"{n}. {title}", s["h1"])


def kv_table(rows, s):
    data = [[Paragraph(f"<b>{k}</b>", s["body_b"]), Paragraph(v, s["body"])] for k, v in rows]
    t = Table(data, colWidths=[38 * mm, 140 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("BACKGROUND", (0, 0), (0, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
    ]))
    return t


def people_cards(s):
    people = [
        ("이재명  대표이사", "PM / Strategy", "총괄 기획 · 데이터 분석 · 위기관리", "010-9443-7881", "강원대 데이터사이언스 대학원"),
        ("허나연  실장", "Admin / Finance", "운영 총괄 · 행정 · 정산 · S2B/G2B", "010-5066-0433", "계약·예약 관리 총괄"),
        ("조 혁  이사", "Partnership / Field", "대외협력 · 파트너십 · 현장 운영", "010-4249-4026", "국내외 로컬 네트워크"),
    ]
    cells = []
    for name, role, desc, phone, note in people:
        cell = [
            Paragraph(name, s["card_t"]),
            Paragraph(role, ParagraphStyle("r", parent=s["small"], textColor=BRAND, fontName="MalgunBold")),
            Paragraph(desc, s["card_d"]),
            Paragraph(f"☎ {phone}", s["card_d"]),
            Paragraph(note, s["small"]),
        ]
        cells.append(cell)
    # flatten to single paragraphs joined
    def pack(paras):
        story = []
        for p in paras:
            story.append(p)
        return story

    # Use nested mini tables as cards
    cards = []
    for cell in cells:
        inner = Table([[c] for c in cell], colWidths=[56 * mm])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        cards.append(inner)
    t = Table([cards], colWidths=[58 * mm, 58 * mm, 58 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def strength_grid(s):
    items = [
        ("검증된 실행력", "설립 이후 50건 이상 공공·학교 용역 완수. 행정 요구에 신속 대응."),
        ("데이터 기반 기획", "데이터 분석으로 목적·동선 최적화. AI·스마트시티 등 SIT 전문."),
        ("지역 전문성", "강원랜드·정선군·교육청 등 로컬 네트워크와 현지 파트너십."),
        ("스마트 가이드북", "모바일 일정·항공·호텔·동선·비상연락망을 URL 하나로 공유."),
    ]
    rows = []
    pair = []
    for title, desc in items:
        box = Table([[
            Paragraph(f"<b>{title}</b>", s["card_t"]),
        ], [
            Paragraph(desc, s["card_d"]),
        ]], colWidths=[86 * mm])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.5, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        pair.append(box)
        if len(pair) == 2:
            rows.append(pair)
            pair = []
    t = Table(rows, colWidths=[90 * mm, 90 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def digital_steps(s):
    steps = [
        ("STEP 01", "디지털 제안·견적", "학교·기관 맞춤 제안서·일정표 웹 제공. 입찰·수의계약용 PDF 동시 생성."),
        ("STEP 02", "스마트 가이드북", "항공·호텔·일정·입국카드·실시간 정보를 모바일 한 페이지에 공유."),
        ("STEP 03", "디지털 행정·정산", "선금·착수·완료·최종 단계별 공문·계약·정산·증빙을 제출 형식으로 통합."),
    ]
    cells = []
    for tag, title, desc in steps:
        box = Table([[
            Paragraph(f'<font color="#1e40af"><b>{tag}</b></font>', s["small"]),
            Paragraph(f"<b>{title}</b>", s["card_t"]),
            Paragraph(desc, s["card_d"]),
        ]], colWidths=[56 * mm])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.6, BRAND),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        cells.append(box)
    t = Table([cells], colWidths=[58 * mm, 58 * mm, 58 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def track_block(s, label, items):
    parts = [Paragraph(f"<b>[{label}]</b>", s["body_b"])]
    for it in items:
        parts.append(Paragraph(f"• {it}", s["bullet"]))
    return KeepTogether(parts)


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=56 * mm,  # room for cover on p1; adjusted per page via onPage
        bottomMargin=18 * mm,
        title="(주)투어메이커 회사소개서",
        author="(주)투어메이커",
    )

    story = []

    # ===== 1. Overview =====
    story.append(section_title(s, "1", "기업 개요 (Company Overview)"))
    story.append(kv_table([
        ("기업명", "(주)투어메이커 (TOURMAKER Corp.)"),
        ("대표이사", "이재명 (CEO & Planning Director)"),
        ("설립일", "2024년 4월 23일"),
        ("사업자등록번호", "473-81-03183"),
        ("관광사업등록", "제2024-000001호"),
        ("소재지", "본사: 강원특별자치도 정선군 정선읍 봉양3길 22-10 3층<br/>지사: 강원특별자치도 태백시 (태백 사무소)"),
        ("주요 사업", "국내·해외 여행업, 학교·관공서·단체 연수, MICE 기획, 스마트 가이드북·디지털 행정"),
        ("Vision", "\"여행을 만드는 사람들, 투어메이커\" — 데이터 기반 분석과 로컬 전문성을 결합해 최적의 경험을 기획합니다."),
    ], s))

    story.append(section_title(s, "2", "핵심 인력 (Key People)"))
    story.append(people_cards(s))

    story.append(section_title(s, "3", "핵심 경쟁력 (Competitiveness)"))
    story.append(strength_grid(s))

    story.append(section_title(s, "4", "3단계 디지털 운영 (Digital Operation)"))
    story.append(Paragraph(
        "종이 일정표 대신 URL로 공유하고, 행정·정산은 투어메이커 자체 디지털 프로세스로 관리합니다.",
        s["body"],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(digital_steps(s))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "대외 공개 데모: tourmaker.kr → 스마트 가이드북 체험 (황지고 제주 · 고한중 오사카 · 태백해설사 · 춘천 힐링 등)",
        s["small"],
    ))

    story.append(section_title(s, "5", "주요 전략 상품 (Strategic Focus)"))
    story.append(Paragraph("<b>2026 강원대학교 글로컬 패스파인더</b>", s["body_b"]))
    story.append(Paragraph("컨셉: 중국 AI 혁신 &amp; 글로벌 캠퍼스 현장 — 상해·항주 AI 첨단 기업 탐방 · 글로벌 해커톤", s["body"]))
    for line in [
        "단순 견학이 아닌 실무형 기술 교육 및 프로젝트 수행",
        "현지 대학·기업 연계 심화 세션 (Deep Dive)",
        "모바일 최적화 스마트 가이드북으로 교육·현장 운영 일원화",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    story.append(Paragraph("<b>스마트 가이드북 (2026 라인업)</b>", s["body_b"]))
    for line in [
        "황지정보산업고 제주 3박4일 문화탐방 (학생 단체 · 당일 UI·지도 동선)",
        "고한중학교 오사카·교토·USJ 탐방 (청주 직항)",
        "태백해설사 1박2일 심화교육 (지질공원 현장답사)",
        "산소휴드림 실버카페 춘천 힐링 당일여행 (시니어 맞춤)",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    # ===== Track record =====
    story.append(section_title(s, "6", "주요 수행 실적 (Track Record)"))
    story.append(Paragraph(
        "스마트 가이드북 적용·완수 실적 중심. 홈페이지 포트폴리오(2026.09 기준)와 동기화.",
        s["small"],
    ))
    story.append(Spacer(1, 2 * mm))

    story.append(track_block(s, "2026 Smart Guidebook / 최근 수행", [
        "2026.09  산소휴드림 실버카페 춘천 힐링 당일여행",
        "2026.09  황지정보산업고등학교 제주 문화탐방 (3박4일)",
        "2026.09  고한중학교 오사카·교토·USJ 탐방",
        "2026.09  강원고생대국가지질공원 태백해설사 심화교육",
        "2026.06  정선군 가족행복과 보육교직원 제주 워크숍",
        "2026.05  사북고등학교 대만 역사문화탐방",
        "2026.05  사북중학교·문곡중학교 오사카 문화탐방",
        "2026.05  정선군청 환경과 기타큐슈 선진지 견학",
        "2026.03  태백의용소방대 오사카 문화탐방",
        "2026.01  강원대학교 글로컬 패스파인더 (상해/항주)",
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(track_block(s, "Global / Tech — 해외 기술 연수", [
        "2025.01  데이터보안·활용 혁신융합 사업 싱가포르 기술연수 (강원대 등 5개 대학)",
        "2025.09  강원대 데이터사이언스학과 일본 단기 연수 (AI 융합)",
        "2025.08  첨단소재·나노융합 혁신융합대학사업단 일본 교류",
        "2024.10  KAIST × NYU 교환학생 한국문화체험",
        "2024.07  강원대 지역지능화혁신 인재양성 상해 연수 (스마트시티)",
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(track_block(s, "Public Sector — 공공/지자체", [
        "2025.11  정선 시장활성화 사업단 제주 선진지 견학",
        "2025.06  정선군 중국 자매도시(구강시) 방문 운영",
        "2025.05  정선군청 모범공무원 중국 선진지 견학",
        "2024.11  정선군 이장단 일본 큐슈 선진지 견학",
        "2024.09  정선 시설관리공단 말레이시아 선진시설 견학",
        "2024.06  정선군청 모범공무원 일본 북해도 연수",
        "2024.05  양양전통시장 벤치마킹 대행 용역",
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(track_block(s, "Education — 학교/교육기관", [
        "2025.12  함백고등학교 3학년 현장체험학습",
        "2025.10  정선고·사북고 제주 테마 학습 / 함백중 서울역사 문화탐방",
        "2025.09  철암고등학교 제주 테마 학습",
        "2025.07  영월 신천초등학교 필리핀 연수",
        "2024.09  태백 황지고등학교 제주도 수학여행",
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(track_block(s, "Corporate / MICE — 기업·행사", [
        "2025.11  강원랜드 협력사 서비스 우수직원 연수",
        "2025.02  HCI KOREA 2025 학술대회 지원 (MICE)",
        "2024.11  강원랜드 협력사 우수직원 마카오 연수 / 희망재단 일본 힐링 연수",
        "2024.09  정선아리랑문화재단 직원 역량강화 워크숍",
        "2025.05  정선 청소년수련관 해커톤 대회 행사 지원",
    ]))

    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=LINE))
    story.append(Spacer(1, 3 * mm))
    story.append(section_title(s, "7", "문의 (Contact)"))
    story.append(kv_table([
        ("대표전화", "033-562-2551"),
        ("이메일", "이재명 대표 jmlojm@nate.com  /  조혁 이사 siriusjh85@naver.com"),
        ("카카오톡", "pf.kakao.com/_fxjxiQn/chat"),
        ("웹사이트", "https://tourmaker.kr/"),
        ("서류·계약", "S2B·나라장터(G2B) 등록 · 서울보증보험 · 단계별 정산 증빙 지원"),
    ], s))

    def on_first(c, d):
        cover_first(c, d)

    def on_later(c, d):
        header_band(c, d)

    # Two-pass: page 1 uses cover, rest use header.
    # SimpleDocTemplate supports onFirstPage / onLaterPages.
    # Adjust top margin: first page needs space below cover (52mm), later pages 18mm header.
    doc.topMargin = 56 * mm
    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
