// Cache Manager for AI models and processing results
// Implements IndexedDB storage with compression and TTL

import { CacheStats, ProcessedContent } from '../types';
import { CACHE_CONFIG } from '../config';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
  compressed?: boolean;
}

class CacheManager {
  private dbName = 'ai-cache-db';
  private dbVersion = 1;
  private db: IDBDatabase | null = null;

  private async initDB(): Promise<IDBDatabase> {
    if (this.db) return this.db;

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Create object stores
        if (!db.objectStoreNames.contains('models')) {
          db.createObjectStore('models', { keyPath: 'name' });
        }
        
        if (!db.objectStoreNames.contains('results')) {
          db.createObjectStore('results', { keyPath: 'key' });
        }
        
        if (!db.objectStoreNames.contains('stats')) {
          db.createObjectStore('stats', { keyPath: 'id' });
        }
      };
    });
  }

  private async compress(data: any): Promise<string> {
    if (!CACHE_CONFIG.compressionEnabled) {
      return JSON.stringify(data);
    }
    
    // Simple compression using JSON + base64
    // In production, consider using a proper compression library
    const jsonString = JSON.stringify(data);
    return btoa(jsonString);
  }

  private async decompress(compressedData: string): Promise<any> {
    if (!CACHE_CONFIG.compressionEnabled) {
      return JSON.parse(compressedData);
    }
    
    try {
      const jsonString = atob(compressedData);
      return JSON.parse(jsonString);
    } catch (error) {
      // Fallback for uncompressed data
      return JSON.parse(compressedData);
    }
  }

  private isExpired(entry: CacheEntry<any>): boolean {
    return Date.now() - entry.timestamp > entry.ttl;
  }

  async cacheModel(modelName: string, modelData: ArrayBuffer): Promise<void> {
    const db = await this.initDB();
    
    const entry: CacheEntry<ArrayBuffer> = {
      data: modelData,
      timestamp: Date.now(),
      ttl: CACHE_CONFIG.modelCacheTTL
    };

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['models'], 'readwrite');
      const store = transaction.objectStore('models');
      
      const request = store.put({ name: modelName, ...entry });
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getCachedModel(modelName: string): Promise<ArrayBuffer | null> {
    const db = await this.initDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['models'], 'readonly');
      const store = transaction.objectStore('models');
      
      const request = store.get(modelName);
      request.onsuccess = () => {
        const result = request.result;
        if (!result) {
          resolve(null);
          return;
        }

        const entry: CacheEntry<ArrayBuffer> = result;
        if (this.isExpired(entry)) {
          // Clean up expired entry
          this.deleteModel(modelName);
          resolve(null);
          return;
        }

        resolve(entry.data);
      };
      request.onerror = () => reject(request.error);
    });
  }

  async cacheProcessingResult(key: string, result: ProcessedContent): Promise<void> {
    const db = await this.initDB();
    
    const compressedData = await this.compress(result);
    const entry: CacheEntry<string> = {
      data: compressedData,
      timestamp: Date.now(),
      ttl: CACHE_CONFIG.resultCacheTTL,
      compressed: CACHE_CONFIG.compressionEnabled
    };

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['results'], 'readwrite');
      const store = transaction.objectStore('results');
      
      const request = store.put({ key, ...entry });
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getCachedResult(key: string): Promise<ProcessedContent | null> {
    const db = await this.initDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['results'], 'readonly');
      const store = transaction.objectStore('results');
      
      const request = store.get(key);
      request.onsuccess = async () => {
        const result = request.result;
        if (!result) {
          resolve(null);
          return;
        }

        const entry: CacheEntry<string> = result;
        if (this.isExpired(entry)) {
          // Clean up expired entry
          this.deleteResult(key);
          resolve(null);
          return;
        }

        try {
          const decompressedData = await this.decompress(entry.data);
          resolve(decompressedData);
        } catch (error) {
          console.error('Failed to decompress cached result:', error);
          resolve(null);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }

  private async deleteModel(modelName: string): Promise<void> {
    const db = await this.initDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['models'], 'readwrite');
      const store = transaction.objectStore('models');
      
      const request = store.delete(modelName);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  private async deleteResult(key: string): Promise<void> {
    const db = await this.initDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['results'], 'readwrite');
      const store = transaction.objectStore('results');
      
      const request = store.delete(key);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async clearExpiredCache(): Promise<void> {
    const db = await this.initDB();

    // Clear expired models
    const modelTransaction = db.transaction(['models'], 'readwrite');
    const modelStore = modelTransaction.objectStore('models');
    
    const modelRequest = modelStore.getAll();
    modelRequest.onsuccess = () => {
      const models = modelRequest.result;
      models.forEach((model) => {
        const entry: CacheEntry<ArrayBuffer> = model;
        if (this.isExpired(entry)) {
          modelStore.delete(model.name);
        }
      });
    };

    // Clear expired results
    const resultTransaction = db.transaction(['results'], 'readwrite');
    const resultStore = resultTransaction.objectStore('results');
    
    const resultRequest = resultStore.getAll();
    resultRequest.onsuccess = () => {
      const results = resultRequest.result;
      results.forEach((result) => {
        const entry: CacheEntry<string> = result;
        if (this.isExpired(entry)) {
          resultStore.delete(result.key);
        }
      });
    };
  }

  async getCacheStats(): Promise<CacheStats> {
    const db = await this.initDB();

    const modelTransaction = db.transaction(['models'], 'readonly');
    const modelStore = modelTransaction.objectStore('models');
    
    const resultTransaction = db.transaction(['results'], 'readonly');
    const resultStore = resultTransaction.objectStore('results');

    const [models, results] = await Promise.all([
      new Promise<any[]>((resolve, reject) => {
        const request = modelStore.getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      }),
      new Promise<any[]>((resolve, reject) => {
        const request = resultStore.getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      })
    ]);

    const modelCacheSize = models.reduce((total, model) => {
      return total + (model.data?.byteLength || 0);
    }, 0);

    const resultCacheSize = results.reduce((total, result) => {
      return total + (result.data?.length || 0) * 2; // Rough estimate for string size
    }, 0);

    const totalEntries = models.length + results.length;

    // Simple hit rate calculation (would need more sophisticated tracking in production)
    const hitRate = 0.8; // Placeholder

    return {
      modelCacheSize,
      resultCacheSize,
      totalEntries,
      hitRate,
      lastCleanup: new Date()
    };
  }

  async clearAllCache(): Promise<void> {
    const db = await this.initDB();

    const transaction = db.transaction(['models', 'results'], 'readwrite');
    
    await Promise.all([
      new Promise<void>((resolve, reject) => {
        const request = transaction.objectStore('models').clear();
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      }),
      new Promise<void>((resolve, reject) => {
        const request = transaction.objectStore('results').clear();
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      })
    ]);
  }

  generateCacheKey(content: string, context: any): string {
    // Create a hash-like key from content and context
    const contextString = JSON.stringify(context);
    const combined = content + contextString;
    
    // Simple hash function (for production, use a proper hash function)
    let hash = 0;
    for (let i = 0; i < combined.length; i++) {
      const char = combined.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    
    return `cache_${Math.abs(hash)}`;
  }
}

export const cacheManager = new CacheManager();