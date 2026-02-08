/**
 * Root layout component.
 *
 * Wraps the application with AuthProvider, ToastProvider and includes global styles.
 */

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthProvider } from '@/lib/auth';
import { ToastProvider } from '@/lib/toast';
import FloatingChatButton from '@/components/FloatingChatButton';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App - Secure Multi-User Task Management',
  description: 'A secure, multi-user todo application with JWT authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <ToastProvider>
            {children}
            <FloatingChatButton />
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
