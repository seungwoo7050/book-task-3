from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import typer
from api.main import app as fastapi_app
from chatbot.bot import ChatbotService
from chatbot.retriever import Retriever
from core.config import load_settings
from core.dependency_health import collect_dependency_health, require_llm_strict_dependencies
from core.errors import DependencyUnavailableError
from core.json_utils import loads_json
from db.database import init_db, reset_engines, session_scope
from db.models import Conversation, Evaluation, GoldenSet, Turn
from db.seed import golden_set_count, seed_golden_set, seed_knowledge_base
from evaluator.golden_assertion import evaluate_golden_case, summarize_assertions
from evaluator.pipeline import EvaluationPipeline, serialize_evaluation
from evaluator.pipeline_stats import reset_stats_store
from evaluator.rule_eval import evaluate_rules
from fastapi.testclient import TestClient
from rich.console import Console
from rich.table import Table
from sqlalchemy import select

app = typer.Typer(help="Chat QA Ops CLI")
console = Console()


@app.command("init-db")
def init_db_command() -> None:
    init_db()
    console.print("[green]Database initialized[/green]")


@app.command("seed-demo")
def seed_demo() -> None:
    init_db()
    with session_scope() as session:
        kb_count = seed_knowledge_base(session, Path("backend/knowledge_base"))
        gs_count = seed_golden_set(session, Path("backend/golden_set/phase1_seed.yaml"))
        session.flush()
        total_gs = golden_set_count(session)
    console.print(
        f"[green]Seed completed[/green] kb_upsert={kb_count}, golden_upsert={gs_count}, golden_total={total_gs}"
    )


@app.command("chat")
def chat(message: str, conversation_id: str | None = None) -> None:
    init_db()
    with session_scope() as session:
        convo_id = conversation_id
        if not convo_id:
            convo = Conversation(id=str(uuid.uuid4()), prompt_version="v1.0", kb_version="v1.0")
            session.add(convo)
            session.flush()
            convo_id = convo.id

        max_index = (
            session.scalar(select(Turn.turn_index).where(Turn.conversation_id == convo_id).order_by(Turn.turn_index.desc()))
            or 0
        )

        reply = ChatbotService(session).answer(message)
        turn = Turn(
            id=str(uuid.uuid4()),
            conversation_id=convo_id,
            turn_index=max_index + 1,
            user_message=message,
            assistant_response=reply.assistant_response,
            retrieved_doc_ids=json.dumps(reply.retrieved_doc_ids, ensure_ascii=False),
            latency_ms=reply.latency_ms,
        )
        session.add(turn)
        session.flush()

        console.print(f"[cyan]conversation_id[/cyan]: {convo_id}")
        console.print(f"[cyan]turn_id[/cyan]: {turn.id}")
        console.print(f"[magenta]assistant[/magenta]: {reply.assistant_response}")
        console.print(f"[yellow]retrieved[/yellow]: {reply.retrieved_doc_ids}")


@app.command("index-kb")
def index_kb(path: str = "backend/knowledge_base") -> None:
    init_db()
    with session_scope() as session:
        retriever = Retriever(session)
        count = retriever.index_directory(path)
    console.print(f"[green]indexed[/green]: {count}")


@app.command("check-rules")
def check_rules(response: str, user_message: str = "") -> None:
    results = evaluate_rules(user_message=user_message, assistant_response=response, rules_dir="backend/rules")
    if not results:
        console.print("[green]No rule violations[/green]")
        return

    table = Table(title="Rule Violations")
    table.add_column("rule_id")
    table.add_column("severity")
    table.add_column("failure_type")
    table.add_column("evidence")
    for item in results:
        table.add_row(item.rule_id, item.severity, item.failure_type, item.evidence[:80])
    console.print(table)


