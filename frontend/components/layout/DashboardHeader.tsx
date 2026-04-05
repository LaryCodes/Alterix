'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { auth } from '@/lib/auth'

export default function DashboardHeader() {
  const pathname = usePathname()
  const user = auth.getUser()

  const handleLogout = () => {
    auth.logout()
  }

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { href: '/skills', label: 'Skills', icon: '🎯' },
    { href: '/matches', label: 'Matches', icon: '🔍' },
    { href: '/exchanges', label: 'Exchanges', icon: '🔄' },
  ]

  const isActive = (href: string) => pathname === href

  return (
    <motion.header 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass-strong border-b border-white/30 sticky top-0 z-50"
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/dashboard">
            <motion.h1 
              className="text-3xl font-bold gradient-text cursor-pointer"
              whileHover={{ scale: 1.05 }}
            >
              Alterix
            </motion.h1>
          </Link>
          
          <div className="flex gap-4 items-center">
            <div className="glass px-4 py-2 rounded-full hidden md:block">
              <span className="text-brown-800 font-medium">Welcome, {user?.name || 'User'}</span>
            </div>
            
            {navItems.map((item) => (
              <Link key={item.href} href={item.href}>
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-4 py-2 rounded-full font-medium transition-all ${
                    isActive(item.href)
                      ? 'bg-gradient-to-r from-pink-500 to-brown-500 text-white shadow-glass'
                      : 'text-brown-700 hover:text-pink-600'
                  }`}
                >
                  <span className="hidden md:inline">{item.label}</span>
                  <span className="md:hidden">{item.icon}</span>
                </motion.button>
              </Link>
            ))}
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="px-4 py-2 bg-gradient-to-r from-pink-500 to-brown-500 text-white rounded-full font-medium shadow-glass hover:shadow-glass-lg transition-all"
            >
              Logout
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  )
}
