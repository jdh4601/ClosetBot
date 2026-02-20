export interface AnalysisResult {
  username: string
  profile_picture_url?: string
  followers_count: number
  media_count: number
  biography?: string
  scores: {
    similarity_score: number
    engagement_score: number
    category_score: number
    final_score: number
    grade: 'A' | 'B' | 'C' | 'D'
  }
  top_posts: TopPost[]
  collaboration_signals: CollaborationSignal[]
  hashtag_distribution: Record<string, number>
  common_hashtags_with_brand: string[]
}

export interface TopPost {
  permalink: string
  caption_preview: string
  engagement_rate: number
  likes_count?: number
  comments_count: number
  posted_at: string
}

export interface CollaborationSignal {
  brand_username: string
  collaboration_type: string
  post_permalink: string
  posted_at: string
}

export const exportToCSV = (data: AnalysisResult[], brandUsername: string): void => {
  const headers = [
    'username',
    'grade',
    'final_score',
    'followers_count',
    'engagement_rate',
    'similarity_score',
    'category_score',
    'media_count',
    'common_hashtags',
    'collaboration_count'
  ]

  const rows = data.map(item => [
    item.username,
    item.scores.grade,
    item.scores.final_score,
    item.followers_count,
    item.scores.engagement_score,
    item.scores.similarity_score,
    item.scores.category_score,
    item.media_count,
    item.common_hashtags_with_brand.join(', '),
    item.collaboration_signals.length
  ])

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `analysis_${brandUsername}_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