@app.command("evaluate")
def evaluate(
    turn: str | None = typer.Option(None, "--turn"),
    conversation: str | None = typer.Option(None, "--conversation"),
    golden_set: bool = typer.Option(False, "--golden-set"),
) -> None:
    init_db()
    assertion_summary: dict[str, object] | None = None
    with session_scope() as session:
        pipeline = EvaluationPipeline(session)
        results = []

        if turn:
            results.append(serialize_evaluation(pipeline.evaluate_turn(turn, allow_cache=False)))
        elif conversation:
            for item in pipeline.evaluate_conversation(conversation):
                results.append(serialize_evaluation(item))
        elif golden_set:
            golden_rows = list(session.scalars(select(GoldenSet).order_by(GoldenSet.id.asc())).all())
            assertions = []
            for row in golden_rows:
                convo = Conversation(id=str(uuid.uuid4()), prompt_version="v1.0", kb_version="v1.0")
                session.add(convo)
                session.flush()

                reply = ChatbotService(session).answer(row.user_message)
                t = Turn(
                    id=str(uuid.uuid4()),
                    conversation_id=convo.id,
                    turn_index=1,
                    user_message=row.user_message,
                    assistant_response=reply.assistant_response,
                    retrieved_doc_ids=json.dumps(reply.retrieved_doc_ids, ensure_ascii=False),
                    latency_ms=reply.latency_ms,
                )
                session.add(t)
                session.flush()
                serialized = serialize_evaluation(pipeline.evaluate_turn(t.id, allow_cache=False))
                assertion = evaluate_golden_case(
                    case_id=row.id,
                    expected_config=loads_json(row.expected_config, {}),
                    evaluation=serialized,
                    retrieved_doc_ids=reply.retrieved_doc_ids,
                )
                serialized["assertion"] = assertion.to_dict()
                results.append(serialized)
                assertions.append(assertion)
            assertion_summary = summarize_assertions(assertions).to_dict()
        else:
            raise typer.BadParameter("하나의 타깃(--turn | --conversation | --golden-set)을 지정해야 합니다.")

    score_sum = 0.0
    for result_item in results:
        raw = result_item.get("total_score")
        if isinstance(raw, int | float):
            score_sum += float(raw)
    avg_score = round(score_sum / len(results), 2) if results else 0.0
    critical = sum(1 for item in results if bool(item["is_critical"]))
    if assertion_summary is None:
        console.print(f"evaluated={len(results)} avg_score={avg_score} critical={critical}")
    else:
        pass_count = assertion_summary.get("pass_count", 0)
        fail_count = assertion_summary.get("fail_count", 0)
        console.print(
            f"evaluated={len(results)} avg_score={avg_score} critical={critical} "
            f"pass_count={pass_count} fail_count={fail_count}"
        )


