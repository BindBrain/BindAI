from pathlib import Path

from reportlab.pdfgen import canvas

from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    PDFLoader,
)


def test_pdf_loader(tmp_path: Path):

    pdf = tmp_path / "notes.pdf"

    c = canvas.Canvas(str(pdf))
    c.drawString(100, 700, "BindAI Framework")
    c.save()

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    count = knowledge.load(
        PDFLoader(str(pdf)),
    )

    assert count == 1

    result = knowledge.search(
        "BindAI",
    )

    assert result.success
    assert len(result.value) == 1