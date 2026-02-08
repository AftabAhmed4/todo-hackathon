/**
 * Floating Chat Button Component
 *
 * A professional floating action button that appears on the bottom right
 * of the screen for authenticated users to access the AI chat interface.
 */

'use client';

import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { usePathname } from 'next/navigation';

export default function FloatingChatButton() {
  const { isAuthenticated } = useAuth();
  const pathname = usePathname();

  // Don't show on chat page or auth pages
  if (!isAuthenticated || pathname === '/chat' || pathname === '/signin' || pathname === '/signup') {
    return null;
  }

  return (
    <Link
      href="/chat"
      className="fixed bottom-6 right-6 z-50 group"
      aria-label="Open AI Chat"
    >
      <div className="relative">
        {/* Main button */}
        <div className="flex items-center justify-center w-14 h-14 bg-blue-600 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 hover:scale-110 group-hover:shadow-xl">
          {/* Chat Icon SVG */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-7 w-7 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </div>

        {/* Tooltip */}
        <div className="absolute bottom-full right-0 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
          <div className="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg whitespace-nowrap shadow-lg">
            AI Chat Assistant
            <div className="absolute top-full right-6 -mt-1">
              <div className="border-4 border-transparent border-t-gray-900"></div>
            </div>
          </div>
        </div>

        {/* Pulse animation ring */}
        <div className="absolute inset-0 rounded-full bg-blue-600 opacity-75 animate-ping"></div>
      </div>
    </Link>
  );
}
