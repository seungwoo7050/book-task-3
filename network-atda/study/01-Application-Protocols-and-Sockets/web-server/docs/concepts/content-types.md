# MIME Types와 Content-Type 헤더

## 개요

MIME(Multipurpose Internet Mail Extensions) 타입은 인터넷에서 전송되는 데이터의 종류를 식별하는 표준 레이블이다. HTTP에서 `Content-Type` 헤더는 응답 본문의 미디어 유형을 클라이언트에 알려주어, 브라우저가 데이터를 올바르게 렌더링하거나 처리할 수 있도록 한다.

> **참고**: MIME 타입은 원래 이메일 첨부 파일을 위해 설계되었지만(RFC 2045–2049), HTTP에서도 동일한 체계를 사용한다(RFC 7231 §3.1.1.5).

## MIME 타입 형식

```
type/subtype
```

- **type**: 대분류 (예: `text`, `image`, `application`, `audio`, `video`)
- **subtype**: 세부 형식 (예: `html`, `png`, `json`)

### 예시

| MIME Type | 설명 |
| :--- | :--- |
| `text/html` | HTML 문서 |
| `text/plain` | 일반 텍스트 |
| `text/css` | CSS 스타일시트 |
| `application/javascript` | JavaScript 코드 |
| `application/json` | JSON 데이터 |
| `application/octet-stream` | 임의의 바이너리 데이터 (기본값) |
| `image/png` | PNG 이미지 |
| `image/jpeg` | JPEG 이미지 |
| `image/gif` | GIF 이미지 |
| `image/x-icon` | 파비콘 (ICO) |

## 파일 확장자 → MIME 매핑

웹 서버는 요청된 파일의 **확장자**를 보고 적절한 `Content-Type`을 결정한다:

```python
import os

CONTENT_TYPES = {
    ".html": "text/html",
    ".htm":  "text/html",
    ".css":  "text/css",
    ".js":   "application/javascript",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".ico":  "image/x-icon",
    ".txt":  "text/plain",
}

def get_content_type(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return CONTENT_TYPES.get(ext.lower(), "application/octet-stream")
```

확장자가 매핑에 없는 경우 `application/octet-stream`을 기본값으로 사용한다. 이 타입은 "알 수 없는 바이너리 데이터"를 의미하며, 브라우저는 일반적으로 파일 다운로드를 제안한다.

## Content-Type이 중요한 이유

### 1. 브라우저 렌더링 결정

| Content-Type 설정 | 브라우저 동작 |
| :--- | :--- |
| `text/html` | HTML로 파싱하여 페이지 렌더링 |
| `text/plain` | 원본 텍스트 그대로 표시 |
| `image/png` | 이미지로 디코딩하여 표시 |
| `application/octet-stream` | 파일 다운로드 대화상자 표시 |

### 2. 보안

잘못된 `Content-Type` 설정은 보안 취약점을 야기할 수 있다:
- `text/html`로 설정된 사용자 업로드 파일이 XSS 공격의 매개체가 될 수 있음
- 일부 구형 브라우저는 `Content-Type`을 무시하고 내용을 "스니핑"하여 자체 판단하기도 함

## Content-Length 헤더

`Content-Type`과 함께 `Content-Length` 헤더도 중요하다:

```
Content-Length: 153
```

- 응답 본문의 **바이트 수**를 명시
- 클라이언트가 데이터 수신 완료 시점을 판단하는 데 사용
- HTTP/1.1에서는 `Content-Length` 또는 `Transfer-Encoding: chunked` 중 하나를 사용해야 함

## Python 표준 라이브러리의 mimetypes 모듈

과제에서는 수동 매핑을 사용하지만, Python 표준 라이브러리에는 `mimetypes` 모듈이 있다:

```python
import mimetypes

content_type, _ = mimetypes.guess_type("hello.html")
# content_type → "text/html"
```

이 모듈은 운영체제의 MIME 데이터베이스를 활용하여 약 500개 이상의 확장자를 지원한다.  
단, 이 과제에서는 학습 목적으로 직접 매핑 딕셔너리를 구현한다.

## 참고 자료

- [RFC 7231 §3.1.1.5 — Content-Type](https://www.rfc-editor.org/rfc/rfc7231#section-3.1.1.5)
- [MDN Web Docs — MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- Kurose & Ross, *Computer Networking: A Top-Down Approach* — Chapter 2 (Application Layer)
