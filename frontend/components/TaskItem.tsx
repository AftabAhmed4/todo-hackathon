/**
 * TaskItem component for displaying individual task.
 *
 * Shows task title, description, status, and timestamps.
 */

'use client';

import { Task, TaskStatus } from '@/lib/types';

interface TaskItemProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

export default function TaskItem({ task, onEdit, onDelete }: TaskItemProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case TaskStatus.COMPLETED:
        return 'bg-green-100 text-green-800';
      case TaskStatus.IN_PROGRESS:
        return 'bg-blue-100 text-blue-800';
      case TaskStatus.PENDING:
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case TaskStatus.COMPLETED:
        return 'Completed';
      case TaskStatus.IN_PROGRESS:
        return 'In Progress';
      case TaskStatus.PENDING:
      default:
        return 'Pending';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {/* Header with title and status */}
      <div className="flex items-start justify-between mb-2">
        <h3 className="text-lg font-semibold text-gray-900 flex-1">
          {task.title}
        </h3>
        <span
          className={`ml-4 px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
            task.status
          )}`}
        >
          {getStatusLabel(task.status)}
        </span>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-600 text-sm mb-3 whitespace-pre-wrap">
          {task.description}
        </p>
      )}

      {/* Timestamps */}
      <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
        <span>Created: {formatDate(task.created_at)}</span>
        {task.updated_at !== task.created_at && (
          <span>Updated: {formatDate(task.updated_at)}</span>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex gap-2">
        {onEdit && (
          <button
            onClick={() => onEdit(task)}
            className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={() => onDelete(task.id)}
            className="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
}
