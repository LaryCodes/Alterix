import { motion } from 'framer-motion'
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100 p-6">
      <div className="glass-strong rounded-3xl p-12 text-center max-w-md shadow-glass-xl">
        <div className="text-8xl mb-6">🔍</div>
        <h2 className="text-5xl font-bold gradient-text mb-4">404</h2>
        <p className="text-xl text-brown-700 mb-2">Page Not Found</p>
        <p className="text-brown-600 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link href="/dashboard">
          <button className="px-8 py-4 bg-gradient-to-r from-pink-500 to-brown-500 text-white rounded-2xl font-bold shadow-glass-lg hover:shadow-glass-xl transition-all text-lg">
            Go to Dashboard
          </button>
        </Link>
      </div>
    </div>
  )
}
