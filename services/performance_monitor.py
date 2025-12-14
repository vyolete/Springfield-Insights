"""
Monitor de performance en tiempo real para Springfield Insights
Rastrea métricas clave y proporciona alertas de performance
"""
import streamlit as st
import time
import psutil
import gc
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor de performance en tiempo real con alertas automáticas"""
    
    def __init__(self):
        self.metrics = {
            'page_load_time': [],
            'search_time': [],
            'llm_response_time': [],
            'memory_usage': [],
            'cache_hit_rate': {},
            'api_calls': [],
            'errors': []
        }
        
        # Umbrales de alerta
        self.thresholds = {
            'page_load_warning': 3.0,  # segundos
            'page_load_critical': 5.0,
            'memory_warning': 200,     # MB
            'memory_critical': 400,
            'cache_hit_minimum': 70    # porcentaje
        }
    
    def track_page_load(self, start_time: float, page_name: str = "unknown"):
        """Rastrea tiempo de carga de página"""
        load_time = time.time() - start_time
        self.metrics['page_load_time'].append({
            'time': load_time,
            'page': page_name,
            'timestamp': datetime.now()
        })
        
        # Alertas automáticas
        if load_time > self.thresholds['page_load_critical']:
            st.error(f"🚨 Carga crítica lenta: {load_time:.2f}s en {page_name}")
        elif load_time > self.thresholds['page_load_warning']:
            st.warning(f"⚠️ Carga lenta detectada: {load_time:.2f}s en {page_name}")
        
        logger.info(f"Page load: {page_name} - {load_time:.2f}s")
    
    def track_search_time(self, start_time: float, query: str, results_count: int):
        """Rastrea tiempo de búsqueda"""
        search_time = time.time() - start_time
        self.metrics['search_time'].append({
            'time': search_time,
            'query': query,
            'results': results_count,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Search: '{query}' - {search_time:.2f}s - {results_count} results")
    
    def track_llm_response(self, start_time: float, character: str, success: bool):
        """Rastrea tiempo de respuesta del LLM"""
        response_time = time.time() - start_time
        self.metrics['llm_response_time'].append({
            'time': response_time,
            'character': character,
            'success': success,
            'timestamp': datetime.now()
        })
        
        if not success:
            self.metrics['errors'].append({
                'type': 'llm_error',
                'character': character,
                'timestamp': datetime.now()
            })
        
        logger.info(f"LLM response: {character} - {response_time:.2f}s - {'success' if success else 'failed'}")
    
    def track_cache_hit(self, cache_name: str, hit: bool):
        """Rastrea eficiencia del cache"""
        if cache_name not in self.metrics['cache_hit_rate']:
            self.metrics['cache_hit_rate'][cache_name] = {'hits': 0, 'misses': 0}
        
        if hit:
            self.metrics['cache_hit_rate'][cache_name]['hits'] += 1
        else:
            self.metrics['cache_hit_rate'][cache_name]['misses'] += 1
        
        # Verificar eficiencia del cache
        total = self.metrics['cache_hit_rate'][cache_name]['hits'] + self.metrics['cache_hit_rate'][cache_name]['misses']
        if total >= 10:  # Solo alertar después de 10 operaciones
            hit_rate = (self.metrics['cache_hit_rate'][cache_name]['hits'] / total) * 100
            if hit_rate < self.thresholds['cache_hit_minimum']:
                st.warning(f"⚠️ Baja eficiencia de cache {cache_name}: {hit_rate:.1f}%")
    
    def track_memory_usage(self):
        """Rastrea uso de memoria"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            self.metrics['memory_usage'].append({
                'memory_mb': memory_mb,
                'timestamp': datetime.now()
            })
            
            # Alertas de memoria
            if memory_mb > self.thresholds['memory_critical']:
                st.error(f"🚨 Uso crítico de memoria: {memory_mb:.1f} MB")
                self._trigger_memory_cleanup()
            elif memory_mb > self.thresholds['memory_warning']:
                st.warning(f"⚠️ Alto uso de memoria: {memory_mb:.1f} MB")
            
            # Mantener solo las últimas 100 mediciones
            if len(self.metrics['memory_usage']) > 100:
                self.metrics['memory_usage'] = self.metrics['memory_usage'][-100:]
            
            return memory_mb
            
        except Exception as e:
            logger.error(f"Error tracking memory: {e}")
            return 0
    
    def track_api_call(self, api_name: str, success: bool, response_time: float):
        """Rastrea llamadas a APIs externas"""
        self.metrics['api_calls'].append({
            'api': api_name,
            'success': success,
            'response_time': response_time,
            'timestamp': datetime.now()
        })
        
        if not success:
            self.metrics['errors'].append({
                'type': 'api_error',
                'api': api_name,
                'timestamp': datetime.now()
            })
    
    def _trigger_memory_cleanup(self):
        """Ejecuta limpieza de memoria automática"""
        logger.info("Triggering automatic memory cleanup")
        
        # Limpiar cache de Streamlit
        st.cache_data.clear()
        
        # Limpiar cache de sesión antiguo
        if hasattr(st.session_state, 'image_cache'):
            old_threshold = datetime.now() - timedelta(minutes=30)
            old_keys = [
                k for k, v in st.session_state.image_cache.items()
                if v.get('timestamp', datetime.min) < old_threshold
            ]
            for key in old_keys:
                del st.session_state.image_cache[key]
        
        # Garbage collection
        gc.collect()
        
        st.info("🧹 Limpieza automática de memoria ejecutada")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de performance"""
        summary = {}
        
        # Tiempo promedio de carga
        if self.metrics['page_load_time']:
            recent_loads = [m for m in self.metrics['page_load_time'] 
                          if datetime.now() - m['timestamp'] < timedelta(minutes=10)]
            if recent_loads:
                summary['avg_page_load'] = sum(m['time'] for m in recent_loads) / len(recent_loads)
        
        # Tiempo promedio de búsqueda
        if self.metrics['search_time']:
            recent_searches = [m for m in self.metrics['search_time']
                             if datetime.now() - m['timestamp'] < timedelta(minutes=10)]
            if recent_searches:
                summary['avg_search_time'] = sum(m['time'] for m in recent_searches) / len(recent_searches)
        
        # Eficiencia de cache
        summary['cache_efficiency'] = {}
        for cache_name, data in self.metrics['cache_hit_rate'].items():
            total = data['hits'] + data['misses']
            if total > 0:
                summary['cache_efficiency'][cache_name] = (data['hits'] / total) * 100
        
        # Uso actual de memoria
        summary['current_memory'] = self.track_memory_usage()
        
        # Errores recientes
        recent_errors = [e for e in self.metrics['errors']
                        if datetime.now() - e['timestamp'] < timedelta(minutes=10)]
        summary['recent_errors'] = len(recent_errors)
        
        # Llamadas API exitosas
        recent_api_calls = [c for c in self.metrics['api_calls']
                           if datetime.now() - c['timestamp'] < timedelta(minutes=10)]
        if recent_api_calls:
            successful_calls = sum(1 for c in recent_api_calls if c['success'])
            summary['api_success_rate'] = (successful_calls / len(recent_api_calls)) * 100
        
        return summary
    
    def render_performance_sidebar(self):
        """Renderiza métricas de performance en sidebar"""
        with st.sidebar:
            st.markdown("### ⚡ Performance")
            
            summary = self.get_performance_summary()
            
            # Memoria actual
            memory = summary.get('current_memory', 0)
            memory_color = "red" if memory > 300 else "orange" if memory > 200 else "green"
            st.markdown(f"**Memoria:** <span style='color:{memory_color}'>{memory:.1f} MB</span>", 
                       unsafe_allow_html=True)
            
            # Tiempo de carga promedio
            if 'avg_page_load' in summary:
                load_time = summary['avg_page_load']
                load_color = "red" if load_time > 3 else "orange" if load_time > 1 else "green"
                st.markdown(f"**Carga:** <span style='color:{load_color}'>{load_time:.2f}s</span>", 
                           unsafe_allow_html=True)
            
            # Eficiencia de cache
            if summary.get('cache_efficiency'):
                avg_cache = sum(summary['cache_efficiency'].values()) / len(summary['cache_efficiency'])
                cache_color = "green" if avg_cache > 80 else "orange" if avg_cache > 60 else "red"
                st.markdown(f"**Cache:** <span style='color:{cache_color}'>{avg_cache:.1f}%</span>", 
                           unsafe_allow_html=True)
            
            # Errores recientes
            errors = summary.get('recent_errors', 0)
            if errors > 0:
                st.markdown(f"**Errores:** <span style='color:red'>{errors}</span>", 
                           unsafe_allow_html=True)
            
            # Botón de limpieza manual
            if st.button("🧹 Limpiar Cache", help="Limpia cache y libera memoria"):
                self._trigger_memory_cleanup()
                st.rerun()
    
    def render_detailed_metrics(self):
        """Renderiza métricas detalladas para debugging"""
        st.markdown("### 📊 Métricas Detalladas de Performance")
        
        summary = self.get_performance_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Memoria Actual", 
                f"{summary.get('current_memory', 0):.1f} MB",
                delta=None
            )
        
        with col2:
            if 'avg_page_load' in summary:
                st.metric(
                    "Carga Promedio", 
                    f"{summary['avg_page_load']:.2f}s",
                    delta=None
                )
        
        with col3:
            if 'avg_search_time' in summary:
                st.metric(
                    "Búsqueda Promedio", 
                    f"{summary['avg_search_time']:.2f}s",
                    delta=None
                )
        
        with col4:
            st.metric(
                "Errores Recientes", 
                summary.get('recent_errors', 0),
                delta=None
            )
        
        # Gráfico de uso de memoria (si hay datos)
        if len(self.metrics['memory_usage']) > 1:
            import pandas as pd
            
            df_memory = pd.DataFrame(self.metrics['memory_usage'])
            df_memory['timestamp'] = pd.to_datetime(df_memory['timestamp'])
            
            st.line_chart(
                df_memory.set_index('timestamp')['memory_mb'],
                use_container_width=True
            )
        
        # Eficiencia de cache por servicio
        if summary.get('cache_efficiency'):
            st.markdown("#### 🗄️ Eficiencia de Cache por Servicio")
            
            for cache_name, efficiency in summary['cache_efficiency'].items():
                color = "🟢" if efficiency > 80 else "🟡" if efficiency > 60 else "🔴"
                st.markdown(f"{color} **{cache_name}**: {efficiency:.1f}%")

# Instancia global del monitor
performance_monitor = PerformanceMonitor()