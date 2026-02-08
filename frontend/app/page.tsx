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
        <div className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
              backgroundSize: '40px 40px'
            }}></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
            <div className="text-center">
              <div className="inline-flex items-center px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/20">
                <span className="mr-2">✨</span>
                AI-Powered Task Management
              </div>
              <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-tight">
                Manage Tasks with
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-cyan-200 mt-2">
                  Intelligence & Security
                </span>
              </h1>
              <p className="mt-6 text-lg sm:text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
                Experience the future of task management with AI-powered chat assistant,
                enterprise-grade security, and seamless collaboration.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
                <Link
                  href="/signup"
                  className="group inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-semibold rounded-xl text-blue-700 bg-white hover:bg-blue-50 md:text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
                >
                  Get Started Free
                  <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
                <Link
                  href="/signin"
                  className="inline-flex items-center justify-center px-8 py-4 border-2 border-white/30 text-base font-semibold rounded-xl text-white hover:bg-white/10 md:text-lg backdrop-blur-sm transition-all duration-200"
                >
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-20 bg-gradient-to-b from-gray-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-base font-semibold text-blue-600 tracking-wide uppercase">
                Features
              </h2>
              <p className="mt-2 text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900">
                Why Choose Our Todo App?
              </p>
              <p className="mt-4 max-w-2xl text-xl text-gray-600 mx-auto">
                Built with modern technology and security best practices
              </p>
            </div>

            <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 - AI Chat */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  AI Chat Assistant
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Manage tasks naturally with our AI-powered chat. Just tell it what you need, and it handles the rest.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Secure Authentication
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  JWT-based authentication ensures your data is protected with industry-standard security protocols.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Multi-User Support
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Each user has their own private workspace. Your tasks are completely isolated and secure.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Lightning Fast
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Built with Next.js and FastAPI for blazing-fast performance on any device, anywhere.
                </p>
              </div>

              {/* Feature 5 */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Mobile Friendly
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Responsive design that works seamlessly on desktop, tablet, and mobile devices.
                </p>
              </div>

              {/* Feature 6 */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Production Ready
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Built with production-quality code, comprehensive error handling, and industry best practices.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 overflow-hidden">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
              backgroundSize: '40px 40px'
            }}></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white leading-tight">
                Ready to Transform Your Productivity?
              </h2>
              <p className="mt-6 text-lg sm:text-xl text-blue-100 leading-relaxed">
                Join thousands of users who are managing their tasks smarter with AI assistance.
                Create your account today and experience the future of task management.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
                <Link
                  href="/signup"
                  className="group inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-semibold rounded-xl text-blue-700 bg-white hover:bg-blue-50 md:text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
                >
                  Start Free Today
                  <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
              </div>
              <p className="mt-6 text-sm text-blue-200">
                No credit card required • Free forever • Get started in seconds
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
