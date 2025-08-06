'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Project, ServicePackage } from '@/types';
import { storage } from '@/lib/storage';
import { ArrowLeft, Calendar, CheckCircle, Clock, Plus, Edit3, Trash2, Target, TrendingUp, Users, DollarSign, BarChart3 } from 'lucide-react';
import Link from 'next/link';

interface ImplementationTask {
  id: string;
  title: string;
  description: string;
  category: 'setup' | 'optimization' | 'content' | 'analysis' | 'scaling';
  priority: 'high' | 'medium' | 'low';
  estimatedHours: number;
  budget?: number;
  assignedTo?: string;
  completed: boolean;
  notes: string;
}

interface MonthlyPlan {
  month: number;
  year: number;
  name: string;
  focus: string;
  budget: number;
  tasks: ImplementationTask[];
  goals: string[];
  kpis: string[];
}

export default function ImplementationPlanning() {
  const params = useParams();
  const router = useRouter();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [monthlyPlans, setMonthlyPlans] = useState<MonthlyPlan[]>([]);
  const [activeMonth, setActiveMonth] = useState(0);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [editingTask, setEditingTask] = useState<ImplementationTask | null>(null);

  useEffect(() => {
    loadProject();
  }, [params.id]);

  const loadProject = async () => {
    try {
      const projectData = await storage.getProject(params.id as string);
      if (!projectData) {
        router.push('/');
        return;
      }
      setProject(projectData);
      generateImplementationPlan(projectData);
    } catch (error) {
      console.error('Failed to load project:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateImplementationPlan = (projectData: Project) => {
    const allResponses = Object.values(projectData.claudePhases)
      .map(phase => phase.response)
      .join('\n\n');

    const extractedTasks = extractTasksFromResponses(allResponses, projectData.businessData.servicePackage);
    const plans = createMonthlyPlans(extractedTasks, projectData);
    setMonthlyPlans(plans);
  };

  const extractTasksFromResponses = (responses: string, servicePackage: ServicePackage): ImplementationTask[] => {
    const tasks: ImplementationTask[] = [];
    
    // Extract implementation tasks using keyword matching and pattern recognition
    const sentences = responses.split(/[.!?]\s+/);
    let taskId = 1;

    // Common task patterns to look for
    const taskPatterns = [
      /implement|create|develop|build|set up|establish/i,
      /optimize|improve|enhance|refine|adjust/i,
      /launch|start|begin|initiate|deploy/i,
      /monitor|track|measure|analyze|review/i,
      /scale|expand|grow|increase|extend/i
    ];

    const categoryKeywords = {
      setup: ['setup', 'create', 'establish', 'build', 'configure', 'install'],
      optimization: ['optimize', 'improve', 'enhance', 'refine', 'adjust', 'tune'],
      content: ['content', 'copy', 'creative', 'ad', 'keyword', 'landing page'],
      analysis: ['analyze', 'monitor', 'track', 'measure', 'report', 'review'],
      scaling: ['scale', 'expand', 'grow', 'increase', 'broaden', 'extend']
    };

    sentences.forEach(sentence => {
      const matchesPattern = taskPatterns.some(pattern => pattern.test(sentence));
      
      if (matchesPattern && sentence.length > 30 && sentence.length < 200) {
        const category = Object.entries(categoryKeywords).find(([, keywords]) =>
          keywords.some(keyword => sentence.toLowerCase().includes(keyword))
        )?.[0] as ImplementationTask['category'] || 'setup';

        const priority = sentence.toLowerCase().includes('critical') || sentence.toLowerCase().includes('essential') ? 'high' :
                        sentence.toLowerCase().includes('important') || sentence.toLowerCase().includes('key') ? 'medium' : 'low';

        tasks.push({
          id: `task-${taskId++}`,
          title: extractTaskTitle(sentence),
          description: sentence.trim(),
          category,
          priority,
          estimatedHours: estimateHours(sentence, category),
          completed: false,
          notes: ''
        });
      }
    });

    // Add service-package specific default tasks
    tasks.push(...getDefaultTasks(servicePackage));

    return tasks.slice(0, 24); // Limit to 24 tasks (6 per quarter)
  };

  const extractTaskTitle = (sentence: string): string => {
    // Extract a concise title from the sentence
    const words = sentence.split(' ');
    if (words.length <= 8) return sentence;
    
    // Find the main action and object
    const actionWords = ['implement', 'create', 'develop', 'build', 'set up', 'establish', 'optimize', 'launch'];
    const actionIndex = words.findIndex(word => 
      actionWords.some(action => word.toLowerCase().includes(action.toLowerCase()))
    );
    
    if (actionIndex !== -1) {
      return words.slice(actionIndex, Math.min(actionIndex + 6, words.length)).join(' ');
    }
    
    return words.slice(0, 8).join(' ') + '...';
  };

  const estimateHours = (sentence: string, category: ImplementationTask['category']): number => {
    const baseHours = {
      setup: 8,
      optimization: 4,
      content: 6,
      analysis: 3,
      scaling: 10
    };

    const complexity = sentence.toLowerCase().includes('complex') || sentence.toLowerCase().includes('comprehensive') ? 1.5 : 1;
    return Math.round(baseHours[category] * complexity);
  };

  const getDefaultTasks = (servicePackage: ServicePackage): ImplementationTask[] => {
    const baseTasks = [
      {
        id: 'default-1',
        title: 'Initial Account Setup',
        description: 'Set up tracking, analytics, and account structure',
        category: 'setup' as const,
        priority: 'high' as const,
        estimatedHours: 8,
        completed: false,
        notes: ''
      },
      {
        id: 'default-2',
        title: 'Performance Monitoring Setup',
        description: 'Establish KPI tracking and reporting systems',
        category: 'analysis' as const,
        priority: 'high' as const,
        estimatedHours: 6,
        completed: false,
        notes: ''
      }
    ];

    if (servicePackage === ServicePackage.PPC_ONLY) {
      baseTasks.push({
        id: 'default-ppc-1',
        title: 'PPC Campaign Launch',
        description: 'Launch initial PPC campaigns across selected platforms',
        category: 'setup',
        priority: 'high',
        estimatedHours: 12,
        completed: false,
        notes: ''
      });
    } else if (servicePackage === ServicePackage.SEO_ONLY) {
      baseTasks.push({
        id: 'default-seo-1',
        title: 'SEO Foundation Setup',
        description: 'Implement technical SEO and content strategy foundation',
        category: 'setup',
        priority: 'high',
        estimatedHours: 16,
        completed: false,
        notes: ''
      });
    } else {
      baseTasks.push({
        id: 'default-combined-1',
        title: 'Integrated Campaign Launch',
        description: 'Launch coordinated PPC and SEO campaigns',
        category: 'setup',
        priority: 'high',
        estimatedHours: 20,
        completed: false,
        notes: ''
      });
    }

    return baseTasks;
  };

  const createMonthlyPlans = (tasks: ImplementationTask[], projectData: Project): MonthlyPlan[] => {
    const currentDate = new Date();
    const plans: MonthlyPlan[] = [];
    const totalBudget = getBudgetValue(projectData.businessData.budgetRange);
    const monthlyBudget = Math.round(totalBudget / 12);

    for (let i = 0; i < 12; i++) {
      const monthDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + i);
      const monthTasks = distributeTasksToMonth(tasks, i);
      
      plans.push({
        month: monthDate.getMonth() + 1,
        year: monthDate.getFullYear(),
        name: monthDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
        focus: getMonthFocus(i, projectData.businessData.servicePackage),
        budget: monthlyBudget,
        tasks: monthTasks,
        goals: getMonthGoals(i),
        kpis: getMonthKPIs(i, projectData.businessData.servicePackage)
      });
    }

    return plans;
  };

  const distributeTasksToMonth = (allTasks: ImplementationTask[], monthIndex: number): ImplementationTask[] => {
    const tasksPerMonth = Math.ceil(allTasks.length / 12);
    const startIndex = monthIndex * tasksPerMonth;
    const endIndex = Math.min(startIndex + tasksPerMonth, allTasks.length);
    
    return allTasks.slice(startIndex, endIndex);
  };

  const getBudgetValue = (budgetRange: string): number => {
    const budgetMap: Record<string, number> = {
      'under_1k': 750,
      '1k_5k': 3000,
      '5k_10k': 7500,
      '10k_25k': 17500,
      '25k_50k': 37500,
      'over_50k': 75000
    };
    return budgetMap[budgetRange] || 3000;
  };

  const getMonthFocus = (monthIndex: number, servicePackage: ServicePackage): string => {
    const phase = Math.floor(monthIndex / 3);
    const focuses = {
      [ServicePackage.PPC_ONLY]: [
        'Foundation & Setup', 'Optimization & Scaling', 'Advanced Strategies', 'Growth & Expansion'
      ],
      [ServicePackage.SEO_ONLY]: [
        'Technical Foundation', 'Content Development', 'Authority Building', 'Advanced Optimization'
      ],
      [ServicePackage.PPC_SEO_COMBINED]: [
        'Integrated Setup', 'Synergistic Optimization', 'Advanced Integration', 'Unified Growth'
      ]
    };
    return focuses[servicePackage][phase] || 'Strategic Implementation';
  };

  const getMonthGoals = (monthIndex: number): string[] => {
    const quarter = Math.floor(monthIndex / 3);
    const goals = {
      0: ['Establish foundation', 'Begin tracking', 'Initial optimization'],
      1: ['Scale successful elements', 'Expand targeting', 'Improve performance'],
      2: ['Advanced strategies', 'Market expansion', 'Competitive advantage'],
      3: ['Long-term growth', 'Innovation testing', 'Market leadership']
    };
    return goals[quarter as keyof typeof goals] || ['Strategic progress'];
  };

  const getMonthKPIs = (monthIndex: number, servicePackage: ServicePackage): string[] => {
    // monthIndex is used for potential future month-specific KPIs
    if (servicePackage === ServicePackage.PPC_ONLY) {
      return ['CPC', 'CTR', 'Conversion Rate', 'ROAS', 'Quality Score'];
    } else if (servicePackage === ServicePackage.SEO_ONLY) {
      return ['Organic Traffic', 'Keyword Rankings', 'Page Authority', 'Backlinks', 'CTR'];
    } else {
      return ['Total Traffic', 'Cost per Lead', 'Organic + Paid CTR', 'Overall ROAS', 'Brand Visibility'];
    }
  };

  const updateTask = (monthIndex: number, taskId: string, updates: Partial<ImplementationTask>) => {
    const updatedPlans = [...monthlyPlans];
    const taskIndex = updatedPlans[monthIndex].tasks.findIndex(t => t.id === taskId);
    if (taskIndex !== -1) {
      updatedPlans[monthIndex].tasks[taskIndex] = {
        ...updatedPlans[monthIndex].tasks[taskIndex],
        ...updates
      };
      setMonthlyPlans(updatedPlans);
    }
  };

  const addNewTask = (monthIndex: number, task: Omit<ImplementationTask, 'id'>) => {
    const newTask: ImplementationTask = {
      ...task,
      id: `custom-${Date.now()}`
    };
    
    const updatedPlans = [...monthlyPlans];
    updatedPlans[monthIndex].tasks.push(newTask);
    setMonthlyPlans(updatedPlans);
  };

  const deleteTask = (monthIndex: number, taskId: string) => {
    const updatedPlans = [...monthlyPlans];
    updatedPlans[monthIndex].tasks = updatedPlans[monthIndex].tasks.filter(t => t.id !== taskId);
    setMonthlyPlans(updatedPlans);
  };

  const getCategoryIcon = (category: ImplementationTask['category']) => {
    const icons = {
      setup: Target,
      optimization: TrendingUp,
      content: Edit3,
      analysis: BarChart3,
      scaling: Users
    };
    return icons[category];
  };

  const getCategoryColor = (category: ImplementationTask['category']) => {
    const colors = {
      setup: 'blue',
      optimization: 'green',
      content: 'purple',
      analysis: 'orange',
      scaling: 'indigo'
    };
    return colors[category];
  };

  const getPriorityColor = (priority: ImplementationTask['priority']) => {
    const colors = {
      high: 'red',
      medium: 'yellow',
      low: 'gray'
    };
    return colors[priority];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading implementation plan...</p>
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

  const currentPlan = monthlyPlans[activeMonth];
  const completedTasks = currentPlan?.tasks.filter(t => t.completed).length || 0;
  const totalTasks = currentPlan?.tasks.length || 0;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link
                href={`/projects/${project.id}/analysis`}
                className="flex items-center text-gray-600 hover:text-gray-900 mr-4"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Analysis
              </Link>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{project.name} - Implementation Plan</h1>
                <p className="text-sm text-gray-500">12-Month Strategic Roadmap</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {monthlyPlans.length} Months Planned
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Month Navigation Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Monthly Timeline</h3>
                <p className="text-sm text-gray-500 mt-1">12-month implementation plan</p>
              </div>
              <nav className="p-4">
                <ul className="space-y-2">
                  {monthlyPlans.map((plan, index) => {
                    const completed = plan.tasks.filter(t => t.completed).length;
                    const total = plan.tasks.length;
                    const progress = total > 0 ? (completed / total) * 100 : 0;
                    
                    return (
                      <li key={index}>
                        <button
                          onClick={() => setActiveMonth(index)}
                          className={`w-full text-left px-3 py-3 rounded-md transition-colors ${
                            activeMonth === index
                              ? 'bg-blue-50 text-blue-700 border border-blue-200'
                              : 'text-gray-700 hover:bg-gray-50'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <Calendar className="h-4 w-4 mr-2" />
                              <span className="font-medium text-sm">{plan.name}</span>
                            </div>
                          </div>
                          <div className="mt-1 text-xs text-gray-500">{plan.focus}</div>
                          <div className="mt-2">
                            <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                              <span>{completed}/{total} tasks</span>
                              <span>{Math.round(progress)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1.5">
                              <div
                                className="bg-blue-600 h-1.5 rounded-full transition-all"
                                style={{ width: `${progress}%` }}
                              />
                            </div>
                          </div>
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {currentPlan && (
              <div className="space-y-6">
                {/* Month Overview */}
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">{currentPlan.name}</h2>
                        <p className="text-gray-600 mt-1">Focus: {currentPlan.focus}</p>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-600">{completionRate}%</div>
                          <div className="text-xs text-gray-500">Complete</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">${currentPlan.budget.toLocaleString()}</div>
                          <div className="text-xs text-gray-500">Budget</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 mb-3">Monthly Goals</h3>
                        <ul className="space-y-2">
                          {currentPlan.goals.map((goal, index) => (
                            <li key={index} className="flex items-center text-sm text-gray-700">
                              <Target className="h-4 w-4 text-blue-500 mr-2" />
                              {goal}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 mb-3">Key Performance Indicators</h3>
                        <div className="flex flex-wrap gap-2">
                          {currentPlan.kpis.map((kpi, index) => (
                            <span
                              key={index}
                              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                            >
                              {kpi}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Tasks */}
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-gray-900">Implementation Tasks</h3>
                      <button
                        onClick={() => setShowTaskModal(true)}
                        className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                      >
                        <Plus className="h-4 w-4 mr-1" />
                        Add Task
                      </button>
                    </div>
                  </div>

                  <div className="divide-y divide-gray-200">
                    {currentPlan.tasks.map((task) => {
                      const CategoryIcon = getCategoryIcon(task.category);
                      
                      return (
                        <div key={task.id} className="p-6 hover:bg-gray-50">
                          <div className="flex items-start justify-between">
                            <div className="flex items-start space-x-3">
                              <button
                                onClick={() => updateTask(activeMonth, task.id, { completed: !task.completed })}
                                className={`mt-1 h-5 w-5 rounded border-2 flex items-center justify-center ${
                                  task.completed
                                    ? 'bg-green-500 border-green-500 text-white'
                                    : 'border-gray-300 hover:border-green-500'
                                }`}
                              >
                                {task.completed && <CheckCircle className="h-3 w-3" />}
                              </button>
                              <div className="flex-1">
                                <div className="flex items-center space-x-2">
                                  <h4 className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                                    {task.title}
                                  </h4>
                                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-${getCategoryColor(task.category)}-100 text-${getCategoryColor(task.category)}-800`}>
                                    <CategoryIcon className="h-3 w-3 mr-1" />
                                    {task.category}
                                  </span>
                                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-${getPriorityColor(task.priority)}-100 text-${getPriorityColor(task.priority)}-800`}>
                                    {task.priority}
                                  </span>
                                </div>
                                <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                                  {task.description}
                                </p>
                                <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                                  <span className="flex items-center">
                                    <Clock className="h-3 w-3 mr-1" />
                                    {task.estimatedHours}h estimated
                                  </span>
                                  {task.budget && (
                                    <span className="flex items-center">
                                      <DollarSign className="h-3 w-3 mr-1" />
                                      ${task.budget}
                                    </span>
                                  )}
                                  {task.assignedTo && (
                                    <span className="flex items-center">
                                      <Users className="h-3 w-3 mr-1" />
                                      {task.assignedTo}
                                    </span>
                                  )}
                                </div>
                                {task.notes && (
                                  <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                                    <strong>Notes:</strong> {task.notes}
                                  </div>
                                )}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <button
                                onClick={() => {
                                  setEditingTask(task);
                                  setShowTaskModal(true);
                                }}
                                className="p-1 text-gray-400 hover:text-gray-600"
                              >
                                <Edit3 className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => deleteTask(activeMonth, task.id)}
                                className="p-1 text-gray-400 hover:text-red-600"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Task Modal */}
      {showTaskModal && (
        <TaskModal
          task={editingTask}
          onSave={(task) => {
            if (editingTask) {
              updateTask(activeMonth, editingTask.id, task);
            } else {
              addNewTask(activeMonth, task);
            }
            setShowTaskModal(false);
            setEditingTask(null);
          }}
          onCancel={() => {
            setShowTaskModal(false);
            setEditingTask(null);
          }}
        />
      )}
    </div>
  );
}

// Task Modal Component
interface TaskModalProps {
  task?: ImplementationTask | null;
  onSave: (task: Omit<ImplementationTask, 'id'>) => void;
  onCancel: () => void;
}

function TaskModal({ task, onSave, onCancel }: TaskModalProps) {
  const [formData, setFormData] = useState<Omit<ImplementationTask, 'id'>>({
    title: task?.title || '',
    description: task?.description || '',
    category: task?.category || 'setup',
    priority: task?.priority || 'medium',
    estimatedHours: task?.estimatedHours || 4,
    budget: task?.budget || undefined,
    assignedTo: task?.assignedTo || '',
    completed: task?.completed || false,
    notes: task?.notes || ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <form onSubmit={handleSubmit}>
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              {task ? 'Edit Task' : 'Add New Task'}
            </h3>
          </div>
          
          <div className="px-6 py-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                rows={3}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value as ImplementationTask['category'] }))}
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="setup">Setup</option>
                  <option value="optimization">Optimization</option>
                  <option value="content">Content</option>
                  <option value="analysis">Analysis</option>
                  <option value="scaling">Scaling</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value as ImplementationTask['priority'] }))}
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Estimated Hours</label>
                <input
                  type="number"
                  value={formData.estimatedHours}
                  onChange={(e) => setFormData(prev => ({ ...prev, estimatedHours: parseInt(e.target.value) }))}
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  min="1"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Budget ($)</label>
                <input
                  type="number"
                  value={formData.budget || ''}
                  onChange={(e) => setFormData(prev => ({ ...prev, budget: e.target.value ? parseInt(e.target.value) : undefined }))}
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  min="0"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Assigned To</label>
              <input
                type="text"
                value={formData.assignedTo}
                onChange={(e) => setFormData(prev => ({ ...prev, assignedTo: e.target.value }))}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                placeholder="Team member or role"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                rows={2}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                placeholder="Additional notes or requirements"
              />
            </div>
          </div>

          <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
            >
              {task ? 'Update' : 'Create'} Task
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}