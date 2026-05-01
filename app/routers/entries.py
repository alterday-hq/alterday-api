from datetime import date as Date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.database import supabase
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/days", tags=["entries"])


class EntryOut(BaseModel):
    id: str
    activity_id: str | None
    name: str | None
    category: str
    duration_minutes: int
    start_time: str | None
    satisfaction: int
    created_at: str


class EntryCreate(BaseModel):
    activity_id: str | None = None
    name: str | None = Field(default=None, max_length=100)
    category: str
    duration_minutes: int = Field(gt=0)
    start_time: str | None = None
    satisfaction: int = Field(ge=1, le=10)


class EntryUpdate(BaseModel):
    activity_id: str | None = None
    name: str | None = Field(default=None, max_length=100)
    category: str | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    start_time: str | None = None
    satisfaction: int | None = Field(default=None, ge=1, le=10)


def _get_or_create_day_log_id(user_id: str, date: str) -> str:
    result = (
        supabase.table("day_logs")
        .select("id")
        .eq("user_id", user_id)
        .eq("date", date)
        .limit(1)
        .execute()
    )
    if result.data:
        return result.data[0]["id"]

    created = (
        supabase.table("day_logs")
        .insert({"user_id": user_id, "date": date})
        .execute()
    )
    return created.data[0]["id"]


def _get_day_log_id(user_id: str, date: str) -> str | None:
    result = (
        supabase.table("day_logs")
        .select("id")
        .eq("user_id", user_id)
        .eq("date", date)
        .limit(1)
        .execute()
    )
    return result.data[0]["id"] if result.data else None


@router.get("/{date}/entries", response_model=list[EntryOut])
def get_entries(date: Date, user_id: str = Depends(get_current_user)):
    day_log_id = _get_day_log_id(user_id, str(date))
    if not day_log_id:
        return []

    result = (
        supabase.table("day_entries")
        .select("id,activity_id,name,category,duration_minutes,start_time,satisfaction,created_at")
        .eq("day_log_id", day_log_id)
        .order("start_time", nullsfirst=True)
        .execute()
    )
    return result.data


@router.post("/{date}/entries", response_model=EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(date: Date, body: EntryCreate, user_id: str = Depends(get_current_user)):
    if body.activity_id is None and body.name is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Either activity_id or name is required")

    day_log_id = _get_or_create_day_log_id(user_id, str(date))

    payload = {
        "day_log_id": day_log_id,
        "category": body.category,
        "duration_minutes": body.duration_minutes,
        "satisfaction": body.satisfaction,
        **({"activity_id": body.activity_id} if body.activity_id is not None else {}),
        **({"name": body.name} if body.name is not None else {}),
        **({"start_time": body.start_time} if body.start_time is not None else {}),
    }

    result = supabase.table("day_entries").insert(payload).execute()

    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create entry")

    return result.data[0]


@router.put("/{date}/entries/{entry_id}", response_model=EntryOut)
def update_entry(date: Date, entry_id: str, body: EntryUpdate, user_id: str = Depends(get_current_user)):
    day_log_id = _get_day_log_id(user_id, str(date))
    if not day_log_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No entries found for this date")

    existing = (
        supabase.table("day_entries")
        .select("id")
        .eq("id", entry_id)
        .eq("day_log_id", day_log_id)
        .limit(1)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No fields to update")

    result = (
        supabase.table("day_entries")
        .update(updates)
        .eq("id", entry_id)
        .execute()
    )
    return result.data[0]


@router.delete("/{date}/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(date: Date, entry_id: str, user_id: str = Depends(get_current_user)):
    day_log_id = _get_day_log_id(user_id, str(date))
    if not day_log_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No entries found for this date")

    existing = (
        supabase.table("day_entries")
        .select("id")
        .eq("id", entry_id)
        .eq("day_log_id", day_log_id)
        .limit(1)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    supabase.table("day_entries").delete().eq("id", entry_id).execute()
