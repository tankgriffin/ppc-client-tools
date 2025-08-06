'use client';

import { useEffect, useState } from 'react';
import { Project, ProjectStatus } from '@/types';
import { storage } from '@/lib/storage';
import { Plus, Search, MoreHorizontal, Calendar, TrendingUp, Users, FolderOpen } from 'lucide-react';
import Link from 'next/link';

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<ProjectStatus | 'all'>('all');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const allProjects = await storage.getAllProjects();
      setProjects(allProjects);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.industry.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || project.completionStatus === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.COMPLETED:
        return 'bg-green-100 text-green-800';
      case ProjectStatus.IN_PROGRESS:
        return 'bg-blue-100 text-blue-800';
      case ProjectStatus.ANALYSIS:
        return 'bg-purple-100 text-purple-800';
      case ProjectStatus.DRAFT:
        return 'bg-gray-100 text-gray-800';
      case ProjectStatus.ARCHIVED:
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.COMPLETED:
        return 'Completed';
      case ProjectStatus.IN_PROGRESS:
        return 'In Progress';
      case ProjectStatus.ANALYSIS:
        return 'Analysis';
      case ProjectStatus.DRAFT:
        return 'Draft';
      case ProjectStatus.ARCHIVED:
        return 'Archived';
      default:
        return 'Unknown';
    }
  };

  const getCompletionRate = () => {
    if (projects.length === 0) return 0;
    const completed = projects.filter(p => p.completionStatus === ProjectStatus.COMPLETED).length;
    return Math.round((completed / projects.length) * 100);
  };

  const getRecentProjects = () => {
    return projects
      .sort((a, b) => new Date(b.lastModified).getTime() - new Date(a.lastModified).getTime())
      .slice(0, 3);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your projects...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">
                PPC Strategic Intelligence
              </h1>
            </div>
            <Link
              href="/projects/new"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <Plus className="h-4 w-4 mr-2" />
              New Project
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FolderOpen className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Projects</p>
                <p className="text-2xl font-bold text-gray-900">{projects.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Completed</p>
                <p className="text-2xl font-bold text-gray-900">
                  {projects.filter(p => p.completionStatus === ProjectStatus.COMPLETED).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Calendar className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">In Progress</p>
                <p className="text-2xl font-bold text-gray-900">
                  {projects.filter(p => p.completionStatus === ProjectStatus.IN_PROGRESS).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Users className="h-8 w-8 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900">{getCompletionRate()}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Filter */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="p-6 border-b border-gray-200">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div className="flex-1 min-w-0">
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Search projects..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <div className="mt-4 sm:mt-0 sm:ml-4">
                <select
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-md"
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value as ProjectStatus | 'all')}
                >
                  <option value="all">All Projects</option>
                  <option value={ProjectStatus.DRAFT}>Draft</option>
                  <option value={ProjectStatus.IN_PROGRESS}>In Progress</option>
                  <option value={ProjectStatus.ANALYSIS}>Analysis</option>
                  <option value={ProjectStatus.COMPLETED}>Completed</option>
                  <option value={ProjectStatus.ARCHIVED}>Archived</option>
                </select>
              </div>
            </div>
          </div>

          {/* Projects List */}
          <div className="divide-y divide-gray-200">
            {filteredProjects.length === 0 ? (
              <div className="p-12 text-center">
                <FolderOpen className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No projects found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {searchTerm || filterStatus !== 'all' 
                    ? 'Try adjusting your search or filter criteria.'
                    : 'Get started by creating your first PPC research project.'
                  }
                </p>
                {!searchTerm && filterStatus === 'all' && (
                  <div className="mt-6">
                    <Link
                      href="/projects/new"
                      className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Create Your First Project
                    </Link>
                  </div>
                )}
              </div>
            ) : (
              filteredProjects.map((project) => (
                <div key={project.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3">
                        <Link
                          href={`/projects/${project.id}`}
                          className="text-lg font-medium text-blue-600 hover:text-blue-800 truncate"
                        >
                          {project.name}
                        </Link>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.completionStatus)}`}>
                          {getStatusLabel(project.completionStatus)}
                        </span>
                      </div>
                      <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                        <span>{project.industry}</span>
                        <span>•</span>
                        <span>Created {new Date(project.created).toLocaleDateString()}</span>
                        <span>•</span>
                        <span>Updated {new Date(project.lastModified).toLocaleDateString()}</span>
                      </div>
                      {project.businessData.description && (
                        <p className="mt-2 text-sm text-gray-600 truncate max-w-2xl">
                          {project.businessData.description}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      {project.completionStatus === ProjectStatus.COMPLETED ? (
                        <>
                          <Link
                            href={`/projects/${project.id}/analysis`}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                          >
                            Analysis
                          </Link>
                          <Link
                            href={`/projects/${project.id}/implementation`}
                            className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                          >
                            Plan
                          </Link>
                        </>
                      ) : (
                        <Link
                          href={`/projects/${project.id}`}
                          className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          Open
                        </Link>
                      )}
                      <button className="p-1.5 text-gray-400 hover:text-gray-600">
                        <MoreHorizontal className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Activity */}
        {getRecentProjects().length > 0 && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {getRecentProjects().map((project) => (
                <div key={project.id} className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <Link
                        href={`/projects/${project.id}`}
                        className="text-sm font-medium text-blue-600 hover:text-blue-800"
                      >
                        {project.name}
                      </Link>
                      <p className="text-sm text-gray-500">
                        Last updated {new Date(project.lastModified).toLocaleDateString()}
                      </p>
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.completionStatus)}`}>
                      {getStatusLabel(project.completionStatus)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}