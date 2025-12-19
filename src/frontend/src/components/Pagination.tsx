import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const Pagination = ({ currentPage, totalPages, onPageChange }: PaginationProps) => {
  const getVisiblePages = () => {
    const pages: number[] = [];
    const start = Math.max(1, currentPage - 1);
    const end = Math.min(totalPages, currentPage + 2);

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  };

  if (totalPages <= 1) return null;

  return (
    <nav className="flex flex-col items-center gap-4 py-8 border-t border-border mt-6">
      <span className="text-sm text-muted-foreground">
        Page {currentPage} of {totalPages}
      </span>

      <div className="flex items-center gap-1">
        {currentPage > 1 && (
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(1)}
          >
            <ChevronsLeft className="w-4 h-4" />
          </Button>
        )}

        {currentPage > 1 && (
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(currentPage - 1)}
          >
            <ChevronLeft className="w-4 h-4" />
          </Button>
        )}

        {getVisiblePages().map((page) => (
          <Button
            key={page}
            variant={page === currentPage ? "default" : "outline"}
            size="sm"
            className="h-9 w-9 p-0"
            onClick={() => onPageChange(page)}
          >
            {page}
          </Button>
        ))}

        {currentPage < totalPages && (
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(currentPage + 1)}
          >
            <ChevronRight className="w-4 h-4" />
          </Button>
        )}

        {currentPage < totalPages && (
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(totalPages)}
          >
            <ChevronsRight className="w-4 h-4" />
          </Button>
        )}
      </div>
    </nav>
  );
};

export default Pagination;
