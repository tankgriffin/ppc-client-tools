// Local storage management for PPC Strategic Intelligence App
import { Project, UserSettings, BackupData, StorageConfig } from '@/types';
import { v4 as uuidv4 } from 'uuid';

const STORAGE_PREFIX = 'ppc_app_';
const PROJECTS_KEY = `${STORAGE_PREFIX}projects`;
const SETTINGS_KEY = `${STORAGE_PREFIX}settings`;
const CONFIG_KEY = `${STORAGE_PREFIX}config`;

// Default storage configuration
const defaultConfig: StorageConfig = {
  autoSaveInterval: 30000, // 30 seconds
  maxStorageSize: 50 * 1024 * 1024, // 50MB
  compressionEnabled: true,
  backupEnabled: true,
};

// Default user settings
const defaultSettings: UserSettings = {
  theme: 'light' as const,
  language: 'en',
  autoSave: true,
  notifications: true,
  recentProjects: [],
};

export class StorageManager {
  private static instance: StorageManager;
  private config: StorageConfig;

  private constructor() {
    this.config = this.loadConfig();
  }

  public static getInstance(): StorageManager {
    if (!StorageManager.instance) {
      StorageManager.instance = new StorageManager();
    }
    return StorageManager.instance;
  }

  // Project Management
  public async saveProject(project: Project): Promise<void> {
    try {
      const projects = await this.getAllProjects();
      const existingIndex = projects.findIndex(p => p.id === project.id);
      
      project.lastModified = new Date();
      
      if (existingIndex >= 0) {
        projects[existingIndex] = project;
      } else {
        projects.push(project);
      }

      await this.setItem(PROJECTS_KEY, projects);
      await this.updateRecentProjects(project.id);
    } catch (error) {
      console.error('Failed to save project:', error);
      throw new Error('Failed to save project data');
    }
  }

  public async getProject(id: string): Promise<Project | null> {
    try {
      const projects = await this.getAllProjects();
      return projects.find(p => p.id === id) || null;
    } catch (error) {
      console.error('Failed to get project:', error);
      return null;
    }
  }

  public async getAllProjects(): Promise<Project[]> {
    try {
      const stored = await this.getItem<Project[]>(PROJECTS_KEY);
      return stored || [];
    } catch (error) {
      console.error('Failed to get projects:', error);
      return [];
    }
  }

  public async deleteProject(id: string): Promise<void> {
    try {
      const projects = await this.getAllProjects();
      const filtered = projects.filter(p => p.id !== id);
      await this.setItem(PROJECTS_KEY, filtered);
      
      // Remove from recent projects
      const settings = await this.getSettings();
      settings.recentProjects = settings.recentProjects.filter(pid => pid !== id);
      await this.saveSettings(settings);
    } catch (error) {
      console.error('Failed to delete project:', error);
      throw new Error('Failed to delete project');
    }
  }

  public async duplicateProject(id: string, newName: string): Promise<Project> {
    try {
      const original = await this.getProject(id);
      if (!original) {
        throw new Error('Project not found');
      }

      const duplicate: Project = {
        ...original,
        id: uuidv4(),
        name: newName,
        created: new Date(),
        lastModified: new Date(),
      };

      await this.saveProject(duplicate);
      return duplicate;
    } catch (error) {
      console.error('Failed to duplicate project:', error);
      throw new Error('Failed to duplicate project');
    }
  }

  // Settings Management
  public async getSettings(): Promise<UserSettings> {
    try {
      const stored = await this.getItem<UserSettings>(SETTINGS_KEY);
      return { ...defaultSettings, ...stored };
    } catch (error) {
      console.error('Failed to get settings:', error);
      return defaultSettings;
    }
  }

  public async saveSettings(settings: UserSettings): Promise<void> {
    try {
      await this.setItem(SETTINGS_KEY, settings);
    } catch (error) {
      console.error('Failed to save settings:', error);
      throw new Error('Failed to save settings');
    }
  }

