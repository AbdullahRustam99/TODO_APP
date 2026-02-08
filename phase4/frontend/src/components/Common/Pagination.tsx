// Pagination component for task lists
import { Button } from '@/components/UI/Button';
import { cn } from '@/lib/utils';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
}

export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  className
}: PaginationProps) => {
  const pages = [];
  const maxVisiblePages = 5;

  // Calculate visible page range
  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <div className={cn("flex items-center justify-center space-x-2", className)}>
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
        className="px-3 py-2"
      >
        Previous
      </Button>

      {startPage > 1 && (
        <>
          <Button
            variant={1 === currentPage ? 'primary' : 'outline'}
            size="sm"
            onClick={() => onPageChange(1)}
            className="px-3 py-2"
          >
            1
          </Button>
          {startPage > 2 && (
            <span className="px-3 py-2 text-gray-500">...</span>
          )}
        </>
      )}

      {pages.map(page => (
        <Button
          key={page}
          variant={page === currentPage ? 'primary' : 'outline'}
          size="sm"
          onClick={() => onPageChange(page)}
          className="px-3 py-2"
        >
          {page}
        </Button>
      ))}

      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && (
            <span className="px-3 py-2 text-gray-500">...</span>
          )}
          <Button
            variant={totalPages === currentPage ? 'primary' : 'outline'}
            size="sm"
            onClick={() => onPageChange(totalPages)}
            className="px-3 py-2"
          >
            {totalPages}
          </Button>
        </>
      )}

      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
        disabled={currentPage === totalPages}
        className="px-3 py-2"
      >
        Next
      </Button>
    </div>
  );
};