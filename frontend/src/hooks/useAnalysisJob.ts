import { useState, useEffect, useCallback } from 'react'
import { apiClient } from '../api/client'

interface JobStatus {
  job_id: string
  status: 'queued' | 'running' | 'done' | 'failed'
  progress_percent?: number
  estimated_completion_minutes?: number
  error_message?: string
}

export const useAnalysisJob = (jobId: string | null) => {
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [isPolling, setIsPolling] = useState(false)

  const pollJobStatus = useCallback(async () => {
    if (!jobId) return

    try {
      const response = await apiClient.get(`/analysis/jobs/${jobId}`)
      setJobStatus(response.data)

      // Stop polling if job is done or failed
      if (response.data.status === 'done' || response.data.status === 'failed') {
        setIsPolling(false)
      }
    } catch (error) {
      console.error('Failed to poll job status:', error)
      setIsPolling(false)
    }
  }, [jobId])

  useEffect(() => {
    if (!jobId || !isPolling) return

    const interval = setInterval(pollJobStatus, 2000)
    return () => clearInterval(interval)
  }, [jobId, isPolling, pollJobStatus])

  const startPolling = useCallback(() => {
    setIsPolling(true)
    pollJobStatus()
  }, [pollJobStatus])

  const stopPolling = useCallback(() => {
    setIsPolling(false)
  }, [])

  return {
    jobStatus,
    isPolling,
    startPolling,
    stopPolling
  }
}
