<template>
  <span :class="badgeClasses">
    <!-- Icon -->
    <component v-if="icon" :is="icon" class="h-3.5 w-3.5" />
    
    <!-- Content -->
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral'
  size?: 'sm' | 'md' | 'lg'
  text?: string
  icon?: any
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'neutral',
  size: 'md',
})

const badgeClasses = computed(() => {
  const base = ['inline-flex items-center gap-1 font-medium rounded-full']
  
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs',
    lg: 'px-3 py-1.5 text-sm',
  }
  
  const variants = {
    success: 'bg-success/20 text-success',
    warning: 'bg-warning/20 text-warning',
    danger: 'bg-danger/20 text-danger',
    info: 'bg-cta/20 text-cta',
    neutral: 'bg-text-muted/20 text-text-secondary',
  }
  
  return [...base, sizes[props.size], variants[props.variant]]
})
</script>