  // Configuration Management
  public loadConfig(): StorageConfig {
    try {
      const stored = localStorage.getItem(CONFIG_KEY);
      return stored ? { ...defaultConfig, ...JSON.parse(stored) } : defaultConfig;
    } catch (error) {
      console.error('Failed to load config:', error);
      return defaultConfig;
    }
  }

  public async saveConfig(config: StorageConfig): Promise<void> {
    try {
      this.config = config;
      await this.setItem(CONFIG_KEY, config);
    } catch (error) {
      console.error('Failed to save config:', error);
      throw new Error('Failed to save configuration');
    }
  }

  // Backup and Restore
  public async createBackup(): Promise<BackupData> {
    try {
      const projects = await this.getAllProjects();
      const settings = await this.getSettings();
      
      return {
        version: '1.0',
        timestamp: new Date(),
        projects,
        settings,
      };
    } catch (error) {
      console.error('Failed to create backup:', error);
      throw new Error('Failed to create backup');
    }
  }

  public async restoreBackup(backup: BackupData): Promise<void> {
    try {
      // Validate backup structure
      if (!backup.projects || !backup.settings) {
        throw new Error('Invalid backup format');
      }

      await this.setItem(PROJECTS_KEY, backup.projects);
      await this.setItem(SETTINGS_KEY, backup.settings);
    } catch (error) {
      console.error('Failed to restore backup:', error);
      throw new Error('Failed to restore backup');
    }
  }

  // Storage Utilities
  public async getStorageInfo(): Promise<{
    used: number;
    available: number;
    quota: number;
    projects: number;
  }> {
    try {
      const projects = await this.getAllProjects();
      const allData = JSON.stringify(projects);
      const used = new Blob([allData]).size;
      
      return {
        used,
        available: this.config.maxStorageSize - used,
        quota: this.config.maxStorageSize,
        projects: projects.length,
      };
    } catch (error) {
      console.error('Failed to get storage info:', error);
      return { used: 0, available: 0, quota: 0, projects: 0 };
    }
  }

  public async clearStorage(): Promise<void> {
    try {
      localStorage.removeItem(PROJECTS_KEY);
      localStorage.removeItem(SETTINGS_KEY);
      localStorage.removeItem(CONFIG_KEY);
    } catch (error) {
      console.error('Failed to clear storage:', error);
      throw new Error('Failed to clear storage');
    }
  }

  // Private Methods
  private async updateRecentProjects(projectId: string): Promise<void> {
    try {
      const settings = await this.getSettings();
      const recentProjects = settings.recentProjects.filter(id => id !== projectId);
      recentProjects.unshift(projectId);
      
      // Keep only last 10 recent projects
      settings.recentProjects = recentProjects.slice(0, 10);
      
      await this.saveSettings(settings);
    } catch (error) {
      console.error('Failed to update recent projects:', error);
    }
  }

  private async getItem<T>(key: string): Promise<T | null> {
    try {
      const item = localStorage.getItem(key);
      if (!item) return null;
      
      const parsed = JSON.parse(item);
      
      // Parse dates
      return this.parseDates(parsed);
    } catch (error) {
      console.error(`Failed to get item ${key}:`, error);
      return null;
    }
  }

  private async setItem<T>(key: string, value: T): Promise<void> {
    try {
      const serialized = JSON.stringify(value);
      
      // Check storage size
      const size = new Blob([serialized]).size;
      if (size > this.config.maxStorageSize) {
        throw new Error('Data exceeds maximum storage size');
      }
      
      localStorage.setItem(key, serialized);
    } catch (error) {
      console.error(`Failed to set item ${key}:`, error);
      throw error;
    }
  }

  private parseDates(obj: any): any {
    if (obj === null || obj === undefined) return obj;
    
    if (typeof obj === 'string') {
      // Check if string is an ISO date
      if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(obj)) {
        return new Date(obj);
      }
      return obj;
    }
    
    if (Array.isArray(obj)) {
      return obj.map(item => this.parseDates(item));
    }
    
    if (typeof obj === 'object') {
      const result: any = {};
      for (const key in obj) {
        result[key] = this.parseDates(obj[key]);
      }
      return result;
    }
    
    return obj;
  }
}

// Export singleton instance
export const storage = StorageManager.getInstance();