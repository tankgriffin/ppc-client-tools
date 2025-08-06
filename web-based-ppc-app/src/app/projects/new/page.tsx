'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Project, ProjectStatus, BusinessIntelligence, CampaignGoal, BudgetRange, ServicePackage } from '@/types';
import { storage } from '@/lib/storage';
import { ClaudePromptGenerator } from '@/lib/prompt-generator';
import { v4 as uuidv4 } from 'uuid';
import { ArrowLeft, Save, RefreshCw } from 'lucide-react';
import Link from 'next/link';

export default function NewProject() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 4;

  const [businessData, setBusinessData] = useState<BusinessIntelligence>({
    businessName: '',
    industry: '',
    website: '',
    location: '',
    serviceArea: '',
    description: '',
    services: '',
    uniqueValue: '',
    targetAudience: '',
    customerPainPoints: '',
    competitors: [],
    servicePackage: ServicePackage.PPC_ONLY,
    primaryGoal: CampaignGoal.LEAD_GENERATION,
    budgetRange: BudgetRange.RANGE_1K_5K,
    successMetrics: '',
    seasonalTrends: '',
    currentMarketing: '',
    biggestChallenges: '',
  });

  const updateBusinessData = (field: keyof BusinessIntelligence, value: string | string[] | CampaignGoal | BudgetRange | ServicePackage) => {
    setBusinessData(prev => ({ ...prev, [field]: value }));
  };

  const addCompetitor = () => {
    if (businessData.competitors.length < 10) {
      setBusinessData(prev => ({
        ...prev,
        competitors: [...prev.competitors, '']
      }));
    }
  };

  const updateCompetitor = (index: number, value: string) => {
    setBusinessData(prev => ({
      ...prev,
      competitors: prev.competitors.map((comp, i) => i === index ? value : comp)
    }));
  };

  const removeCompetitor = (index: number) => {
    setBusinessData(prev => ({
      ...prev,
      competitors: prev.competitors.filter((_, i) => i !== index)
    }));
  };

  const handleSaveProject = async () => {
    setLoading(true);
    try {
      const claudePhases = ClaudePromptGenerator.generateAllPrompts(businessData);
      
      const newProject: Project = {
        id: uuidv4(),
        name: businessData.businessName,
        industry: businessData.industry,
        created: new Date(),
        lastModified: new Date(),
        completionStatus: ProjectStatus.DRAFT,
        businessData,
        claudePhases,
        assets: [],
        analysis: {
          executiveSummary: '',
          competitiveAdvantages: [],
          marketOpportunities: [],
          implementationRoadmap: [],
          riskAssessment: [],
          keyMetrics: [],
        },
      };

      await storage.saveProject(newProject);
      router.push(`/projects/${newProject.id}`);
    } catch (error) {
      console.error('Failed to save project:', error);
      alert('Failed to save project. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isStepValid = (step: number) => {
    switch (step) {
      case 1:
        return businessData.businessName && businessData.industry && businessData.location;
      case 2:
        return businessData.description && businessData.services && businessData.uniqueValue;
      case 3:
        return businessData.targetAudience && businessData.customerPainPoints;
      case 4:
        return businessData.servicePackage && businessData.successMetrics;
      default:
        return false;
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Business Overview</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Business Name *
                </label>
                <input
                  type="text"
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.businessName}
                  onChange={(e) => updateBusinessData('businessName', e.target.value)}
                  placeholder="Enter your business name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry *
                </label>
                <input
                  type="text"
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.industry}
                  onChange={(e) => updateBusinessData('industry', e.target.value)}
                  placeholder="e.g., Legal Services, Healthcare, Real Estate"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Website
                </label>
                <input
                  type="url"
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.website}
                  onChange={(e) => updateBusinessData('website', e.target.value)}
                  placeholder="https://yourwebsite.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Primary Location *
                </label>
                <input
                  type="text"
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.location}
                  onChange={(e) => updateBusinessData('location', e.target.value)}
                  placeholder="City, State"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Service Area
              </label>
              <input
                type="text"
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.serviceArea}
                onChange={(e) => updateBusinessData('serviceArea', e.target.value)}
                placeholder="Geographic area you serve (e.g., Greater Boston Area, Nationwide)"
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Business Details</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Business Description *
              </label>
              <textarea
                rows={4}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.description}
                onChange={(e) => updateBusinessData('description', e.target.value)}
                placeholder="Describe what your business does, your mission, and what makes you unique"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Services Offered *
              </label>
              <textarea
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.services}
                onChange={(e) => updateBusinessData('services', e.target.value)}
                placeholder="List your main services or products"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Unique Value Proposition *
              </label>
              <textarea
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.uniqueValue}
                onChange={(e) => updateBusinessData('uniqueValue', e.target.value)}
                placeholder="What makes you different from competitors? Why should customers choose you?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Marketing Efforts
              </label>
              <textarea
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.currentMarketing}
                onChange={(e) => updateBusinessData('currentMarketing', e.target.value)}
                placeholder="Describe your current marketing channels and strategies"
              />
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Target Market</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience *
              </label>
              <textarea
                rows={4}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.targetAudience}
                onChange={(e) => updateBusinessData('targetAudience', e.target.value)}
                placeholder="Describe your ideal customers (demographics, psychographics, behaviors)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Customer Pain Points *
              </label>
              <textarea
                rows={4}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.customerPainPoints}
                onChange={(e) => updateBusinessData('customerPainPoints', e.target.value)}
                placeholder="What problems do your customers face that you solve?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Known Competitors
              </label>
              <div className="space-y-2">
                {businessData.competitors.map((competitor, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <input
                      type="text"
                      className="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                      value={competitor}
                      onChange={(e) => updateCompetitor(index, e.target.value)}
                      placeholder="Competitor name"
                    />
                    <button
                      type="button"
                      onClick={() => removeCompetitor(index)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={addCompetitor}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  + Add Competitor
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Seasonal Trends
              </label>
              <textarea
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.seasonalTrends}
                onChange={(e) => updateBusinessData('seasonalTrends', e.target.value)}
                placeholder="How does your business performance vary by season or time of year?"
              />
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Service Package & Goals</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Service Package *
              </label>
              <select
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.servicePackage}
                onChange={(e) => updateBusinessData('servicePackage', e.target.value as ServicePackage)}
              >
                <option value={ServicePackage.PPC_ONLY}>PPC Only</option>
                <option value={ServicePackage.SEO_ONLY}>SEO Only</option>
                <option value={ServicePackage.PPC_SEO_COMBINED}>PPC + SEO Combined</option>
              </select>
              <p className="mt-1 text-sm text-gray-500">
                This determines the type of strategic analysis and recommendations you&apos;ll receive
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Primary Campaign Goal *
                </label>
                <select
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.primaryGoal}
                  onChange={(e) => updateBusinessData('primaryGoal', e.target.value as CampaignGoal)}
                >
                  <option value={CampaignGoal.LEAD_GENERATION}>Lead Generation</option>
                  <option value={CampaignGoal.SALES}>Sales</option>
                  <option value={CampaignGoal.BRAND_AWARENESS}>Brand Awareness</option>
                  <option value={CampaignGoal.WEBSITE_TRAFFIC}>Website Traffic</option>
                  <option value={CampaignGoal.LOCAL_VISIBILITY}>Local Visibility</option>
                  <option value={CampaignGoal.ECOMMERCE}>E-commerce</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Monthly Budget Range *
                </label>
                <select
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={businessData.budgetRange}
                  onChange={(e) => updateBusinessData('budgetRange', e.target.value as BudgetRange)}
                >
                  <option value={BudgetRange.UNDER_1K}>Under $1,000</option>
                  <option value={BudgetRange.RANGE_1K_5K}>$1,000 - $5,000</option>
                  <option value={BudgetRange.RANGE_5K_10K}>$5,000 - $10,000</option>
                  <option value={BudgetRange.RANGE_10K_25K}>$10,000 - $25,000</option>
                  <option value={BudgetRange.RANGE_25K_50K}>$25,000 - $50,000</option>
                  <option value={BudgetRange.OVER_50K}>Over $50,000</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Success Metrics *
              </label>
              <textarea
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.successMetrics}
                onChange={(e) => updateBusinessData('successMetrics', e.target.value)}
                placeholder="How will you measure campaign success? (e.g., leads per month, cost per acquisition, revenue targets)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Biggest Challenges
              </label>
              <textarea
                rows={4}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                value={businessData.biggestChallenges}
                onChange={(e) => updateBusinessData('biggestChallenges', e.target.value)}
                placeholder="What are your biggest marketing or business challenges?"
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link
                href="/"
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Dashboard
              </Link>
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Create New Project</h1>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>Step {currentStep} of {totalSteps}</span>
            <span>{Math.round((currentStep / totalSteps) * 100)}% Complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / totalSteps) * 100}%` }}
            />
          </div>
        </div>

        {/* Form Content */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            {renderStepContent()}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <button
              type="button"
              onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
              disabled={currentStep === 1}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>

            <div className="flex space-x-3">
              {currentStep < totalSteps ? (
                <button
                  type="button"
                  onClick={() => setCurrentStep(Math.min(totalSteps, currentStep + 1))}
                  disabled={!isStepValid(currentStep)}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleSaveProject}
                  disabled={!isStepValid(currentStep) || loading}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  ) : (
                    <Save className="h-4 w-4 mr-2" />
                  )}
                  Create Project
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}