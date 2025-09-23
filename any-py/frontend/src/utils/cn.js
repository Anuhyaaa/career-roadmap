import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Utility function to merge Tailwind classes
 * Combines clsx for conditional classes and twMerge for proper Tailwind conflict resolution
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
