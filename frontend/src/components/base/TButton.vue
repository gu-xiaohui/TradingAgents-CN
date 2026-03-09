<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin h-5 w-5"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    
    <!-- Icon (left) -->
    <component
      v-else-if="iconLeft && !loading"
      :is="iconLeft"
      class="h-5 w-5"
    />
    
    <!-- Slot content -->
    <slot />
    
    <!-- Icon (right) -->
    <component
      v-if="iconRight"
      :is="iconRight"
      class="h-5 w-5"
    />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  iconLeft?: any
  iconRight?: any
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
  block: false,
})

defineEmits(['click'])

const buttonClasses = computed(() => {
  const base = [
    'inline-flex items-center justify-center gap-2 font-medium transition-all duration-200 cursor-pointer',
    'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-primary-dark',
    'disabled:opacity-50 disabled:cursor-not-allowed',
  ]
  
  // Size variants
  const sizes = {
    sm: 'px-3 py-1.5 text-sm rounded-lg',
    md: 'px-4 py-2 text-sm rounded-xl',
    lg: 'px-6 py-3 text-base rounded-xl',
  }
  
  // Color variants
  const variants = {
    primary: 'bg-success text-white hover:bg-success/90 focus:ring-success active:scale-95',
    secondary: 'bg-primary-light border border-border text-text-primary hover:bg-primary focus:ring-text-muted',
    danger: 'bg-danger text-white hover:bg-danger/90 focus:ring-danger',
    ghost: 'bg-transparent text-text-secondary hover:bg-primary-light hover:text-text-primary',
  }
  
  return [
    ...base,
    sizes[props.size],
    variants[props.variant],
    props.block ? 'w-full' : '',
  ]
})
</script>
