# -*- coding: utf-8 -*-
"""홈 '이번 주 추천 퍼즐'에 쓸 가벼운 목록(home_picks.js) 생성. data.js(약 875KB)를 홈에서 불러오지 않도록 한다.
data.js 를 고친 뒤에는 이 스크립트를 다시 실행한다: python3 gen_home_picks.py (node 필요)"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
JS = r'''
const fs=require("fs"),vm=require("vm");
const s=fs.readFileSync("data.js","utf8");const ctx={};vm.createContext(ctx);
vm.runInContext(s+";this.Q=QUIZ_DATABASE;this.F=getWordPoolSizeForQuiz",ctx);
const out=[];for(const id of Object.keys(ctx.Q)){if(ctx.F(id)>=50)out.push([id,ctx.Q[id].title||id]);}
console.log(JSON.stringify(out));
'''
r = subprocess.run(["node", "-e", JS], cwd=ROOT, capture_output=True, text=True, check=True)
picks = json.loads(r.stdout)
open(os.path.join(ROOT, "home_picks.js"), "w", encoding="utf-8").write(
    "window.HOME_PICKS=" + json.dumps(picks, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(f"home_picks.js: {len(picks)}개")
