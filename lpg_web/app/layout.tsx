import './globals.css'
import type { Metadata } from 'next'
import { Sidebar } from '@/components/nav/Sidebar'
import { TopNav } from '@/components/nav/TopNav'

export const metadata: Metadata = {
  title: 'LPG RouteX',
  description: 'LPG Delivery Route Optimization Platform',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background">
        <div className="min-h-screen grid grid-rows-[auto,1fr]">
          <TopNav />
          <div className="grid grid-cols-[260px,1fr]">
            <Sidebar />
            <main className="p-6">{children}</main>
          </div>
        </div>
      </body>
    </html>
  )
}
