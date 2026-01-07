// Search input component with suggestions
import { useState, useEffect, useRef } from 'react';
import { Input } from '@/components/UI/Input';
import { cn } from '@/lib/utils';

interface SearchInputProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  suggestions?: string[];
  className?: string;
}

export const SearchInput = ({
  placeholder = 'Search...',
  onSearch,
  suggestions = [],
  className
}: SearchInputProps) => {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    onSearch(value);
    setShowSuggestions(value.length > 0 && suggestions.length > 0);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
    setShowSuggestions(false);
  };

  const handleBlur = () => {
    // Delay hiding suggestions to allow click on suggestion
    setTimeout(() => setShowSuggestions(false), 200);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          value={query}
          onChange={handleInputChange}
          onFocus={() => query && suggestions.length > 0 && setShowSuggestions(true)}
          onBlur={handleBlur}
          className={cn("pl-10", className)}
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {showSuggestions && (
        <div className="absolute z-10 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="px-4 py-2 hover:bg-gray-700 cursor-pointer text-gray-200 first:rounded-t-lg last:rounded-b-lg"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};