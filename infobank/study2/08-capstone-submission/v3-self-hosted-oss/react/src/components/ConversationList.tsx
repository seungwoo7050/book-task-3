import { gradeKo } from "../i18n/ko";

type Conversation = {
  id: string;
  created_at: string;
  turn_count: number;
  session_score: number | null;
  session_grade: string | null;
};

type Props = {
  items: Conversation[];
  selectedId: string | null;
  onSelect: (id: string) => void;
};

export function ConversationList({ items, selectedId, onSelect }: Props) {
  return (
    <ul className="conversation-list">
      {items.map((item) => (
        <li
          key={item.id}
          className={selectedId === item.id ? "selected" : ""}
          onClick={() => onSelect(item.id)}
        >
          <div>{item.id.slice(0, 8)}</div>
          <small>
            턴={item.turn_count} 점수={item.session_score ?? "-"} 등급={gradeKo(item.session_grade)}
          </small>
        </li>
      ))}
    </ul>
  );
}
