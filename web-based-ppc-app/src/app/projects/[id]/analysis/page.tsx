'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Project, ServicePackage } from '@/types';
import { storage } from '@/lib/storage';
import { ArrowLeft, Download, TrendingUp, Target, Lightbulb, AlertTriangle, Calendar, BarChart3, PieChart, FileText, CheckCircle, Clock, Edit, Plus, X, Sparkles } from 'lucide-react';
import Link from 'next/link';
import { FormattedText } from '@/components/FormattedText';
import { SmartSummaryCard } from '@/components/ai/SmartSummaryCard';
import { AIStatusIndicator } from '@/components/ai/AIStatusIndicator';
import { useSimpleAI } from '@/hooks/useSimpleAI';
import { useSimplePageContent } from '@/hooks/useSimplePageContent';

export default function ProjectAnalysis() {
  const params = useParams();
  const router = useRouter();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [activePhase, setActivePhase] = useState('phase1');
  const [showFullText, setShowFullText] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [showDataSelector, setShowDataSelector] = useState(false);
  const [targetTab, setTargetTab] = useState<string>('');
  const [editingContent, setEditingContent] = useState<string>('');
  const [modalActivePhase, setModalActivePhase] = useState('phase1');
  const [aiEnabled, setAiEnabled] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState('');
  
  // Simple AI Hooks (clean implementation)
  const { isLoading: aiLoading, isReady: aiReady, error: aiError } = useSimpleAI();
  const { 
    content: aiOpportunitiesContent, 
    isProcessing: processingOpportunities 
  } = useSimplePageContent(project?.claudePhases, 'opportunities', refreshTrigger);
  
  const { 
    content: aiStrategyContent, 
    isProcessing: processingStrategy 
  } = useSimplePageContent(project?.claudePhases, 'strategy', refreshTrigger);
  
  const { 
    content: aiTimelineContent, 
    isProcessing: processingTimeline 
  } = useSimplePageContent(project?.claudePhases, 'timeline', refreshTrigger);
  
  const { 
    content: aiMetricsContent, 
    isProcessing: processingMetrics 
  } = useSimplePageContent(project?.claudePhases, 'metrics', refreshTrigger);

  useEffect(() => {
    loadProject();
  }, [params.id]); // loadProject is stable, no need to include

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

  const extractInsights = () => {
    if (!project) return { opportunities: [], threats: [], recommendations: [], metrics: [] };
    
    const allResponses = Object.values(project.claudePhases)
      .map(phase => phase.response)
      .join('\n\n');

    // Simple keyword-based extraction
    const opportunities = extractSections(allResponses, ['opportunity', 'opportunities', 'growth', 'potential']);
    const threats = extractSections(allResponses, ['threat', 'risk', 'challenge', 'weakness']);
    const recommendations = extractSections(allResponses, ['recommend', 'should', 'strategy', 'implement']);
    const metrics = extractSections(allResponses, ['metric', 'kpi', 'measure', 'track', 'roi']);

    return { opportunities, threats, recommendations, metrics };
  };

  const extractSections = (text: string, keywords: string[]): string[] => {
    const sentences = text.split(/[.!?]\s+/);
    return sentences
      .filter(sentence => 
        keywords.some(keyword => 
          sentence.toLowerCase().includes(keyword.toLowerCase())
        )
      )
      .slice(0, 5) // Limit to 5 items per category
      .map(sentence => sentence.trim())
      .filter(sentence => sentence.length > 20);
  };

  const updatePhaseResponse = async (phase: string, response: string) => {
    if (!project) return;

    const updatedPhases = {
      ...project.claudePhases,
      [phase]: {
        ...project.claudePhases[phase as keyof typeof project.claudePhases],
        response,
        completed: response.trim().length > 0,
        lastModified: new Date(),
      }
    };

    const updatedProject = {
      ...project,
      claudePhases: updatedPhases,
      lastModified: new Date(),
    };

    try {
      await storage.saveProject(updatedProject);
      setProject(updatedProject);
    } catch (error) {
      console.error('Failed to save project:', error);
    }
  };

  const getTabContent = (tab: string): string => {
    if (!project?.tabContent) return '';
    return project.tabContent[tab] || '';
  };

  const updateTabContent = async (tab: string, content: string) => {
    if (!project) return;

    const updatedProject = {
      ...project,
      tabContent: {
        ...project.tabContent,
        [tab]: content
      },
      lastModified: new Date(),
    };

    try {
      await storage.saveProject(updatedProject);
      setProject(updatedProject);
    } catch (error) {
      console.error('Failed to save project:', error);
    }
  };

  const extractSectionsFromResearch = (specificPhase?: string) => {
    if (!project) return [];
    
    const sections: Array<{id: string, title: string, content: string, phase: string}> = [];
    
    const phasesToProcess = specificPhase ? { [specificPhase]: project.claudePhases[specificPhase] } : project.claudePhases;
    
    Object.entries(phasesToProcess).forEach(([phaseKey, phaseData]) => {
      if (!phaseData.response) return;
      
      const lines = phaseData.response.split('\n');
      let currentSection = '';
      let currentContent: string[] = [];
      
      lines.forEach((line) => {
        const trimmedLine = line.trim();
        
        // Check for H1 or H2 headings
        if (trimmedLine.match(/^#{1,2}\s+(.+)/)) {
          // Save previous section if it exists
          if (currentSection && currentContent.length > 0) {
            sections.push({
              id: `${phaseKey}-${sections.length}`,
              title: currentSection,
              content: currentContent.join('\n').trim(),
              phase: `Phase ${phaseKey.slice(-1)}`
            });
          }
          
          // Start new section
          currentSection = trimmedLine.replace(/^#{1,2}\s+/, '');
          currentContent = [];
        } else if (currentSection && trimmedLine.length > 0) {
          currentContent.push(line);
        }
      });
      
      // Add the last section
      if (currentSection && currentContent.length > 0) {
        sections.push({
          id: `${phaseKey}-${sections.length}`,
          title: currentSection,
          content: currentContent.join('\n').trim(),
          phase: `Phase ${phaseKey.slice(-1)}`
        });
      }
    });
    
    return sections;
  };

  const openDataSelector = (tab: string) => {
    setTargetTab(tab);
    setShowDataSelector(true);
  };

  const selectDataForTab = async (sectionData: string) => {
    if (!targetTab) return;
    
    const currentContent = getTabContent(targetTab);
    const newContent = currentContent ? `${currentContent}\n\n${sectionData}` : sectionData;
    
    await updateTabContent(targetTab, newContent);
    setShowDataSelector(false);
    setTargetTab('');
  };

  const exportToText = () => {
    if (!project) return;
    
    const exportData = `
${project.name} - Strategic Analysis Report
Generated: ${new Date().toLocaleDateString()}
Service Package: ${project.businessData.servicePackage}
Industry: ${project.businessData.industry}
Location: ${project.businessData.location}

=== EXECUTIVE SUMMARY ===
Business: ${project.businessData.businessName}
Description: ${project.businessData.description}
Unique Value: ${project.businessData.uniqueValue}
Target Audience: ${project.businessData.targetAudience}
Primary Goal: ${project.businessData.primaryGoal}
Budget Range: ${project.businessData.budgetRange}

=== RESEARCH PHASES ===
${Object.entries(project.claudePhases).map(([phaseKey, phaseData]) => `
PHASE ${phaseKey.slice(-1)}: ${getPhaseTitle(phaseKey)}
${phaseData.response || 'No response provided'}
`).join('\n')}

=== SUCCESS METRICS ===
${project.businessData.successMetrics}

=== CHALLENGES ===
${project.businessData.biggestChallenges}
    `.trim();

    const blob = new Blob([exportData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project.name}-strategic-analysis.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getServicePackageStrategy = (servicePackage: ServicePackage) => {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return {
          title: 'PPC Campaign Strategy',
          color: 'blue',
          icon: TrendingUp,
          focus: 'Paid Advertising Excellence'
        };
      case ServicePackage.SEO_ONLY:
        return {
          title: 'SEO Optimization Strategy',
          color: 'green',
          icon: Target,
          focus: 'Organic Search Dominance'
        };
      case ServicePackage.PPC_SEO_COMBINED:
        return {
          title: 'Integrated Marketing Strategy',
          color: 'purple',
          icon: BarChart3,
          focus: 'Unified Digital Presence'
        };
      default:
        return {
          title: 'Digital Marketing Strategy',
          color: 'gray',
          icon: TrendingUp,
          focus: 'Digital Growth'
        };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Project not found</p>
        </div>
      </div>
    );
  }

  const insights = extractInsights();
  const strategy = getServicePackageStrategy(project.businessData.servicePackage);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link
                href={`/projects/${project.id}`}
                className="flex items-center text-gray-600 hover:text-gray-900 mr-4"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Research
              </Link>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{project.name} - Strategic Analysis</h1>
                <p className="text-sm text-gray-500">{strategy.title}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Analysis Complete
              </span>
              <Link
                href={`/projects/${project.id}/implementation`}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                <Calendar className="h-4 w-4 mr-2" />
                Implementation Plan
              </Link>
              <button 
                onClick={exportToText}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <Download className="h-4 w-4 mr-2" />
                Export Report
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Executive Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <strategy.icon className={`h-8 w-8 text-${strategy.color}-600`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Strategy Focus</p>
                <p className="text-lg font-bold text-gray-900">{strategy.focus}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Lightbulb className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Opportunities</p>
                <p className="text-2xl font-bold text-gray-900">{insights.opportunities.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-8 w-8 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Risk Factors</p>
                <p className="text-2xl font-bold text-gray-900">{insights.threats.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Target className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Action Items</p>
                <p className="text-2xl font-bold text-gray-900">{insights.recommendations.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', name: 'Executive Overview', icon: BarChart3 },
                { id: 'opportunities', name: 'Market Opportunities', icon: Lightbulb },
                { id: 'strategy', name: 'Implementation Strategy', icon: Target },
                { id: 'timeline', name: 'Roadmap & Timeline', icon: Calendar },
                { id: 'metrics', name: 'Success Metrics', icon: PieChart },
                { id: 'research', name: 'Research Data', icon: FileText }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="h-4 w-4 mr-2" />
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Executive Summary</h2>
                  <div className="bg-gray-50 rounded-lg p-6">
                    <p className="text-gray-700">
                      Comprehensive strategic analysis completed for <strong>{project.name}</strong> in the {project.businessData.industry} industry. 
                      The research reveals significant opportunities for {strategy.focus.toLowerCase()} with a focus on {project.businessData.primaryGoal.replace('_', ' ')}.
                      Budget allocation of {project.businessData.budgetRange.replace('_', ' ')} provides substantial opportunity for market penetration.
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-3">Key Strengths</h3>
                    <div className="space-y-2">
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-green-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">Unique value proposition: {project.businessData.uniqueValue}</p>
                      </div>
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-green-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">Established in {project.businessData.location} market</p>
                      </div>
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-green-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">Clear target audience: {project.businessData.targetAudience}</p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-3">Strategic Priorities</h3>
                    <div className="space-y-2">
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">{strategy.focus} implementation</p>
                      </div>
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">Market positioning optimization</p>
                      </div>
                      <div className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 mr-3"></div>
                        <p className="text-sm text-gray-700">Performance measurement framework</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'opportunities' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <h2 className="text-xl font-semibold text-gray-900">Market Opportunities</h2>
                    <AIStatusIndicator 
                      status={aiReady ? 'ready' : aiLoading ? 'loading' : aiError ? 'error' : 'unloaded'}
                      onRetry={() => window.location.reload()}
                    />
                  </div>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => {
                        setAiEnabled(!aiEnabled);
                        if (aiEnabled) setRefreshTrigger(Date.now().toString());
                      }}
                      className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                        aiEnabled 
                          ? 'text-blue-600 bg-blue-50 border border-blue-200 hover:bg-blue-100' 
                          : 'text-gray-600 bg-gray-50 border border-gray-200 hover:bg-gray-100'
                      }`}
                    >
                      <Sparkles className="h-4 w-4 mr-2 inline" />
                      {aiEnabled ? 'AI On' : 'AI Off'}
                    </button>
                    <button
                      onClick={() => setEditingContent(editingContent === 'opportunities' ? '' : 'opportunities')}
                      className="px-4 py-2 text-sm font-medium text-purple-600 bg-purple-50 border border-purple-200 rounded-md hover:bg-purple-100 transition-colors"
                    >
                      <Edit className="h-4 w-4 mr-2 inline" />
                      {editingContent === 'opportunities' ? 'Stop Editing' : 'Edit Content'}
                    </button>
                    <button
                      onClick={() => openDataSelector('opportunities')}
                      className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      <Plus className="h-4 w-4 mr-2 inline" />
                      Add from Research
                    </button>
                  </div>
                </div>

                {/* AI-Generated Summary */}
                {aiEnabled && aiReady && aiOpportunitiesContent && !editingContent && (
                  <div className="mb-6">
                    <SmartSummaryCard
                      title="AI-Generated Market Opportunities Summary"
                      content={aiOpportunitiesContent.summary}
                      confidence={aiOpportunitiesContent.confidence}
                      sources={aiOpportunitiesContent.sources}
                      actionable={true}
                      onActionClick={() => {
                        // Auto-fill with AI content if tab is empty
                        if (!getTabContent('opportunities')) {
                          updateTabContent('opportunities', aiOpportunitiesContent.summary);
                        }
                      }}
                    />
                  </div>
                )}

                {/* Processing Indicator */}
                {aiEnabled && processingOpportunities && (
                  <div className="mb-6 text-center py-8 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="inline-flex items-center text-blue-600">
                      <Sparkles className="h-5 w-5 mr-2 animate-pulse" />
                      <span>AI is analyzing market opportunities...</span>
                    </div>
                  </div>
                )}

                {getTabContent('opportunities') ? (
                  editingContent === 'opportunities' ? (
                    <div className="space-y-4">
                      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                        <p className="text-yellow-800 text-sm">
                          <strong>Editing Mode:</strong> Make changes to the Market Opportunities content below. 
                          Changes are saved automatically.
                        </p>
                      </div>
                      <textarea
                        className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        rows={20}
                        placeholder="Enter market opportunities content..."
                        value={getTabContent('opportunities')}
                        onChange={(e) => updateTabContent('opportunities', e.target.value)}
                      />
                    </div>
                  ) : (
                    <div className="bg-white border border-gray-200 rounded-lg p-6">
                      <FormattedText 
                        text={getTabContent('opportunities')}
                        className="text-gray-700"
                      />
                    </div>
                  )
                ) : (
                  <div className="space-y-6">
                    {/* Empty State */}
                    <div className="text-center py-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                      <Lightbulb className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No Market Opportunities Added Yet</h3>
                      <p className="text-gray-500 mb-6">
                        {aiEnabled && aiReady 
                          ? 'AI is ready to analyze your research data, or you can manually add content.' 
                          : 'Select relevant sections from your research data to build your market opportunities analysis.'}
                      </p>
                      <div className="flex items-center justify-center space-x-3">
                        {aiEnabled && aiReady && aiOpportunitiesContent && (
                          <button
                            onClick={() => updateTabContent('opportunities', aiOpportunitiesContent.summary)}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                          >
                            <Sparkles className="h-4 w-4 mr-2" />
                            Use AI Summary
                          </button>
                        )}
                        <button
                          onClick={() => openDataSelector('opportunities')}
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add from Research Data
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'strategy' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <h2 className="text-xl font-semibold text-gray-900">Implementation Strategy</h2>
                    <AIStatusIndicator 
                      status={aiReady ? 'ready' : aiLoading ? 'loading' : aiError ? 'error' : 'unloaded'}
                    />
                  </div>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setEditingContent(editingContent === 'strategy' ? '' : 'strategy')}
                      className="px-4 py-2 text-sm font-medium text-purple-600 bg-purple-50 border border-purple-200 rounded-md hover:bg-purple-100 transition-colors"
                    >
                      <Edit className="h-4 w-4 mr-2 inline" />
                      {editingContent === 'strategy' ? 'Stop Editing' : 'Edit Content'}
                    </button>
                    <button
                      onClick={() => openDataSelector('strategy')}
                      className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      <Plus className="h-4 w-4 mr-2 inline" />
                      Add from Research
                    </button>
                  </div>
                </div>

                {/* AI-Generated Summary */}
                {aiEnabled && aiReady && aiStrategyContent && !editingContent && (
                  <div className="mb-6">
                    <SmartSummaryCard
                      title="AI-Generated Implementation Strategy Summary"
                      content={aiStrategyContent.summary}
                      confidence={aiStrategyContent.confidence}
                      sources={aiStrategyContent.sources}
                      actionable={true}
                      onActionClick={() => {
                        if (!getTabContent('strategy')) {
                          updateTabContent('strategy', aiStrategyContent.summary);
                        }
                      }}
                    />
                  </div>
                )}

                {/* Processing Indicator */}
                {aiEnabled && processingStrategy && (
                  <div className="mb-6 text-center py-8 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="inline-flex items-center text-blue-600">
                      <Sparkles className="h-5 w-5 mr-2 animate-pulse" />
                      <span>AI is analyzing implementation strategy...</span>
                    </div>
                  </div>
                )}

                {getTabContent('strategy') ? (
                  editingContent === 'strategy' ? (
                    <div className="space-y-4">
                      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                        <p className="text-yellow-800 text-sm">
                          <strong>Editing Mode:</strong> Make changes to the Implementation Strategy content below. 
                          Changes are saved automatically.
                        </p>
                      </div>
                      <textarea
                        className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        rows={20}
                        placeholder="Enter implementation strategy content..."
                        value={getTabContent('strategy')}
                        onChange={(e) => updateTabContent('strategy', e.target.value)}
                      />
                    </div>
                  ) : (
                    <div className="bg-white border border-gray-200 rounded-lg p-6">
                      <FormattedText 
                        text={getTabContent('strategy')}
                        className="text-gray-700"
                      />
                    </div>
                  )
                ) : (
                  <div className="space-y-6">
                    <div className="text-center py-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                      <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No Implementation Strategy Added Yet</h3>
                      <p className="text-gray-500 mb-6">
                        {aiEnabled && aiReady 
                          ? 'AI is ready to analyze your research data, or you can manually add content.' 
                          : 'Select relevant sections from your research data to build your implementation strategy.'}
                      </p>
                      <div className="flex items-center justify-center space-x-3">
                        {aiEnabled && aiReady && aiStrategyContent && (
                          <button
                            onClick={() => updateTabContent('strategy', aiStrategyContent.summary)}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                          >
                            <Sparkles className="h-4 w-4 mr-2" />
                            Use AI Summary
                          </button>
                        )}
                        <button
                          onClick={() => openDataSelector('strategy')}
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add from Research Data
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'timeline' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <h2 className="text-xl font-semibold text-gray-900">Roadmap & Timeline</h2>
                    <AIStatusIndicator 
                      status={aiReady ? 'ready' : aiLoading ? 'loading' : aiError ? 'error' : 'unloaded'}
                    />
                  </div>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setEditingContent(editingContent === 'timeline' ? '' : 'timeline')}
                      className="px-4 py-2 text-sm font-medium text-purple-600 bg-purple-50 border border-purple-200 rounded-md hover:bg-purple-100 transition-colors"
                    >
                      <Edit className="h-4 w-4 mr-2 inline" />
                      {editingContent === 'timeline' ? 'Stop Editing' : 'Edit Content'}
                    </button>
                    <button
                      onClick={() => openDataSelector('timeline')}
                      className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      <Plus className="h-4 w-4 mr-2 inline" />
                      Add from Research
                    </button>
                  </div>
                </div>

                {/* AI-Generated Summary */}
                {aiEnabled && aiReady && aiTimelineContent && !editingContent && (
                  <div className="mb-6">
                    <SmartSummaryCard
                      title="AI-Generated Roadmap & Timeline Summary"
                      content={aiTimelineContent.summary}
                      confidence={aiTimelineContent.confidence}
                      sources={aiTimelineContent.sources}
                      actionable={true}
                      onActionClick={() => {
                        if (!getTabContent('timeline')) {
                          updateTabContent('timeline', aiTimelineContent.summary);
                        }
                      }}
                    />
                  </div>
                )}

                {/* Processing Indicator */}
                {aiEnabled && processingTimeline && (
                  <div className="mb-6 text-center py-8 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="inline-flex items-center text-blue-600">
                      <Sparkles className="h-5 w-5 mr-2 animate-pulse" />
                      <span>AI is analyzing roadmap and timeline...</span>
                    </div>
                  </div>
                )}

                {getTabContent('timeline') ? (
                  editingContent === 'timeline' ? (
                    <div className="space-y-4">
                      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                        <p className="text-yellow-800 text-sm">
                          <strong>Editing Mode:</strong> Make changes to the Roadmap & Timeline content below. 
                          Changes are saved automatically.
                        </p>
                      </div>
                      <textarea
                        className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        rows={20}
                        placeholder="Enter roadmap and timeline content..."
                        value={getTabContent('timeline')}
                        onChange={(e) => updateTabContent('timeline', e.target.value)}
                      />
                    </div>
                  ) : (
                    <div className="bg-white border border-gray-200 rounded-lg p-6">
                      <FormattedText 
                        text={getTabContent('timeline')}
                        className="text-gray-700"
                      />
                    </div>
                  )
                ) : (
                  <div className="space-y-6">
                    <div className="text-center py-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                      <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No Roadmap & Timeline Added Yet</h3>
                      <p className="text-gray-500 mb-6">
                        {aiEnabled && aiReady 
                          ? 'AI is ready to analyze your research data, or you can manually add content.' 
                          : 'Select relevant sections from your research data to build your implementation roadmap.'}
                      </p>
                      <div className="flex items-center justify-center space-x-3">
                        {aiEnabled && aiReady && aiTimelineContent && (
                          <button
                            onClick={() => updateTabContent('timeline', aiTimelineContent.summary)}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                          >
                            <Sparkles className="h-4 w-4 mr-2" />
                            Use AI Summary
                          </button>
                        )}
                        <button
                          onClick={() => openDataSelector('timeline')}
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add from Research Data
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'metrics' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <h2 className="text-xl font-semibold text-gray-900">Success Metrics</h2>
                    <AIStatusIndicator 
                      status={aiReady ? 'ready' : aiLoading ? 'loading' : aiError ? 'error' : 'unloaded'}
                    />
                  </div>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setEditingContent(editingContent === 'metrics' ? '' : 'metrics')}
                      className="px-4 py-2 text-sm font-medium text-purple-600 bg-purple-50 border border-purple-200 rounded-md hover:bg-purple-100 transition-colors"
                    >
                      <Edit className="h-4 w-4 mr-2 inline" />
                      {editingContent === 'metrics' ? 'Stop Editing' : 'Edit Content'}
                    </button>
                    <button
                      onClick={() => openDataSelector('metrics')}
                      className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      <Plus className="h-4 w-4 mr-2 inline" />
                      Add from Research
                    </button>
                  </div>
                </div>

                {/* AI-Generated Summary */}
                {aiEnabled && aiReady && aiMetricsContent && !editingContent && (
                  <div className="mb-6">
                    <SmartSummaryCard
                      title="AI-Generated Success Metrics Summary"
                      content={aiMetricsContent.summary}
                      confidence={aiMetricsContent.confidence}
                      sources={aiMetricsContent.sources}
                      actionable={true}
                      onActionClick={() => {
                        if (!getTabContent('metrics')) {
                          updateTabContent('metrics', aiMetricsContent.summary);
                        }
                      }}
                    />
                  </div>
                )}

                {/* Processing Indicator */}
                {aiEnabled && processingMetrics && (
                  <div className="mb-6 text-center py-8 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="inline-flex items-center text-blue-600">
                      <Sparkles className="h-5 w-5 mr-2 animate-pulse" />
                      <span>AI is analyzing success metrics...</span>
                    </div>
                  </div>
                )}

                {getTabContent('metrics') ? (
                  editingContent === 'metrics' ? (
                    <div className="space-y-4">
                      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                        <p className="text-yellow-800 text-sm">
                          <strong>Editing Mode:</strong> Make changes to the Success Metrics content below. 
                          Changes are saved automatically.
                        </p>
                      </div>
                      <textarea
                        className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        rows={20}
                        placeholder="Enter success metrics content..."
                        value={getTabContent('metrics')}
                        onChange={(e) => updateTabContent('metrics', e.target.value)}
                      />
                    </div>
                  ) : (
                    <div className="bg-white border border-gray-200 rounded-lg p-6">
                      <FormattedText 
                        text={getTabContent('metrics')}
                        className="text-gray-700"
                      />
                    </div>
                  )
                ) : (
                  <div className="space-y-6">
                    <div className="text-center py-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                      <PieChart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No Success Metrics Added Yet</h3>
                      <p className="text-gray-500 mb-6">
                        {aiEnabled && aiReady 
                          ? 'AI is ready to analyze your research data, or you can manually add content.' 
                          : 'Select relevant sections from your research data to build your success metrics framework.'}
                      </p>
                      <div className="flex items-center justify-center space-x-3">
                        {aiEnabled && aiReady && aiMetricsContent && (
                          <button
                            onClick={() => updateTabContent('metrics', aiMetricsContent.summary)}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                          >
                            <Sparkles className="h-4 w-4 mr-2" />
                            Use AI Summary
                          </button>
                        )}
                        <button
                          onClick={() => openDataSelector('metrics')}
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add from Research Data
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'research' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900">Research Data by Phase</h2>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setEditMode(!editMode)}
                      className="px-4 py-2 text-sm font-medium text-purple-600 bg-purple-50 border border-purple-200 rounded-md hover:bg-purple-100 transition-colors"
                    >
                      <Edit className="h-4 w-4 mr-2 inline" />
                      {editMode ? 'Stop Editing' : 'Edit Phase'}
                    </button>
                    <button
                      onClick={() => setShowFullText(!showFullText)}
                      className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      {showFullText ? 'Show Formatted' : 'Show Raw Text'}
                    </button>
                  </div>
                </div>

                {/* Phase Sub-tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8" aria-label="Research phases">
                    {Object.entries(project.claudePhases).map(([phaseKey, phaseData]) => (
                      <button
                        key={phaseKey}
                        onClick={() => setActivePhase(phaseKey)}
                        className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap flex items-center ${
                          activePhase === phaseKey
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        <div className={`w-6 h-6 rounded-full text-xs font-medium flex items-center justify-center mr-2 ${
                          activePhase === phaseKey 
                            ? 'bg-blue-100 text-blue-600' 
                            : phaseData.completed 
                              ? 'bg-green-100 text-green-600' 
                              : 'bg-gray-100 text-gray-500'
                        }`}>
                          {phaseKey.slice(-1)}
                        </div>
                        Phase {phaseKey.slice(-1)}
                        {phaseData.completed && (
                          <CheckCircle className="h-4 w-4 text-green-500 ml-2" />
                        )}
                      </button>
                    ))}
                  </nav>
                </div>

                {/* Active Phase Content */}
                <div className="bg-white border border-gray-200 rounded-lg">
                  <div className="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
                    <div className="flex items-center justify-between">
                      <h3 className="text-xl font-semibold text-gray-900 flex items-center">
                        <div className="w-10 h-10 rounded-full bg-blue-600 text-white text-lg font-bold flex items-center justify-center mr-4">
                          {activePhase.slice(-1)}
                        </div>
                        {getPhaseTitle(activePhase)}
                      </h3>
                      <div className="flex items-center space-x-2">
                        {project.claudePhases[activePhase].completed ? (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Completed
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                            <Clock className="h-4 w-4 mr-1" />
                            In Progress
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    {project.claudePhases[activePhase].response ? (
                      editMode ? (
                        <div className="space-y-4">
                          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                            <p className="text-yellow-800 text-sm">
                              <strong>Editing Mode:</strong> Make changes to the Phase {activePhase.slice(-1)} response below. 
                              Changes are saved automatically.
                            </p>
                          </div>
                          <textarea
                            className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                            rows={25}
                            placeholder="Enter Claude AI response for this phase..."
                            value={project.claudePhases[activePhase].response}
                            onChange={(e) => updatePhaseResponse(activePhase, e.target.value)}
                          />
                          <div className="text-sm text-gray-500">
                            {project.claudePhases[activePhase].response.length} characters | 
                            Last updated: {project.claudePhases[activePhase].lastModified.toLocaleDateString()}
                          </div>
                        </div>
                      ) : showFullText ? (
                        <div className="bg-gray-50 rounded-lg p-4">
                          <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed font-mono">
                            {project.claudePhases[activePhase].response}
                          </pre>
                        </div>
                      ) : (
                        <FormattedText 
                          text={project.claudePhases[activePhase].response}
                          className="text-gray-700"
                        />
                      )
                    ) : (
                      <div className="text-center py-12">
                        <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-500 italic">No response data available for this phase.</p>
                        <p className="text-gray-400 text-sm mt-2">
                          {editMode ? 'Use the text area above to add content for this phase.' : 'Complete the research for Phase ' + activePhase.slice(-1) + ' to see content here.'}
                        </p>
                        {editMode && (
                          <div className="mt-6">
                            <textarea
                              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                              rows={15}
                              placeholder="Enter Claude AI response for this phase..."
                              value=""
                              onChange={(e) => updatePhaseResponse(activePhase, e.target.value)}
                            />
                          </div>
                        )}
                      </div>
                    )}
                    
                    {!editMode && project.claudePhases[activePhase].response && (
                      <div className="mt-6 flex items-center justify-between border-t pt-4">
                        <div className="flex space-x-3">
                          {Object.keys(project.claudePhases).indexOf(activePhase) > 0 && (
                            <button
                              onClick={() => {
                                const phases = Object.keys(project.claudePhases);
                                const currentIndex = phases.indexOf(activePhase);
                                setActivePhase(phases[currentIndex - 1]);
                              }}
                              className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                            >
                              <ArrowLeft className="h-4 w-4 mr-1" />
                              Previous Phase
                            </button>
                          )}
                          {Object.keys(project.claudePhases).indexOf(activePhase) < Object.keys(project.claudePhases).length - 1 && (
                            <button
                              onClick={() => {
                                const phases = Object.keys(project.claudePhases);
                                const currentIndex = phases.indexOf(activePhase);
                                setActivePhase(phases[currentIndex + 1]);
                              }}
                              className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                            >
                              Next Phase
                              <ArrowLeft className="h-4 w-4 ml-1 rotate-180" />
                            </button>
                          )}
                        </div>
                        
                        <div className="text-sm text-gray-500">
                          Phase {activePhase.slice(-1)} of {Object.keys(project.claudePhases).length}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Data Selector Modal */}
        {showDataSelector && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" onClick={() => setShowDataSelector(false)}>
            <div className="relative top-12 mx-auto p-6 border w-3/4 h-3/4 shadow-lg rounded-md bg-white flex flex-col" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between pb-3 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">
                  Select Research Data to Add to {targetTab === 'opportunities' ? 'Market Opportunities' : 
                                                  targetTab === 'strategy' ? 'Implementation Strategy' : 
                                                  targetTab === 'timeline' ? 'Roadmap & Timeline' : 
                                                  targetTab === 'metrics' ? 'Success Metrics' : targetTab}
                </h3>
                <button
                  onClick={() => setShowDataSelector(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              {/* Phase Selection Tabs */}
              <div className="border-b border-gray-200 mt-4">
                <nav className="-mb-px flex space-x-8" aria-label="Research phases">
                  {Object.entries(project.claudePhases).map(([phaseKey, phaseData]) => (
                    <button
                      key={phaseKey}
                      onClick={() => setModalActivePhase(phaseKey)}
                      className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap flex items-center ${
                        modalActivePhase === phaseKey
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      <div className={`w-6 h-6 rounded-full text-xs font-medium flex items-center justify-center mr-2 ${
                        modalActivePhase === phaseKey 
                          ? 'bg-blue-100 text-blue-600' 
                          : phaseData.completed 
                            ? 'bg-green-100 text-green-600' 
                            : 'bg-gray-100 text-gray-500'
                      }`}>
                        {phaseKey.slice(-1)}
                      </div>
                      Phase {phaseKey.slice(-1)}
                      {phaseData.completed && (
                        <CheckCircle className="h-4 w-4 text-green-500 ml-2" />
                      )}
                    </button>
                  ))}
                </nav>
              </div>
              
              {/* Content Area */}
              <div className="flex-1 mt-4 overflow-y-auto">
                <div className="space-y-4">
                  {extractSectionsFromResearch(modalActivePhase).map((section) => (
                    <div key={section.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors" 
                         onClick={() => selectDataForTab(section.content)}>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {section.phase}
                            </span>
                            <h4 className="text-sm font-medium text-gray-900">{section.title}</h4>
                          </div>
                          <div className="text-sm text-gray-600">
                            <FormattedText text={section.content.substring(0, 300) + (section.content.length > 300 ? '...' : '')} />
                          </div>
                        </div>
                        <Plus className="h-5 w-5 text-blue-600 ml-4 flex-shrink-0" />
                      </div>
                    </div>
                  ))}
                </div>
                
                {extractSectionsFromResearch(modalActivePhase).length === 0 && (
                  <div className="text-center py-12">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No research sections available in Phase {modalActivePhase.slice(-1)}.</p>
                    <p className="text-gray-400 text-sm mt-2">
                      {project.claudePhases[modalActivePhase].completed 
                        ? 'This phase has no H1/H2 sections to extract.' 
                        : 'Complete this research phase to add content.'}
                    </p>
                  </div>
                )}
              </div>
              
              <div className="mt-6 flex justify-end space-x-3 border-t pt-4">
                <button
                  onClick={() => setShowDataSelector(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  function getPhaseTitle(phaseKey: string): string {
    const titles = {
      phase1: 'Business Intelligence Analysis',
      phase2: 'Competitive Landscape Mapping',
      phase3: 'Market Gap Identification',
      phase4: 'Strategic Positioning Development',
      phase5: 'Content & Campaign Strategy',
    };
    return titles[phaseKey as keyof typeof titles] || 'Research Phase';
  }
}