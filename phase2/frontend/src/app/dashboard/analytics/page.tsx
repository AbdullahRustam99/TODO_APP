  'use client';


  import { useState, useEffect } from 'react';
  import { useAuth } from '@/context/AuthContext';
  import { useTheme } from '@/context/ThemeContext';
  import { Sidebar } from '@/components/UI/Sidebar';
  import { Button } from '@/components/UI/Button';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
  import { ProgressBar } from '@/components/UI/ProgressBar';
  import { Task } from '@/lib/types';
  import { useRouter } from 'next/navigation';
  import { cn } from '@/lib/utils';
  import { useTaskContext } from '@/context/TaskContext';

  export default function AnalyticsPage() {
    const { user, logout } = useAuth();
    const { theme } = useTheme();
    const router = useRouter();
    const [isVisible, setIsVisible] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [weeklyProgressData, setWeeklyProgressData] = useState<{ day: string; tasks: number }[]>([]);
    const [hasCompletedTasks, setHasCompletedTasks] = useState<boolean>(false);
    // Search functionality has been removed
    const { tasks, loading: tasksLoading } = useTaskContext(); // Get tasks and loading state from context

    useEffect(() => {
      setIsVisible(true);
      if (!user) {
        router.push('/login');
      }
    }, [user, router]);

    // Filter tasks based on search query (search functionality removed)
    const filteredTasks = tasks;

    // Helper to parse UTC timestamp strings safely
    const parseUTCDate = (dateString: string): Date | null => {
      if (!dateString) {
        return null;
      }

      try {
        // Handle "YYYY-MM-DD HH:MM:SS.microseconds" format
        if (dateString.includes(' ')) {
          let [datePart, timePart] = dateString.split(' ');

          // Handle microseconds (keep milliseconds only)
          if (timePart.includes('.')) {
            const [sec, micro] = timePart.split('.');
            // Take only first 3 digits as milliseconds, pad with zeros if needed
            let milli = micro.slice(0, 3);
            if (milli.length < 3) {
              milli = milli.padEnd(3, '0'); // e.g., "1" -> "100", "12" -> "120"
            }
            timePart = `${sec}.${milli}`;
          }
          const isoString = `${datePart}T${timePart}Z`; // force UTC
          return new Date(isoString);
        }

        // Handle standard ISO format (may already include 'T')
        return new Date(dateString);
      } catch (e) {
        console.error('Error parsing UTC date:', dateString, e);
        return null;
      }
    };

    // Calculate weekly progress when tasks change
    useEffect(() => {
      console.log('Weekly progress effect triggered - tasksLoading:', tasksLoading, 'tasks count:', tasks?.length || 0);

      if (tasksLoading) {
        console.log('Tasks still loading, skipping calculation');
        return;
      }

      const tasksToUse = filteredTasks;

      if (!tasksToUse) {
        console.log('No tasks available, skipping calculation');
        return;
      }

      console.log('Calculating weekly progress with', tasksToUse.length, 'tasks');

      // Debug: Log some sample task data to understand the format
      if (tasksToUse.length > 0) {
        console.log('Sample task data:', {
          firstTask: tasksToUse[0],
          updatedAtFormat: tasksToUse[0]?.updatedAt,
          createdAtFormat: tasksToUse[0]?.createdAt,
          completed: tasksToUse[0]?.completed
        });

        // Test the parseUTCDate function with sample data
        if (tasksToUse[0]?.updatedAt) {
          const parsedDate = parseUTCDate(tasksToUse[0].updatedAt);
          console.log('Parsed updatedAt:', tasksToUse[0].updatedAt, '->', parsedDate);
        }
      }

      /**
       * Calculate weekly progress for the last 7 days (UTC-safe)
       * This function creates an array of 7 objects representing each day in the past week
       * Each day object contains the day name and count of completed tasks for that day
       * Requirements:
       * - Calculate the last 7 days including today using UTC boundaries
       * - Use UTC day boundaries (00:00-23:59) for updatedAt comparisons
       * - Count tasks where completed=true and updatedAt falls within day range
       * - Avoid local timezone conversions for comparison
       * - Return an array: { day: string; tasks: number }[] for chart rendering
       */
      const calculateWeeklyProgress = (): { day: string; tasks: number }[] => {
        // Get current date in UTC
        const now = new Date();
        const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 0, 0, 0, 0));

        console.log('Calculating from today (UTC):', today.toISOString());

        // Create an array of 7 days, starting from 6 days ago to today (in UTC)
        // The range is [6 days ago, 5 days ago, 4 days ago, 3 days ago, 2 days ago, 1 day ago, today]
        return Array.from({ length: 7 }, (_, i) => {
          // Calculate the date for this day in the range using UTC
          // For i=0: 6 days ago, i=1: 5 days ago, ..., i=6: today
          // Use safe millisecond subtraction to avoid month/year boundary issues
          const daysAgo = 6 - i; // 6 days ago (i=0) to today (i=6)
          const targetDate = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000);

          // Calculate the start and end of the target day using UTC boundaries
          // Start of day: 00:00:00.000 UTC
          const startOfDay = new Date(Date.UTC(
            targetDate.getUTCFullYear(),
            targetDate.getUTCMonth(),
            targetDate.getUTCDate(),
            0, 0, 0, 0
          ));

          // End of day: 23:59:59.999 UTC
          const endOfDay = new Date(Date.UTC(
            targetDate.getUTCFullYear(),
            targetDate.getUTCMonth(),
            targetDate.getUTCDate(),
            23, 59, 59, 999
          ));

          console.log(`Day ${i}: ${targetDate.toISOString()} (from ${startOfDay.toISOString()} to ${endOfDay.toISOString()}) UTC boundaries`);

          // Count tasks that were completed on this specific date (using UTC boundaries)
          // A task qualifies if:
          // 1. It has completed = true
          // 2. It has an updatedAt field
          // 3. The updatedAt timestamp falls within the target day (startOfDay to endOfDay) UTC

          // Pre-parse all task timestamps to avoid redundant parsing (each task is checked against all 7 days)
          const parsedTaskTimestamps = new Map<string, Date | null>();
          tasksToUse.forEach(task => {
            if (task.updatedAt) {
              parsedTaskTimestamps.set(task.id, parseUTCDate(task.updatedAt));
            }
          });

          const dayCompletedTasks = tasksToUse.filter(task => {
            if (!task.completed) {
              return false; // Only completed tasks
            }

            if (!task.updatedAt) {
              return false; // Task must have an updatedAt field
            }

            // Get the pre-parsed timestamp
            const taskTimestamp = parsedTaskTimestamps.get(task.id);
            if (!taskTimestamp) {
              console.error('Failed to parse updatedAt date:', task.updatedAt);
              return false;
            }

            // Check if the task timestamp falls within the UTC target day range
            // This avoids local timezone conversions and compares in UTC
            const isWithinDay = taskTimestamp >= startOfDay && taskTimestamp <= endOfDay;

            if (isWithinDay) {
              console.log(`Task ${task.id} completed at ${taskTimestamp.toISOString()} falls within UTC ${startOfDay.toISOString()} - ${endOfDay.toISOString()}`);
            }

            return isWithinDay;
          });

          console.log(`UTC Day ${targetDate.toISOString()}: ${dayCompletedTasks.length} completed tasks`);

          // Return the day name and count of completed tasks for this day
          return {
            day: targetDate.toLocaleDateString('en-US', { weekday: 'short' }), // e.g., "Mon", "Tue"
            tasks: dayCompletedTasks.length, // Count of completed tasks
          };
        });
      };

      // Calculate completed tasks progress for the last 7 days
      const weeklyProgress = calculateWeeklyProgress();

      // Check if there are any completed tasks in the last 7 days
      const hasCompletedTasksInWeek = weeklyProgress.some(day => day.tasks > 0);
      console.log('Has completed tasks in week:', hasCompletedTasksInWeek);

      // Calculate fallback progress using created tasks if no completed tasks exist
      const calculateFallbackProgress = (): { day: string; tasks: number }[] => {
        // Get current date in UTC
        const now = new Date();
        const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 0, 0, 0, 0));

        console.log('Calculating fallback from today (UTC):', today.toISOString());

        return Array.from({ length: 7 }, (_, i) => {
          // Calculate the date for this day in the range using UTC
          // Use safe millisecond subtraction to avoid month/year boundary issues
          const daysAgo = 6 - i; // 6 days ago (i=0) to today (i=6)
          const targetDate = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000);

          // Calculate the start and end of the target day using UTC boundaries
          const startOfDay = new Date(Date.UTC(
            targetDate.getUTCFullYear(),
            targetDate.getUTCMonth(),
            targetDate.getUTCDate(),
            0, 0, 0, 0
          ));

          const endOfDay = new Date(Date.UTC(
            targetDate.getUTCFullYear(),
            targetDate.getUTCMonth(),
            targetDate.getUTCDate(),
            23, 59, 59, 999
          ));

          console.log(`Fallback Day ${i}: ${targetDate.toISOString()} (from ${startOfDay.toISOString()} to ${endOfDay.toISOString()}) UTC boundaries`);

          // Count tasks that were created on this specific date (using UTC boundaries)

          // Pre-parse all task timestamps to avoid redundant parsing (each task is checked against all 7 days)
          const parsedTaskTimestamps = new Map<string, Date | null>();
          tasksToUse.forEach(task => {
            if (task.createdAt) {
              parsedTaskTimestamps.set(task.id, parseUTCDate(task.createdAt));
            }
          });

          const dayCreatedTasks = tasksToUse.filter(task => {
            if (!task.createdAt) {
              return false; // Task must have a createdAt field
            }

            // Get the pre-parsed timestamp
            const taskTimestamp = parsedTaskTimestamps.get(task.id);
            if (!taskTimestamp) {
              console.error('Failed to parse createdAt date:', task.createdAt);
              return false;
            }

            // Compare using UTC boundaries to avoid local timezone conversions
            const isWithinDay = taskTimestamp >= startOfDay && taskTimestamp <= endOfDay;

            if (isWithinDay) {
              console.log(`Task ${task.id} created at ${taskTimestamp.toISOString()} falls within UTC ${startOfDay.toISOString()} - ${endOfDay.toISOString()}`);
            }

            return isWithinDay;
          });

          console.log(`UTC Fallback Day ${targetDate.toISOString()}: ${dayCreatedTasks.length} created tasks`);

          return {
            day: targetDate.toLocaleDateString('en-US', { weekday: 'short' }),
            tasks: dayCreatedTasks.length,
          };
        });
      };

      // Use completed tasks progress, or fall back to created tasks if no completed tasks exist
      const finalWeeklyProgress = hasCompletedTasksInWeek
        ? weeklyProgress
        : calculateFallbackProgress();

      console.log('Final weekly progress:', finalWeeklyProgress);

      // Update state
      setWeeklyProgressData(finalWeeklyProgress);
      setHasCompletedTasks(hasCompletedTasksInWeek);

      // Debug: Log the weekly progress data to console
      console.log('Weekly Progress Data:', finalWeeklyProgress);
      console.log('Total tasks:', tasksToUse.length);
      console.log('Completed tasks:', tasksToUse.filter(t => t.completed).length);
      console.log('Tasks with updatedAt:', tasksToUse.filter(t => t.updatedAt).length);
      console.log('Tasks with createdAt:', tasksToUse.filter(t => t.createdAt).length);
      console.log('Has completed tasks in week:', hasCompletedTasksInWeek);
    }, [tasks, tasksLoading, filteredTasks]);

    // Debug: Log task loading state and tasks
    console.log('TaskContext loading:', tasksLoading);
    console.log('TaskContext tasks:', tasks);
    console.log('Weekly progress state:', weeklyProgressData);
    console.log('Has completed tasks state:', hasCompletedTasks);

    // State variables for analytics data
    const [analyticsData, setAnalyticsData] = useState({
      totalTasks: 0,
      completedTasks: 0,
      pendingTasks: 0,
      overdueTasks: 0,
      taskDistribution: { high: 0, medium: 0, low: 0 },
      completionRate: 0,
      productivityScore: 0
    });

    // Calculate analytics data when tasks change
    useEffect(() => {
      const tasksToUse = filteredTasks;

      if (tasksLoading || !tasksToUse) return;

      console.log('Calculating analytics data with', tasksToUse.length, 'tasks');

      const totalTasks = tasksToUse.length;
      const completedTasks = tasksToUse.filter(task => task.completed).length;
      const pendingTasks = tasksToUse.filter(task => !task.completed).length;
      const overdueTasks = tasksToUse.filter(task => {
        if (!task.dueDate) return false;
        return new Date(task.dueDate) < new Date() && !task.completed;
      }).length;
      const taskDistribution = {
        high: tasksToUse.filter(task => task.priority === 'high').length,
        medium: tasksToUse.filter(task => task.priority === 'medium').length,
        low: tasksToUse.filter(task => task.priority === 'low').length,
      };
      const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

      // Calculate productivity score based on completion rate and other factors
      let productivityScore = completionRate;
      if (overdueTasks > 0) {
        // Reduce score based on overdue tasks
        const overduePenalty = Math.min(overdueTasks * 5, 30); // Max 30% penalty
        productivityScore = Math.max(productivityScore - overduePenalty, 0);
      }

      setAnalyticsData({
        totalTasks,
        completedTasks,
        pendingTasks,
        overdueTasks,
        taskDistribution,
        completionRate,
        productivityScore
      });

      console.log('Analytics data calculated:', {
        totalTasks,
        completedTasks,
        pendingTasks,
        overdueTasks,
        taskDistribution,
        completionRate,
        productivityScore
      });
    }, [tasks, tasksLoading, filteredTasks]);

    // Additional debugging to track when render occurs
    console.log('Component rendering - tasks length:', tasks?.length || 0, 'loading:', tasksLoading, 'weeklyProgressData length:', weeklyProgressData.length);

    const { totalTasks, completedTasks, pendingTasks, overdueTasks, taskDistribution, completionRate, productivityScore } = analyticsData;


    const handleLogout = () => {
      logout();
      router.push('/login');
    };

    if (!user) {
      return null;
    }

    return (
      <div className="min-h-screen bg-[#0F0F0F] text-white flex">
        {/* Sidebar */}
        <Sidebar isOpen={sidebarOpen} />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top Header */}
          <header className="border-b border-gray-700 bg-[#1C1C1C] backdrop-blur-sm sticky top-0 z-10 animate-fade-in">
            <div className="flex items-center justify-between px-6 py-4">
              <div className="flex items-center">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="lg:hidden mr-4 text-gray-400 hover:text-white focus:outline-none"
                  aria-label="Toggle sidebar"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                <h1 className="text-xl font-bold">Analytics</h1>
              </div>

              <div className="flex items-center space-x-4">
                {/* Notifications */}
                <button className="text-gray-400 hover:text-white relative" aria-label="Notifications">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                  <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>

                {/* User Profile */}
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                    <span className="text-sm font-medium">U</span>
                  </div>
                  <span className="ml-2 text-sm hidden md:block">{user?.name || user?.email}</span>
                </div>

                <Button
                  variant="outline"
                  onClick={handleLogout}
                  className="ml-4 animate-scale"
                  aria-label="Logout"
                >
                  Logout
                </Button>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main id="main-content" className="flex-1 overflow-y-auto p-6 focus:outline-none" tabIndex={-1}>
            {/* Analytics Overview Stats */}
            <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`} role="region" aria-labelledby="analytics-heading">
              <h3 id="analytics-heading" className="sr-only">Analytics Overview</h3>

              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-orange-500/10 animate-slide-in-left">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-400">Total Tasks</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-orange-500">{totalTasks}</p>
                  <p className="text-sm text-gray-500 mt-1">All tasks created</p>
                </CardContent>
              </Card>

              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-green-500/10 animate-slide-down">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-400">Completed</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-500">{completedTasks}</p>
                  <p className="text-sm text-gray-500 mt-1">Tasks finished</p>
                </CardContent>
              </Card>

              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-yellow-500/10 animate-slide-in-right">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-400">Pending</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-yellow-500">{pendingTasks}</p>
                  <p className="text-sm text-gray-500 mt-1">Tasks to complete</p>
                </CardContent>
              </Card>

              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-red-500/10 animate-slide-in-up">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-400">Overdue</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-red-500">{overdueTasks}</p>
                  <p className="text-sm text-gray-500 mt-1">Tasks past due</p>
                </CardContent>
              </Card>
            </div>

            {/* Productivity Metrics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              {/* Productivity Score Card */}
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm p-6 animate-fade-in">
                <CardHeader>
                  <CardTitle className="text-xl">Productivity Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center mb-6">
                    <div className="relative w-48 h-48">
                      <svg className="w-full h-full" viewBox="0 0 100 100">
                        {/* Background circle */}
                        <circle
                          cx="50"
                          cy="50"
                          r="45"
                          fill="none"
                          stroke="#374151"
                          strokeWidth="8"
                        />
                        {/* Progress circle */}
                        <circle
                          cx="50"
                          cy="50"
                          r="45"
                          fill="none"
                          stroke="url(#gradient)"
                          strokeWidth="8"
                          strokeLinecap="round"
                          strokeDasharray={`${productivityScore * 2.83} 283`}
                          transform="rotate(-90 50 50)"
                        />
                        <defs>
                          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#F97316" />
                            <stop offset="100%" stopColor="#EAB308" />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-bold text-white">{productivityScore}%</span>
                        <span className="text-sm text-gray-400">Weekly Score</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-center text-gray-400">
                    Your productivity is {productivityScore > 75 ? 'excellent' : productivityScore > 50 ? 'good' : 'needs improvement'}.
                    Keep up the great work!
                  </p>
                </CardContent>
              </Card>

              {/* Task Distribution Card */}
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm p-6 animate-fade-in delay-150">
                <CardHeader>
                  <CardTitle className="text-xl">Task Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-gray-400">High Priority</span>
                        <span className="text-white">{taskDistribution.high} tasks</span>
                      </div>
                      <ProgressBar
                        value={Math.round((taskDistribution.high / totalTasks) * 100)}
                        max={100}
                        className="bg-red-500/20"
                        indicatorClassName="bg-red-500"
                      />
                    </div>
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-gray-400">Medium Priority</span>
                        <span className="text-white">{taskDistribution.medium} tasks</span>
                      </div>
                      <ProgressBar
                        value={Math.round((taskDistribution.medium / totalTasks) * 100)}
                        max={100}
                        className="bg-yellow-500/20"
                        indicatorClassName="bg-yellow-500"
                      />
                    </div>
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-gray-400">Low Priority</span>
                        <span className="text-white">{taskDistribution.low} tasks</span>
                      </div>
                      <ProgressBar
                        value={Math.round((taskDistribution.low / totalTasks) * 100)}
                        max={100}
                        className="bg-green-500/20"
                        indicatorClassName="bg-green-500"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Weekly Progress Chart */}
            <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm p-6 animate-fade-in delay-300">
              <CardHeader>
                <CardTitle className="text-xl">Weekly Progress</CardTitle>
                {tasksLoading ? (
                  <p className="text-sm text-gray-400 mt-1">Loading tasks...</p>
                ) : tasks.length === 0 ? (
                  <p className="text-sm text-gray-400 mt-1">No tasks available</p>
                ) : hasCompletedTasks ? (
                  <p className="text-sm text-gray-400 mt-1">Showing completed tasks per day</p>
                ) : (
                  <p className="text-sm text-gray-400 mt-1">No completed tasks in the last 7 days. Showing created tasks per day.</p>
                )}
              </CardHeader>
              <CardContent>
                {tasksLoading ? (
                  <div className="flex items-center justify-center h-48">
                    <p className="text-gray-400">Loading...</p>
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="flex items-center justify-center h-48">
                    <p className="text-gray-400">No tasks to display</p>
                  </div>
                ) : (
                  <div className="flex items-end justify-between h-48 gap-2">
                    {weeklyProgressData.map((day, index) => {
                      // Calculate max value to determine height scale, ensuring it's at least 1 to avoid division by zero
                      const maxValue = Math.max(...weeklyProgressData.map(d => d.tasks), 1);
                      const heightPercentage = day.tasks > 0 ? (day.tasks / maxValue) * 100 : 0;

                      return (
                        <div key={index} className="flex flex-col items-center flex-1">
                          <div
                            className={`w-full rounded-t-md transition-all duration-500 ease-out ${
                              day.tasks > 0
                                ? 'bg-gradient-to-t from-orange-500 to-yellow-500'
                                : 'bg-gray-700' // Show gray bar when no tasks completed
                            }`}
                            style={{
                              height: `${heightPercentage > 0 ? heightPercentage : 4}%`, // Show minimum height so users can see the bar
                              minHeight: '4px' // Ensure minimum visibility
                            }}
                          />
                          <div className="text-xs text-gray-400 mt-2">{day.day}</div>
                          <div className="text-xs text-white mt-1">{day.tasks}</div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    );
  }