'use client'

import { ReactNode } from 'react'
import DashboardHeader from './DashboardHeader'

interface DashboardLayoutProps {
  children: ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100">
      <DashboardHeader />
      <main className="container mx-auto px-6 py-8">
        {children}
      </main>
    </div>
  )
}
