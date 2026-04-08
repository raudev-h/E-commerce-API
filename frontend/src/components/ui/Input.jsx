export default function Input({ label, id, className = '', ...props }) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-')

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-sm text-white/60">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`bg-surface border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-white/30 focus:outline-none focus:border-brand/50 transition-colors ${className}`}
        {...props}
      />
    </div>
  )
}
