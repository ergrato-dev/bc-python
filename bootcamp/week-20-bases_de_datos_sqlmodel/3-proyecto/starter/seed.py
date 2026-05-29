"""Poblar la DB con datos de prueba de Studio BC."""
from __future__ import annotations

from sqlmodel import Session
from src.database import engine, create_db_and_tables
from src.models import Client, Project, Asset, Tag

def seed() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        # Clientes
        c1 = Client(name="Canal 9 Argentina", email="prod@canal9.com", country="AR")
        c2 = Client(name="Canal 7 Bariloche", email="hola@canal7.com", country="AR")
        c3 = Client(name="Agencia Norte", email="info@norte.com", country="AR")
        session.add_all([c1, c2, c3])
        session.flush()

        # Proyectos
        p1 = Project(name="Spot Verano 2025", client_id=c1.id, budget=5000)
        p2 = Project(name="Reel Institucional", client_id=c1.id, budget=12000)
        p3 = Project(name="Documental Patagonia", client_id=c2.id, budget=35000)
        p4 = Project(name="Jingle Navidad", client_id=c3.id, budget=8000)
        p5 = Project(name="Campaña Digital", client_id=c3.id, budget=4500, status="draft")
        session.add_all([p1, p2, p3, p4, p5])
        session.flush()

        # Assets
        assets = [
            Asset(name="intro.mp4", type="video", size_mb=450, project_id=p1.id),
            Asset(name="main-spot.mp4", type="video", size_mb=2100, project_id=p1.id),
            Asset(name="jingle.mp3", type="audio", size_mb=8, project_id=p1.id),
            Asset(name="reel-v1.mp4", type="video", size_mb=800, project_id=p2.id),
            Asset(name="entrevista.mp4", type="video", size_mb=3200, project_id=p3.id),
            Asset(name="paisajes.mp4", type="video", size_mb=15000, project_id=p3.id),
            Asset(name="mapa-animado.mp4", type="video", size_mb=250, project_id=p3.id),
            Asset(name="jingle-nav.mp3", type="audio", size_mb=5, project_id=p4.id),
            Asset(name="banner-1080.png", type="image", size_mb=2, project_id=p5.id),
            Asset(name="banner-story.png", type="image", size_mb=1.5, project_id=p5.id),
        ]
        session.add_all(assets)
        session.flush()

        # Tags
        tags = {name: Tag(name=name) for name in ["hd", "4k", "color-graded", "raw", "final"]}
        session.add_all(tags.values())
        session.flush()

        # Asociar tags
        assets[0].tags = [tags["hd"], tags["final"]]
        assets[1].tags = [tags["4k"], tags["color-graded"], tags["final"]]
        assets[4].tags = [tags["raw"]]
        assets[5].tags = [tags["4k"], tags["raw"]]

        session.commit()
        print(f"Seed completado: {len(assets)} assets, 5 proyectos, 3 clientes")


if __name__ == "__main__":
    seed()
