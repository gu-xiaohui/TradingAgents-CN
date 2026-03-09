<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div v-if="$slots.header || title" class="flex items-center justify-between mb-4">
      <div>
        <h3 v-if="title" class="text-lg font-semibold text-text-primary">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="text-sm text-text-muted mt-1">
          {{ subtitle }}
        </p>
      </div>
      <slot name="header-actions" />
    </div>
    
    <!-- Content -->
    <div :class="contentClass">
      <slot />
    </div>
    
    <!-- Footer -->
    <div v-if="$slots.footer" class="mt-4 pt-4 border-t border-border">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  subtitle?: string
  variant?: 'default' | 'glass' | 'gradient'
  hover?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
  contentClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  hover: false,
  padding: 'md',
  contentClass: '',
})

const cardClasses = computed(() => {
  const base = ['rounded-2xl transition-all duration-300']
  
  const variants = {
    default: 'bg-primary-light/70 backdrop-blur-xl border border-border',
    glass: 'bg-white/5 backdrop-blur-xl border border-white/10',
    gradient: 'bg-gradient-to-br from-primary-light to-primary border border-border',
  }
  
  const paddings = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }
  
  const hoverClasses = props.hover
    ? 'hover:border-success/50 hover:shadow-lg hover:shadow-success/10 hover:-translate-y-1'
    : ''
  
  return [
    ...base,
    variants[props.variant],
    paddings[props.padding],
    hoverClasses,
  ]
})
</script>
