// Task analytics component for dashboard insights
import { ProgressBar } from '@/components/Common/ProgressBar';
import { cn } from '@/lib/utils';

interface TaskAnalyticsProps {
  completedTasks: number;
  totalTasks: number;
  overdueTasks: number;
  highPriorityTasks: number;
  className?: string;
}

export const TaskAnalytics = ({
  completedTasks,
  totalTasks,
  overdueTasks,
  highPriorityTasks,
  className
}: TaskAnalyticsProps) => {
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className={cn("bg-[#1C1C1C] p-6 rounded-xl border border-gray-700 backdrop-blur-sm", className)}>
      <h3 className="text-lg font-semibold text-white mb-4">Task Analytics</h3>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-400">Completion Rate</span>
            <span className="text-white">{completionRate}%</span>
          </div>
          <ProgressBar
            value={completionRate}
            max={100}
            variant={completionRate >= 80 ? 'success' : completionRate >= 50 ? 'warning' : 'error'}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-800/50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-white">{overdueTasks}</div>
            <div className="text-sm text-gray-400">Overdue</div>
          </div>
          <div className="bg-gray-800/50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-white">{highPriorityTasks}</div>
            <div className="text-sm text-gray-400">High Priority</div>
          </div>
        </div>

        <div className="pt-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Tasks Completed</span>
            <span className="text-white">{completedTasks}/{totalTasks}</span>
          </div>
        </div>
      </div>
    </div>
  );
};