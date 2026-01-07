// Select component for form inputs (simplified)
import { cn } from '@/lib/utils';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode;
  value?: string;
  onValueChange?: (value: string) => void;
  defaultValue?: string;
  className?: string;
  placeholder?: string;
}

interface SelectItemProps {
  children: React.ReactNode;
  value: string;
  className?: string;
}

interface SelectContentProps {
  children: React.ReactNode;
  className?: string;
}

interface SelectTriggerProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode;
  className?: string;
}

interface SelectValueProps {
  placeholder?: string;
}

// Main Select component - simplified to work as a controlled select
export const Select = ({ children, value, onValueChange, defaultValue, className, ...props }: SelectProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (onValueChange) {
      onValueChange(e.target.value);
    }
    // Call any onChange handler passed via props
    if (props.onChange) {
      props.onChange(e);
    }
  };

  return (
    <select
      value={value}
      onChange={handleChange}
      className={cn(
        "w-full rounded-lg border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent",
        className
      )}
      {...props}
    >
      {children}
    </select>
  );
};

// Select Item component - just an option element
export const SelectItem = ({ children, value, className }: SelectItemProps) => {
  return (
    <option value={value} className={className}>
      {children}
    </option>
  );
};

// SelectTrigger, SelectContent, SelectValue - for compatibility with the expected API
export const SelectTrigger = ({ children, className, ...props }: SelectTriggerProps) => {
  return (
    <select
      className={cn(
        "w-full rounded-lg border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent",
        className
      )}
      {...props}
    >
      {children}
    </select>
  );
};

export const SelectContent = ({ children, className }: SelectContentProps) => {
  return <>{children}</>;
};

export const SelectValue = ({ placeholder }: SelectValueProps) => {
  return <>{placeholder}</>;
};

export const SelectGroup = ({ children }: { children: React.ReactNode }) => {
  return <optgroup>{children}</optgroup>;
};

export const SelectLabel = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};