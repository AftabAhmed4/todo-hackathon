/**
 * Landing page component.
 *
 * Displays application information and calls-to-action for signup and signin.
 */

import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-grow">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
            <div className="text-center">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight">
                Secure Multi-User Todo App
              </h1>
              <p className="mt-6 text-xl sm:text-2xl text-blue-100 max-w-3xl mx-auto">
                Manage your tasks with confidence. Built with enterprise-grade security and JWT authentication.
              </p>
              <div className="mt-10 flex justify-center gap-4">
                <Link
                  href="/signup"
                  className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50 md:text-lg"
                >
                  Get Started
                </Link>
                <Link
                  href="/signin"
                  className="inline-flex items-center px-8 py-3 border border-white text-base font-medium rounded-md text-white hover:bg-blue-700 md:text-lg"
                >
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                Why Choose Our Todo App?
              </h2>
              <p className="mt-4 text-xl text-gray-600">
                Built with modern technology and security best practices
              </p>
            </div>

            <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">🔒</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Secure Authentication
                </h3>
                <p className="text-gray-600">
                  JWT-based authentication ensures your data is protected with industry-standard security.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">👥</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Multi-User Support
                </h3>
                <p className="text-gray-600">
                  Each user has their own private workspace. Your tasks are completely isolated from other users.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">🔐</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Data Privacy
                </h3>
                <p className="text-gray-600">
                  Your data is yours alone. We enforce strict data isolation to prevent any cross-user access.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">⚡</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Fast & Responsive
                </h3>
                <p className="text-gray-600">
                  Built with Next.js and FastAPI for lightning-fast performance on any device.
                </p>
              </div>

              {/* Feature 5 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">📱</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Mobile Friendly
                </h3>
                <p className="text-gray-600">
                  Responsive design works seamlessly on desktop, tablet, and mobile devices.
                </p>
              </div>

              {/* Feature 6 */}
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-blue-600 text-3xl mb-4">🚀</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Production Ready
                </h3>
                <p className="text-gray-600">
                  Built with production-quality code, comprehensive error handling, and best practices.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-blue-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
              Ready to get started?
            </h2>
            <p className="mt-4 text-xl text-blue-100">
              Create your account today and start managing your tasks securely.
            </p>
            <div className="mt-8">
              <Link
                href="/signup"
                className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50 md:text-lg"
              >
                Sign Up Now
              </Link>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
