"""
Gestor de citas favoritas con persistencia local
"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FavoritesManager:
    """Gestor para almacenar y recuperar citas favoritas"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.favorites_file = os.path.join(data_dir, "favorites.json")
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Crea el directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_favorite(self, quote_data: Dict[str, Any]) -> bool:
        """
        Guarda una cita como favorita
        
        Args:
            quote_data: Datos de la cita a guardar
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            favorites = self.load_favorites()
            
            # Agregar timestamp y ID único
            favorite_entry = {
                **quote_data,
                'saved_at': datetime.now().isoformat(),
                'favorite_id': self._generate_favorite_id(quote_data)
            }
            
            # Evitar duplicados
            if not self._is_duplicate(favorite_entry, favorites):
                favorites.append(favorite_entry)
                return self._save_to_file(favorites)
            
            return False
            
        except Exception as e:
            logger.error(f"Error guardando favorito: {e}")
            return False
    
    def load_favorites(self) -> List[Dict[str, Any]]:
        """
        Carga todas las citas favoritas
        
        Returns:
            Lista de citas favoritas
        """
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
            
        except Exception as e:
            logger.error(f"Error cargando favoritos: {e}")
            return []
    
    def remove_favorite(self, favorite_id: str) -> bool:
        """
        Elimina una cita favorita por ID
        
        Args:
            favorite_id: ID del favorito a eliminar
            
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            favorites = self.load_favorites()
            original_count = len(favorites)
            
            favorites = [f for f in favorites if f.get('favorite_id') != favorite_id]
            
            if len(favorites) < original_count:
                return self._save_to_file(favorites)
            
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando favorito: {e}")
            return False
    
    def get_favorites_by_character(self, character: str) -> List[Dict[str, Any]]:
        """
        Obtiene favoritos filtrados por personaje
        
        Args:
            character: Nombre del personaje
            
        Returns:
            Lista de favoritos del personaje especificado
        """
        favorites = self.load_favorites()
        return [f for f in favorites if f.get('character', '').lower() == character.lower()]
    
    def get_recent_favorites(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene los favoritos más recientes
        
        Args:
            limit: Número máximo de favoritos a retornar
            
        Returns:
            Lista de favoritos más recientes
        """
        favorites = self.load_favorites()
        
        # Ordenar por fecha de guardado (más reciente primero)
        favorites.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        
        return favorites[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los favoritos
        
        Returns:
            Diccionario con estadísticas
        """
        favorites = self.load_favorites()
        
        if not favorites:
            return {
                'total_favorites': 0,
                'unique_characters': 0,
                'most_quoted_character': None,
                'oldest_favorite': None,
                'newest_favorite': None
            }
        
        # Contar por personaje
        character_counts = {}
        for fav in favorites:
            char = fav.get('character', 'Unknown')
            character_counts[char] = character_counts.get(char, 0) + 1
        
        most_quoted = max(character_counts.items(), key=lambda x: x[1]) if character_counts else None
        
        # Fechas
        dates = [fav.get('saved_at') for fav in favorites if fav.get('saved_at')]
        dates.sort()
        
        return {
            'total_favorites': len(favorites),
            'unique_characters': len(character_counts),
            'most_quoted_character': most_quoted[0] if most_quoted else None,
            'most_quoted_count': most_quoted[1] if most_quoted else 0,
            'oldest_favorite': dates[0] if dates else None,
            'newest_favorite': dates[-1] if dates else None,
            'character_distribution': character_counts
        }
    
    def _generate_favorite_id(self, quote_data: Dict[str, Any]) -> str:
        """
        Genera un ID único para un favorito
        
        Args:
            quote_data: Datos de la cita
            
        Returns:
            ID único como string
        """
        quote_text = quote_data.get('quote', '')
        character = quote_data.get('character', '')
        timestamp = datetime.now().timestamp()
        
        # Crear hash simple basado en contenido y timestamp
        content = f"{character}_{quote_text[:50]}_{timestamp}"
        return str(hash(content))
    
    def _is_duplicate(self, new_favorite: Dict[str, Any], existing_favorites: List[Dict[str, Any]]) -> bool:
        """
        Verifica si un favorito ya existe
        
        Args:
            new_favorite: Nuevo favorito a verificar
            existing_favorites: Lista de favoritos existentes
            
        Returns:
            True si es duplicado, False en caso contrario
        """
        new_quote = new_favorite.get('quote', '').strip().lower()
        new_character = new_favorite.get('character', '').strip().lower()
        
        for existing in existing_favorites:
            existing_quote = existing.get('quote', '').strip().lower()
            existing_character = existing.get('character', '').strip().lower()
            
            if new_quote == existing_quote and new_character == existing_character:
                return True
        
        return False
    
    def _save_to_file(self, favorites: List[Dict[str, Any]]) -> bool:
        """
        Guarda la lista de favoritos al archivo
        
        Args:
            favorites: Lista de favoritos a guardar
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(favorites, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            logger.error(f"Error guardando archivo de favoritos: {e}")
            return False
    
    def export_favorites(self, export_path: str) -> bool:
        """
        Exporta favoritos a un archivo específico
        
        Args:
            export_path: Ruta donde exportar los favoritos
            
        Returns:
            True si se exportó exitosamente, False en caso contrario
        """
        try:
            favorites = self.load_favorites()
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(favorites, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error exportando favoritos: {e}")
            return False