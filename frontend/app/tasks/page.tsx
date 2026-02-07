/**
 * Tasks page with task creation and management functionality.
 *
 * Protected route that allows users to create, view, edit, and delete tasks.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { api } from '@/lib/api';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';
import { Task } from '@/lib/types';

export default function TasksPage() {
  const router = useRouter();
  const { isAuthenticated, user, isLoading } = useAuth();
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  // Redirect to signin if not authenticated
  if (!isLoading && !isAuthenticated) {
    router.push('/signin');
    return null;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  const handleTaskCreated = () => {
    // Refresh the task list
    setRefreshTrigger((prev) => prev + 1);
    // Clear editing state if any
    setEditingTask(null);
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    // Scroll to form
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  const handleDeleteClick = (taskId: number) => {
    setDeleteConfirm(taskId);
    setDeleteError(null);
  };

  const handleDeleteConfirm = async () => {
    if (!deleteConfirm || !user?.id) return;

    setDeleteLoading(true);
    setDeleteError(null);

    try {
      await api.deleteTask(user.id, deleteConfirm);
      setDeleteConfirm(null);
      setRefreshTrigger((prev) => prev + 1);
    } catch (error) {
      setDeleteError(error instanceof Error ? error.message : 'Failed to delete task');
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteConfirm(null);
    setDeleteError(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-grow bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              My Tasks
            </h1>
            <p className="mt-2 text-gray-600">
              Create and manage your tasks
            </p>
          </div>

          {/* Create/Edit Task Section */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h2>
              {editingTask && (
                <button
                  onClick={handleCancelEdit}
                  className="text-sm text-gray-600 hover:text-gray-800"
                >
                  Cancel Edit
                </button>
              )}
            </div>
            <TaskForm
              task={editingTask}
              onSuccess={handleTaskCreated}
              onCancel={handleCancelEdit}
            />
          </div>

          {/* Task List Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Your Tasks
            </h2>
            {user?.id && (
              <TaskList
                userId={user.id}
                refreshTrigger={refreshTrigger}
                onEdit={handleEdit}
                onDelete={handleDeleteClick}
              />
            )}
          </div>
        </div>
      </main>

      <Footer />

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Delete Task
            </h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete this task? This action cannot be undone.
            </p>

            {deleteError && (
              <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
                <p className="text-red-800 text-sm">{deleteError}</p>
              </div>
            )}

            <div className="flex gap-3 justify-end">
              <button
                onClick={handleDeleteCancel}
                disabled={deleteLoading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteConfirm}
                disabled={deleteLoading}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                {deleteLoading ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
