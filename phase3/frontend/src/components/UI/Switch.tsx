// Switch component for toggle functionality
import { cn } from '@/lib/utils';

interface SwitchProps extends React.InputHTMLAttributes<HTMLInputElement> {
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  className?: string;
  label?: string;
}

export const Switch = ({ checked, onCheckedChange, className, label, ...props }: SwitchProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onCheckedChange) {
      onCheckedChange(e.target.checked);
    }
    // Call any onChange handler passed via props
    if (props.onChange) {
      props.onChange(e);
    }
  };

  return (
    <div className="relative flex items-center">
      <input
        type="checkbox"
        checked={checked}
        onChange={handleChange}
        className="sr-only"
        {...props}
      />
      <div
        onClick={() => onCheckedChange && onCheckedChange(!checked)}
        className={cn(
          "relative inline-flex h-6 w-11 items-center rounded-full cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
          checked ? 'bg-orange-500' : 'bg-gray-600',
          className
        )}
      >
        <span
          className={cn(
            "inline-block h-4 w-4 transform rounded-full bg-white shadow-lg transition-transform",
            checked ? 'translate-x-6' : 'translate-x-1'
          )}
        />
      </div>
    </div>
  );
};