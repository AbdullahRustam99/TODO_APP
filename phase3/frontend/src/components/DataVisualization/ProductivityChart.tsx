// Productivity chart component for task analytics
import { cn } from '@/lib/utils';

interface ProductivityChartProps {
  data: Array<{ name: string; value: number }>;
  title?: string;
  className?: string;
}

export const ProductivityChart = ({ data, title = 'Productivity Trends', className }: ProductivityChartProps) => {
  const maxValue = Math.max(...data.map(item => item.value), 100);

  return (
    <div className={cn("bg-[#1C1C1C] p-6 rounded-xl border border-gray-700 backdrop-blur-sm", className)}>
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
      <div className="flex items-end justify-between h-48 gap-2">
        {data.map((item, index) => (
          <div key={index} className="flex flex-col items-center flex-1">
            <div className="text-xs text-gray-400 mb-1">{item.value}%</div>
            <div
              className="w-full bg-gradient-to-t from-orange-500 to-yellow-500 rounded-t-md transition-all duration-500 ease-out"
              style={{ height: `${(item.value / maxValue) * 100}%` }}
            />
            <div className="text-xs text-gray-400 mt-2">{item.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};