# -*- coding: utf-8 -*-
"""교회 종소리 합성(음원 없이 수식으로 생성 → 라이선스 문제 없음). 사용: python3 tools/gen_church_bell.py
출력: quiet/church_bell.m4a (afconvert 필요, macOS)"""
import math
import os
import random
import struct
import subprocess
import wave

SR = 32000
DUR = 7.0
F0 = 392.0  # 소리의 기준음(프라임) G4
# (주파수 비율, 세기, 감쇠 시간(초)) — 교회 종의 대표 부분음(허밍·프라임·테르츠·퀸트·노미널 등)
PARTIALS = [(0.5, 0.55, 6.5), (1.0, 1.0, 5.5), (1.183, 0.6, 3.6), (1.506, 0.5, 3.2), (2.0, 0.55, 3.0),
            (2.514, 0.28, 2.0), (2.662, 0.25, 1.9), (3.011, 0.18, 1.5), (4.166, 0.1, 1.0)]


def main():
    random.seed(7)
    n = int(SR * DUR)
    out = [0.0] * n
    for ratio, amp, dec in PARTIALS:
        for det in (-0.35, 0.35):  # 아주 작은 어긋남으로 은은한 울림(맥놀이)
            f = F0 * ratio + det
            ph = random.random() * 6.283
            for i in range(n):
                t = i / SR
                out[i] += amp * 0.5 * math.sin(6.283185 * f * t + ph) * math.exp(-t / dec)
    # 타격음: 짧은 잡음
    prev = 0.0
    for i in range(int(SR * 0.03)):
        t = i / SR
        x = random.uniform(-1, 1)
        prev = prev * 0.85 + x * 0.15
        out[i] += prev * 0.35 * math.exp(-t / 0.008)
    for i in range(int(SR * 0.005)):  # 시작 클릭 방지
        out[i] *= i / (SR * 0.005)
    for i in range(int(SR * 0.6)):  # 끝 페이드
        out[n - 1 - i] *= i / (SR * 0.6)
    pk = max(abs(x) for x in out) or 1
    wav = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_bell.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x / pk * 0.85)) * 32767)) for x in out))
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "quiet", "church_bell.m4a")
    subprocess.run(["afconvert", wav, dst, "-f", "m4af", "-d", "aac", "-b", "64000"], check=True)
    os.remove(wav)
    print("종소리 생성:", os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
