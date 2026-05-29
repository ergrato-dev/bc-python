"""
Studio BC — Week 15 Project Demo
Run this after implementing src/models.py and src/validators.py
"""

from __future__ import annotations

from datetime import date, datetime

from src.models import Asset, Client, Deliverable, Phase, Project
from src.validators import is_active_project, is_image_asset, is_uploadable, is_video_asset


def main() -> None:
    print("=" * 55)
    print("  Studio BC — Domain Models Demo")
    print("=" * 55)

    # --- Clients ---
    client = Client(
        name="Acme Corp",
        email="  Contact@ACME.com  ",
        id=1,
    )
    print(f"\nClient: {client.name} <{client.email}>")

    # --- Project ---
    project = Project(
        name="Campaña Navidad 2026",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 12, 31),
        budget=75_000.0,
        id=1,
        client_id=client.id,
    )
    print(f"Project: {project.name} (slug: {project.slug})")
    print(f"  Budget: ${project.budget:,.0f}")
    print(f"  Duration: {(project.end_date - project.start_date).days} days")

    # --- Phases ---
    phases = [
        Phase("Pre-producción", order=1, id=1, project_id=project.id),
        Phase("Producción", order=2, id=2, project_id=project.id),
        Phase("Post-producción", order=3, id=3, project_id=project.id),
        Phase("Entrega", order=4, id=4, project_id=project.id),
    ]
    print(f"\nPhases ({len(phases)}):")
    for p in phases:
        print(f"  {p.order}. {p.name}")

    # --- Assets ---
    assets = [
        Asset("video_hero.mp4", "video", id=1, file_path="/media/hero.mp4", size_mb=1024.0),
        Asset("thumbnail.png", "image", id=2, file_path="/media/thumb.png", size_mb=0.5),
        Asset("jingle.mp3", "audio", id=3, file_path="/media/jingle.mp3", size_mb=8.2),
        Asset("brief.pdf", "document", id=4, file_path="", size_mb=0.1),  # no file_path
    ]

    print(f"\nAssets ({len(assets)}):")
    for a in assets:
        print(f"  [{a.asset_type}] {a.name} ({a.size_mb} MB)")

    # --- TypeGuard in action ---
    print("\n--- TypeGuard ---")
    videos = [a for a in assets if is_video_asset(a)]
    images = [a for a in assets if is_image_asset(a)]
    uploadable = [a for a in assets if is_uploadable(a)]

    print(f"Videos:     {[a.name for a in videos]}")
    print(f"Images:     {[a.name for a in images]}")
    print(f"Uploadable: {[a.name for a in uploadable]}")

    # --- Active projects ---
    mixed: list[object] = [project, "not a project", 42, client]
    active = [obj for obj in mixed if is_active_project(obj)]
    print(f"\nActive projects: {len(active)}")

    print("\n✅ All models working correctly!")


if __name__ == "__main__":
    main()
