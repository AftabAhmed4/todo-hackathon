'use client';

/**
 * Chat Page
 *
 * Main page for the AI-powered todo chat interface.
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';
import { getToken } from '@/lib/api';

export default function ChatPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = getToken();
    if (!token) {
      router.push('/signin?redirect=/chat');
      return;
    }
    setIsAuthenticated(true);
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">AI Todo Chat</h1>
            <p className="text-gray-600 mt-2">
              Manage your todos through natural conversation
            </p>
          </div>

          <div className="h-[calc(100vh-200px)]">
            <ChatInterface />
          </div>
        </div>
      </div>
    </div>
  );
}
