export interface InfluencerProfile {
  id: string
  ig_username: string
  followers_count: number
  media_count: number
  biography?: string
  is_verified: boolean
  categories: string[]
  last_fetched_at: string
}

export interface InfluencerMedia {
  id: string
  caption?: string
  comments_count: number
  like_count?: number
  media_type: string
  permalink: string
  posted_at: string
}

export interface InfluencerDetail extends InfluencerProfile {
  recent_media: InfluencerMedia[]
  hashtag_distribution: Record<string, number>
  avg_engagement_rate: number
}
