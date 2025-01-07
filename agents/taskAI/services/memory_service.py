# services/memory_service.py

class MemoryService:
     def __init__(self, store: BaseStore, user_id: str):
        self.store = store
        self.user_id = user_id
        self._cache = {}
        
    def get_profile(self, use_cache: bool = True):
        cache_key = f"profile_{self.user_id}"
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
            
        namespace = ("profile", self.user_id)
        memories = self.store.search(namespace)
        result = memories[0].value if memories else None
        
        if use_cache:
            self._cache[cache_key] = result
        return result
    
    def get_todos(self):
        namespace = ("todo", self.user_id)
        memories = self.store.search(namespace)
        return "\n".join(f"{mem.value}" for mem in memories)
    
    def get_instructions(self):
        namespace = ("instructions", self.user_id)
        memories = self.store.search(namespace)
        return memories[0].value if memories else ""