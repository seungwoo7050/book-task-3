import { ReactNode } from "react";

type Props = {
  label: string;
  value: ReactNode;
};

export function ScoreCard({ label, value }: Props) {
  return (
    <div className="card score-card">
      <p className="label">{label}</p>
      <p className="value">{value}</p>
    </div>
  );
}
