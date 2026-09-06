"""Resource handlers for 360Learning Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListCourseParams, GetCourseParams,
    CourseRecord, CourseList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_courses", "List courses in 360Learning.", action_type="read", chain_callable=True, event="360learning-connector.list_courses", effects=["read:courses"], data_model=CourseList)
async def list_courses(params: ListCourseParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_courses(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.ok({"courses": items, "total": len(items)}, summary=f"Found {len(items)} courses.")
    except Exception as e:
        return ActionResult.error(f"Error listing courses: {e}")

@chat.function("get_course", "Get details of one Course in 360Learning.", action_type="read", chain_callable=True, event="360learning-connector.get_course", effects=["read:course"], data_model=CourseRecord)
async def get_course(params: GetCourseParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_course(params.course_id)
        rid = str(r.get("id") or params.course_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.ok({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved Course {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Course: {e}")

@chat.function("audit_course_health", "Audit health of 360Learning courses and connectivity.", action_type="read", chain_callable=True, event="360learning-connector.audit_course_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_course_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_courses(limit=50)
        return ActionResult.ok({
            "healthy": True,
            "total_courses": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"360Learning healthy. Sampled {len(items)} courses."
        }, summary=f"360Learning health check passed with {len(items)} courses.")
    except Exception as e:
        return ActionResult.error(f"Error auditing 360Learning health: {e}")
