// Filter tabs component for task filtering
import { cn } from '@/lib/utils';

interface FilterTabsProps {
  tabs: Array<{ id: string; label: string; count?: number }>;
  activeTab: string;
  onTabChange: (tabId: string) => void;
  className?: string;
}

export const FilterTabs = ({
  tabs,
  activeTab,
  onTabChange,
  className
}: FilterTabsProps) => {
  return (
    <div className={cn("flex space-x-1 bg-gray-800/50 p-1 rounded-lg", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={cn(
            "px-4 py-2 rounded-md text-sm font-medium transition-all duration-200",
            activeTab === tab.id
              ? "bg-orange-500 text-white shadow-md"
              : "text-gray-400 hover:text-white hover:bg-gray-700/50"
          )}
        >
          {tab.label}
          {tab.count !== undefined && (
            <span className={cn(
              "ml-2 px-2 py-0.5 rounded-full text-xs",
              activeTab === tab.id
                ? "bg-orange-400/20 text-orange-300"
                : "bg-gray-700 text-gray-400"
            )}>
              {tab.count}
            </span>
          )}
        </button>
      ))}
    </div>
  );
};