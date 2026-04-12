<div align="center">

# 📡 NodCast

**Automated deeptech & semiconductor news bot — scans, summarizes, and posts to X twice a day.**

[![version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)](https://github.com/YMJ-02/DeepTech_Scanner)
[![python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![scheduler](https://img.shields.io/badge/scheduler-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/YMJ-02/DeepTech_Scanner/actions)
[![AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

</div>

---

NodCast monitors RSS feeds from major deeptech and semiconductor news outlets, filters for relevant signals, and uses Gemini AI to generate dry, factual X (Twitter) posts — automatically, twice a day.

No server required. Runs entirely on GitHub Actions.

---

## How It Works

```
RSS Feeds (Tom's Hardware, Wccftech, TechCrunch, VentureBeat)
  ↓
  Parallel scraping + og:image extraction
  ↓
  Keyword filtering (chip, TSMC, GPU, AI, fab, node ...)
  ↓
  Gemini 2.5 Flash — summarize & format as X post (≤280 chars)
  ↓
  Image processing (16:9 crop for Twitter card)
  ↓
  Post to X — 8:00 AM & 5:00 PM EST daily
```

---

## Project Structure

```
NodCast/
├── src/
│   ├── main.py             # Orchestrator — runs the full pipeline
│   ├── scraper.py          # Parallel RSS fetcher + image extractor
│   ├── ai_translator.py    # Gemini API — summarize & format post
│   ├── image_maker.py      # Image download & 16:9 crop for Twitter
│   └── sns_uploader.py     # X (Twitter) uploader via Tweepy v2
├── data/
│   ├── posted_urls.txt     # Duplicate prevention (cached across runs)
│   └── raw_articles_*.json # Scraped article snapshots (auto-cleaned, 7d)
├── assets/                 # Processed tweet images (runtime)
├── .github/
│   └── workflows/
│       └── twitter_bot.yml # GitHub Actions schedule (8AM / 5PM EST)
├── requirements.txt
└── setup_project.py
```

---

## Setup

### Requirements

- Python 3.12 or later
- A [Google AI Studio](https://aistudio.google.com/) API key (Gemini)
- A [Twitter Developer](https://developer.twitter.com/) app with **Read and Write** permissions

### 1. Clone the repository

```bash
git clone https://github.com/YMJ-02/DeepTech_Scanner.git
cd DeepTech_Scanner
pip install -r requirements.txt
```

### 2. Configure environment variables

Create `config/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here

TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### 3. Register GitHub Secrets

For automated runs via GitHub Actions, register the same keys under:

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

| Secret Name | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `TWITTER_API_KEY` | Twitter app consumer key |
| `TWITTER_API_SECRET` | Twitter app consumer secret |
| `TWITTER_ACCESS_TOKEN` | Twitter OAuth access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter OAuth access token secret |

### 4. Run manually (optional)

```bash
python src/main.py
```

---

## Scheduling

NodCast runs automatically via GitHub Actions cron — no server needed.

| Run | UTC | EST |
|---|---|---|
| Morning | 13:00 | 8:00 AM |
| Evening | 22:00 | 5:00 PM |

You can also trigger a run manually anytime from the **Actions** tab → `DeepTech Scanner Bot` → `Run workflow`.

---

## Keyword Filter

NodCast prioritizes articles containing any of the following terms:

`chip` `semiconductor` `wafer` `tsmc` `nvidia` `intel` `amd` `arm` `qualcomm` `samsung` `foundry` `gpu` `ai` `cpu` `fab` `node`

If no matching article is found in the current batch, it falls back to the most recent unposted article.

---

## Duplicate Prevention

Posted article URLs are stored in `data/posted_urls.txt` and persisted across GitHub Actions runs via `actions/cache`. A URL is only written to the file after a successful upload — failed posts are automatically retried on the next run.

---

## Developer

| Item | Detail |
|---|---|
| GitHub | [@YMJ-02](https://github.com/YMJ-02) |
| Repository | https://github.com/YMJ-02/DeepTech_Scanner |

---

## Bug Reports

Open an issue at https://github.com/YMJ-02/DeepTech_Scanner/issues.

Include:
- OS and Python version
- Full error traceback from terminal or GitHub Actions log
- Which step failed (scrape / AI / image / upload)

---

## References

- [Tweepy](https://www.tweepy.org/) — Twitter API v2 client
- [Google Generative AI (Gemini)](https://ai.google.dev/) — Post summarization
- [feedparser](https://feedparser.readthedocs.io/) — RSS feed parsing
- [Pillow](https://python-pillow.org/) — Image processing
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — og:image extraction

---

## Version History

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-04 | Initial release. Parallel scraping, Gemini AI, X auto-posting via GitHub Actions. |

---

<div align="center">

# 📡 NodCast (한국어)

**딥테크 · 반도체 뉴스를 자동으로 스캔하고, AI가 요약해서 X(트위터)에 하루 두 번 올려주는 봇.**

</div>

---

서버 없이 GitHub Actions만으로 작동합니다. RSS 피드에서 최신 기사를 수집하고, Gemini AI가 트위터 형식에 맞게 요약한 뒤 자동으로 포스팅합니다.

---

## 작동 방식

```
RSS 피드 (Tom's Hardware, Wccftech, TechCrunch, VentureBeat)
  ↓
  병렬 스크래핑 + og:image 추출
  ↓
  키워드 필터링 (chip, TSMC, GPU, AI, fab, node ...)
  ↓
  Gemini 2.5 Flash — X 포스트 형식으로 요약 (280자 이하)
  ↓
  이미지 처리 (16:9 크롭, Twitter 카드 최적화)
  ↓
  X에 포스팅 — 매일 오전 8시 / 오후 5시 (EST)
```

---

## 프로젝트 구성

```
NodCast/
├── src/
│   ├── main.py             # 오케스트레이터 — 전체 파이프라인 실행
│   ├── scraper.py          # 병렬 RSS 수집 + 이미지 추출
│   ├── ai_translator.py    # Gemini API — 요약 및 포맷
│   ├── image_maker.py      # 이미지 다운로드 및 16:9 크롭
│   └── sns_uploader.py     # Tweepy v2로 X 업로드
├── data/
│   ├── posted_urls.txt     # 중복 방지용 URL 목록 (캐시로 유지)
│   └── raw_articles_*.json # 수집된 기사 스냅샷 (7일 후 자동 삭제)
├── assets/                 # 처리된 트윗 이미지 (실행 시 생성)
├── .github/
│   └── workflows/
│       └── twitter_bot.yml # GitHub Actions 스케줄 (오전 8시 / 오후 5시 EST)
├── requirements.txt
└── setup_project.py
```

---

## 설치 방법

### 요구 사항

- Python 3.12 이상
- [Google AI Studio](https://aistudio.google.com/) API 키 (Gemini)
- **읽기 + 쓰기** 권한이 있는 [Twitter Developer](https://developer.twitter.com/) 앱

### 1. 저장소 클론

```bash
git clone https://github.com/YMJ-02/DeepTech_Scanner.git
cd DeepTech_Scanner
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`config/.env` 파일 생성:

```env
GEMINI_API_KEY=your_gemini_api_key_here

TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### 3. GitHub Secrets 등록

GitHub Actions 자동 실행을 위해 동일한 키를 등록:

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

| Secret 이름 | 설명 |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API 키 |
| `TWITTER_API_KEY` | Twitter 앱 consumer key |
| `TWITTER_API_SECRET` | Twitter 앱 consumer secret |
| `TWITTER_ACCESS_TOKEN` | Twitter OAuth access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter OAuth access token secret |

### 4. 수동 실행 (선택)

```bash
python src/main.py
```

---

## 실행 스케줄

| 실행 | UTC | EST |
|---|---|---|
| 오전 | 13:00 | 오전 8:00 |
| 오후 | 22:00 | 오후 5:00 |

**Actions** 탭 → `DeepTech Scanner Bot` → `Run workflow`로 언제든 수동 실행도 가능합니다.

---

## 중복 방지

포스팅된 기사 URL은 `data/posted_urls.txt`에 저장되며 `actions/cache`로 실행 간에 유지됩니다. URL은 업로드 성공 후에만 기록되므로, 실패한 포스트는 다음 실행에서 자동으로 재시도됩니다.

---

## 버그 신고

https://github.com/YMJ-02/DeepTech_Scanner/issues 에서 이슈 등록.

아래 정보를 포함해주세요:
- OS 및 Python 버전
- 터미널 또는 GitHub Actions 로그 전체 에러 트레이스백
- 어떤 단계에서 실패했는지 (수집 / AI / 이미지 / 업로드)

---

## 참고

- [Tweepy](https://www.tweepy.org/) — Twitter API v2 클라이언트
- [Google Generative AI (Gemini)](https://ai.google.dev/) — 포스트 요약 AI
- [feedparser](https://feedparser.readthedocs.io/) — RSS 파싱
- [Pillow](https://python-pillow.org/) — 이미지 처리
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — og:image 추출

---

## 버전 히스토리

| 버전 | 날짜 | 내용 |
|---|---|---|
| 1.0.0 | 2026-04 | 최초 릴리즈. 병렬 스크래핑, Gemini AI 요약, GitHub Actions 자동 포스팅. |
