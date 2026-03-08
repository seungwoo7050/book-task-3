import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { ConversationList } from "../components/ConversationList";
import { failureTypeKo, gradeKo } from "../i18n/ko";

type Conversation = {
  id: string;
  external_id: string | null;
  created_at: string;
  prompt_version: string;
  kb_version: string;
  run_id: string | null;
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
    lineage: {
      run_label?: string;
      dataset?: string;
      trace_id?: string;
      run_id?: string;
      evaluator_version?: string;
      retrieval_version?: string;
    };
    judge_trace: {
      provider?: string;
      model?: string;
      short_circuit?: boolean;
      short_circuit_reason?: string | null;
      failure_types?: string[];
    };
  };
};

export function SessionReviewPage({ selectedJobId }: { selectedJobId: string | null }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [conversationMeta, setConversationMeta] = useState<Conversation | null>(null);

  useEffect(() => {
    const params = selectedJobId ? `?job_id=${selectedJobId}` : "";
    apiGet<{ items: Conversation[] }>(`/api/conversations${params}`)
      .then((result) => {
        setConversations(result.items);
        if (result.items.length > 0) {
          setSelected(result.items[0].id);
        }
      })
      .catch(() => setConversations([]));
  }, [selectedJobId]);

  useEffect(() => {
    if (!selected) {
      return;
    }
    const params = selectedJobId ? `?job_id=${selectedJobId}` : "";
    apiGet<{ conversation: Conversation; turns: Turn[] }>(`/api/conversations/${selected}${params}`)
      .then((result) => {
        setConversationMeta(result.conversation);
        setTurns(result.turns);
      })
      .catch(() => {
        setConversationMeta(null);
        setTurns([]);
      });
  }, [selected, selectedJobId]);

  return (
    <div className="stack">
      <h2>Session Review</h2>
      <div className="split">
        <div className="card sidebar-card">
          <ConversationList items={conversations} selectedId={selected} onSelect={setSelected} />
        </div>
        <div className="card">
          {conversationMeta && (
            <div className="key-value">
              <span>external={conversationMeta.external_id ?? conversationMeta.id.slice(0, 8)}</span>
              <span>prompt={conversationMeta.prompt_version}</span>
              <span>kb={conversationMeta.kb_version}</span>
              <span>run={conversationMeta.run_id ?? "-"}</span>
              <span>점수={conversationMeta.session_score ?? "-"}</span>
              <span>등급={gradeKo(conversationMeta.session_grade)}</span>
            </div>
          )}
          {turns.length === 0 && <p>선택된 job에 연결된 대화가 없습니다.</p>}
          {turns.map((turn) => (
            <div key={turn.id} className="chat-turn">
              <div className="bubble user">사용자: {turn.user_message}</div>
              <div className="bubble bot">상담 응답: {turn.assistant_response}</div>
              <div className="meta">
                등급={gradeKo(turn.evaluation?.grade)}, 점수={turn.evaluation?.total_score ?? "-"}, 실패유형=
                {(turn.evaluation?.failure_types ?? []).map((code) => failureTypeKo(code)).join(", ") || "-"}
              </div>
              <div className="trace-grid">
                <div className="inset-card">
                  <strong>Retrieved docs</strong>
                  <div>{turn.retrieved_doc_ids.join(", ") || "-"}</div>
                </div>
                <div className="inset-card">
                  <strong>Lineage</strong>
                  <div>run={turn.evaluation?.lineage.run_label ?? "-"}</div>
                  <div>trace={turn.evaluation?.lineage.trace_id ?? "-"}</div>
                  <div>retrieval={turn.evaluation?.lineage.retrieval_version ?? "-"}</div>
                </div>
                <div className="inset-card">
                  <strong>Judge trace</strong>
                  <div>
                    {turn.evaluation?.judge_trace.provider ?? "-"} / {turn.evaluation?.judge_trace.model ?? "-"}
                  </div>
                  <div>short-circuit={String(turn.evaluation?.judge_trace.short_circuit ?? false)}</div>
                  <div>reason={turn.evaluation?.judge_trace.short_circuit_reason ?? "-"}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
