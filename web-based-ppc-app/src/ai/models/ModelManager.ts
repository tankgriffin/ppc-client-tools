// AI Model Manager for loading and managing Transformers.js models
// Implements caching, loading states, and error handling

import { pipeline, Pipeline, env } from '@xenova/transformers';
import { ModelStatus, ModelInfo } from '../types';
import { AI_CONFIG, checkBrowserCompatibility } from '../config';
import { cacheManager } from '../cache/CacheManager';

class ModelManager {
  private models: Map<string, Pipeline> = new Map();
  private modelStatus: Map<string, ModelStatus> = new Map();
  private modelInfo: Map<string, ModelInfo> = new Map();
  private loadingPromises: Map<string, Promise<Pipeline>> = new Map();

  constructor() {
    this.initializeModelInfo();
    this.checkCompatibility();
    this.configureEnvironment();
  }

  private configureEnvironment() {
    // Configure Transformers.js for browser environment
    if (typeof window !== 'undefined') {
      try {
        // Use CDN for models instead of local cache in browser
        env.allowRemoteModels = true;
        env.allowLocalModels = false;
        
        // Configure cache directory (will use browser cache/IndexedDB)
        env.cacheDir = './.cache';
        
        // Disable telemetry
        env.useBrowserCache = true;
        
        console.log('Transformers.js configured for browser environment');
      } catch (error) {
        console.warn('Failed to configure Transformers.js environment:', error);
      }
    }
  }

  private initializeModelInfo() {
    const modelConfigs = [
      { name: 'summarization', model: AI_CONFIG.models.summarization.model },
      { name: 'classification', model: AI_CONFIG.models.classification.model },
      { name: 'embedding', model: AI_CONFIG.models.embedding.model }
    ];

    modelConfigs.forEach(({ name, model }) => {
      this.modelStatus.set(name, 'unloaded');
      this.modelInfo.set(name, {
        name: model,
        status: 'unloaded',
        size: 0
      });
    });
  }

  private checkCompatibility() {
    const compatibility = checkBrowserCompatibility();
    if (!compatibility.supported) {
      console.warn('Browser compatibility issues detected:', compatibility.issues);
      // Could set all models to error state here if needed
    }
  }

  private updateModelStatus(modelName: string, status: ModelStatus, error?: string) {
    this.modelStatus.set(modelName, status);
    const info = this.modelInfo.get(modelName);
    if (info) {
      info.status = status;
      if (error) {
        info.error = error;
      }
      this.modelInfo.set(modelName, info);
    }
  }

  private async loadModelWithTimeout<T>(
    loadFunction: () => Promise<T>,
    modelName: string,
    timeout: number = AI_CONFIG.performance.modelLoadTimeout
  ): Promise<T> {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`Model loading timeout after ${timeout}ms`));
      }, timeout);

      loadFunction()
        .then((result) => {
          clearTimeout(timeoutId);
          resolve(result);
        })
        .catch((error) => {
          clearTimeout(timeoutId);
          reject(error);
        });
    });
  }

  private async loadModel(modelName: string, task: string, modelPath: string): Promise<Pipeline> {
    // Check if already loading
    const existingPromise = this.loadingPromises.get(modelName);
    if (existingPromise) {
      return existingPromise;
    }

    // Check if already loaded
    const existingModel = this.models.get(modelName);
    if (existingModel) {
      return existingModel;
    }

    const loadStartTime = Date.now();
    this.updateModelStatus(modelName, 'loading');

    const loadPromise = this.loadModelWithTimeout(
      async () => {
        try {
          console.log(`Loading ${modelName} model: ${modelPath}`);
          
          // Load the model using Transformers.js
          const model = await pipeline(task, modelPath, {
            // Enable caching
            cache_dir: '.cache',
            // Use local files when available
            local_files_only: false,
            // Progress callback could be added here
          });

          const loadTime = Date.now() - loadStartTime;
          console.log(`${modelName} model loaded in ${loadTime}ms`);

          // Update model info
          const info = this.modelInfo.get(modelName);
          if (info) {
            info.loadTime = loadTime;
            info.status = 'ready';
            this.modelInfo.set(modelName, info);
          }

          this.models.set(modelName, model);
          this.updateModelStatus(modelName, 'ready');
          
          return model;
        } catch (error) {
          console.error(`Failed to load ${modelName} model:`, error);
          this.updateModelStatus(modelName, 'error', error instanceof Error ? error.message : 'Unknown error');
          throw error;
        }
      },
      modelName
    );

    this.loadingPromises.set(modelName, loadPromise);

    try {
      const model = await loadPromise;
      this.loadingPromises.delete(modelName);
      return model;
    } catch (error) {
      this.loadingPromises.delete(modelName);
      throw error;
    }
  }

  async loadModels(): Promise<void> {
    try {
      console.log('Loading AI models...');
      
      // Load models in parallel
      await Promise.all([
        this.getSummarizer(),
        this.getClassifier(),
        this.getEmbedder()
      ]);
      
      console.log('All AI models loaded successfully');
    } catch (error) {
      console.error('Failed to load one or more AI models:', error);
      throw new Error(`Model loading failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async getSummarizer(): Promise<Pipeline> {
    return this.loadModel(
      'summarization',
      'summarization',
      AI_CONFIG.models.summarization.model
    );
  }

  async getClassifier(): Promise<Pipeline> {
    return this.loadModel(
      'classification', 
      'zero-shot-classification',
      AI_CONFIG.models.classification.model
    );
  }

  async getEmbedder(): Promise<Pipeline> {
    return this.loadModel(
      'embedding',
      'feature-extraction',
      AI_CONFIG.models.embedding.model
    );
  }

  getModelStatus(): Record<string, ModelStatus> {
    const status: Record<string, ModelStatus> = {};
    this.modelStatus.forEach((value, key) => {
      status[key] = value;
    });
    return status;
  }

  getModelInfo(): Record<string, ModelInfo> {
    const info: Record<string, ModelInfo> = {};
    this.modelInfo.forEach((value, key) => {
      info[key] = value;
    });
    return info;
  }

  isReady(): boolean {
    return Array.from(this.modelStatus.values()).every(status => status === 'ready');
  }

  hasErrors(): boolean {
    return Array.from(this.modelStatus.values()).some(status => status === 'error');
  }

  async clearCache(): Promise<void> {
    try {
      await cacheManager.clearAllCache();
      console.log('AI model cache cleared');
    } catch (error) {
      console.error('Failed to clear AI model cache:', error);
    }
  }

  async unloadModels(): Promise<void> {
    // Clear all loaded models from memory
    this.models.clear();
    this.loadingPromises.clear();
    
    // Reset status
    this.modelStatus.forEach((_, key) => {
      this.updateModelStatus(key, 'unloaded');
    });
    
    console.log('All AI models unloaded from memory');
  }

  // Retry loading a failed model
  async retryModel(modelName: string): Promise<void> {
    const currentStatus = this.modelStatus.get(modelName);
    if (currentStatus !== 'error') {
      return;
    }

    // Reset status and try again
    this.updateModelStatus(modelName, 'unloaded');
    this.models.delete(modelName);

    switch (modelName) {
      case 'summarization':
        await this.getSummarizer();
        break;
      case 'classification':
        await this.getClassifier();
        break;
      case 'embedding':
        await this.getEmbedder();
        break;
      default:
        throw new Error(`Unknown model: ${modelName}`);
    }
  }
}

export const modelManager = new ModelManager();