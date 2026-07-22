# Jason Y. Cho — Portfolio

순수 정적 HTML 사이트입니다. 빌드 과정이 없어서 실패할 것도 없습니다 — push하면 그대로 배포됩니다.

## 배포 (기존 저장소 교체)

1. 저장소의 기존 파일 전부 삭제 후 이 폴더 내용 업로드 (또는 새 저장소).
   - 웹 업로드는 `.github` 폴더를 못 올리므로, `.github/workflows/publish.yml`과
     `.github/workflows/sync-writing.yml` 두 파일은 **Add file → Create new file**로
     경로를 직접 입력해 각각 생성하세요.
2. **Settings → Pages → Source = `GitHub Actions`** 인지 확인 (이미 설정했다면 그대로).
3. push하면 Actions의 "Publish site"가 돌고 → https://jywcho8.github.io/pf/ 완료.

## 블로그 연동 (Writing 자동 동기화)

글은 아무 블로그에서나 쓰세요 (Tistory / Velog / Medium / 네이버 / Substack — RSS만 있으면 됩니다).
이 사이트가 **매일 자동으로** 새 글을 가져와 Writing 페이지에 카드로 추가합니다.

1. `config.json` 열고 RSS 주소만 바꾸면 끝:
   ```json
   { "feeds": [ { "name": "Velog", "url": "https://v2.velog.io/rss/@내아이디" } ] }
   ```
   - Tistory: `https://블로그명.tistory.com/rss`
   - Velog: `https://v2.velog.io/rss/@아이디`
   - Medium: `https://medium.com/feed/@아이디`
   - 네이버: `https://rss.blog.naver.com/아이디.xml`
   - 여러 블로그를 쓰면 feeds 배열에 여러 개 넣으면 됩니다.
2. 바로 반영하고 싶으면: Actions 탭 → "Sync writing from blog" → Run workflow.
   이후엔 매일 오전 10시(시카고)에 자동 실행됩니다.

## 프로젝트 추가

1. `projects/새프로젝트/` 폴더에 `index.html`(기존 것 복사해서 내용 수정)과 대시보드 HTML을 넣고
2. `assets/projects.json`에 항목 하나 추가 (제목·설명·썸네일·링크) — 홈 카드가 자동 생성됩니다.

## 파일 구조

```
├── index.html                  홈 (히어로 + 프로젝트 카드 + 최신 글)
├── writing.html                글 목록 (블로그에서 자동 동기화)
├── projects/pga-elo-rating/    프로젝트 페이지 (대시보드 임베드)
├── assets/
│   ├── site.css / site.js      디자인·렌더링
│   ├── projects.json           프로젝트 목록 (여기만 수정)
│   └── writing.json            글 데이터 (자동 생성 — 손대지 마세요)
├── config.json                 블로그 RSS 주소 (여기만 수정)
└── .github/workflows/          자동 배포 + 자동 글 동기화
```
