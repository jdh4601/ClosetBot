import { Link } from 'react-router-dom'
import { Sparkles } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white border-b border-brand-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="bg-lime p-2 rounded-lg">
              <Sparkles className="w-6 h-6 text-brand-black" />
            </div>
            <span className="text-xl font-bold">Fasion</span>
          </Link>
          
          <nav className="flex items-center gap-6">
            <Link 
              to="/" 
              className="text-brand-gray-600 hover:text-brand-black transition-colors"
            >
              홈
            </Link>
            <Link 
              to="/analysis" 
              className="text-brand-gray-600 hover:text-brand-black transition-colors"
            >
              분석하기
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
