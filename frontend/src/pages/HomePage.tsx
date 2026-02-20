import { Link } from 'react-router-dom'
import { ArrowRight, BarChart3, Clock, Users } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          Decode<br />
          <span className="text-lime-dark">the Influence</span>
        </h1>
        <p className="text-lg text-brand-gray-600 mb-8 max-w-2xl mx-auto">
          브랜드와 인플루언서의 적합도를 0-100점으로 분석하여
          최적의 시딩 파트너를 찾아드립니다
        </p>
        <Link to="/analysis" className="btn-primary inline-flex items-center gap-2">
          분석 시작하기
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-6 py-12">
        <div className="card text-center">
          <Clock className="w-10 h-10 mx-auto mb-4 text-lime-dark" />
          <h3 className="text-lg font-semibold mb-2">5분 완료</h3>
          <p className="text-brand-gray-500">
            반나절 걸리던 분석을<br />5분으로 단축
          </p>
        </div>
        
        <div className="card text-center">
          <BarChart3 className="w-10 h-10 mx-auto mb-4 text-lime-dark" />
          <h3 className="text-lg font-semibold mb-2">데이터 기반</h3>
          <p className="text-brand-gray-500">
            감이 아닌 데이터로<br />객관적 판단
          </p>
        </div>
        
        <div className="card text-center">
          <Users className="w-10 h-10 mx-auto mb-4 text-lime-dark" />
          <h3 className="text-lg font-semibold mb-2">5명 비교</h3>
          <p className="text-brand-gray-500">
            한 번에 5명의 인플루언서를<br />동시 분석
          </p>
        </div>
      </div>
    </div>
  )
}
