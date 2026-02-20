import { useParams } from 'react-router-dom'
import { ArrowLeft, Instagram, ExternalLink } from 'lucide-react'
import { Link } from 'react-router-dom'

// Mock data
const mockDetail = {
  username: 'influencer_a',
  followers_count: 45000,
  media_count: 1230,
  biography: 'Minimal fashion / Seoul based',
  scores: {
    similarity_score: 92,
    engagement_score: 85,
    category_score: 78,
    final_score: 87,
    grade: 'A',
  },
  collaboration_signals: [
    { brand: 'luxury_brand_a', type: '#ad', date: '2025.12' },
    { brand: 'indie_designer_b', type: '#협찬', date: '2025.09' },
  ],
  top_posts: [
    { engagement_rate: 9.2, comments: 156, date: '2025.12.03' },
    { engagement_rate: 8.7, comments: 142, date: '2025.11.28' },
    { engagement_rate: 7.4, comments: 128, date: '2025.11.15' },
  ],
  hashtag_distribution: {
    fashion: 45,
    minimal: 22,
    ootd: 18,
    luxury: 10,
    lifestyle: 5,
  },
  common_hashtags: ['minimal', 'fashion', 'seoul'],
}

export default function DetailPage() {
  const { username } = useParams<{ username: string }>()

  return (
    <div className="max-w-4xl mx-auto">
      <Link 
        to="/dashboard/mock-job-id"
        className="inline-flex items-center gap-2 text-brand-gray-600 hover:text-brand-black mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        결과 목록으로 돌아가기
      </Link>

      {/* Profile Header */}
      <div className="card mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">@{mockDetail.username}</h1>
            <p className="text-brand-gray-600 mb-4">{mockDetail.biography}</p>
            <div className="flex gap-6 text-sm">
              <div>
                <span className="font-semibold">{(mockDetail.followers_count / 1000).toFixed(0)}K</span>
                <span className="text-brand-gray-400 ml-1">팔로워</span>
              </div>
              <div>
                <span className="font-semibold">{mockDetail.media_count.toLocaleString()}</span>
                <span className="text-brand-gray-400 ml-1">게시물</span>
              </div>
            </div>
          </div>
          <a
            href={`https://instagram.com/${mockDetail.username}`}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary flex items-center gap-2"
          >
            <Instagram className="w-4 h-4" />
            프로필 보기
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">점수 분해</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-brand-gray-600">브랜드 유사도 (40%)</span>
            <div className="flex items-center gap-3">
              <div className="w-32 h-2 bg-brand-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-lime rounded-full"
                  style={{ width: `${mockDetail.scores.similarity_score}%` }}
                />
              </div>
              <span className="font-semibold w-12 text-right">{mockDetail.scores.similarity_score}</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-brand-gray-600">참여율 품질 (35%)</span>
            <div className="flex items-center gap-3">
              <div className="w-32 h-2 bg-brand-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-lime rounded-full"
                  style={{ width: `${mockDetail.scores.engagement_score}%` }}
                />
              </div>
              <span className="font-semibold w-12 text-right">{mockDetail.scores.engagement_score}</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-brand-gray-600">카테고리 적합성 (25%)</span>
            <div className="flex items-center gap-3">
              <div className="w-32 h-2 bg-brand-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-lime rounded-full"
                  style={{ width: `${mockDetail.scores.category_score}%` }}
                />
              </div>
              <span className="font-semibold w-12 text-right">{mockDetail.scores.category_score}</span>
            </div>
          </div>
          <div className="border-t border-brand-gray-200 pt-4 flex items-center justify-between">
            <span className="font-semibold">종합 점수</span>
            <div className="flex items-center gap-3">
              <span className="text-2xl font-bold text-lime-dark">{mockDetail.scores.final_score}</span>
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                {mockDetail.scores.grade}등급
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Collaboration History */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">과거 협업 브랜드</h2>
          <div className="space-y-3">
            {mockDetail.collaboration_signals.map((collab, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-brand-gray-100 last:border-0">
                <div>
                  <span className="font-medium">@{collab.brand}</span>
                  <span className="text-brand-gray-400 text-sm ml-2">{collab.type}</span>
                </div>
                <span className="text-brand-gray-400 text-sm">{collab.date}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Hashtag Distribution */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">해시태그 분포</h2>
          <div className="space-y-3">
            {Object.entries(mockDetail.hashtag_distribution).map(([tag, percentage]) => (
              <div key={tag} className="flex items-center justify-between">
                <span className="text-brand-gray-600">#{tag}</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-2 bg-brand-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-lime rounded-full"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <span className="text-sm w-10 text-right">{percentage}%</span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-brand-gray-200">
            <span className="text-sm text-brand-gray-500">브랜드 교집합: </span>
            {mockDetail.common_hashtags.map(tag => (
              <span key={tag} className="text-sm text-lime-dark font-medium mr-2">
                #{tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
