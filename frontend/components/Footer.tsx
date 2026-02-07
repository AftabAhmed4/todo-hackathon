/**
 * Footer component.
 *
 * Displays footer information.
 */

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="text-center text-sm text-gray-500">
          <p>© 2026 Todo App. Secure multi-user task management.</p>
          <p className="mt-2">
            Built with Next.js, FastAPI, and JWT authentication.
          </p>
        </div>
      </div>
    </footer>
  );
}
