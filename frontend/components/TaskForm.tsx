/**
 * TaskForm component for creating and editing tasks.
 *
 * Provides form with validation, loading states, and error handling.
 * Supports both create and edit modes.
 */

'use client';

import { useState, useEffect } from 'react';
import { z } from 'zod';
import { api } from '@/lib/api';
import { Task, TaskStatus } from '@/lib/types';
import { useAuth } from '@/lib/auth';

// Validation schema using Zod
const taskSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(500, 'Title cannot exceed 500 characters')
    .trim(),
  description: z
    .string()
    .max(2000, 'Description cannot exceed 2000 characters')
    .optional(),
  status: z.nativeEnum(TaskStatus).optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormProps {
  task?: Task | null;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export default function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const { user } = useAuth();
  const isEditMode = !!task;

  const [formData, setFormData] = useState<TaskFormData>({
    title: task?.title || '',
    description: task?.description || '',
    status: (task?.status as TaskStatus) || TaskStatus.PENDING,
  });

  // Update form data when task prop changes
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status as TaskStatus,
      });
    } else {
      setFormData({
        title: '',
        description: '',
        status: TaskStatus.PENDING,
      });
    }
  }, [task]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear field error when user starts typing
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
    // Clear API error when user makes changes
    if (apiError) {
      setApiError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setApiError(null);
    setSuccessMessage(null);

    // Client-side validation
    try {
      taskSchema.parse(formData);
    } catch (error) {
      if (error instanceof z.ZodError) {
        const fieldErrors: Record<string, string> = {};
        error.errors.forEach((err) => {
          if (err.path[0]) {
            fieldErrors[err.path[0].toString()] = err.message;
          }
        });
        setErrors(fieldErrors);
        return;
      }
    }

    // Submit to API
    if (!user?.id) {
      setApiError('User not authenticated');
      return;
    }

    setIsLoading(true);

    try {
      if (isEditMode && task) {
        // Update existing task
        await api.updateTask(user.id, task.id, {
          title: formData.title,
          description: formData.description || undefined,
          status: formData.status,
        });
        setSuccessMessage('Task updated successfully!');
      } else {
        // Create new task
        await api.createTask(user.id, {
          title: formData.title,
          description: formData.description || undefined,
          status: formData.status,
        });
        setSuccessMessage('Task created successfully!');

        // Reset form only for create mode
        setFormData({
          title: '',
          description: '',
          status: TaskStatus.PENDING,
        });
      }

      // Call onSuccess callback if provided
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      setApiError(error instanceof Error ? error.message : `Failed to ${isEditMode ? 'update' : 'create'} task`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Success Message */}
      {successMessage && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <p className="text-green-800 text-sm">{successMessage}</p>
        </div>
      )}

      {/* API Error Message */}
      {apiError && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800 text-sm">{apiError}</p>
        </div>
      )}

      {/* Title Field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          disabled={isLoading}
          className={`w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.title ? 'border-red-500' : 'border-gray-300'
          } ${isLoading ? 'bg-gray-100 cursor-not-allowed' : ''}`}
          placeholder="Enter task title"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          {formData.title.length}/500 characters
        </p>
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          disabled={isLoading}
          rows={4}
          className={`w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.description ? 'border-red-500' : 'border-gray-300'
          } ${isLoading ? 'bg-gray-100 cursor-not-allowed' : ''}`}
          placeholder="Enter task description (optional)"
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          {(formData.description?.length || 0)}/2000 characters
        </p>
      </div>

      {/* Status Field */}
      <div>
        <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
          Status
        </label>
        <select
          id="status"
          name="status"
          value={formData.status}
          onChange={handleChange}
          disabled={isLoading}
          className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            isLoading ? 'bg-gray-100 cursor-not-allowed' : ''
          }`}
        >
          <option value={TaskStatus.PENDING}>Pending</option>
          <option value={TaskStatus.IN_PROGRESS}>In Progress</option>
          <option value={TaskStatus.COMPLETED}>Completed</option>
        </select>
      </div>

      {/* Submit Button */}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isLoading}
          className={`flex-1 px-6 py-3 text-white font-medium rounded-md transition-colors ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {isEditMode ? 'Updating Task...' : 'Creating Task...'}
            </span>
          ) : (
            isEditMode ? 'Update Task' : 'Create Task'
          )}
        </button>

        {isEditMode && onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="px-6 py-3 text-gray-700 font-medium bg-gray-100 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
