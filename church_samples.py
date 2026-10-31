# -*- coding: utf-8 -*-
"""'교회 이름 넣기' 예시 카드 블록(새해 카드 갤러리·송구영신 가이드·새해 말씀 뽑기 페이지 공용).
이미지는 tools/gen_church_samples.js 로 만든다(○○교회 청년부 예시)."""


def church_sample_block():
    figs = "".join(
        f'<a href="/images/cards/church-sample-{i}.jpg" style="display:block;border-radius:12px;overflow:hidden;border:1px solid #d6e4f7;background:#e9eef5" data-ga="church_sample_click" data-ga-label="{i}">'
        f'<img src="/images/cards/church-sample-{i}_t.jpg" width="360" height="450" loading="lazy" alt="새해 말씀 카드 아래에 교회 이름(○○교회 청년부)을 넣은 예시 {i}" style="display:block;width:100%;height:auto"></a>'
        for i in (1, 2, 3))
    return ('<h2>우리 교회 이름을 넣은 새해 말씀 카드 (예시)</h2>'
            '<p style="max-width:780px">새해 말씀 카드 아래에 <b>교회·모임 이름</b>을 넣어 저장하고 인쇄할 수 있습니다. 아래는 "○○교회 청년부"를 넣은 예시입니다. '
            '이름을 입력해 카드 위에서 미리 보는 것은 누구나 할 수 있고, 저장·인쇄·여러 장 인쇄에 넣는 것은 후원 기능입니다.</p>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;max-width:780px;margin:12px 0">{figs}</div>'
            '<p style="max-width:780px"><a href="/verse/" data-ga="church_sample_to_studio" style="font-weight:700">✍️ 내 교회 이름으로 미리 보기 →</a> '
            '(더보기 탭 → 교회 이름 넣기) · <a href="/support.html" data-ga="church_sample_to_support" style="font-weight:700">후원 안내 →</a></p>')
