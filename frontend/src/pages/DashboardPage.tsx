import { useParams } from 'react-router-dom'
import { useEffect, useState, useCallback } from 'react'
import { Download, RefreshCw } from 'lucide-react'
import { apiClient } from '../api/client'
import type { AnalysisResultResponse, InfluencerResult } from '../types/analysis'

export default function DashboardPage() {
  const { jobId } = useParams<{ jobId: string }>()
  const [results, setResults] = useState<InfluencerResult[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [notReady, setNotReady] = useState<boolean>(false)

  const fetchResults = useCallback(async () => {
    if (!jobId) return
    setLoading(true)
    setError(null)
    setNotReady(false)
    try {
      const response = await apiClient.get<AnalysisResultResponse>(`/analysis/jobs/${jobId}/results`)
      setResults(response.data.results)
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setNotReady(true)
      } else {
        setError(err?.message || '결과를 불러오지 못했습니다')
      }
    } finally {
      setLoading(false)
    }
  }, [jobId])

  useEffect(() => {
    fetchResults()
  }, [fetchResults])

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A': return 'bg-green-100 text-green-800'
      case 'B': return 'bg-blue-100 text-blue-800'
      case 'C': return 'bg-yellow-100 text-yellow-800'
      case 'D': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const onRefresh = () => fetchResults()

  const onExportCSV = () => {
    const headers = ['username','grade','final_score','followers_count','avg_engagement_rate','engagement_score','similarity_score']
    const rows = results.map(r => [
      r.username,
      r.scores.grade,
      r.scores.final_score.toString(),
      r.followers_count.toString(),
      r.avg_engagement_rate != null ? r.avg_engagement_rate.toString() : '',
      r.scores.engagement_score.toString(),
      r.scores.similarity_score.toString(),
    ])
    const csv = [headers, ...rows].map(r => r.map(v => `"${String(v).replace(/"/g,'""')}"`).join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `analysis_results_${jobId}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold mb-1">분석 결과</h1>
          <p className="text-brand-gray-500">
            Job ID: {jobId}
          </p>
        </div>
        <div className="flex gap-3">
          <button onClick={onRefresh} className="btn-secondary flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            새로고침
          </button>
          <button onClick={onExportCSV} className="btn-primary flex items-center gap-2" disabled={results.length===0}>
            <Download className="w-4 h-4" />
            CSV 내보내기
          </button>
        </div>
      </div>

      {loading && (
        <div className="card p-6 mb-6">결과를 불러오는 중...</div>
      )}
      {!loading && notReady && (
        <div className="card p-6 mb-6 text-brand-gray-700">
          분석이 아직 완료되지 않았습니다. 잠시 후 새로고침 해주세요.
        </div>
      )}
      {!loading && error && (
        <div className="card p-6 mb-6 text-red-700">
          오류: {error}
        </div>
      )}

      {/* Results Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-brand-gray-200">
                <th className="text-left py-4 px-4 font-semibold">인플루언서</th>
                <th className="text-center py-4 px-4 font-semibold">등급</th>
                <th className="text-center py-4 px-4 font-semibold">종합 점수</th>
                <th className="text-center py-4 px-4 font-semibold">팔로워</th>
                <th className="text-center py-4 px-4 font-semibold">참여율</th>
                <th className="text-center py-4 px-4 font-semibold">참여 점수</th>
                <th className="text-center py-4 px-4 font-semibold">브랜드 유사도</th>
                <th className="text-center py-4 px-4 font-semibold">상세</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result) => (
                <tr 
                  key={result.username}
                  className="border-b border-brand-gray-100 hover:bg-brand-gray-50"
                >
                  <td className="py-4 px-4 font-medium">@{result.username}</td>
                  <td className="py-4 px-4 text-center">
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getGradeColor(result.scores.grade)}`}>
                      {result.scores.grade}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-center font-bold text-lg">
                    {result.scores.final_score}
                  </td>
                  <td className="py-4 px-4 text-center text-brand-gray-600">
                    {(result.followers_count / 1000).toFixed(0)}K
                  </td>
                  <td className="py-4 px-4 text-center text-brand-gray-600">
                    {result.avg_engagement_rate != null ? `${result.avg_engagement_rate}%` : '-'}
                  </td>
                  <td className="py-4 px-4 text-center text-brand-gray-600">
                    {result.scores.engagement_score}
                  </td>
                  <td className="py-4 px-4 text-center text-brand-gray-600">
                    {result.scores.similarity_score}%
                  </td>
                  <td className="py-4 px-4 text-center">
                    <button className="text-lime-dark hover:underline font-medium">
                      보기
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Score Legend */}
      <div className="mt-6 flex flex-wrap gap-4 text-sm text-brand-gray-500">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-green-500"></span>
          A등급 (80-100점): 강력 추천
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-blue-500"></span>
          B등급 (60-79점): 추천
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
          C등급 (40-59점): 보통
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-500"></span>
          D등급 (0-39점): 부적합
        </div>
      </div>
    </div>
  )
}
