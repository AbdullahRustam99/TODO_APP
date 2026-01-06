// Statistics card component for dashboard analytics
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { cn } from '@/lib/utils';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  color?: 'orange' | 'yellow' | 'blue' | 'green' | 'purple';
  className?: string;
}

export const StatsCard = ({
  title,
  value,
  subtitle,
  icon,
  color = 'orange',
  className
}: StatsCardProps) => {
  const colorClasses = {
    orange: 'text-orange-500 border-orange-500/30',
    yellow: 'text-yellow-500 border-yellow-500/30',
    blue: 'text-blue-500 border-blue-500/30',
    green: 'text-green-500 border-green-500/30',
    purple: 'text-purple-500 border-purple-500/30',
  };

  return (
    <Card className={cn("bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300", className)}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div>
          <CardTitle className="text-sm font-medium text-gray-400">{title}</CardTitle>
          <p className="text-3xl font-bold mt-1">{value}</p>
        </div>
        <div className={cn(
          "p-3 rounded-lg",
          color === 'orange' ? 'bg-orange-500/20' :
          color === 'yellow' ? 'bg-yellow-500/20' :
          color === 'blue' ? 'bg-blue-500/20' :
          color === 'green' ? 'bg-green-500/20' : 'bg-purple-500/20'
        )}>
          {icon}
        </div>
      </CardHeader>
      {subtitle && (
        <CardContent>
          <p className="text-sm text-gray-500">{subtitle}</p>
        </CardContent>
      )}
    </Card>
  );
};