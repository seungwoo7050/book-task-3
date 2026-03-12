/**
 * 애플리케이션 진입점.
 *
 * TODO:
 *   1. BookService -> BookController -> BookRouter 인스턴스를 생성한다.
 *   2. constructor로 의존성을 연결한다(수동 DI).
 *   3. router를 "/books"에 mount한다.
 *   4. JSON body parsing middleware를 추가한다.
 *   5. PORT 3000에서 서버를 시작한다.
 */

import express from "express";

const app = express();
const PORT = process.env.PORT || 3000;

// TODO: 의존성을 연결하고 라우트를 mount한다

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

export default app;
