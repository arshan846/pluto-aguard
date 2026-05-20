"""Tests for the AI config scanner."""

from pathlib import Path

from pluto_aguard.models import Severity
from pluto_aguard.scanners.ai_config_scanner import scan_ai_configs


class TestAIConfigScanner:
    """Tests for AI framework configuration scanning."""

    def test_detects_eval_on_llm_output(self, tmp_path: Path) -> None:
        code = tmp_path / "agent.py"
        code.write_text("result = eval(response.content)")
        findings = scan_ai_configs(tmp_path)
        assert any(f.severity == Severity.CRITICAL and "eval" in f.title.lower() for f in findings)

    def test_detects_exec_on_llm_output(self, tmp_path: Path) -> None:
        code = tmp_path / "agent.py"
        code.write_text("exec(completion.text)")
        findings = scan_ai_configs(tmp_path)
        assert any("exec" in f.title.lower() for f in findings)

    def test_detects_langchain_verbose(self, tmp_path: Path) -> None:
        code = tmp_path / "chain.py"
        code.write_text("agent = AgentExecutor(tools=tools, verbose=True)")
        findings = scan_ai_configs(tmp_path)
        assert any("verbose" in f.title.lower() for f in findings)

    def test_detects_langchain_dangerous_requests(self, tmp_path: Path) -> None:
        code = tmp_path / "chain.py"
        code.write_text("loader = WebBaseLoader(url, allow_dangerous_requests=True)")
        findings = scan_ai_configs(tmp_path)
        assert any("dangerous" in f.title.lower() for f in findings)

    def test_detects_docker_root(self, tmp_path: Path) -> None:
        dockerfile = tmp_path / "Dockerfile"
        dockerfile.write_text('FROM python:3.12\nCOPY . /app\nCMD ["python", "agent.py"]')
        findings = scan_ai_configs(tmp_path)
        assert any("root" in f.title.lower() for f in findings)

    def test_detects_docker_env_secret(self, tmp_path: Path) -> None:
        dockerfile = tmp_path / "Dockerfile"
        dockerfile.write_text('FROM python:3.12\nENV OPENAI_API_KEY=sk-abc123\nCMD ["python", "agent.py"]')
        findings = scan_ai_configs(tmp_path)
        assert any("secret" in f.title.lower() and "dockerfile" in f.title.lower() for f in findings)

    def test_detects_env_not_gitignored(self, tmp_path: Path) -> None:
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=sk-test123")
        findings = scan_ai_configs(tmp_path)
        assert any("gitignore" in f.title.lower() for f in findings)

    def test_env_gitignored_no_finding(self, tmp_path: Path) -> None:
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=sk-test123")
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text(".env\n")
        findings = scan_ai_configs(tmp_path)
        assert not any("gitignore" in f.title.lower() for f in findings)

    def test_detects_unpinned_ai_deps(self, tmp_path: Path) -> None:
        req = tmp_path / "requirements.txt"
        req.write_text("openai\nlangchain\nflask==2.0.0\n")
        findings = scan_ai_configs(tmp_path)
        assert any("unpinned" in f.title.lower() for f in findings)

    def test_pinned_deps_no_finding(self, tmp_path: Path) -> None:
        req = tmp_path / "requirements.txt"
        req.write_text("openai==1.30.0\nlangchain>=0.2.0\n")
        findings = scan_ai_configs(tmp_path)
        assert not any("unpinned" in f.title.lower() for f in findings)

    def test_clean_project_no_findings(self, tmp_path: Path) -> None:
        code = tmp_path / "app.py"
        code.write_text('print("hello world")')
        findings = scan_ai_configs(tmp_path)
        assert len(findings) == 0
