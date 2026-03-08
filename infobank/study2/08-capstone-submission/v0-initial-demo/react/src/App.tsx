import { Link, Route, Routes } from "react-router-dom";
import { EvalRunnerPage } from "./pages/EvalRunner";
import { FailuresPage } from "./pages/Failures";
import { OverviewPage } from "./pages/Overview";
import { SessionReviewPage } from "./pages/SessionReview";

export function App() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>상담 품질 운영</h1>
        <nav>
          <Link to="/">개요</Link>
          <Link to="/failures">실패 분석</Link>
          <Link to="/sessions">세션 리뷰</Link>
          <Link to="/runner">평가 실행</Link>
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/failures" element={<FailuresPage />} />
          <Route path="/sessions" element={<SessionReviewPage />} />
          <Route path="/runner" element={<EvalRunnerPage />} />
        </Routes>
      </main>
    </div>
  );
}
