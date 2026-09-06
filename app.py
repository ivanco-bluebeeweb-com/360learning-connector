"""Extension declaration, capabilities, health check for 360Learning Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "360learning-connector",
    version="0.1.0",
    display_name="360Learning",
    icon="icon.svg",
    capabilities=["threesixty_learning:manage"],
    description="Official Imperal connector for 360Learning (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("threesixty_learning_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} 360Learning connection(s) configured." if count else "Not connected yet."
    }