@app.command("report")
def report(format: str = typer.Option("table", "--format")) -> None:
    with session_scope() as session:
        rows = list(session.scalars(select(Evaluation).order_by(Evaluation.created_at.desc()).limit(200)).all())
        golden_rows = list(session.scalars(select(GoldenSet).order_by(GoldenSet.id.asc())).all())
        assertion_failures: list[dict[str, object]] = []
        for case in golden_rows:
            latest_turn = session.scalar(
                select(Turn)
                .where(Turn.user_message == case.user_message)
                .order_by(Turn.created_at.desc())
                .limit(1)
            )
            if latest_turn is None:
                continue
            latest_eval = session.scalar(
                select(Evaluation).where(Evaluation.turn_id == latest_turn.id).order_by(Evaluation.created_at.desc()).limit(1)
            )
            if latest_eval is None:
                continue
            serialized = serialize_evaluation(latest_eval)
            assertion = evaluate_golden_case(
                case_id=case.id,
                expected_config=loads_json(case.expected_config, {}),
                evaluation=serialized,
                retrieved_doc_ids=loads_json(latest_turn.retrieved_doc_ids, []),
            )
            if not assertion.passed:
                assertion_failures.append(assertion.to_dict())

    if format == "json":
        payload = [
            {
                "id": row.id,
                "grade": row.grade,
                "total_score": row.total_score,
                "failure_types": loads_json(row.failure_types, []),
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
        console.print_json(json.dumps({"evaluations": payload, "assertion_failures": assertion_failures}, ensure_ascii=False))
        return

    table = Table(title="Evaluation Report")
    table.add_column("id")
    table.add_column("grade")
    table.add_column("score")
    table.add_column("failures")
    for row in rows[:20]:
        failures = ",".join(loads_json(row.failure_types, []))
        table.add_row(row.id[:8], row.grade, f"{row.total_score:.2f}", failures[:64])
    console.print(table)

    mismatch_table = Table(title="Golden Assertion Mismatches")
    mismatch_table.add_column("case_id")
    mismatch_table.add_column("reason_codes")
    mismatch_table.add_column("expected_failures")
    mismatch_table.add_column("actual_failures")
    for failure in assertion_failures[:20]:
        expected = failure.get("expected", {})
        actual = failure.get("actual", {})
        expected_failures_raw = expected.get("expected_failure_types", []) if isinstance(expected, dict) else []
        actual_failures_raw = actual.get("failure_types", []) if isinstance(actual, dict) else []
        expected_failures = (
            ",".join(str(code) for code in expected_failures_raw) if isinstance(expected_failures_raw, list) else ""
        )
        actual_failures = (
            ",".join(str(code) for code in actual_failures_raw) if isinstance(actual_failures_raw, list) else ""
        )
        reason_codes_raw = failure.get("reason_codes", [])
        reason_codes = ",".join(str(code) for code in reason_codes_raw) if isinstance(reason_codes_raw, list) else "-"
        mismatch_table.add_row(
            str(failure.get("case_id", "-")),
            reason_codes,
            expected_failures or "-",
            actual_failures or "-",
        )
    if assertion_failures:
        console.print(mismatch_table)
    else:
        console.print("[green]Golden assertion mismatches: none[/green]")


@app.command("compare")
def compare(baseline: str, candidate: str) -> None:
    with session_scope() as session:
        base_rows = list(session.scalars(select(Evaluation).where(Evaluation.prompt_version == baseline)).all())
        cand_rows = list(session.scalars(select(Evaluation).where(Evaluation.prompt_version == candidate)).all())

    def _avg(rows: list[Evaluation]) -> float:
        return round(sum(item.total_score for item in rows) / len(rows), 2) if rows else 0.0

    base_avg = _avg(base_rows)
    cand_avg = _avg(cand_rows)

    table = Table(title="Version Compare")
    table.add_column("metric")
    table.add_column("baseline")
    table.add_column("candidate")
    table.add_column("delta")
    table.add_row("avg_score", str(base_avg), str(cand_avg), str(round(cand_avg - base_avg, 2)))
    table.add_row(
        "critical_count",
        str(sum(1 for item in base_rows if item.is_critical)),
        str(sum(1 for item in cand_rows if item.is_critical)),
        "-",
    )
    console.print(table)


@app.command("preflight")
def preflight() -> None:
    try:
        health = collect_dependency_health(load_settings())
        console.print_json(json.dumps(health.to_dict(), ensure_ascii=False))
        require_llm_strict_dependencies(health)
        console.print("[green]preflight passed[/green]")
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    except DependencyUnavailableError as exc:
        console.print_json(json.dumps(exc.to_dict(), ensure_ascii=False))
        raise typer.Exit(code=1) from exc


def _configure_demo_mode(mode: str) -> None:
    os.environ["QUALBOT_EVAL_MODE"] = mode
    if mode == "llm":
        os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
        os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
        os.environ["QUALBOT_ENABLE_CHROMA"] = "1"
    else:
        os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "keyword"
        os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
        os.environ["QUALBOT_ENABLE_CHROMA"] = "0"


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


@app.command("demo-proof")
def demo_proof(
    mode: str = typer.Option("llm", "--mode"),
    limit: int = typer.Option(30, "--limit"),
) -> None:
    if mode not in {"llm", "heuristic"}:
        raise typer.BadParameter("--mode must be one of [llm, heuristic]")

    artifact_dir = Path("docs/demo/proof-artifacts")
    artifact_dir.mkdir(parents=True, exist_ok=True)

    _configure_demo_mode(mode)
    reset_stats_store()
    reset_engines()
    init_db()
    with session_scope() as session:
        seed_knowledge_base(session, Path("backend/knowledge_base"))
        seed_golden_set(session, Path("backend/golden_set/phase1_seed.yaml"))

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    (artifact_dir / "run-timestamp.txt").write_text(timestamp + "\n", encoding="utf-8")

    try:
        health = collect_dependency_health(load_settings())
        require_llm_strict_dependencies(health)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    except DependencyUnavailableError as exc:
        _write_json(artifact_dir / "api-dependency-health.json", exc.to_dict())
        if mode == "llm":
            console.print_json(json.dumps(exc.to_dict(), ensure_ascii=False))
            raise typer.Exit(code=1) from exc
        health = collect_dependency_health(load_settings())

    _write_json(artifact_dir / "api-dependency-health.json", health.to_dict())

    with TestClient(fastapi_app) as client:
        console.print(f"running golden-set proof mode={mode} limit={limit}")
        golden_resp = client.post(
            "/api/golden-set/run",
            json={"prompt_version": "v1.6", "kb_version": "v1.6", "limit": limit},
        )
        try:
            golden_payload: object = golden_resp.json()
        except Exception:  # noqa: BLE001
            golden_payload = {"raw": golden_resp.text}
        _write_json(artifact_dir / "api-golden-run.json", golden_payload)

        overview_resp = client.get("/api/dashboard/overview")
        _write_json(artifact_dir / "api-overview.json", overview_resp.json())

        failures_resp = client.get("/api/dashboard/failures")
        _write_json(artifact_dir / "api-failures.json", failures_resp.json())

        pipeline_stats_resp = client.get("/api/system/pipeline-stats")
        _write_json(artifact_dir / "api-pipeline-stats.json", pipeline_stats_resp.json())

    if isinstance(golden_payload, dict):
        evaluated = int(golden_payload.get("count", 0))
        avg_score = float(golden_payload.get("avg_score", 0.0))
        critical = int(golden_payload.get("critical_count", 0))
        pass_count = int(golden_payload.get("pass_count", 0))
        fail_count = int(golden_payload.get("fail_count", 0))
        summary_line = (
            f"evaluated={evaluated} avg_score={avg_score:.2f} critical={critical} "
            f"pass_count={pass_count} fail_count={fail_count}\n"
        )
    else:
        summary_line = "evaluated=0 avg_score=0.00 critical=0 pass_count=0 fail_count=0\n"
    (artifact_dir / "cli-evaluate-golden.txt").write_text(summary_line, encoding="utf-8")

    with session_scope() as session:
        rows = list(session.scalars(select(Evaluation).order_by(Evaluation.created_at.desc()).limit(20)).all())
    report_lines = ["Evaluation Report (latest 20)\n"]
    for row in rows:
        failures = ",".join(loads_json(row.failure_types, []))
        report_lines.append(f"{row.id[:8]} grade={row.grade} score={row.total_score:.2f} failures={failures}\n")
    (artifact_dir / "cli-report.txt").write_text("".join(report_lines), encoding="utf-8")

    if mode == "llm" and golden_resp.status_code != 200:
        console.print_json(json.dumps(golden_payload, ensure_ascii=False))
        raise typer.Exit(code=1)

    console.print(f"[green]demo proof artifacts written[/green]: {artifact_dir}")


if __name__ == "__main__":
    app()
