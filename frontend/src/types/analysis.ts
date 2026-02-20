export interface AnalysisRequest {
  brand_username: string
  influencer_usernames: string[]
}

export interface AnalysisJobResponse {
  job_id: string
  status: 'queued' | 'running' | 'done' | 'failed'
  message?: string
  progress_percent?: number
  estimated_completion_minutes?: number
  created_at?: string
  started_at?: string
  finished_at?: string
  error_message?: string
}

export interface ScoreBreakdown {
  similarity_score: number
  engagement_score: number
  category_score: number
  final_score: number
  grade: 'A' | 'B' | 'C' | 'D'
}

export interface CollaborationSignal {
  brand_username: string
  collaboration_type: string
  post_permalink: string
  posted_at: string
}

export interface TopPost {
  permalink: string
  caption_preview: string
  engagement_rate: number
  likes_count?: number
  comments_count: number
  posted_at: string
}

export interface InfluencerResult {
  username: string
  profile_picture_url?: string
  followers_count: number
  media_count: number
  biography?: string
  avg_engagement_rate?: number
  scores: ScoreBreakdown
  top_posts: TopPost[]
  collaboration_signals: CollaborationSignal[]
  hashtag_distribution: Record<string, number>
  common_hashtags_with_brand: string[]
}

export interface AnalysisResultResponse {
  job_id: string
  brand_username: string
  status: string
  results: InfluencerResult[]
  total_api_calls: number
  created_at: string
  completed_at?: string
}
