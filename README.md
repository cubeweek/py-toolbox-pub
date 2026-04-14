<img src="resources/imgs/py-toolbox-README.jpg" style="max-width: 100%; height: auto;"><br>
일상적인 반복 작업을 자동화하기 위한 스크립트 모음 레포입니다.<br>
각 스크립트는 독립적으로 실행 가능합니다.

## 🚀 Tool List
<small>

| 카테고리                 | 스크립트 명                                              | 주요 기능 | 핵심 lib                                                            | 비고 |
|:---------------------|:----------------------------------------------------| :--- |:------------------------------------------------------------------| :--- |
| - 이미지 프로세싱           | [`make_reward_chart.py`](/src/make_reward_chart.py) | A4 가로 사이즈의 번호 기반 칭찬 스티커 판(Grid) 생성 | `Pillow (PIL)`<br>`Matplotlib`                                        | - |
| - 웹 크롤링<br>- 자동화 테스트 | [`autotest_backjoon.py`](src/autotest_backjoon.py)  | 백준 예제 문제를 크롤링하여 로컬 JAR 파일과 자동 비교 테스트 | `Selenium`<br>`Webdriver-manager`<br>`BeautifulSoup4`<br>`Subprocess` | **Chrome 필요** |
| - API 연동<br>- 파일 시스템 | [`move_by_tier.py`](src/move_by_tier.py)            | solved.ac API 연동을 통해 백준/LeetCode 소스코드를 난이도별 폴더로 자동 분류 | `Requests`<br>`Pathlib`<br>`Urllib`<br>`JSON`<br>`Shutil`                 | - |
| - 텍스트 파싱<br>- 문서 자동화 | [`update_readme.py`](src/update_readme.py)                              | 문제 풀이 현황을 분석하여 README.md의 문제 리스트(티어별) 자동 갱신 | `Regular Expression (re)`<br>`JSON`<br>`Collections`<br>`Pathlib`       | - |
</small>
## 🛠 Installation & Setup
### 파이썬 가상환경 설치
```bash
# 가상환경 설치
python -m venv .venv

# 가상환경 활성화
source .venv/bin/activate # Mac/Linux
# .venv\Scripts\activate # Windows
```

### 필요 라이브러리 설치
```bash
pip install -r config/requirements.txt
```

## 📂 Project Structure

```text
.
├── config/                 # 환경설정 관련 파일
├── scripts/                # 실행 가능한 독립 스크립트 (.py)
├── resources/              # 스크립트 실행에 필요한 리소스
│   ├── imgs/               # 이미지 파일 (apple.png 등)
│   ├── etc/                # 폰트 및 기타 설정 파일
│   └── fonts_license/      # 사용된 오픈 폰트의 라이선스 고지
├── output/                 # 스크립트 결과물 저장 폴더
└── README.md
```

## ⚖️ License & Open Source
- **Fonts:**
    - 본 프로젝트는 [Pretendard](https://github.com/orioncactus/pretendard) 폰트를 사용하였습니다. ([`라이선스 전문`](/guide/LICENSE_FONT.txt))
