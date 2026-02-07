/**
 * TaskList component for displaying paginated list of tasks.
 *
 * Fetches tasks from API, displays loading/error states, and handles pagination.
 */

'use client';

import { useEffect, useState } from 'react';
import { Task } from '@/lib/types';
import { api } from '@/lib/api';
import TaskItem from './TaskItem';

interface TaskListProps {
  userId: number;
  refreshTrigger?: number;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

export default function TaskList({
  userId,
  refreshTrigger = 0,
  onEdit,
  onDelete,
}: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const pageSize = 20;

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.getTasks(userId, page, pageSize);
      setTasks(response.items);
      setTotalPages(response.total_pages);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [userId, page, refreshTrigger]);

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  const handleDeleteWithRefresh = async (taskId: number) => {
    if (onDelete) {
      onDelete(taskId);
      // Refresh the list after a short delay to allow the delete to complete
      setTimeout(() => {
        fetchTasks();
      }, 500);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="border border-gray-200 rounded-lg p-4 animate-pulse"
          >
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800 text-sm">Error: {error}</p>
        <button
          onClick={fetchTasks}
          className="mt-2 text-sm text-red-600 hover:text-red-700 underline"
        >
          Try again
        </button>
      </div>
    );
  }

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-md p-8 text-center">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">
          Get started by creating a new task above.
        </p>
      </div>
    );
  }

  // Task list with pagination
  return (
    <div>
      {/* Task count */}
      <div className="mb-4 text-sm text-gray-600">
        Showing {tasks.length} of {total} tasks
      </div>

      {/* Task items */}
      <div className="space-y-4 mb-6">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={onEdit}
            onDelete={handleDeleteWithRefresh}
          />
        ))}
      </div>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t border-gray-200 pt-4">
          <button
            onClick={handlePreviousPage}
            disabled={page === 1}
            className={`px-4 py-2 text-sm font-medium rounded-md ${
              page === 1
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            Previous
          </button>

          <span className="text-sm text-gray-700">
            Page {page} of {totalPages}
          </span>

          <button
            onClick={handleNextPage}
            disabled={page === totalPages}
            className={`px-4 py-2 text-sm font-medium rounded-md ${
              page === totalPages
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
