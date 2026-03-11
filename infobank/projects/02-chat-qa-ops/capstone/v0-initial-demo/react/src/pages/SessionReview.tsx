import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { ConversationList } from "../components/ConversationList";
import { failureTypeKo, gradeKo } from "../i18n/ko";

type Conversation = {
  id: string;
  created_at: string;
  turn_count: number;
  session_score: number | null;
  session_grade: string | null;
};

type Turn = {
  id: string;
  turn_index: number;
  user_message: string;
  assistant_response: string;
  retrieved_doc_ids: string[];
  evaluation: null | {
    id: string;
    grade: string;
    total_score: number;
    failure_types: string[];
  };
};

export function SessionReviewPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);

  useEffect(() => {
    apiGet<{ items: Conversation[] }>("/api/conversations")
      .then((result) => {
        setConversations(result.items);
        if (result.items.length > 0) {
          setSelected(result.items[0].id);
        }
      })
      .catch(() => setConversations([]));
  }, []);

  useEffect(() => {
    if (!selected) return;
    apiGet<{ turns: Turn[] }>(`/api/conversations/${selected}`)
      .then((result) => setTurns(result.turns))
      .catch(() => setTurns([]));
  }, [selected]);

  return (
    <div className="stack">
      <h2>세션 리뷰</h2>
      <div className="split">
        <div className="card sidebar-card">
          <ConversationList items={conversations} selectedId={selected} onSelect={setSelected} />
        </div>
        <div className="card">
          {turns.length === 0 && <p>대화 데이터가 없습니다.</p>}
          {turns.map((turn) => (
            <div key={turn.id} className="chat-turn">
              <div className="bubble user">사용자: {turn.user_message}</div>
              <div className="bubble bot">챗봇: {turn.assistant_response}</div>
              <div className="meta">
                등급={gradeKo(turn.evaluation?.grade)}, 점수={turn.evaluation?.total_score ?? "-"}, 실패유형=
                {(turn.evaluation?.failure_types ?? []).map((code) => failureTypeKo(code)).join(", ") || "-"}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
