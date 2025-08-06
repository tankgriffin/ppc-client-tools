'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Project, ProjectStatus, PhaseKey, ServicePackage } from '@/types';
import { storage } from '@/lib/storage';
import { ArrowLeft, Download, FileText, CheckCircle, Clock, AlertCircle, Copy, ExternalLink, TrendingUp, Edit } from 'lucide-react';
import Link from 'next/link';
import { FormattedText } from '@/components/FormattedText';

export default function ProjectDetail() {
  const params = useParams();
  const router = useRouter();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [activePhase, setActivePhase] = useState<PhaseKey>('phase1');
  const [copySuccess, setCopySuccess] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    loadProject();
  }, [params.id]);

  // Auto-redirect to analysis when completed
  useEffect(() => {
    if (project && project.completionStatus === ProjectStatus.COMPLETED) {
      // Small delay to let users see the completion status change
      setTimeout(() => {
        router.push(`/projects/${project.id}/analysis`);
      }, 2000);
    }
  }, [project, router]);

  const loadProject = async () => {
    try {
      const projectData = await storage.getProject(params.id as string);
      if (!projectData) {
        router.push('/');
        return;
      }
      setProject(projectData);
    } catch (error) {
      console.error('Failed to load project:', error);
    } finally {
      setLoading(false);
    }
  };

  const updatePhaseResponse = async (phase: PhaseKey, response: string) => {
    if (!project) return;

    const updatedPhases = {
      ...project.claudePhases,
      [phase]: {
        ...project.claudePhases[phase],
        response,
        completed: response.trim().length > 0,
        lastModified: new Date(),
      }
    };

    // Check if all phases are completed (must have responses with meaningful content)
    const allPhasesCompleted = Object.values(updatedPhases).every(p => 
      p.completed && p.response && p.response.trim().length > 50
    );
    
    const updatedProject = {
      ...project,
      claudePhases: updatedPhases,
      completionStatus: allPhasesCompleted ? ProjectStatus.COMPLETED : 
                       Object.values(updatedPhases).some(p => p.completed) ? ProjectStatus.IN_PROGRESS : 
                       ProjectStatus.DRAFT,
      lastModified: new Date(),
    };

    try {
      await storage.saveProject(updatedProject);
      setProject(updatedProject);
    } catch (error) {
      console.error('Failed to save project:', error);
    }
  };

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(type);
      setTimeout(() => setCopySuccess(null), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  const getPhaseTitle = (phase: PhaseKey): string => {
    const titles = {
      phase1: 'Business Intelligence Analysis',
      phase2: 'Competitive Landscape Mapping',
      phase3: 'Market Gap Identification',
      phase4: 'Strategic Positioning Development',
      phase5: 'Content & Campaign Strategy',
    };
    return titles[phase];
  };

  const getPhaseIcon = (phase: PhaseKey, completed: boolean) => {
    if (completed) {
      return <CheckCircle className="h-5 w-5 text-green-600" />;
    }
    return <Clock className="h-5 w-5 text-gray-400" />;
  };

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

  const getCompletedPhases = () => {
    if (!project) return 0;
    return Object.values(project.claudePhases).filter(phase => phase.completed).length;
  };

  const completeProject = async () => {
    if (!project) return;
    
    const updatedProject = {
      ...project,
      completionStatus: ProjectStatus.COMPLETED,
      lastModified: new Date(),
    };

    try {
      await storage.saveProject(updatedProject);
      setProject(updatedProject);
    } catch (error) {
      console.error('Failed to complete project:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading project...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
          <p className="text-gray-600">Project not found</p>
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
              <Link
                href="/"
                className="flex items-center text-gray-600 hover:text-gray-900 mr-4"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Dashboard
              </Link>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{project.name}</h1>
                <p className="text-sm text-gray-500">{project.industry}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.completionStatus)}`}>
                {project.completionStatus.replace('_', ' ').toUpperCase()}
              </span>
              {getCompletedPhases() === 5 && project.completionStatus !== ProjectStatus.COMPLETED && (
                <button
                  onClick={completeProject}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Complete Project
                </button>
              )}
              {project.completionStatus === ProjectStatus.COMPLETED && (
                <Link
                  href={`/projects/${project.id}/analysis`}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
                >
                  <TrendingUp className="h-4 w-4 mr-2" />
                  View Analysis
                </Link>
              )}
              <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Ready to Complete Banner */}
        {getCompletedPhases() === 5 && project.completionStatus !== ProjectStatus.COMPLETED && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-blue-600 mr-4" />
              <div className="flex-1">
                <h3 className="text-lg font-medium text-blue-900">🎉 All Research Phases Complete!</h3>
                <p className="text-blue-700 mt-1">
                  You&apos;ve completed all 5 research phases. Click below to finalize your project and access the strategic analysis dashboard.
                </p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={completeProject}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
                >
                  Complete Project
                </button>
                <Link
                  href={`/projects/${project.id}/analysis`}
                  className="inline-flex items-center px-4 py-2 border border-blue-300 rounded-md shadow-sm text-sm font-medium text-blue-700 bg-white hover:bg-blue-50"
                >
                  View Analysis
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Completion Banner */}
        {project.completionStatus === ProjectStatus.COMPLETED && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-600 mr-4" />
              <div className="flex-1">
                <h3 className="text-lg font-medium text-green-900">🎉 Research Complete!</h3>
                <p className="text-green-700 mt-1">
                  All 5 research phases have been completed. Your strategic analysis is ready for review.
                </p>
              </div>
              <div className="flex space-x-3">
                <Link
                  href={`/projects/${project.id}/analysis`}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
                >
                  View Complete Analysis
                </Link>
                <Link
                  href={`/projects/${project.id}/implementation`}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Implementation Plan
                </Link>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Phase Navigation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Research Phases</h3>
                <p className="text-sm text-gray-500 mt-1">
                  {getCompletedPhases()} of 5 phases completed
                </p>
                {getCompletedPhases() === 5 && project.completionStatus !== ProjectStatus.COMPLETED && (
                  <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-md">
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                      <span className="text-sm font-medium text-green-800">Ready to complete!</span>
                    </div>
                  </div>
                )}
              </div>
              <nav className="p-4">
                <ul className="space-y-2">
                  {Object.entries(project.claudePhases).map(([phaseKey, phaseData]) => (
                    <li key={phaseKey}>
                      <button
                        onClick={() => setActivePhase(phaseKey as PhaseKey)}
                        className={`w-full flex items-center px-3 py-2 text-left text-sm rounded-md transition-colors ${
                          activePhase === phaseKey
                            ? 'bg-blue-50 text-blue-700 border-blue-200'
                            : 'text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <div className="mr-3">
                          {getPhaseIcon(phaseKey as PhaseKey, phaseData.completed)}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">
                            Phase {phaseKey.slice(-1)}
                          </div>
                          <div className="text-xs text-gray-500 truncate">
                            {getPhaseTitle(phaseKey as PhaseKey)}
                          </div>
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              </nav>
            </div>

            {/* Business Summary */}
            <div className="bg-white rounded-lg shadow mt-6">
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Business Summary</h3>
              </div>
              <div className="p-4 space-y-3">
                <div>
                  <dt className="text-xs font-medium text-gray-500 uppercase">Industry</dt>
                  <dd className="text-sm text-gray-900">{project.businessData.industry}</dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-gray-500 uppercase">Service Package</dt>
                  <dd className="text-sm text-gray-900">
                    {project.businessData.servicePackage === ServicePackage.PPC_ONLY && 'PPC Only'}
                    {project.businessData.servicePackage === ServicePackage.SEO_ONLY && 'SEO Only'}
                    {project.businessData.servicePackage === ServicePackage.PPC_SEO_COMBINED && 'PPC + SEO Combined'}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-gray-500 uppercase">Location</dt>
                  <dd className="text-sm text-gray-900">{project.businessData.location}</dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-gray-500 uppercase">Primary Goal</dt>
                  <dd className="text-sm text-gray-900">
                    {project.businessData.primaryGoal.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-gray-500 uppercase">Budget Range</dt>
                  <dd className="text-sm text-gray-900">
                    {project.businessData.budgetRange.replace('_', ' ').toUpperCase()}
                  </dd>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content - Phase Details */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">
                      {getPhaseTitle(activePhase)}
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">
                      Phase {activePhase.slice(-1)} of 5
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    {project.claudePhases[activePhase].completed && (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    )}
                  </div>
                </div>
              </div>

              <div className="p-6">
                {/* Claude Prompt */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">Claude AI Prompt</h3>
                    <button
                      onClick={() => copyToClipboard(project.claudePhases[activePhase].prompt, 'prompt')}
                      className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    >
                      <Copy className="h-4 w-4 mr-2" />
                      {copySuccess === 'prompt' ? 'Copied!' : 'Copy Prompt'}
                    </button>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 border">
                    <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
                      {project.claudePhases[activePhase].prompt}
                    </pre>
                  </div>
                  <div className="mt-3 flex items-center text-sm text-gray-500">
                    <FileText className="h-4 w-4 mr-1" />
                    <span>Copy this prompt and paste it into Claude AI for analysis</span>
                    <ExternalLink className="h-4 w-4 ml-2" />
                  </div>
                </div>

                {/* Response Area */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">Claude AI Response</h3>
                    <div className="flex items-center space-x-2">
                      {project.claudePhases[activePhase].response && (
                        <>
                          <button
                            onClick={() => setEditMode(!editMode)}
                            className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                          >
                            <Edit className="h-4 w-4 mr-2" />
                            {editMode ? 'View Formatted' : 'Edit Response'}
                          </button>
                          <button
                            onClick={() => copyToClipboard(project.claudePhases[activePhase].response, 'response')}
                            className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                          >
                            <Copy className="h-4 w-4 mr-2" />
                            {copySuccess === 'response' ? 'Copied!' : 'Copy Response'}
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                  
                  {editMode || !project.claudePhases[activePhase].response ? (
                    <textarea
                      className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                      rows={20}
                      placeholder="Paste Claude AI's response here..."
                      value={project.claudePhases[activePhase].response}
                      onChange={(e) => updatePhaseResponse(activePhase, e.target.value)}
                    />
                  ) : (
                    <div className="border border-gray-300 rounded-md p-6 bg-white min-h-[500px]">
                      <FormattedText 
                        text={project.claudePhases[activePhase].response}
                        className="text-gray-800"
                      />
                    </div>
                  )}
                  
                  <div className="mt-3 flex items-center justify-between text-sm text-gray-500">
                    <span>
                      {project.claudePhases[activePhase].response.length > 0
                        ? `${project.claudePhases[activePhase].response.length} characters`
                        : 'No response yet'
                      }
                    </span>
                    <span>
                      Last updated: {project.claudePhases[activePhase].lastModified.toLocaleDateString()}
                    </span>
                  </div>
                </div>

                {/* Phase Status */}
                <div className="mt-6 p-4 rounded-lg border border-gray-200 bg-gray-50">
                  <div className="flex items-center">
                    {project.claudePhases[activePhase].completed ? (
                      <>
                        <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                        <span className="text-sm font-medium text-green-800">Phase Completed</span>
                      </>
                    ) : (
                      <>
                        <Clock className="h-5 w-5 text-yellow-600 mr-2" />
                        <span className="text-sm font-medium text-yellow-800">Awaiting Response</span>
                      </>
                    )}
                  </div>
                  {project.claudePhases[activePhase].completed && (
                    <p className="text-sm text-gray-600 mt-1">
                      This phase is complete. You can move on to the next phase or continue refining this analysis.
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}