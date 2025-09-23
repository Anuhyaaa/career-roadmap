import { forwardRef } from 'react'
import { cn } from '../../utils/cn'

const Input = forwardRef(({
  className,
  type = 'text',
  label,
  error,
  helperText,
  required = false,
  ...props
}, ref) => {
  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-gray-900">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        type={type}
        className={cn(
          'input-field',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
          className
        )}
        ref={ref}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600" id={`${props.id}-error`}>
          {error}
        </p>
      )}
      {helperText && !error && (
        <p className="text-sm text-gray-500" id={`${props.id}-helper`}>
          {helperText}
        </p>
      )}
    </div>
  )
})

Input.displayName = 'Input'

export { Input }
