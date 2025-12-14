"""
Optimizador de cache inteligente para Springfield Insights
Implementa estrategias avanzadas de caching y limpieza automática
"""
import streamlit as st
import hashlib
import time
import gc
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta
import logging
from services.performance_monitor import performance_monitor

logger = logging.getLogger(__name__)

class IntelligentCache:
    """Cache inteligente con limpieza automática y métricas"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache_data = {}
        self.access_times = {}
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del cache con tracking de hits/misses"""
        if key in self.cache_data:
            entry = self.cache_data[key]
            
            # Verificar TTL
            if time.time() - entry['timestamp'] < entry['ttl']:
                self.access_times[key] = time.time()
                self.hit_count += 1
                performance_monitor.track_cache_hit('intelligent_cache', True)
                return entry['data']
            else:
                # Entrada expirada
                del self.cache_data[key]
                if key in self.access_times:
                    del self.access_times[key]
        
        self.miss_count += 1
        performance_monitor.track_cache_hit('intelligent_cache', False)
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Establece valor en cache con TTL"""
        if ttl is None:
            ttl = self.default_ttl
        
        # Limpiar cache si está lleno
        if len(self.cache_data) >= self.max_size:
            self._evict_old_entries()
        
        self.cache_data[key] = {
            'data': value,
            'timestamp': time.time(),
            'ttl': ttl
        }
        self.access_times[key] = time.time()
    
    def _evict_old_entries(self):
        """Elimina entradas antiguas usando LRU"""
        # Ordenar por tiempo de acceso (LRU)
        sorted_keys = sorted(
            self.access_times.keys(),
            key=lambda k: self.access_times[k]
        )
        
        # Eliminar 25% de las entradas más antiguas
        entries_to_remove = len(sorted_keys) // 4
        
        for key in sorted_keys[:entries_to_remove]:
            if key in self.cache_data:
                del self.cache_data[key]
            if key in self.access_times:
                del self.access_times[key]
        
        logger.info(f"Cache eviction: removed {entries_to_remove} old entries")
    
    def clear(self):
        """Limpia todo el cache"""
        self.cache_data.clear()
        self.access_times.clear()
        self.hit_count = 0
        self.miss_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache_data),
            'max_size': self.max_size,
            'hit_rate': hit_rate,
            'hits': self.hit_count,
            'misses': self.miss_count
        }

class CacheOptimizer:
    """Optimizador principal de cache para la aplicación"""
    
    def __init__(self):
        self.llm_cache = IntelligentCache(max_size=500, default_ttl=86400)  # 24h para LLM
        self.episodes_cache = IntelligentCache(max_size=200, default_ttl=3600)  # 1h para episodios
        self.images_cache = IntelligentCache(max_size=300, default_ttl=1800)  # 30min para imágenes
        self.search_cache = IntelligentCache(max_size=100, default_ttl=1800)  # 30min para búsquedas
    
    def cache_llm_response(self, prompt_hash: str, response: str, ttl: int = 86400):
        """Cachea respuesta de LLM por hash del prompt"""
        self.llm_cache.set(prompt_hash, response, ttl)
    
    def get_cached_llm_response(self, prompt_hash: str) -> Optional[str]:
        """Obtiene respuesta cacheada de LLM"""
        return self.llm_cache.get(prompt_hash)
    
    def cache_episode_data(self, episode_id: str, data: Dict[str, Any]):
        """Cachea datos de episodio"""
        self.episodes_cache.set(f"episode_{episode_id}", data)
    
    def get_cached_episode_data(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene datos cacheados de episodio"""
        return self.episodes_cache.get(f"episode_{episode_id}")
    
    def cache_search_results(self, query_hash: str, results: list):
        """Cachea resultados de búsqueda"""
        self.search_cache.set(query_hash, results)
    
    def get_cached_search_results(self, query_hash: str) -> Optional[list]:
        """Obtiene resultados cacheados de búsqueda"""
        return self.search_cache.get(query_hash)
    
    def cache_image_validation(self, url: str, is_valid: bool):
        """Cachea validación de imagen"""
        self.images_cache.set(f"img_valid_{url}", is_valid, ttl=3600)
    
    def get_cached_image_validation(self, url: str) -> Optional[bool]:
        """Obtiene validación cacheada de imagen"""
        return self.images_cache.get(f"img_valid_{url}")
    
    def create_content_hash(self, *args) -> str:
        """Crea hash único para contenido"""
        content = "|".join(str(arg) for arg in args)
        return hashlib.md5(content.encode()).hexdigest()
    
    def cleanup_expired_entries(self):
        """Limpia entradas expiradas de todos los caches"""
        caches = [self.llm_cache, self.episodes_cache, self.images_cache, self.search_cache]
        
        for cache in caches:
            expired_keys = []
            current_time = time.time()
            
            for key, entry in cache.cache_data.items():
                if current_time - entry['timestamp'] >= entry['ttl']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                if key in cache.cache_data:
                    del cache.cache_data[key]
                if key in cache.access_times:
                    del cache.access_times[key]
        
        # Garbage collection después de limpieza
        gc.collect()
        
        logger.info(f"Cache cleanup completed: removed expired entries")
    
    def get_global_cache_stats(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene estadísticas de todos los caches"""
        return {
            'llm_cache': self.llm_cache.get_stats(),
            'episodes_cache': self.episodes_cache.get_stats(),
            'images_cache': self.images_cache.get_stats(),
            'search_cache': self.search_cache.get_stats()
        }
    
    def clear_all_caches(self):
        """Limpia todos los caches"""
        self.llm_cache.clear()
        self.episodes_cache.clear()
        self.images_cache.clear()
        self.search_cache.clear()
        
        # También limpiar cache de Streamlit
        st.cache_data.clear()
        st.cache_resource.clear()
        
        gc.collect()
        logger.info("All caches cleared")

# Decorador para cache automático
def smart_cache(cache_type: str = 'general', ttl: int = 3600):
    """Decorador para cache automático con el optimizador"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # Crear hash único para los argumentos
            cache_key = cache_optimizer.create_content_hash(
                func.__name__, 
                str(args), 
                str(sorted(kwargs.items()))
            )
            
            # Intentar obtener del cache apropiado
            if cache_type == 'llm':
                cached_result = cache_optimizer.get_cached_llm_response(cache_key)
            elif cache_type == 'episodes':
                cached_result = cache_optimizer.episodes_cache.get(cache_key)
            elif cache_type == 'search':
                cached_result = cache_optimizer.get_cached_search_results(cache_key)
            else:
                cached_result = cache_optimizer.episodes_cache.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)
            
            if cache_type == 'llm':
                cache_optimizer.cache_llm_response(cache_key, result, ttl)
            elif cache_type == 'episodes':
                cache_optimizer.episodes_cache.set(cache_key, result, ttl)
            elif cache_type == 'search':
                cache_optimizer.cache_search_results(cache_key, result)
            else:
                cache_optimizer.episodes_cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator

