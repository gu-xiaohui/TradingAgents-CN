<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" class="block text-sm font-medium text-text-secondary mb-2">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    
    <!-- Input wrapper -->
    <div class="relative">
      <!-- Icon left -->
      <div v-if="iconLeft" class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted">
        <component :is="iconLeft" class="h-5 w-5" />
      </div>
      
      <!-- Input element -->
      <input
        v-if="type !== 'textarea'"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :class="inputClasses"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      
      <!-- Textarea -->
      <textarea
        v-else
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :rows="rows"
        :class="inputClasses"
        @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
      />
      
      <!-- Icon right -->
      <div v-if="iconRight" class="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted">
        <component :is="iconRight" class="h-5 w-5" />
      </div>
      
      <!-- Clear button -->
      <button
        v-if="clearable && modelValue"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary transition-colors"
        @click="$emit('update:modelValue', '')"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Error message -->
    <p v-if="error" class="mt-2 text-sm text-danger">
      {{ error }}
    </p>
    
    <!-- Helper text -->
    <p v-else-if="helper" class="mt-2 text-sm text-text-muted">
      {{ helper }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string
  label?: string
  placeholder?: string
  type?: 'text' | 'password' | 'email' | 'number' | 'textarea'
  disabled?: boolean
  required?: boolean
  error?: string
  helper?: string
  iconLeft?: any
  iconRight?: any
  clearable?: boolean
  rows?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  clearable: false,
  rows: 4,
})

defineEmits(['update:modelValue'])

const inputClasses = computed(() => {
  const base = [
    'w-full bg-primary-dark border rounded-xl text-text-primary placeholder-text-muted',
    'transition-all duration-200',
    'focus:outline-none focus:ring-2 focus:ring-success/50',
    'disabled:opacity-50 disabled:cursor-not-allowed',
  ]
  
  const padding = props.iconLeft
    ? 'pl-10 pr-4 py-3'
    : props.iconRight || props.clearable
    ? 'pl-4 pr-10 py-3'
    : 'px-4 py-3'
  
  const borderColor = props.error
    ? 'border-danger focus:border-danger'
    : 'border-border focus:border-success'
  
  return [...base, padding, borderColor]
})
</script>
