import { failureTypeKo } from "../i18n/ko";

type FailureItem = {
  failure_type: string;
  count: number;
  critical_count?: number;
  avg_score?: number;
};

type Props = {
  items: FailureItem[];
};

export function FailureTable({ items }: Props) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>실패 유형</th>
          <th>건수</th>
          <th>치명 건수</th>
          <th>평균 점수</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.failure_type}>
            <td>{failureTypeKo(item.failure_type)}</td>
            <td>{item.count}</td>
            <td>{item.critical_count ?? 0}</td>
            <td>{item.avg_score ?? "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
