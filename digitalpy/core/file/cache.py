"""
 * Cache defines the interface for cache implementations.
 *
 * Caches are divided into different sections, which store
 * key value pairs.
"""

class Cache:
"""
   * Check if a cache entry exists
   * @param $section The cache section
   * @param $key The cache key
   * @return boolean
"""
    def exists(self, section: str, key: str) -> bool:
        pass
"""
   * Get the date of the specified cache entry
   * @param $section The cache section
   * @param $key The cache key
   * @return DateTime or null, if not cached
"""
    def getDate(self, section: str, key: str) -> datetime.datetime:
        pass
"""
   * Get the value of the specified cache entry
   * @param $section The cache section
   * @param $key The cache key
   * @return Mixed
"""
    def get(self, section: str, key: str) -> Any:
        pass
"""
   * Store the value of the specified cache entry with an optional lifetime.
   * @param $section The cache section
   * @param $key The key
   * @param $value The value
   * @param $lifetime The lifetime in seconds (optional)
"""
    def put(self, section: str, key: str, value: Any, lifetime: Optional[int]=None):
        pass
"""
   * Clear the given cache section. The wildcard char '*'
   * may be added to the section name in order to
   * clear all matching sections.
   * @param $section The cache section
"""
    def clear(self, section: str):
        pass
"""
   * Clear all cache sections
"""
    def clearAll(self):
        pass



