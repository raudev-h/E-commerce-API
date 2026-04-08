export default function Button({ children, type = 'button', disabled, loading, variant = 'primary', className = '', ...props }) {
  const base = 'flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'

  const variants = {
    primary: 'bg-brand text-[#0a0a0a] hover:bg-brand/90 active:scale-[0.98]',
    secondary: 'border border-white/20 text-white/70 hover:text-white hover:border-white/40',
    ghost: 'text-white/50 hover:text-white',
  }

  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {loading && (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin shrink-0" />
      )}
      {children}
    </button>
  )
}
