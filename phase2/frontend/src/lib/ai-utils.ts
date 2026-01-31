// AI utilities and service handlers for the Todo App

// Interface for AI service configuration
export interface AIServiceConfig {
  baseUrl: string;
  apiKey: string;
  timeout?: number;
}

// Interface for AI task suggestions
export interface AITaskSuggestion {
  id: string;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  estimatedTime?: number; // in minutes
  category?: string;
  tags?: string[];
  confidence: number; // 0-1
  reason?: string;
}

// Interface for AI analysis results
export interface AIAnalysisResult {
  productivityScore: number; // 0-100
  recommendations: string[];
  taskPriorities: Array<{ taskId: string; newPriority: 'low' | 'medium' | 'high' }>;
  timeEstimates: Array<{ taskId: string; estimatedTime: number }>;
  suggestions: AITaskSuggestion[];
}

// Mock AI service for demonstration
class MockAIService {
  private config: AIServiceConfig;

  constructor(config: AIServiceConfig) {
    this.config = config;
  }

  // Generate task suggestions based on user's patterns
  async generateTaskSuggestions(context: {
    currentTasks: any[];
    userPreferences: any;
    timeOfDay?: string;
    dayOfWeek?: string;
  }): Promise<AITaskSuggestion[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 500));

    // Mock suggestions based on context
    const suggestions: AITaskSuggestion[] = [];

    // If user has many high-priority tasks, suggest some lower priority ones
    const highPriorityCount = context.currentTasks.filter((t: any) => t.priority === 'high').length;
    if (highPriorityCount > 3) {
      suggestions.push({
        id: `sug-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        title: "Take a break and recharge",
        description: "Consider taking some time to relax and prevent burnout",
        priority: 'low',
        estimatedTime: 60,
        category: 'wellness',
        tags: ['break', 'relaxation'],
        confidence: 0.85,
        reason: "High workload detected"
      });
    }

    // If it's morning, suggest planning tasks
    if (context.timeOfDay === 'morning') {
      suggestions.push({
        id: `sug-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        title: "Plan your day",
        description: "Review and prioritize today's tasks",
        priority: 'high',
        estimatedTime: 15,
        category: 'planning',
        tags: ['planning', 'prioritization'],
        confidence: 0.92,
        reason: "Morning routine suggestion"
      });
    }

    // If it's late evening, suggest tomorrow's planning
    if (context.timeOfDay === 'evening') {
      suggestions.push({
        id: `sug-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        title: "Prepare for tomorrow",
        description: "Set up tasks and priorities for tomorrow",
        priority: 'medium',
        estimatedTime: 10,
        category: 'planning',
        tags: ['preparation', 'organization'],
        confidence: 0.78,
        reason: "Evening preparation suggestion"
      });
    }

    // Add some general suggestions
    suggestions.push({
      id: `sug-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      title: "Review project deadlines",
      description: "Check upcoming deadlines and adjust priorities",
      priority: 'high',
      estimatedTime: 30,
      category: 'review',
      tags: ['deadline', 'review'],
      confidence: 0.88,
      reason: "Regular review recommendation"
    });

    return suggestions;
  }

  // Analyze user's task patterns and productivity
  async analyzeProductivity(userId: string, tasks: any[]): Promise<AIAnalysisResult> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400));

    // Calculate productivity score based on completion rate and due dates
    const completedTasks = tasks.filter((t: any) => t.completed).length;
    const totalTasks = tasks.length;
    const completionRate = totalTasks > 0 ? completedTasks / totalTasks : 0;

    // Count overdue tasks
    const now = new Date();
    const overdueTasks = tasks.filter((t: any) => {
      if (!t.dueDate || t.completed) return false;
      return new Date(t.dueDate) < now;
    }).length;

    // Calculate productivity score (0-100)
    let productivityScore = Math.min(100, Math.max(0,
      (completionRate * 70) - (overdueTasks * 2)
    ));

    // Generate recommendations
    const recommendations: string[] = [];
    if (completionRate < 0.5) {
      recommendations.push("Try breaking large tasks into smaller, manageable chunks");
    }
    if (overdueTasks > 3) {
      recommendations.push("Consider adjusting deadlines or reprioritizing tasks");
    }
    if (tasks.some((t: any) => t.priority === 'high' && !t.completed)) {
      recommendations.push("Focus on completing high-priority tasks first");
    }

    // Generate task priority adjustments
    const taskPriorities = tasks.map((task: any) => {
      let newPriority = task.priority;

      // If task is overdue and high priority, maybe it needs attention
      if (task.dueDate && new Date(task.dueDate) < now && !task.completed) {
        if (task.priority === 'low') newPriority = 'medium';
        else if (task.priority === 'medium') newPriority = 'high';
      }

      return {
        taskId: task.id,
        newPriority
      };
    });

    // Generate time estimates
    const timeEstimates = tasks.map((task: any) => ({
      taskId: task.id,
      estimatedTime: task.estimatedTime || Math.floor(Math.random() * 120) + 15 // 15-135 minutes
    }));

    // Generate additional suggestions
    const suggestions: AITaskSuggestion[] = [];
    if (tasks.length > 0 && completionRate > 0.8) {
      suggestions.push({
        id: `sug-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        title: "Increase challenge level",
        description: "You're completing tasks efficiently. Consider more challenging assignments.",
        priority: 'medium',
        estimatedTime: 0,
        category: 'development',
        tags: ['challenge', 'growth'],
        confidence: 0.95,
        reason: "High completion rate detected"
      });
    }

    return {
      productivityScore: Math.round(productivityScore),
      recommendations,
      taskPriorities,
      timeEstimates,
      suggestions
    };
  }

  // Optimize task schedule based on user patterns
  async optimizeSchedule(tasks: any[], preferences: any): Promise<any[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 600 + Math.random() * 300));

    // Sort tasks by priority and deadline
    return [...tasks].sort((a, b) => {
      // First, sort by priority (high to low)
<<<<<<< HEAD
      const getPriorityValue = (priority: any) => {
        if (priority === 'high') return 3;
        if (priority === 'medium') return 2;
        return 1; // default to low
      };

      const aPriorityValue = getPriorityValue(a.priority);
      const bPriorityValue = getPriorityValue(b.priority);

      if (aPriorityValue !== bPriorityValue) {
        return bPriorityValue - aPriorityValue; // Higher priority first
=======
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      if (priorityOrder[b.priority] !== priorityOrder[a.priority]) {
        return priorityOrder[b.priority] - priorityOrder[a.priority];
>>>>>>> main
      }

      // Then by deadline (earlier first)
      if (a.dueDate && b.dueDate) {
        return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
      }

      // Finally by creation date (older first)
      return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
    });
  }
}

// Create a singleton instance of the AI service
let aiService: MockAIService | null = null;

// Initialize the AI service with configuration
export function initializeAIService(config: AIServiceConfig): void {
  aiService = new MockAIService(config);
}

// Get the AI service instance (will create default if not initialized)
export function getAIService(): MockAIService {
  if (!aiService) {
    // Use default configuration if not initialized
    aiService = new MockAIService({
      baseUrl: process.env.NEXT_PUBLIC_AI_API_BASE_URL || 'http://localhost:8001',
      apiKey: process.env.NEXT_PUBLIC_AI_API_KEY || 'mock-key',
      timeout: 10000
    });
  }
  return aiService;
}

// Convenience functions for common AI operations
export async function getTaskSuggestions(
  currentTasks: any[],
  userPreferences: any,
  timeContext?: { timeOfDay?: string; dayOfWeek?: string }
): Promise<AITaskSuggestion[]> {
  const service = getAIService();
  return service.generateTaskSuggestions({
    currentTasks,
    userPreferences,
    timeOfDay: timeContext?.timeOfDay,
    dayOfWeek: timeContext?.dayOfWeek
  });
}

export async function analyzeUserProductivity(
  userId: string,
  tasks: any[]
): Promise<AIAnalysisResult> {
  const service = getAIService();
  return service.analyzeProductivity(userId, tasks);
}

export async function optimizeTaskSchedule(
  tasks: any[],
  preferences: any
): Promise<any[]> {
  const service = getAIService();
  return service.optimizeSchedule(tasks, preferences);
}

// Function to simulate AI processing with loading states
export async function withAILoading<T>(
  operation: () => Promise<T>,
  onProgress?: (progress: number) => void
): Promise<T> {
  if (onProgress) {
    // Simulate progress updates
    const intervals = [0.2, 0.4, 0.6, 0.8];
    for (const progress of intervals) {
      setTimeout(() => onProgress(progress), Math.random() * 300);
    }
  }

  try {
    const result = await operation();
    if (onProgress) {
      onProgress(1); // Complete
    }
    return result;
  } catch (error) {
    if (onProgress) {
      onProgress(-1); // Error state
    }
    throw error;
  }
}