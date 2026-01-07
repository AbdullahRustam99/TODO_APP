// Glassmorphism card component for dashboard elements
import { Card, CardProps } from '@/components/UI/Card';
import { cn } from '@/lib/utils';

interface GlassCardProps extends CardProps {
  blur?: 'sm' | 'md' | 'lg' | 'xl';
  opacity?: '5' | '10' | '20' | '30';
}

export const GlassCard = ({
  className,
  blur = 'md',
  opacity = '10',
  children,
  ...props
}: GlassCardProps) => {
  const blurClasses = {
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
    xl: 'backdrop-blur-xl',
  };

  return (
    <Card
      className={cn(
        `bg-white/${opacity} border border-white/${parseInt(opacity) + 10} ${blurClasses[blur]}`,
        'shadow-lg shadow-white/10',
        className
      )}
      {...props}
    >
      {children}
    </Card>
  );
};