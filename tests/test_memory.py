from app.memory.store import MemoryStore


def test_memory_save_and_read(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")
    store.save_user_memory("user-1", {"preferred_style": "concise"})
    assert store.get_user_memory("user-1")["preferred_style"] == "concise"

