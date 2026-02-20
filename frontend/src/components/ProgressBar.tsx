import React from 'react'

interface ProgressBarProps {
  progress: number
  status: 'queued' | 'running' | 'done' | 'failed'
  estimatedMinutes?: number
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  status,
  estimatedMinutes
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'done':
        return 'bg-green-500'
      case 'failed':
        return 'bg-red-500'
      case 'running':
        return 'bg-lime'
      default:
        return 'bg-brand-gray-300'
    }
  }

  const getStatusText = () => {
    switch (status) {
      case 'queued':
        return '대기 중...'
      case 'running':
        return '분석 중...'
      case 'done':
        return '완료!'
      case 'failed':
        return '분석 실패'
      default:
        return '준비'
    }
  }

  return (
    <div className="w-full">
      <div className="flex justify-between mb-2">
        <span className="text-sm font-medium text-brand-gray-700">
          {getStatusText()}
        </span>
        <span className="text-sm text-brand-gray-500">
          {progress}%
        </span>
      </div>
      
      <div className="w-full bg-brand-gray-200 rounded-full h-2.5">
        <div
          className={`${getStatusColor()} h-2.5 rounded-full transition-all duration-500`}
          style={{ width: `${progress}%` }}
        />
      </div>
      
      {estimatedMinutes && status === 'running' && (
        <p className="text-sm text-brand-gray-500 mt-2">
          예상 완료 시간: 약 {estimatedMinutes}분
        </p>
      )}
      
      {status === 'queued' && (
        <p className="text-sm text-brand-gray-500 mt-2">
          Instagram API Rate Limit을 준수하며 순차적으로 처리 중입니다.
        </p>
      )}
    </div>
  )
}