# Instancia global del optimizador
cache_optimizer = CacheOptimizer()

# Función para limpieza automática periódica
def setup_automatic_cleanup():
    """Configura limpieza automática del cache"""
    if 'last_cleanup' not in st.session_state:
        st.session_state.last_cleanup = time.time()
    
    # Limpiar cada 30 minutos
    if time.time() - st.session_state.last_cleanup > 1800:
        cache_optimizer.cleanup_expired_entries()
        st.session_state.last_cleanup = time.time()

# Función para mostrar estadísticas de cache
def render_cache_stats():
    """Renderiza estadísticas de cache en la UI"""
    st.markdown("### 🗄️ Estadísticas de Cache")
    
    stats = cache_optimizer.get_global_cache_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        llm_stats = stats['llm_cache']
        st.metric(
            "Cache LLM",
            f"{llm_stats['hit_rate']:.1f}%",
            f"{llm_stats['size']}/{llm_stats['max_size']}"
        )
    
    with col2:
        ep_stats = stats['episodes_cache']
        st.metric(
            "Cache Episodios",
            f"{ep_stats['hit_rate']:.1f}%",
            f"{ep_stats['size']}/{ep_stats['max_size']}"
        )
    
    with col3:
        img_stats = stats['images_cache']
        st.metric(
            "Cache Imágenes",
            f"{img_stats['hit_rate']:.1f}%",
            f"{img_stats['size']}/{img_stats['max_size']}"
        )
    
    with col4:
        search_stats = stats['search_cache']
        st.metric(
            "Cache Búsquedas",
            f"{search_stats['hit_rate']:.1f}%",
            f"{search_stats['size']}/{search_stats['max_size']}"
        )
    
    # Botones de control
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Limpiar Cache Expirado"):
            cache_optimizer.cleanup_expired_entries()
            st.success("Cache expirado limpiado")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Limpiar Todo el Cache"):
            cache_optimizer.clear_all_caches()
            st.success("Todo el cache limpiado")
            st.rerun()