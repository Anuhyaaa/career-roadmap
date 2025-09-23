import { forwardRef } from 'react'
import { cn } from '../../utils/cn'

const buttonVariants = {
  default: 'btn-primary',
  secondary: 'btn-secondary',
  outline: 'inline-flex items-center justify-center px-6 py-3 text-base font-medium text-gray-900 bg-transparent border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200',
  ghost: 'inline-flex items-center justify-center px-6 py-3 text-base font-medium text-gray-700 bg-transparent hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200 rounded-lg',
  link: 'inline-flex items-center justify-center text-base font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 underline-offset-4 hover:underline'
}

const buttonSizes = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg',
  icon: 'p-3'
}

const Button = forwardRef(({
  className,
  variant = 'default',
  size = 'md',
  children,
  loading = false,
  disabled = false,
  ...props
}, ref) => {
  const isDisabled = disabled || loading

  return (
    <button
      className={cn(
        buttonVariants[variant],
        buttonSizes[size],
        isDisabled && 'opacity-50 cursor-not-allowed',
        loading && 'cursor-wait',
        className
      )}
      ref={ref}
      disabled={isDisabled}
      {...props}
    >
      {loading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  )
})

Button.displayName = 'Button'

export { Button }
