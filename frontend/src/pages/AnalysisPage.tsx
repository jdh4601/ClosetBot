import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Loader2, Instagram, User, AlertCircle } from 'lucide-react'

export default function AnalysisPage() {
  const navigate = useNavigate()
  const [brandUsername, setBrandUsername] = useState('')
  const [influencerUsernames, setInfluencerUsernames] = useState(['', '', '', '', ''])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInfluencerChange = (index: number, value: string) => {
    const newUsernames = [...influencerUsernames]
    newUsernames[index] = value
    setInfluencerUsernames(newUsernames)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // Validation
    if (!brandUsername.trim()) {
      setError('브랜드 계정을 입력해주세요')
      return
    }

    const validInfluencers = influencerUsernames.filter(u => u.trim())
    if (validInfluencers.length === 0) {
      setError('최소 1명의 인플루언서를 입력해주세요')
      return
    }

    setIsLoading(true)

    try {
      // TODO: Call API to create analysis job
      // const response = await api.createAnalysisJob({
      //   brand_username: brandUsername,
      //   influencer_usernames: validInfluencers
      // })
      // navigate(`/dashboard/${response.job_id}`)
      
      // Mock for now
      setTimeout(() => {
        navigate('/dashboard/mock-job-id')
      }, 1500)
    } catch (err) {
      setError('분석 요청 중 오류가 발생했습니다')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">인플루언서 분석</h1>
      <p className="text-brand-gray-500 mb-8">
        브랜드와 인플루언서 계정을 입력하면 적합도를 분석합니다
      </p>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <span className="text-red-700">{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="card space-y-6">
        {/* Brand Input */}
        <div>
          <label className="block text-sm font-medium mb-2">
            <span className="flex items-center gap-2">
              <Instagram className="w-4 h-4" />
              브랜드 Instagram 계정
            </span>
          </label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-brand-gray-400">@</span>
            <input
              type="text"
              value={brandUsername}
              onChange={(e) => setBrandUsername(e.target.value)}
              placeholder="brand_username"
              className="input pl-8"
            />
          </div>
          <p className="text-sm text-brand-gray-400 mt-1">
            Business 또는 Creator 계정만 분석 가능합니다
          </p>
        </div>

        {/* Influencer Inputs */}
        <div>
          <label className="block text-sm font-medium mb-2">
            <span className="flex items-center gap-2">
              <User className="w-4 h-4" />
              인플루언서 계정 (최대 5명)
            </span>
          </label>
          <div className="space-y-3">
            {influencerUsernames.map((username, index) => (
              <div key={index} className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-brand-gray-400">@</span>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => handleInfluencerChange(index, e.target.value)}
                  placeholder={`influencer_${index + 1}`}
                  className="input pl-8"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              분석 요청 중...
            </>
          ) : (
            '분석 시작'
          )}
        </button>

        <p className="text-sm text-brand-gray-400 text-center">
          예상 소요 시간: 2-5분 (Rate limit 상황에 따라 달라질 수 있습니다)
        </p>
      </form>
    </div>
  )
}
