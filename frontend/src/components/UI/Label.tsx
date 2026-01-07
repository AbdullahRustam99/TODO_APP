// Label component for form accessibility
import { cn } from '@/lib/utils';

interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  htmlFor?: string;
  children: React.ReactNode;
  className?: string;
}

export const Label = ({ htmlFor, children, className, ...props }: LabelProps) => {
  return (
    <label
      htmlFor={htmlFor}
      className={cn(
        'block text-sm font-medium mb-2 text-gray-300',
        className
      )}
      {...props}
    >
      {children}
    </label>
  );
};